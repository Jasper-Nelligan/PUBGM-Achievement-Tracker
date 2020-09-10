import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import copy
import csv

from scrollable_frame import ScrollableFrame


#**********************************************************************
# Implements a GUI for users track their PUBG MOBILE achievements.

# I made this as a learning experience on making GUI's and using
# python, and so I've overcommented the code accordingly

# Code structure referenced from: https://tinyurl.com/y3g9ab5q

# Helpful links:
# 
# Tkinter info:
# http://effbot.org/tkinterbook
#
# PUBG font
# Colour for PUBG font was DEDF00 for yellow
# and DF0D0D for red, using Gradient-Orange-H from
# https://fontmeme.com/playerunknowns-battlegrounds-font/

# (C) 2020 Jasper Nelligan
#**********************************************************************

# Desired sizes for the button images
BUTTON_SIZE = 277, 45

# Most windows screens have 16 pixels that aren't shown on screen
# ie. on the edges of the screen where the mouses disappear
SCREEN_OFFSET = 16

# Used to create size of window
BACKGROUND_IMG_H = 625
PC_WIDTH = 1366


class AppController(tk.Tk):
    """This class is a way for different frames to communicate with each other.
   
    This class initializes itself as the root frame onto which all other frame
    classes (MainMenuFrame, OverviewFrame, AchievementsFrame, 
    and CompletedFrame) will be placed on.
    This class acts as the controller, meaning that any communication done 
    between the frame classes is done via this class.
    """

    def __init__(self):
        """Initializes self as root frame and calls on other frame
        classes to initialize them.
        """

        # Creates the root. Root is referenced using 'self'
        tk.Tk.__init__(self)
        # Users will not be able to resize the window. This is because clicking
        # on buttons will be pixel specific, and so resizing the window will
        # cause the buttons not to work.
        self.resizable(width=False, height=False)
        self.iconbitmap('./Images/icon.ico')
        self.title("PUBG Achievement Tracker")
        #root.overrideredirect(1)   # Removes window border

        # The container is where a bunch of frames will be stacked
        # on top of each other, then the one wanted to be visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # A list for storing references to each instance of the Achievement 
        # class. Each achievement stores an assigned list index so it can be 
        # accessed. Achievements are read from the csv file and placed in the 
        # list when initializing AchievementsFrame.
        self.achievement_list = []
        # Initializing all frames

        # All frames will be stored in a dictionary for quick access
        self.frames = {}
        for F in (MainMenuFrame, OverviewFrame, AchievementsFrame, 
                  CompletedFrame, CreditsFrame):
            page_name = F.__name__
            # Create an instance of each frame
            # AchievementsFrame and CompletedFrame require a reference to the list of achievements
            if (page_name == "AchievementsFrame" or page_name == "CompletedFrame"):
                print(page_name)
                frame = F(parent=container, controller=self, achievement_list=self.achievement_list)
            else:
                frame = F(parent=container, controller=self)
            # Input frame into dictionary
            self.frames[page_name] = frame

            # Put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # Initialize the reward images used for each achievement
        Achievement.__init__(self.achievement_list)

        # Initialize achievements from csv file
        self.init_achievements()

        # Start by showing the Main Menu
        self.show_frame("MainMenuFrame")

    def init_achievements(self):
        """Reads in achievement information from csv file and initiates each one.

        Achievement will be initiated in either AchievementsFrame or 
        CompletedFrame, depending on if it's been completed or not.

        The leveled achievements csv file is formatted in the following way:
        row[0] = category (int)
        row[1] = title (string)
        row[2] = description (string)
        row[3] = levels (string)(I.planned?(Y=1,N=0).
                  completed?(Y=1,N=0).# of tasks needed.points.reward amount.
                  reward type+II.etc...)
        row[4] = overall_completed?(int)(0=No, 1=Yes)
        row[5] = achievement info (string)
         
        Note that in row[3], periods are used as the delimiter between a 
        level's attributes, and a + separates each level.
        """
        # Initiating leveled achievements
        with open('./PUBGM Achievement Tracker/leveled_achievements.csv','r') as csv_file:
            csvReader = csv.DictReader(csv_file, delimiter=',')

            # Keeps track of the index in achievement_list where the
            # next achievement will be placed
            list_index = 0

            for row in csvReader:
                # Starts by initializing the first level
                category = row['Category']
                title = row['Title']
                desc = row['Description']
                # levels_string contains info specific to each level
                levels_string = row['Levels']
                overall_completed = row['Overall_completed']
                info = row['Info']

                # Split levels string into a list of levels
                levels_list = levels_string.split('+')

                # Set to true once the achievement has been initialized onto
                # its corresponding category frame in AchievementsFrame. Only
                # the highest level to not be completed will be initialized
                # as a frame
                frame_initialized = False
                for level in levels_list:
                    # Split each level into its attributes
                    level_attrs = level.split('.')
                    level_rom_num = level_attrs[0]
                    is_planned = level_attrs[1]
                    is_completed = level_attrs[2]
                    num_tasks = level_attrs[3]
                    # Assigning a Tk Image to points and reward
                    points_img = level_attrs[4]
                    reward_amount = level_attrs[5]
                    reward_img = level_attrs[6]

                    # input number of tasks needed in level into description string
                    num_tasks_desc = desc.format(num_tasks=num_tasks)

                    # To save RAM, only the first level of each achievement
                    # will store the info attribute, and so a check
                    # for the first level is done. 
                    if level_rom_num == 'I':
                        print("level is I")
                        achievement = LeveledAchievement(category, title, num_tasks_desc, 
                                                  level_rom_num, is_planned,
                                                  is_completed, num_tasks, 
                                                  points_img, reward_amount, 
                                                  reward_img, list_index, info)
                    else:
                        print("else")
                        achievement = LeveledAchievement(category, title, num_tasks_desc, 
                                                  level_rom_num, is_planned,
                                                  is_completed, num_tasks, 
                                                  points_img, reward_amount, 
                                                  reward_img, list_index)

                    # add achievement to list
                    self.achievement_list.append(achievement)
                    list_index += 1

                    # if achievement is completed, initiate frame in CompletedFrame
                    if overall_completed == 1:
                        self.frames["CompletedFrame"].init_achievement_frame(achievement)
                    # else initiate in AchievementsFrame
                    else:
                        # Only the first level of the achievement to not be completed
                        # will be shown in the category frame. Therefore, if the 
                        # level has been completed, skip to the next level.
                        if is_completed == 1:
                            pass
                        # if this is the next level to be completed, initialize it 
                        # as a frame in AchievementsFrame
                        if frame_initialized == False:
                            self.frames["AchievementsFrame"].init_achievement_frame(achievement)
                            frame_initialized = True
                        # else achievement level has not been completed yet, and a lower level
                        # has already been initialized as a frame in AchievementFrame
                        else:
                            pass

    def show_frame(self, page_name):
            """Shows a frame for the given page name"""
            frame = self.frames[page_name]
            frame.tkraise()


class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        """Creates frame for Main Menu

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
        """

        # tk.Frame.__init__ is used since this class inherits from
        # tk.Frame, meaning the constructor of the parent
        # class must be used.
        # Frame width is set to the max width of my PC since the
        # background image is wider than my PC allows. This means
        # that frame width is hard coded to my PC's width.
        # Therefore, button clicks are calculated based on this fixed size.
        # Allowing variable window sizes for different screens is a feature 
        # that needs to be added.
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMG_H, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        # The root, or AppController is the controller for this frame.
        # The controller is a way for the pages to interact with each other.
        # For this application, the controller is used to bring a particular
        # frame forward when the user requests it.
        self.controller = controller

        #assigned in init_image()
        self.tk_background = None 
        self.tk_overview_clicked = None
        self.tk_achievements_clicked = None
        self.tk_completed_clicked = None
        self.tk_credits_clicked = None
        self.tk_exit_clicked = None

        # Initialize the frame with buttons/text
        self.init_images()

        #Placing background image onto main menu frame

        # Use self as the parent since we are placing 
        # this label onto the frame
        self.main_menu_label = tk.Label(self, image=self.tk_background)
        self.main_menu_label.place(height=BACKGROUND_IMG_H, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to buttons
        self.main_menu_label.bind('<Button-1>', self.on_click)

    def init_images(self):
        """Initializes the background image, text, and
        buttons for this frame. 
        """

        # Initializing background and button images

        background_img = Image.open('./Images/background.png')
        program_title_img = Image.open('./Images/program_title.png')
        overview_btn_img = Image.open('./Images/overview.png')
        achievements_btn_img = Image.open('./Images/achievements.png')
        completed_btn_img = Image.open('./Images/completed.png')
        credits_btn_img = Image.open('./Images/credits.png')
        exit_btn_img = Image.open('./Images/exit.png')
        # Red buttons will be used to indicate when the user 
        # has clicked a button. 
        overview_red_btn_img = Image.open('./Images/overview_red.png')
        achievements_red_btn_img = Image.open('./Images/achievements_red.png')
        completed_red_btn_img = Image.open('./Images/completed_red.png')
        credits_red_btn_image = Image.open('./Images/credits_red.png')
        exit_red_btn_img = Image.open('./Images/exit_red.png')

        # Shrinking button images
        for img in (overview_btn_img, achievements_btn_img,
                   completed_btn_img, credits_btn_img,
                   exit_btn_img, overview_red_btn_img,
                   achievements_red_btn_img, completed_red_btn_img,
                   credits_red_btn_image, exit_red_btn_img):
            img.thumbnail(BUTTON_SIZE, Image.BICUBIC)

        # paste button images onto backgrond
        # third argument is a mask that allows button
        # backgrounds to be transparent
        background_img.paste(program_title_img, (150, 40), 
                               program_title_img)
        background_img.paste(overview_btn_img, (150, 220), 
                               overview_btn_img)
        background_img.paste(achievements_btn_img, (150, 320), 
                               achievements_btn_img)
        background_img.paste(completed_btn_img, (150, 420), 
                               completed_btn_img)
        background_img.paste(credits_btn_img, (150, 520), 
                               credits_btn_img)
        background_img.paste(exit_btn_img, (1300, 40), 
                               exit_btn_img)

        # Convert the Image object into a TkPhoto object

        self.tk_background = ImageTk.PhotoImage(background_img)

        # Placing red buttons over original buttons

        # When a user clicks a button, the intended effect is for the 
        # button to turn red and then back to yellow upon release.
        # To simulate this, each button has an assosciated 
        # image where only that button is red. Once the user clicks on
        # the button, the corresponding image will be placed over the 
        # frame to give this illusion. The image is then removed to
        # restore the button back to yellow. Red button images are 
        # pasted and stored now to allow for quicker access in on_click().

        # Create copies of background image so button images
        # aren't pasted over the same image
        overview_clicked = copy.deepcopy(background_img)
        achievements_clicked = copy.deepcopy(background_img)
        completed_clicked = copy.deepcopy(background_img)
        credits_clicked = copy.deepcopy(background_img)
        exit_clicked = copy.deepcopy(background_img)

        # Pasting button images over original buttons
        overview_clicked.paste(overview_red_btn_img,
                                       (150, 220), 
                                       overview_red_btn_img)
        self.tk_overview_clicked = ImageTk.PhotoImage(overview_clicked)
        achievements_clicked.paste(achievements_red_btn_img,
                                       (150, 320), 
                                       achievements_red_btn_img)
        self.tk_achievements_clicked = ImageTk.PhotoImage(achievements_clicked)
        completed_clicked.paste(completed_red_btn_img,
                                       (150, 420), 
                                       completed_red_btn_img)
        self.tk_completed_clicked = ImageTk.PhotoImage(completed_clicked)
        credits_clicked.paste(credits_red_btn_image,
                                       (150, 520), 
                                       credits_red_btn_image)
        self.tk_credits_clicked = ImageTk.PhotoImage(credits_clicked)
        exit_clicked.paste(exit_red_btn_img,
                                       (1300, 40), 
                                       exit_red_btn_img)
        self.tk_exit_clicked = ImageTk.PhotoImage(exit_clicked)
  
    def on_click(self, event):
        """Turns the clicked on button to red and raises the corresponding 
        frame. Exits the program if Exit is clicked.
        """

        #if "Overview" was clicked
        if 75 <= event.x <= 240 and 220 <= event.y <= 265:
            #On button click, turn button to red
            self.main_menu_label.configure(image=
                                       self.tk_overview_clicked)
            #Go to overview frame and turn button back to yellow
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "OverviewFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background)])
        #if "Achievements" was clicked 
        elif 75 <= event.x <= 300 and 320 <= event.y <= 365:
            self.main_menu_label.configure(image=
                                       self.tk_achievements_clicked)
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "AchievementsFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background)])
        #if "Completed" was clicked
        elif 75 <= event.x <= 240 and 420 <= event.y <= 465:
            self.main_menu_label.configure(image=
                                       self.tk_completed_clicked)
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "CompletedFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background)])
        #if "Credits" was clicked
        elif 75 <= event.x <= 197 and 520 <= event.y <= 565:
            self.main_menu_label.configure(image=
                                       self.tk_credits_clicked)
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "CreditsFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background)])

        #if "Exit" is pressed
        elif 1230 <= event.x <= 1290 and 40 <= event.y <= 85:
            self.main_menu_label.configure(image=
                                       self.tk_exit_clicked)
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      root.destroy())


class OverviewFrame(tk.Frame):

    def __init__(self, parent, controller):
        """Creates frame for 'Overview' section

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
        """
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMG_H, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

        #assigned in init_image()
        self.tk_background_img = None 
        self.tk_back_clicked = None

        # Initialize the background image with buttons/text
        self.init_images()

        #Place image onto frame
        self.overview_label = tk.Label(self, image=self.tk_background_blur)
        self.overview_label.place(height=BACKGROUND_IMG_H, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to back button
        self.overview_label.bind('<Button-1>', self.on_click)

    def init_images(self):
            """Initializes the background image, text, and
            buttons for this frame. Similar code with further
            explanation can be found in MainMenuFrame class.
            """

            background_blur_img = Image.open('./Images/background_blurred.png')
            back_btn_img = Image.open('./Images/back.png')

            # Red buttons will be used to indicate when the user 
            # has clicked a button. These images are used in the 
            # change_button_to_red() method
            back_red_btn_img = Image.open('./Images/back_red.png')

            # Shrinking button images
            for img in (back_btn_img,
                        back_red_btn_img):
                img.thumbnail(BUTTON_SIZE, Image.BICUBIC)

            # Paste button onto background image
            background_blur_img.paste(back_btn_img, (150, 40), 
                                   back_btn_img)

            # Convert the Image object into a TkPhoto object
            self.tk_background_blur = ImageTk.PhotoImage(background_blur_img)

            # Placing red buttons over original buttons

            # Create copies of background image so button images
            # aren't pasted over the same image
            back_clicked = copy.deepcopy(background_blur_img)
        
            # "Back" is clicked
            back_clicked.paste(back_red_btn_img, (150, 40), back_red_btn_img)
            self.tk_back_clicked = ImageTk.PhotoImage(back_clicked)

    def on_click(self, event):
        """Turns the clicked on button to red and raises the corresponding 
        frame. 
        """
        print("Area clicked was", event.x, event.y, sep=" ")
        # if "Back" was clicked
        if 80 <= event.x <= 155 and 40 <= event.y <= 85:
            self.overview_label.configure(image=self.tk_back_clicked)
            #Go to Main Menu frame and turn button back to yellow
            self.overview_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "MainMenuFrame"), 
                                       self.overview_label.configure(image=
                                       self.tk_background_blur)])


class AchievementsFrame(tk.Frame):
    """Contains all widgets and info related to uncompleted achievements.
    
    This class contains the 7 achievement categories, each a scrollable frame,
    onto which achievement frames are placed onto. 
    """

    def __init__(self, parent, controller, achievement_list):
        """Creates frame for 'Achievements' section

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
            achievements_list (List): a reference to the list containing all achievements.
        """
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMG_H, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

        self.achievement_list = achievement_list

        # Assigned in init_images()
        # These contain the background image but with a specific 
        # button turned red to indicate it has been selected.
        self.tk_back_clicked = None
        self.tk_GM_clicked = None
        self.tk_matches_clicked = None
        self.tk_honor_clicked = None
        self.tk_progress_clicked = None
        self.tk_items_clicked = None
        self.tk_social_clicked = None
        self.tk_general_clicked = None
        # exit button for info frame
        self.exit_x = None

        # Initialize the background image with buttons/text
        self.init_images()

        # Place background image onto frame using label. 'GM' is clicked
        # by default.
        self.bg_image_label = tk.Label(self, image=self.tk_GM_clicked)
        self.bg_image_label.place(height=BACKGROUND_IMG_H, 
                               width=PC_WIDTH - SCREEN_OFFSET)

        # Adding functionality to buttons
        self.bg_image_label.bind('<Button-1>', self.on_click)
        
        # categories{} contains a reference to each category frame
        # category_row{} keeps track of which row to place next achievement
        # Initialized in init_categories()
        self.categories = {}
        self.category_row = {}

        # iniate category frames
        self.init_categories()

        # fonts for achievement information
        self.title_font = font.Font(family='Helvetica',
                                            size=12, weight='bold')
        self.desc_font = font.Font(family='Helvetica', 
                                            size=12)
        self.big_title_font = font.Font(family='Helvetica',
                                            size=20, weight='bold')
         
        # cur_category will reference the currently shown category
        # Glorious Moments will always be the starting category
        self.cur_category = self.categories['GM']
        self.show_category('GM')

        # Populating categories with example data

        # Fonts for achievement information
        #self.title_font = font.Font(family='Helvetica',
        #                                    size=12, weight='bold')
        #self.desc_font = font.Font(family='Helvetica', 
        #                                    size=12)
        #self.big_title_font = font.Font(family='Helvetica',
        #                                    size=20, weight='bold')

        ## Each widget is binded to on click, so that whenver the user clicks
        ## anywhere on the achievement, another frame is raised to show 
        ## information for this achievement.
        #GM_frame = self.categories['GM'].scrolled_frame
        #row = 1
        #self.achievements = {}

        #self.level_completed = IntVar()
        #self.level_planned = IntVar()
        #self.list_completed = IntVar()
        #self.list_planned = IntVar()

        #total_columns = 6
        #while row <= 50:
        #    if (row % 2) == 0:
        #       # Initiating achievement frame
        #        achievement = tk.Frame(GM_frame, bd=2, relief = 'solid', 
        #                         background=self.GM_sbf.scrolled_frame \
        #                         .cget('bg'))
        #        achievement.grid(row=row, column=0, sticky='NW')
        #        achievement.bind('<Button-1>', lambda event: 
        #                         self.show_achievement("Leveled Achievement"))

        #        text = "Achievement Title " + str(row)
        #        title=tk.Label(achievement, text=text, anchor=W, fg='white',
        #                  height=1, font=self.title_font,
        #                  bg='#121111')
        #        title.grid(row=0, column=0, sticky=NW)
        #        title.bind('<Button-1>', lambda event: 
        #                   self.show_achievement("Leveled Achievement"))

        #        text = "How to get achievement\npart 2 of how to get achievement"
        #        desc=tk.Label(achievement, text=text, justify=LEFT, anchor=W,
        #                 height=2, fg='white',
        #                 font=self.desc_font,
        #                 background='#121111')
        #        desc.grid(row=1, column=0, sticky=NW)
        #        desc.bind('<Button-1>', lambda event: 
        #                  self.show_achievement("Leveled Achievement"))

        #        # Padding to seperate achievement info from points
        #        text = ""
        #        desc=tk.Label(achievement, width=40,
        #                bg='#121111')
        #        desc.grid(row=1, column=1, sticky=NW)
        #        desc.bind('<Button-1>', lambda event: 
        #                  self.show_achievement("Leveled Achievement"))
        #        # rowspan=2 is a way of centering a label between two other rows
        #        img = tk.Label(achievement, image=self.points_5, anchor=W,
        #                   borderwidth=0, highlightthickness=0)
        #        img.grid(row=0, rowspan=2, column = 2, sticky=W)
        #        img.bind('<Button-1>', lambda event: 
        #                 self.show_achievement("Leveled Achievement"))
        #        text = "3000 x"
        #        desc=tk.Label(achievement, text=text, anchor=E, fg='white',
        #                height=1, width=10, font=self.desc_font, 
        #                bg='#121111')
        #        desc.grid(row=1, column=3, sticky=NW)
        #        desc.bind('<Button-1>', lambda event: 
        #                  self.show_achievement("Leveled Achievement"))
        #        img = tk.Label(achievement, image=self.silver_fragment, anchor=W,
        #                   borderwidth=0, highlightthickness=0)
        #        img.grid(row=0, rowspan=2, column = 4, sticky=W)
        #        img.bind('<Button-1>', lambda event: 
        #                 self.show_achievement("Leveled Achievement"))




        #        # Initiating achievement info frame
        #        self.leveled_achievement_sbf = ScrollableFrame(self, height = 500,
        #                                                     width = 702, 
        #                                                     bg = '#121111')
        #        leveled_achievement_frame = self.leveled_achievement_sbf.scrolled_frame
        #        self.leveled_achievement_sbf.place(x=527, y=BACKGROUND_IMG_H/2, anchor=CENTER)

        #        exit_button = tk.Label(leveled_achievement_frame, image=self.exit_x, anchor=E,
        #                   borderwidth=0, highlightthickness=0)
        #        exit_button.grid(row=0, column = 5, sticky=E, pady = 10)
        #        exit_button.bind('<Button-1>', lambda event: self.exit_achievement("Leveled Achievement"))

        #        text = "  Leveled Achievement"
        #        title=tk.Label(leveled_achievement_frame, text=text, anchor=W, fg='white',
        #                  height=1, font=big_self.title_font,
        #                  bg=self.leveled_achievement_sbf.scrolled_frame.cget('bg'))
        #        title.grid(row=1, column=0, sticky=NW)

        #        text = ""
        #        desc=tk.Label(leveled_achievement_frame, width=5,
        #                bg='#121111')
        #        desc.grid(row=1, column=1, sticky=NW)

        #        planned_button = tk.Checkbutton(leveled_achievement_frame,
        #                                          variable=self.level_planned, activebackground='#121111',
        #                                          bg=self.leveled_achievement_sbf.scrolled_frame.cget('bg'))
        #        planned_button.grid(row=1, column=2, sticky=E)

        #        text = "Planned"
        #        checkbox_text = tk.Label(leveled_achievement_frame, text=text, anchor=W, fg='white',
        #                                     bg='#121111')
        #        checkbox_text.grid(row=1, column=3, sticky=W)

        #        completed_button = tk.Checkbutton(leveled_achievement_frame,  
        #                                          variable=self.level_completed, activebackground='#121111',
        #                                          bg=self.leveled_achievement_sbf.scrolled_frame.cget('bg'))
        #        completed_button.grid(row=1, column=4, sticky=E)

        #        text = "Completed"
        #        checkbox_text = tk.Label(leveled_achievement_frame, text=text, anchor=W, fg='white',
        #                                    bg='#121111')
        #        checkbox_text.grid(row=1, column=5, sticky=W)

        #        # Draws a line under achievement title
        #        text = "     _________________________________________________________________________"
        #        line = tk.Label(leveled_achievement_frame, text=text, anchor=W, fg='white',
        #                  height=1, font=self.title_font,
        #                  bg='#121111')
        #        line.grid(row=2, column=0, columnspan=total_columns, sticky=NW)

        #        this_row=3
        #        # Adding leveled achivement
        #        for level in ('I', 'II', 'III', 'IV', 'V'):
        #            achievement = tk.Frame(leveled_achievement_frame, bd=2, relief = 'solid', 
        #                             background=self.GM_sbf.scrolled_frame \
        #                             .cget('bg'))
        #            achievement.grid(row=this_row, column=0, columnspan=2, sticky=NW)

        #            text = "Achievement Title " + level
        #            title=tk.Label(achievement, text=text, anchor=W, fg='white',
        #                      height=1, font=self.title_font,
        #                      bg='#121111')
        #            title.grid(row=0, column=0, sticky=NW)

        #            text = "How to get achievement\npart 2 of how to get achievement"
        #            desc=tk.Label(achievement, text=text, justify=LEFT, anchor=W,
        #                     height=2, fg='white',
        #                     font=self.desc_font,
        #                     background='#121111')
        #            desc.grid(row=1, column=0, sticky=NW)

             

        #            # Padding to seperate achievement info from points
        #            text = ""
        #            desc=tk.Label(achievement, width=5,
        #                    bg='#121111')
        #            desc.grid(row=1, column=1, sticky=NW)

        #            # rowspan=2 is a way of centering a label between two other rows
        #            img = tk.Label(achievement, image=self.points_5, anchor=W,
        #                       borderwidth=0, highlightthickness=0)
        #            img.grid(row=0, rowspan=2, column = 2, sticky=W)

        #            text = "3000 x"
        #            desc=tk.Label(achievement, text=text, anchor=E, fg='white',
        #                    height=1, width=9, font=self.desc_font, 
        #                    bg='#121111')
        #            desc.grid(row=1, column=3, sticky=NW)

        #            img = tk.Label(achievement, image=self.silver_fragment, anchor=W,
        #                       borderwidth=0, highlightthickness=0)
        #            img.grid(row=0, rowspan=2, column = 4, sticky=W)


        #            planned_button = tk.Checkbutton(leveled_achievement_frame,
        #                                          variable=self.level_planned,
        #                                          bg=self.leveled_achievement_sbf.scrolled_frame.cget('bg'),
        #                                          activebackground='#121111')
        #            planned_button.grid(row=this_row, column=2, sticky=E)

        #            text = "Planned"
        #            checkbox_text = tk.Label(leveled_achievement_frame, text=text, anchor=W, fg='white',
        #                                     bg='#121111')
        #            checkbox_text.grid(row=this_row, column=3, sticky=W)

        #            completed_button = tk.Checkbutton(leveled_achievement_frame,
        #                                          variable=self.level_completed, 
        #                                          bg=self.leveled_achievement_sbf.scrolled_frame.cget('bg'),
        #                                          activebackground='#121111')
        #            completed_button.grid(row=this_row, column=4, sticky=E)

        #            text = "Completed"
        #            checkbox_text = tk.Label(leveled_achievement_frame, text=text, anchor=W, fg='white',
        #                                     bg='#121111')
        #            checkbox_text.grid(row=this_row, column=5, sticky=W)
        #            this_row = this_row+1

        #        # Draws a line under achievement title
        #        text = "     _________________________________________________________________________"
        #        line = tk.Label(leveled_achievement_frame, text=text, anchor=W, fg='white',
        #                  font=self.title_font,
        #                  bg='#121111')
        #        line.grid(row=this_row, column=0, columnspan=total_columns, sticky=NW)

        #        this_row = this_row + 1

        #        text = ("This is where the achievement information will go.\n"
        #        "Things like tips and tricks, and the best way to get the achievement will be placed here.\n"
        #        "Here is another line as an example. Nice!")

        #        desc=tk.Label(leveled_achievement_frame, text=text, justify=LEFT, fg='white',
        #                    font=self.desc_font,
        #                    bg=self.leveled_achievement_sbf.scrolled_frame.cget('bg'))
        #        desc.grid(row=this_row, column=0, columnspan=total_columns, sticky=NW)

        #        self.achievements["Leveled Achievement"] = self.leveled_achievement_sbf

        #    else:
        #        achievement = tk.Frame(GM_frame, bd=2, relief = 'solid',
        #                         background='#121111')
        #        achievement.grid(row=row, column=0, sticky='NW')
        #        achievement.bind('<Button-1>', lambda event: 
        #                         self.show_achievement("List Achievement"))

        #        text = "Achievement Title " + str(row)
        #        title=tk.Label(achievement, text=text, anchor=W, fg='white',
        #                  height=1, font=self.title_font,
        #                  bg='#121111')
        #        title.grid(row=0, column=0, sticky=NW)
        #        title.bind('<Button-1>', lambda event: 
        #                   self.show_achievement("List Achievement"))

        #        text = "How to get achievement\npart 2 of how to get achievement"
        #        desc=tk.Label(achievement, text=text, justify=LEFT, anchor=W,
        #                 height=2, fg='white',
        #                 font=self.desc_font,
        #                 background='#121111')
        #        desc.grid(row=1, column=0, sticky=NW)
        #        desc.bind('<Button-1>', lambda event: 
        #                  self.show_achievement("List Achievement"))

        #        text = ""
        #        desc=tk.Label(achievement, width=40,
        #                bg='#121111')
        #        desc.grid(row=1, column=1, sticky=NW)
        #        desc.bind('<Button-1>', lambda event: 
        #                  self.show_achievement("List Achievement"))
        #        img = tk.Label(achievement, image=self.points_30, anchor=W,
        #                   borderwidth=0, highlightthickness=0)
        #        img.grid(row=0, rowspan=2, column = 2, sticky=W)
        #        img.bind('<Button-1>', lambda event: 
        #                 self.show_achievement("List Achievement"))
        #        text = "5 x"
        #        desc=tk.Label(achievement, text=text, anchor=E, fg='white',
        #                height=1, width=10,
        #                font=self.desc_font, 
        #                bg='#121111')
        #        desc.grid(row=1, column=3, sticky=NW)
        #        desc.bind('<Button-1>', lambda event: 
        #                  self.show_achievement("List Achievement"))
        #        # rowspan=2 is a way of centering a label between two other rows
        #        img = tk.Label(achievement, image=self.premium_crate, anchor=W,
        #                   borderwidth=0, highlightthickness=0)
        #        img.grid(row=0, rowspan=2, column = 4, sticky=W)
        #        img.bind('<Button-1>', lambda event: 
        #                 self.show_achievement("List Achievement"))






        #        # Initiating achievement info frame
        #        self.list_achievement_sbf = ScrollableFrame(self, height = 500,
        #                                                     width = 702, 
        #                                                     bg = '#121111')
        #        list_achievement_frame = self.list_achievement_sbf.scrolled_frame
        #        self.list_achievement_sbf.place(x=527, y=BACKGROUND_IMG_H/2, anchor=CENTER)
                
        #        exit_button = tk.Label(list_achievement_frame, image=self.exit_x, anchor=E,
        #                   borderwidth=0, highlightthickness=0)
        #        exit_button.grid(row=0, column = 5, sticky=E, pady = 10)
        #        exit_button.bind('<Button-1>', lambda event: self.exit_achievement("List achievement"))

        #        text = "  List Achievement"
        #        title=tk.Label(list_achievement_frame, text=text, anchor=W, fg='white',
        #                  height=1, font=big_self.title_font,
        #                  bg='#121111')
        #        title.grid(row=1, column=0, sticky=NW)

        #        text = ""
        #        desc=tk.Label(list_achievement_frame, width=5,
        #                bg='#121111')
        #        desc.grid(row=1, column=1, sticky=NW)

        #        planned_button = tk.Checkbutton(list_achievement_frame, activebackground='#121111',
        #                                          variable=self.level_planned,
        #                                          bg='#121111')
        #        planned_button.grid(row=1, column=2, sticky=E)

        #        text = "Planned"
        #        checkbox_text = tk.Label(list_achievement_frame, text=text, anchor=W, fg='white',
        #                                     bg='#121111')
        #        checkbox_text.grid(row=1, column=3, sticky=W)

        #        completed_button = tk.Checkbutton(list_achievement_frame, activebackground='#121111',
        #                                          variable=self.level_completed,
        #                                          bg='#121111')
        #        completed_button.grid(row=1, column=4, sticky=E)

        #        text = "Completed"
        #        checkbox_text = tk.Label(list_achievement_frame, text=text, anchor=W, fg='white',
        #                                    bg='#121111')
        #        checkbox_text.grid(row=1, column=5, sticky=W)

        #        # Draws a line under achievement title
        #        text = "     _________________________________________________________________________"
        #        line = tk.Label(list_achievement_frame, text=text, anchor=W, fg='white',
        #                  height=1, font=self.title_font,
        #                  bg='#121111')
        #        line.grid(row=2, column=0, columnspan=total_columns, sticky=NW)

        #        this_row=3

        #        for task in range(5):
        #            text="- Do this certain task"
        #            line = tk.Label(list_achievement_frame, text=text, anchor=W, fg='white',
        #                  font=self.desc_font,
        #                  bg='#121111')
        #            line.grid(row=this_row, column=0, columnspan=total_columns, sticky=NW)
        #            this_row = this_row+1

        #        self.achievements["List Achievement"] = self.list_achievement_sbf

        #        # Draws a line under achievement title
        #        text = "     _________________________________________________________________________"
        #        line = tk.Label(list_achievement_frame, text=text, anchor=W, fg='white',
        #                  height=1, font=self.title_font,
        #                  bg='#121111')
        #        line.grid(row=this_row, column=0, columnspan=total_columns, sticky=NW)
        #        this_row = this_row+1

        #        text = ("This is where the achievement information will go.\n"
        #        "Things like tips and tricks, and the best way to get the achievement will be placed here.\n"
        #        "Here is another line as an example. Nice!")

        #        desc=tk.Label(list_achievement_frame, text=text, justify=LEFT, fg='white',
        #                    font=self.desc_font,
        #                    bg='#121111')
        #        desc.grid(row=this_row, column=0, columnspan=total_columns, sticky=NW)

        #        self.achievements["List achievement"] = self.list_achievement_sbf

        #    row=row+1   
    def init_images(self):
        """Initializes images and buttons for this frame.
        
        Refer to init_images() in MainMenuFrame for a more detailed
        description on red button use.
        """

        # Initializing background and button images

        background_blur_img = Image.open('./Images/background_blurred.png')
        back_btn_img = Image.open('./Images/back.png')
        GM_img = Image.open('./Images/glorious_moments.png')
        matches_img = Image.open('./Images/matches.png')
        honor_img = Image.open('./Images/honor.png')
        progress_img = Image.open('./Images/progress.png')
        items_img = Image.open('./Images/items.png')
        social_img = Image.open('./Images/social.png')
        general_img = Image.open('./Images/general.png')
        # Red buttons will be used to indicate when the user 
        # has clicked a button.
        back_btn_red_img = Image.open('./Images/back_red.png')
        G_M_red_img = Image.open('./Images/glorious_moments_red.png')
        matches_red_img = Image.open('./Images/matches_red.png')
        honor_red_img = Image.open('./Images/honor_red.png')
        progress_red_img = Image.open('./Images/progress_red.png')
        items_red_img = Image.open('./Images/items_red.png')
        social_red_img = Image.open('./Images/social_red.png')
        general_red_img = Image.open('./Images/general_red.png')

        # shrinking back button
        back_btn_img.thumbnail(BUTTON_SIZE, Image.BICUBIC)
        back_btn_red_img.thumbnail(BUTTON_SIZE, Image.BICUBIC)

        # Shrinking category images
        for img in (GM_img, G_M_red_img,
                    matches_img, matches_red_img, honor_img, honor_red_img,
                    progress_img, progress_red_img, items_img, 
                    items_red_img, social_img, social_red_img, 
                    general_img, general_red_img):
            img.thumbnail((277, 30), Image.BICUBIC)

        # Paste button onto background image
        background_blur_img.paste(back_btn_img, (150, 40), 
                                back_btn_img)
        background_blur_img.paste(GM_img, (980, 90),
                                GM_img)
        background_blur_img.paste(matches_img, (980, 155),
                                matches_img)
        background_blur_img.paste(honor_img, (980, 225),
                                honor_img)
        background_blur_img.paste(progress_img, (980, 295),
                                progress_img)
        background_blur_img.paste(items_img, (980, 365),
                                items_img)
        background_blur_img.paste(social_img, (980, 435),
                                social_img)
        background_blur_img.paste(general_img, (980, 505),
                                general_img)

        # Pasting red buttons over original buttons

        # Create copies of background image so button images
        # aren't pasted over the same image
        back_clicked = copy.deepcopy(background_blur_img)
        GM_clicked = copy.deepcopy(background_blur_img)
        matches_clicked = copy.deepcopy(background_blur_img)
        honor_clicked = copy.deepcopy(background_blur_img)
        progress_clicked = copy.deepcopy(background_blur_img)
        items_clicked = copy.deepcopy(background_blur_img)
        social_clicked = copy.deepcopy(background_blur_img)
        general_clicked = copy.deepcopy(background_blur_img)
        
        # Pasting button images over original buttons
        back_clicked.paste(back_btn_red_img,
                                        (150, 40), 
                                        back_btn_red_img)
        self.tk_back_clicked = ImageTk.PhotoImage(back_clicked)

        GM_clicked.paste(G_M_red_img, (980, 90), G_M_red_img)
        self.tk_GM_clicked = ImageTk.PhotoImage(GM_clicked)

        matches_clicked.paste(matches_red_img, (980, 155), matches_red_img)
        self.tk_matches_clicked = ImageTk.PhotoImage(matches_clicked)

        honor_clicked.paste(honor_red_img, (980, 225), honor_red_img)
        self.tk_honor_clicked = ImageTk.PhotoImage(honor_clicked)

        progress_clicked.paste(progress_red_img, (980, 295), progress_red_img)
        self.tk_progress_clicked = ImageTk.PhotoImage(progress_clicked)

        items_clicked.paste(items_red_img, (980, 365), items_red_img)
        self.tk_items_clicked = ImageTk.PhotoImage(items_clicked)

        social_clicked.paste(social_red_img, (980, 435), social_red_img)
        self.tk_social_clicked = ImageTk.PhotoImage(social_clicked)

        general_clicked.paste(general_red_img, (980, 505), general_red_img)
        self.tk_general_clicked = ImageTk.PhotoImage(general_clicked)

        # exit button for achievement info frame
        exit_x_img = Image.open('./Images/x.png')
        exit_x_img.thumbnail((30,30))
        self.exit_x = ImageTk.PhotoImage(exit_x_img)

    def init_categories(self):
        """Initializes achievement categories, each as a scrollable frame.

        This method loops through the category names and creates a scrollable frame
        for each. Two dictionaries are initialized here:

        self.categories:
            stores a reference to each category frame under the category name.
            Any achievements will need to be placed onto the scrolled_frame 
            attribute, which is accessed as 
            self.categories[category].scrolled_frame

        self.category_row:
            keeps track of which row to place the next achievement
        """

        for category in ('GM', 'matches', 'honor', 'progress', 
                         'items', 'social','general'):
            category_frame = ScrollableFrame(self, height = 500, width = 702, 
                                               bg = '#121111')
            category_frame.place(x=527, y=BACKGROUND_IMG_H/2, anchor=CENTER)
            # First achievement will be placed on row 0
            self.category_row[category] = 0
            # Store a reference to this category's frame in a dictionary
            self.categories[category] = category_frame

    def init_achievement_frame(self, achievement):
        """Initiates an achievement frame in it's corresponding category"""

        # Get a reference to the corresponding category frame
        category_frame = self.categories[achievement.category].scrolled_frame

        # initiate achievement onto category_frame
        self.achievement_frame = tk.Frame(category_frame, bd=2, 
                                                     relief='solid', 
                                                     bg='#121111')
        self.achievement_frame.grid(row=self.category_row[achievement.category],
                                column=0, sticky='NW')
        self.category_row[achievement.category] += 1

        # Create info frame when clicked
        self.achievement_frame.bind('<Button-1>', lambda event: 
                            self.init_leveled_info_frame(
                                achievement))

        text = achievement.title + " " + achievement.level_rom_num
        frame_title=tk.Label(self.achievement_frame, text=text, anchor=W, 
                        fg='white', height=1, font=self.title_font,
                        bg='#121111')
        frame_title.grid(row=0, column=0, sticky=NW)
        frame_title.bind('<Button-1>', lambda event: 
                    self.init_leveled_info_frame(
                        achievement))

        # in-frame achievement description
        text = achievement.desc
        frame_desc=tk.Label(self.achievement_frame, text=text, justify=LEFT, anchor=W,
                    height=2, fg='white',
                    font=self.desc_font,
                    background='#121111')
        frame_desc.grid(row=1, column=0, sticky=NW)
        frame_desc.bind('<Button-1>', lambda event: 
                    self.init_leveled_info_frame(
                        achievement))

        # padding to seperate achievement info from points
        text = ""
        frame_pad=tk.Label(self.achievement_frame, width=40,
                bg='#121111')
        frame_pad.grid(row=1, column=1, sticky=NW)
        frame_pad.bind('<Button-1>', lambda event: 
                    self.init_leveled_info_frame(
                        achievement))

        img = achievement.points_img
        frame_points = tk.Label(self.achievement_frame, image=img, anchor=W,
                    borderwidth=0, highlightthickness=0)
        # rowspan=2 is a way of centering a label between two other rows
        frame_points.grid(row=0, rowspan=2, column = 2, sticky=W)
        frame_points.bind('<Button-1>', lambda event: 
                    self.init_leveled_info_frame(
                        achievement))

        # reward amount
        text = achievement.reward_amount + " x "
        frame_amount=tk.Label(self.achievement_frame, text=text, anchor=E, fg='white',
                height=1, width=10, font=self.desc_font, 
                bg='#121111')
        frame_amount.grid(row=1, column=3, sticky=NW)
        frame_amount.bind('<Button-1>', lambda event: 
                    self.init_leveled_info_frame(
                        achievement))

        img = achievement.reward_img
        frame_reward = tk.Label(self.achievement_frame, image=img, anchor=W,
                    borderwidth=0, highlightthickness=0)
        frame_reward.grid(row=0, rowspan=2, column = 4, sticky=W)
        frame_reward.bind('<Button-1>', lambda event: 
                    self.init_leveled_info_frame(
                        achievement))

    def init_leveled_achievements(self):
        with open('./PUBGM Achievement Tracker/leveled_achievements.csv','r') as csv_file:
            csvReader = csv.DictReader(csv_file, delimiter=',')
            for row in csvReader:
                # Starts by initializing the first level
                category = row['Category']
                title = row['Title']
                desc = row['Description']
                # levels_string contains info specific to each level
                levels_string = row['Levels']
                overall_completed = row['Overall_completed']
                info = row['Info']

                # if achievement is already completed, initialize in CompletedFrame
                if overall_completed == 1:
                    pass

                # Get a reference to the corresponding category frame
                category_frame = self.categories[category].scrolled_frame

                # Split levels string into a list of levels
                levels_list = levels_string.split('+')

                # Keeps track of the index in achievement_list where the
                # next achievement will be placed
                achievement_index = 0
                # Keeps track of the index of the first level of the achievement
                first_level = 0
                # Set to true once the achievement has been initialized onto
                # it's corresponding category frame
                frame_initialized = False
                for level in levels_list:
                    # Split each level into its attributes
                    level_attrs = level.split('.')
                    level_rom_num = level_attrs[0]
                    is_planned = level_attrs[1]
                    is_completed = level_attrs[2]
                    num_tasks = level_attrs[3]
                    # Assigning a Tk Image to points and reward
                    points_img = self.reward_points[level_attrs[4]]
                    reward_amount = level_attrs[5]
                    reward_img = self.reward_images[level_attrs[6]]

                    # input number of tasks needed in level into description string
                    num_tasks_desc = desc.format(num_tasks=num_tasks)


                    # To save RAM, only the first level of each achievement
                    # will store the info attribute. Therefore a check
                    # for the first level is done. 
                    if level_rom_num == 'I':
                        print("Is I")
                        print(f"Info is: {info}")
                        achievement = LeveledAchievement(category, title, num_tasks_desc, 
                                                  level_rom_num, is_planned,
                                                  is_completed, num_tasks, 
                                                  points_img, reward_amount, 
                                                  reward_img, achievement_index, info)
                        first_level = achievement_index
                    else:
                        print("IN else loop")
                        achievement = LeveledAchievement(category, title, num_tasks_desc, 
                                                  level_rom_num, is_planned,
                                                  is_completed, num_tasks, 
                                                  points_img, reward_amount, 
                                                  reward_img, achievement_index)
                    # add achievement to list
                    self.achievement_list.append(achievement)
                    achievement_index += 1

                    # Only the first level of the achievement to not be completed
                    # will be shown in the category frame. Therefore, if the 
                    # level has been completed, skip to the next level.
                    if is_completed == 1:
                        pass
                    # If this is the next level to be completed, initialize it 
                    # onto the category frame
                    elif frame_initialized == False:
                        # This frame will be placed onto the category frame
                        self.achievement_frame = tk.Frame(category_frame, bd=2, 
                                                     relief='solid', 
                                                     bg='#121111')
                        self.achievement_frame.grid(row=self.category_row[category],
                                              column=0, sticky='NW')
                        # Create info frame when clicked
                        self.achievement_frame.bind('<Button-1>', lambda event: 
                                            self.init_leveled_info_frame(
                                                first_level))
                        self.category_row[category] += 1

                        text = title + " " + level_rom_num
                        frame_title=tk.Label(self.achievement_frame, text=text, anchor=W, 
                                       fg='white', height=1, font=self.title_font,
                                       bg='#121111')
                        frame_title.grid(row=0, column=0, sticky=NW)
                        frame_title.bind('<Button-1>', lambda event: 
                                    self.init_leveled_info_frame(
                                        first_level))

                        # in-frame achievement description
                        text = desc.format(num_tasks=num_tasks)
                        frame_desc=tk.Label(self.achievement_frame, text=text, justify=LEFT, anchor=W,
                                    height=2, fg='white',
                                    font=self.desc_font,
                                    background='#121111')
                        frame_desc.grid(row=1, column=0, sticky=NW)
                        frame_desc.bind('<Button-1>', lambda event: 
                                    self.init_leveled_info_frame(
                                        first_level))

                        # padding to seperate achievement info from points
                        text = ""
                        frame_pad=tk.Label(self.achievement_frame, width=40,
                                bg='#121111')
                        frame_pad.grid(row=1, column=1, sticky=NW)
                        frame_pad.bind('<Button-1>', lambda event: 
                                    self.init_leveled_info_frame(
                                        first_level))

                        img = points_img
                        frame_points = tk.Label(self.achievement_frame, image=img, anchor=W,
                                    borderwidth=0, highlightthickness=0)
                        # rowspan=2 is a way of centering a label between two other rows
                        frame_points.grid(row=0, rowspan=2, column = 2, sticky=W)
                        frame_points.bind('<Button-1>', lambda event: 
                                    self.init_leveled_info_frame(
                                        first_level))

                        # reward amount
                        text = reward_amount + " x "
                        frame_amount=tk.Label(self.achievement_frame, text=text, anchor=E, fg='white',
                                height=1, width=10, font=self.desc_font, 
                                bg='#121111')
                        frame_amount.grid(row=1, column=3, sticky=NW)
                        frame_amount.bind('<Button-1>', lambda event: 
                                    self.init_leveled_info_frame(
                                        first_level))

                        img = reward_img
                        frame_reward = tk.Label(self.achievement_frame, image=img, anchor=W,
                                    borderwidth=0, highlightthickness=0)
                        frame_reward.grid(row=0, rowspan=2, column = 4, sticky=W)
                        frame_reward.bind('<Button-1>', lambda event: 
                                    self.init_leveled_info_frame(
                                        first_level))

                        self.achievement_frame.grid(row = self.category_row[category])

                        self.category_row[category] += 1
                        
                        frame_initialized = True
                    # else achievement level has not been completed yet, and a lower level
                    # has already been initialized onto category_frame
                    else:
                        pass
                    
    def init_list_achievement(self):
        pass

    def init_leveled_info_frame(self,achievement):
        """Creates an info frame for the passed in achievement.
        
        This method works by passing in an achievement, getting
        a reference to the first and last levels of the achievement, 
        and then progressing through each level to create the 
        achievement info frame. This frame is then placed over 
        top of the current category frame, with AchievementFrame 
        as the parent. The info frame is deleted upon clicking 'X'.

        Args:
            achievement (Achievement): a reference an instance of
            LeveledAchievement
        """

        # get a reference to the first level 
        cur_lvl_index = achievement.list_index
        print(cur_lvl_index)
        try:
            while(self.achievement_list[cur_lvl_index].title == achievement.title):
                cur_lvl_index -= 1
            first_level = self.achievement_list[cur_lvl_index]
        # If Level I of the achievemenet is at index 0, index -1 will tried
        # to be accessed which throws an error. First_level will already have
        # been assigned at this point.
        except IndexError:
            pass

        # get a reference to the last level
        cur_lvl_index = achievement.list_index
        try:
            while (self.achievement_list[cur_lvl_index].title == achievement.title):
                cur_lvl_index += 1
            last_level = self.achievement_list[cur_lvl_index]
        # reached the end of the list. last_level will already have been 
        # assigned at this point
        except IndexError:
            last_level = self.achievement_list[cur_lvl_index]

        # Initiating achievement info frame
        leveled_achievement_sbf = ScrollableFrame(self, height = 500,
                                                        width = 702, 
                                                        bg = '#121111')
        # use info_frame as the parent
        info_frame = leveled_achievement_sbf.scrolled_frame
        leveled_achievement_sbf.place(x=527, y=BACKGROUND_IMG_H/2, anchor=CENTER)

        # the total columns used in creating the info frame. Used for column span
        total_columns = 6
        # initiating information at top for all levels

        # the exit button removes the frame from view and destroys it
        img = self.exit_x
        exit_button = tk.Label(info_frame, image=img, anchor=E,
                    borderwidth=0, highlightthickness=0)
        exit_button.grid(row=0, column = 5, sticky=E, pady = 10)
        exit_button.bind('<Button-1>', lambda event:[leveled_achievement_sbf.place_forget(),
                         leveled_achievement_sbf.destroy])

        # The collective title for all levels
        text = first_level.title
        title=tk.Label(info_frame, text=text, anchor=W, fg='white',
                    height=1, font=self.big_title_font,
                    bg='#121111')
        title.grid(row=1, column=0, sticky=NW)

        # padding to seperate title from checkboxes
        text = ""
        pad=tk.Label(info_frame, width=5,
                bg='#121111')
        pad.grid(row=1, column=1, sticky=NW)

        # The planned/completed buttons at the top of the info frame use the
        # same variables as the last level of the achievement. If the last
        # level of the achievement is completed, the entire achievement is
        # completed.
        var = last_level.planned_var
        planned_button = tk.Checkbutton(info_frame,
                                            variable=var, activebackground='#121111',
                                            bg='#121111',
                                            command=achievement.on_planned)
        planned_button.grid(row=1, column=2, sticky=E)

        text = "Planned"
        checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                        bg='#121111')
        checkbox_text.grid(row=1, column=3, sticky=W)

        var = last_level.completed_var
        completed_button = tk.Checkbutton(info_frame,  
                                            variable=var, activebackground='#121111',
                                            bg='#121111', 
                                            command=last_level.on_completed)
        completed_button.grid(row=1, column=4, sticky=E)

        text = "Completed"
        checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                    bg='#121111')
        checkbox_text.grid(row=1, column=5, sticky=W)

        # Draws a line under achievement title
        text = "     _________________________________________________________________________"
        line = tk.Label(info_frame, text=text, anchor=W, fg='white',
                    height=1, font=self.title_font,
                    bg='#121111')
        line.grid(row=2, column=0, columnspan=total_columns, sticky=NW)

        # next_row is the next row for an achievement frame to be placed
        next_row=3

        # Adding a frame for each level, starting with the first level
        cur_lvl_index = first_level.list_index
        achievement = self.achievement_list[cur_lvl_index]
        # set this to True once all levels have been initialized, which exits the loop
        last_level_initialized = False
        while (last_level_initialized == False):
            # if reached the last level, terminate the loop after this iteration
            if achievement == last_level:
                last_level_initialized = True

            self.achievement_frame = tk.Frame(info_frame, bd=2, relief = 'solid', 
                                background='#121111')
            self.achievement_frame.grid(row=next_row, column=0, columnspan=2, sticky=NW)

            text = achievement.title + " " + achievement.level_rom_num
            frame_title=tk.Label(self.achievement_frame, text=text, anchor=W, fg='white',
                        height=1, font=self.title_font,
                        bg='#121111')
            frame_title.grid(row=0, column=0, sticky=NW)

            text = achievement.desc
            frame_desc=tk.Label(self.achievement_frame, text=text, justify=LEFT, anchor=W,
                        height=2, fg='white',
                        font=self.desc_font,
                        background='#121111')
            frame_desc.grid(row=1, column=0, sticky=NW)

            # Padding to seperate achievement info from points
            text = ""
            pad=tk.Label(self.achievement_frame, width=5,
                    bg='#121111')
            pad.grid(row=1, column=1, sticky=NW)
            
            img = achievement.points_img
            frame_points = tk.Label(self.achievement_frame, image=img, anchor=W,
                        borderwidth=0, highlightthickness=0)
            frame_points.grid(row=0, rowspan=2, column = 2, sticky=W)

            text = achievement.reward_amount + " x "
            frame_amount=tk.Label(self.achievement_frame, text=text, anchor=E, fg='white',
                    height=1, width=9, font=self.desc_font, 
                    bg='#121111')
            frame_amount.grid(row=1, column=3, sticky=NW)

            img = achievement.reward_img
            frame_reward = tk.Label(self.achievement_frame, image=img, anchor=W,
                        borderwidth=0, highlightthickness=0)
            frame_reward.grid(row=0, rowspan=2, column = 4, sticky=W)

            var = achievement.planned_var
            planned_button = tk.Checkbutton(info_frame,
                                            variable=var,
                                            bg='#121111',
                                            activebackground='#121111',
                                            command=achievement.on_planned)
            planned_button.grid(row=next_row, column=2, sticky=E)

            text = "Planned"
            checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                        bg='#121111')
            checkbox_text.grid(row=next_row, column=3, sticky=W)

            var = achievement.completed_var
            completed_button = tk.Checkbutton(info_frame,
                                            variable=var, 
                                            bg='#121111',
                                            activebackground='#121111',
                                            command=achievement.on_completed)
            completed_button.grid(row=next_row, column=4, sticky=E)

            text = "Completed"
            checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                        bg='#121111')
            checkbox_text.grid(row=next_row, column=5, sticky=W)
            
            # the next achievement will be added to the row below
            next_row += 1

            
            # move pointer to next achievement
            cur_lvl_index += 1
            # prevents an index error if at the end of the list
            try:
                achievement = self.achievement_list[cur_lvl_index]
            except IndexError:
                pass

        # draws a line under the achievement frames
        text = "     _________________________________________________________________________"
        line = tk.Label(info_frame, text=text, anchor=W, fg='white',
                    font=self.title_font,
                    bg='#121111')
        line.grid(row=next_row, column=0, columnspan=total_columns, sticky=NW)

        next_row += 1

        # information on how to get the achievement
        text = str(first_level.info)
        info=tk.Label(info_frame, text=text, justify=LEFT, fg='white',
                    font=self.desc_font,
                    bg='#121111')
        info.grid(row=next_row, column=0, columnspan=total_columns, sticky=NW)

    def show_achievement(self, achievement):
        """Raises achievement frame to show achievement info
        Args:
            achievement: a string containing the name of the achievement
        """
        achievement_to_be_shown = self.achievements[achievement]
        # Unbind mousewheel to achievement list so it can be bound to
        # achievement information instead
        self.cur_category.unbind_mousewheel()
        achievement_to_be_shown.bind_mousewheel()
        achievement_to_be_shown.tkraise()

    def exit_achievement(self, achievement):
        """Exits achievement and returns to the current category frame"""
        exited_achievement = self.achievements[achievement]
        # Unbind mousewheel to achievement info so it can be re-bound
        # to achievement list
        exited_achievement.unbind_mousewheel()
        self.cur_category.bind_mousewheel()
        self.cur_category.tkraise()

    def on_click(self, event):
        """Turns the clicked on button to red and raises the corresponding 
        frame. 
        """

        # if "Back" was clicked
        if 80 <= event.x <= 155 and 40 <= event.y <= 85:
            self.bg_image_label.configure(image=self.tk_back_clicked)
            # Go to Main Menu frame and return back-button to yellow
            # 'GM' is turned back to red since it's the default category
            self.bg_image_label.bind('<ButtonRelease-1>', lambda event:
                                      [self.controller.show_frame(
                                          "MainMenuFrame"), 
                                       self.bg_image_label.configure(image=
                                       self.tk_GM_clicked), 
                                       self.bg_image_label.unbind(
                                           '<ButtonRelease-1>')])
        # if "Glorious Moments" was clicked
        elif 900 <= event.x <= 1100 and 90 <= event.y <= 120:
            self.bg_image_label.configure(image=self.tk_GM_clicked)
            self.show_category("GM")
        # if "Matches" was clicked
        elif 900 <= event.x <= 1000 and 155 <= event.y <= 185:
            self.bg_image_label.configure(image=self.tk_matches_clicked)
            self.show_category("matches")
        # if "Honor" was clicked
        elif 900 <= event.x <= 975 and 225 <= event.y <= 255:
            self.bg_image_label.configure(image=self.tk_honor_clicked)
            self.show_category("honor")
        # if "Progress" was clicked
        elif 900 <= event.x <= 1010 and 295 <= event.y <= 325:
            self.bg_image_label.configure(image=self.tk_progress_clicked)
            self.show_category("progress")
        # if "Items" was clicked
        elif 900 <= event.x <= 965 and 365 <= event.y <= 395:
            self.bg_image_label.configure(image=self.tk_items_clicked)
            self.show_category("items")
        # if "Social" was clicked
        elif 900 <= event.x <= 975 and 435 <= event.y <= 465:
            self.bg_image_label.configure(image=self.tk_social_clicked)
            self.show_category("social")
        # if "General" was clicked
        elif 900 <= event.x <= 995 and 505 <= event.y <= 535:
            self.bg_image_label.configure(image=self.tk_general_clicked)
            self.show_category("general")

    def show_category(self, category):
        """Shows the frame for the given achievement category.
        Args:
            category: a string containing the name of the category
                to be shown.
        """
        category_to_be_shown = self.categories[category]
        # The current category needs to be unbound to the mousewheel
        # so that category_to_be_shown can bind to it instead
        self.cur_category.unbind_mousewheel()
        category_to_be_shown.bind_mousewheel()
        self.cur_category = category_to_be_shown
        category_to_be_shown.tkraise()


class CompletedFrame(tk.Frame):
    
    def __init__(self, parent, controller, achievement_list):
        """Creates frame for 'Completed' section

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
        """
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMG_H, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

        #assigned in init_image()
        self.tk_background_img = None 
        self.tk_back_clicked = None

        # Initialize the background image with buttons/text
        self.init_images()

        #Place image onto frame using label
        self.completed_label = tk.Label(self, image=self.tk_background_blur)
        self.completed_label.place(height=BACKGROUND_IMG_H, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to back button

        self.completed_label.bind('<Button-1>', self.on_click)

    def init_images(self):
            """Initializes the background image, text, and
            buttons for this frame. Similar code with further
            explanation can be found in MainMenuFrame class.
            """

            background_blur_img = Image.open('./Images/background_blurred.png')
            back_btn_img = Image.open('./Images/back.png')

            # Red buttons will be used to indicate when the user 
            # has clicked a button. These images are used in the 
            # change_button_to_red() method
            back_red_btn_img = Image.open('./Images/back_red.png')

            # Shrinking button images
            for img in (back_btn_img,
                        back_red_btn_img):
                img.thumbnail(BUTTON_SIZE, Image.BICUBIC)

            # Paste button onto background image
            background_blur_img.paste(back_btn_img, (150, 40), 
                                   back_btn_img)

            # Convert the Image object into a TkPhoto object
            self.tk_background_blur = ImageTk.PhotoImage(background_blur_img)

            # Placing red buttons over original buttons

            # Create copies of background image so button images
            # aren't pasted over the same image
            back_clicked = copy.deepcopy(background_blur_img)
        
            # "Back" is clicked
            back_clicked.paste(back_red_btn_img,
                                           (150, 40), 
                                           back_red_btn_img)
            self.tk_back_clicked = ImageTk.PhotoImage(back_clicked)

    def on_click(self, event):
        """Turns the clicked on button to red and raises the corresponding 
        frame. 
        """

        print("Area clicked was", event.x, event.y, sep=" ")
        # if "Back" was clicked
        if 80 <= event.x <= 155 and 40 <= event.y <= 85:
            self.completed_label.configure(image=
                                       self.tk_back_clicked)
            #Go to Main Menu frame and turn button back to yellow
            self.completed_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "MainMenuFrame"), 
                                       self.completed_label.configure(image=
                                       self.tk_background_blur)])


class CreditsFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        """Creates frame for 'Credits' section

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
        """
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMG_H, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

        #assigned in init_image()
        self.tk_background_img = None 
        self.tk_back_clicked = None

        # Initialize the background image with buttons/text
        self.init_images()

        #Place image onto frame using label
        self.credits_label = tk.Label(self, image=self.tk_background_blur)
        self.credits_label.place(height=BACKGROUND_IMG_H, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to back button

        self.credits_label.bind('<Button-1>', self.on_click)

    def init_images(self):
            """Initializes the background image, text, and
            buttons for this frame. Similar code with further
            explanation can be found in MainMenuFrame class.
            """

            background_blur_img = Image.open('./Images/background_blurred.png')
            back_btn_img = Image.open('./Images/back.png')

            # Red buttons will be used to indicate when the user 
            # has clicked a button. These images are used in the 
            # change_button_to_red() method
            back_red_btn_img = Image.open('./Images/back_red.png')

            # Shrinking button images
            for img in (back_btn_img,
                        back_red_btn_img):
                img.thumbnail(BUTTON_SIZE, Image.BICUBIC)

            # Paste button onto background image
            background_blur_img.paste(back_btn_img, (150, 40), 
                                   back_btn_img)

            # Convert the Image object into a TkPhoto object
            self.tk_background_blur = ImageTk.PhotoImage(background_blur_img)

            # Placing red buttons over original buttons

            # Create copies of background image so button images
            # aren't pasted over the same image
            back_clicked = copy.deepcopy(background_blur_img)
        
            # "Back" is clicked
            back_clicked.paste(back_red_btn_img, (150, 40), 
                               back_red_btn_img)
            self.tk_back_clicked = ImageTk.PhotoImage(back_clicked)


    def on_click(self, event):
        """Turns the clicked on button to red and raises the corresponding 
        frame. 
        """

        print("Area clicked was", event.x, event.y, sep=" ")
        # if "Back" was clicked
        if 80 <= event.x <= 155 and 40 <= event.y <= 85:
            self.credits_label.configure(image=
                                       self.tk_back_clicked)
            #Go to Main Menu frame and turn button back to yellow
            self.credits_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "MainMenuFrame"), 
                                       self.credits_label.configure(image=
                                       self.tk_background_blur)])


class Achievement():
    """Contains static dictionaries and lists which both LeveledAchievement
    and ListAchievement can access.
    """
    # a dictionary mapping point amount to an image
    points_images = {}
    # a dictionary mapping reward type to a reward image
    reward_images = {}
    # a list containing a reference to every achievement
    achievement_list = []

    @staticmethod
    def __init__(achievement_list):
        Achievement.achievement_list = achievement_list
        Achievement.init_reward_images()

    @staticmethod
    def init_reward_images():
        """Initializes images for reward and reward points and places
        into a static dictionary.

        Each instance of an Achievement will contains an image for the reward
        and reward points. Each instance will be passed in a string specifying
        the associated reward and reward points. An image is assigned to the
        instance by passing in the string value into the dictionary
        and getting a reference to the corresponding image.
        """
        for points in ('5','10','15','20','30','40','50','60'):
            img = Image.open('./Images/'+points+'_points.png')
            img.thumbnail((40,40), Image.BICUBIC)
            img = ImageTk.PhotoImage(img)
            Achievement.points_images[points] = img
        for reward in ('bp','silver','classic_scrap','classic_crate',
                       'premium_scrap','premium_crate'):
            img = Image.open('./Images/'+reward+'.png')
            img.thumbnail((50,50), Image.BICUBIC)
            img = ImageTk.PhotoImage(img)
            Achievement.reward_images[reward] = img


class LeveledAchievement(Achievement):
    """Each level for a leveled achievement will be stored as an instance
    of this class.

    Args:
        category (string): achievement category
        title (string): achievement title
        desc (string): achievement description
        level_rom_num (string): a roman numeral representing the level of 
            the achievement
        is_planned (int): 1 for planned, 0 for not planned
        is_completed (int): 1 for completed, 0 for not completed
        num_tasks (int): the number of tasks required to complete
            the the level of the achievement. The task is described in
            achievement description.
        points_img (int): amount of points awarded upon level completion.
        reward_amount (int): amount of reward awarded upon level completion
        reward_img (string): name of reward.
        list_index (int): the index at which this level will be placed in
            achievement_list.
        info (string): contains tips and tricks about the achievement. Only
            stored in the first level of each achievement.
    """
    def __init__(self, category, title, desc,
                 level_rom_num, is_planned, is_completed, num_tasks, points_img, 
                 reward_amount, reward_img, list_index, info = None):
        
        self.category = category
        self.title = title
        self.desc = desc
        self.level_rom_num = level_rom_num
        # variables for checkboxes
        self.planned_var = IntVar(value=is_planned)
        self.completed_var = IntVar(value=is_completed)
        self.num_tasks = num_tasks
        # initiate points_img and reward_img using static dictionaries
        self.points_img = Achievement.points_images[points_img]
        self.reward_img = Achievement.reward_images[reward_img]
        self.reward_amount = reward_amount
        self.list_index = list_index
        self.info = info

    def on_completed_checkbox(self):
        """Automatically checks or unchecks "completed" checkboxes in other levels
        of achievement.

        Called when checking or unchecking a "completed" checkbox.

        If checking, this method will automatically check every level lower
        than the current level. Ex. If lvl III is checked, this method
        will check off "completed" for lvl II and lvl I.

        Similarly, if unchecking, this method will automatically uncheck
        every level higher than the current level.
        """
        try:
            # if checking
            if self.completed_var.get() == 1:
                # get the next lower level of achievement
                next_lower_lvl = Achievement.achievement_list[self.list_index-1]
                cur_lvl_index = next_lower_lvl.list_index
                while (Achievement.achievement_list[cur_lvl_index].title == self.title):
                    # check checkboxes
                    next_lower_lvl.completed_var.set(1)
                    cur_lvl_index -= 1
                    next_lower_lvl = Achievement.achievement_list[cur_lvl_index]
            # else, uncheck every higher level
            else:
                # get next higher level
                next_higher_lvl = Achievement.achievement_list[self.list_index+1]
                cur_lvl_index = next_higher_lvl.list_index
                while(Achievement.achievement_list[cur_lvl_index].title == self.title):

                    next_higher_lvl.completed_var.set(0)
                    cur_lvl_index += 1
                    next_higher_lvl = Achievement.achievement_list[cur_lvl_index]
        # list may go out of bounds if at the end or beginning of list
        except IndexError:
            pass

    def on_planned(self):
        """Automatically checks or unchecks "planned" checkboxes in other 
        levels of achievement.

        See on_completed() for a more detailed description of method behaviour.
        """

        next_lower_lvl = Achievement.achievement_list[self.list_index-1]
        cur_lvl_index = next_lower_lvl.list_index
        try:
            while (Achievement.achievement_list[cur_lvl_index].title == self.title):
                if self.planned_var.get() == 1:
                    next_lower_lvl.planned_var.set(1)
                else:
                    next_lower_lvl.planned_var.set(0)
                cur_lvl_index -= 1
                next_lower_lvl = Achievement.achievement_list[cur_lvl_index]
        # list may go out of bounds if at the end or beginning of list
        except IndexError:
            pass


if __name__ == "__main__":
    root = AppController()
    root.mainloop()