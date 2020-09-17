import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import copy
import csv
import textwrap

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

        # Keeps track of the index in achievement_list where the
        # next achievement will be placed
        self.list_index = 0

        # Initializing all frames

        # All frames will be stored in a dictionary for quick access
        self.frames = {}

        for F in (MainMenuFrame, OverviewFrame, CreditsFrame):
            page_name = F.__name__
            # Create an instance of each frame
            frame = F(parent=container, controller=self)
            # Input frame into dictionary
            self.frames[page_name] = frame

            # Put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # In the case of AchievementsFrame, initialize two frames:
        # one for completed achievements, the other for uncompleted

        # first initialize static variables
        AchievementsFrame.static_init(parent=container, controller=self,
                                    achievement_list=self.achievement_list)

        for F in ("UncompletedAchievements", "CompletedAchievements"):
            frame = AchievementsFrame()
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Initialize the reward images used for each achievement
        Achievement.static_init(AchievementsFrame.achievement_list)

        # Initialize achievements from csv file
        self.init_leveled_achievements()
        self.init_list_achievements()

        # Start by showing the Main Menu
        self.show_frame("MainMenuFrame")

    def init_leveled_achievements(self):
        """Reads in leveled achievement information from csv file and initiates each one.
        Achievement will be initiated in either AchievementsFrame or 
        CompletedFrame, depending on if it's been completed or not.
        The leveled_achievements.csv file is formatted in the following way:
        row[0] = category (int)
        row[1] = title (string)
        row[2] = description (string)
        row[3] = levels (string)(Level.planned?(Y=1,N=0).
                  completed?(Y=1,N=0).# of tasks needed.points.reward amount.
                  reward type+etc...)
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
            self.list_index = 0

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

                # reference to the first and last level of achievement
                # these are used for creating an instance of the
                # LeveledAttributes class
                first_lvl = None
                last_lvl = None
                # To save RAM, the category, title, description, info,
                # frame, and a reference to the first and last levels
                # are stored in a seperate class that all levels of
                # the achievement can access. The first and last level
                # references are assigned to shared_attrs in the loop
                # below
                shared_attrs = LeveledAttributes(category, title, desc,
                                                 info, first_lvl, last_lvl)

                # Set to true once the achievement has been initialized onto
                # its one of the category frames. Only the highest level to 
                # not be completed will be initialized as a frame
                frame_initialized = False
                for level in levels_list:
                    # Split each level into its attributes
                    lvl_attrs = level.split('.')
                    lvl_rom_num = lvl_attrs[0]
                    is_planned = lvl_attrs[1]
                    is_completed = lvl_attrs[2]
                    num_tasks = lvl_attrs[3]
                    points = lvl_attrs[4]
                    reward_amount = lvl_attrs[5]
                    reward = lvl_attrs[6]

                    
                    achievement = LeveledAchievement \
                        (lvl_rom_num, is_planned, is_completed, num_tasks, 
                         points, reward_amount, reward, self.list_index, 
                         shared_attrs)

                    if (lvl_rom_num == "I"):
                        shared_attrs.first_lvl = achievement
                    if (level == levels_list[-1]):
                        shared_attrs.last_lvl = achievement
                            
                    # add achievement to list
                    self.achievement_list.append(achievement)
                    self.list_index += 1

                    # if achievement is completed, initiate frame in CompletedAchievements
                    if overall_completed == 1:
                        self.frames["CompletedAchievements"].init_achievement_frame(achievement)
                        break
                    # else initiate in UncompletedAchievements
                    else:
                        # Only the first level of the achievement to not be completed
                        # will be shown in the category frame. Therefore, if the 
                        # level has been completed, skip to the next level.
                        if is_completed == 1:
                            pass
                        # if this is the next level to be completed, initialize it 
                        # as a frame in AchievementsFrame
                        if frame_initialized == False:
                            self.frames["UncompletedAchievements"].init_achievement_frame(achievement)
                            frame_initialized = True
                        # else achievement level has not been completed yet, and a lower level
                        # has already been initialized as a frame
                        else:
                            pass

    def init_list_achievements(self):
        """Reads in list achievement information from csv file and initiates each one.
        Achievement will be initiated in either AchievementsFrame or 
        CompletedFrame, depending on if it's been completed or not.
        The list_achievement.csv file is formatted in the following way:
        row[0] = category (int)
        row[1] = title (string)
        row[2] = description (string)
        row[3] = list of tasks(string)
        row[4] = overall_completed?(int)(0=No, 1=Yes)
        row[5] = achievement info (string)
         
        In row[3], periods are used as the delimiter between a 
        each task.
        """
        # Initiating list achievements
        with open('./PUBGM Achievement Tracker/list_achievements.csv','r') as csv_file:
            csvReader = csv.DictReader(csv_file, delimiter=',')

            # Keeps track of the index in achievement_list where the
            # next achievement will be placed
            self.list_index = 0

            for row in csvReader:
                category = row['Category']
                title = row['Title']
                desc = row['Description']
                is_planned = row['Planned']
                is_completed = row['Completed']
                points = row['Points']
                reward_amount = row['Reward Amount']
                reward = row['Reward']
                info = row['Info']

                # Seperate tasks into a list of individual tasks
                tasks_string = row['Tasks']
                task_list = tasks_string.split('+')

                # frame has not yet been initialized
                frame = None

                achievement = ListAchievement(category, title, desc, task_list, is_planned,
                                              is_completed, points, reward_amount, reward,
                                              self.list_index, info, frame)

                # add achievement to list
                self.achievement_list.append(achievement)
                self.list_index += 1

                # if achievement is completed, initiate frame in CompletedAchievements
                if is_completed == 1:
                    self.frames["CompletedAchievements"].init_achievement_frame(achievement)
                # else initiate in AchievementsAchievements
                else:
                    self.frames["UncompletedAchievements"].init_achievement_frame(achievement)

    def complete_achievement(self, achievement):
        """Initializes given achievement in CompletedAchievements"""
        self.frames["CompletedAchievements"].init_achievement_frame(achievement)

    def revert_achievement(self, achievement):
        """Initializes achievement back into UncompletedAchievements"""
        self.frames["UncompletedAchievements"].init_achievement_frame(achievement)
        
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
                                          "UncompletedAchievements"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background)])
        #if "Completed" was clicked
        elif 75 <= event.x <= 240 and 420 <= event.y <= 465:
            self.main_menu_label.configure(image=
                                       self.tk_completed_clicked)
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "CompletedAchievements"), 
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
    """Contains all widgets related to achievements, uncompleted or completed.
    
    This class contains the 7 achievement categories, each a scrollable frame,
    onto which achievement frames are placed onto. Users will be able to 
    scroll through the achievements and interact with them. Upon clicking an
    achievement, more info about it will be brought up as another frame. 
    The user can then check off if they have already completed the achievement
    or if they're planning to complete it via the checkboxes.

    There will be two instances of this class. One will be for uncompleted 
    achievements, the other for completed. These two instances will pass 
    achievements to each other. ie. When the user checks the 'completed' 
    button, this achievements will be passed to the 'Completed instance'
    and initialized as a frame there. Passing achievements will be done 
    through the Appcontroller.

    For a leveled achievement, it is considered completed when all levels
    are completed.
    """
    
    # a list containing a reference to every achievement
    achievement_list = None
    # The parent and controller should be the same for each instance
    parent = None
    controller = None

    # images shared between each instance

    # These contain the background image but with a specific 
    # button turned red to indicate it has been selected.
    tk_back_clicked = None
    tk_GM_clicked = None
    tk_matches_clicked = None
    tk_honor_clicked = None
    tk_progress_clicked = None
    tk_items_clicked = None
    tk_social_clicked = None
    tk_general_clicked = None
    # exit button for info frame
    exit_x = None

    # fonts for achievement information
    title_font = None
    desc_font = None
    big_title_font = None



    @staticmethod
    def static_init(parent, controller, achievement_list):
        """Initializes static variables used in class.

        THe program is set up so that both instances of this class (completed
        and uncompleted achievements) share the same parent and controller.

        Args: 
            parent (Frame): the frame onto all instances of this class 
                will be placed
            controller (Frame): The controller frame is a way for other frames
                to interact with each other. 
            achievements_list (List): a reference to the list containing all 
                achievements.
        """
        AchievementsFrame.achievement_list = achievement_list
        AchievementsFrame.parent = parent
        AchievementsFrame.controller = controller

        AchievementsFrame.init_images()

        AchievementsFrame.title_font = font.Font(family='Helvetica',
                                        size=12, weight='bold')
        AchievementsFrame.desc_font = font.Font(family='Helvetica', 
                                        size=12)
        AchievementsFrame.big_title_font = font.Font(family='Helvetica',
                                        size=20, weight='bold')


    @staticmethod
    def init_images():
        """Initializes images and buttons for use in this class
        
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

        # add text at bottom right of category frame
        text = Image.open('./Images/click_on_achievement_txt.png')
        text.thumbnail((200, 30), Image.BICUBIC)
        background_blur_img.paste(text, (760, 565), text)

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
        back_clicked.paste(back_btn_red_img, (150, 40), back_btn_red_img)
        AchievementsFrame.tk_back_clicked = \
            ImageTk.PhotoImage(back_clicked)

        GM_clicked.paste(G_M_red_img, (980, 90), G_M_red_img)
        AchievementsFrame.tk_GM_clicked = \
            ImageTk.PhotoImage(GM_clicked)

        matches_clicked.paste(matches_red_img, (980, 155), matches_red_img)
        AchievementsFrame.tk_matches_clicked = \
            ImageTk.PhotoImage(matches_clicked)

        honor_clicked.paste(honor_red_img, (980, 225), honor_red_img)
        AchievementsFrame.tk_honor_clicked = \
            ImageTk.PhotoImage(honor_clicked)

        progress_clicked.paste(progress_red_img, (980, 295), progress_red_img)
        AchievementsFrame.tk_progress_clicked = \
            ImageTk.PhotoImage(progress_clicked)

        items_clicked.paste(items_red_img, (980, 365), items_red_img)
        AchievementsFrame.tk_items_clicked = \
            ImageTk.PhotoImage(items_clicked)

        social_clicked.paste(social_red_img, (980, 435), social_red_img)
        AchievementsFrame.tk_social_clicked = \
            ImageTk.PhotoImage(social_clicked)

        general_clicked.paste(general_red_img, (980, 505), general_red_img)
        AchievementsFrame.tk_general_clicked = \
            ImageTk.PhotoImage(general_clicked)

        # exit button for achievement info frame
        exit_x_img = Image.open('./Images/x.png')
        exit_x_img.thumbnail((30,30))
        AchievementsFrame.exit_x = ImageTk.PhotoImage(exit_x_img)

    def __init__(self):
        """Initializes a frame to contain achievements"""
        tk.Frame.__init__(self, AchievementsFrame.parent, 
                          height=BACKGROUND_IMG_H, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        # Place background image onto frame using label. 
        # 'GM' is clicked by default.
        self.bg_image_label = tk.Label(self, image=
                                       AchievementsFrame.tk_GM_clicked)
        self.bg_image_label.place(height=BACKGROUND_IMG_H, 
                                  width=PC_WIDTH - SCREEN_OFFSET)

        # Adding functionality to buttons
        self.bg_image_label.bind('<Button-1>', self.on_click)
        
        # categories{} contains a reference to each category frame
        # category_row{} keeps track of which row to place next achievement
        # Initialized in init_categories()
        self.categories = {}

        self.category_row = {}

        # initialize category frames
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

    def init_categories(self):
        """Initializes achievement categories, each as a scrollable frame.
        This method loops through the category names and creates a scrollable 
        frame for each. Two dictionaries are initialized here:
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

        is_leveled = isinstance(achievement, LeveledAchievement)
        # shorten code by extracting attributes first
        if is_leveled:
            category = achievement.shared_attrs.category
            title = achievement.shared_attrs.title
            desc = achievement.shared_attrs.desc
            # input number of tasks needed in level into description string
            desc = desc.format(num_tasks=achievement.num_tasks)
        else:
            category = achievement.category
            title = achievement.title
            desc = achievement.desc


        # Get a reference to the corresponding category frame
        category_frame = self.categories[category].scrolled_frame

        # initiate achievement onto category_frame
        achievement_frame = tk.Frame(category_frame, bd=2, 
                                         relief='solid', bg='#121111')
        achievement_frame.grid(row=self.category_row[category],
                                    column=0, sticky='NW')
        self.category_row[category] += 1
        # add frame reference to achievement
        if is_leveled:
            achievement.shared_attrs.frame = achievement_frame
        else:
            achievement.frame = achievement_frame


        # Create info frame when clicked
        achievement_frame.bind('<Button-1>', lambda event: 
                            self.init_info_frame(achievement))

        # Leveled achievement needs to concatenate it's level with it's title
        if is_leveled:
            text = title + " " + achievement.level_rom_num
        else:
            text = title
        frame_title=tk.Label(achievement_frame, text=text, anchor=W, 
                            fg='white', font=AchievementsFrame.title_font, 
                            bg='#121111')
        frame_title.grid(row=0, column=0, sticky=NW)
        frame_title.bind('<Button-1>', lambda event: 
                    self.init_info_frame(achievement))

        # in-frame achievement description
        # max line length is 72 characters
        text = textwrap.fill(desc, width=72)
        frame_desc=tk.Label(achievement_frame, text=text, justify=LEFT, 
                            anchor=W, height=2, width=56, fg='white',
                            font=AchievementsFrame.desc_font, bg='#121111')
        frame_desc.grid(row=1, column=0, sticky=NW)
        frame_desc.bind('<Button-1>', lambda event: 
                    self.init_info_frame(achievement))

        img = achievement.points_img
        frame_points = tk.Label(achievement_frame, image=img, anchor=W,
                                borderwidth=0, highlightthickness=0)
        # rowspan=2 is a way of centering a label between two other rows
        frame_points.grid(row=0, rowspan=2, column = 2, sticky=W)
        frame_points.bind('<Button-1>', lambda event: 
                    self.init_info_frame(achievement))

        # reward amount
        text = achievement.reward_amount + " x "
        frame_amount=tk.Label(achievement_frame, text=text, anchor=E, 
                              fg='white', height=1, width=10, 
                              font=AchievementsFrame.desc_font, bg='#121111')
        frame_amount.grid(row=1, column=3, sticky=NW)
        frame_amount.bind('<Button-1>', lambda event: 
                    self.init_info_frame(achievement))

        img = achievement.reward_img
        frame_reward = tk.Label(achievement_frame, image=img, anchor=W,
                                borderwidth=0, highlightthickness=0)
        frame_reward.grid(row=0, rowspan=2, column = 4, sticky=W)
        frame_reward.bind('<Button-1>', lambda event: 
                    self.init_info_frame(achievement))

    def init_info_frame(self, achievement):
        """Calls init_leveled_info_frame() or init_list_info_frame() depending
        on type of achievement.
        This simplifies code in init_achievement_frame().
        Args:
            achievement (LeveledAchievement or ListAchievement): a reference 
            to an instance of a LeveledAchievement or ListAchievement
        """

        if isinstance(achievement, LeveledAchievement):
            self.init_leveled_info_frame(achievement)
        else:
            self.init_list_info_frame(achievement)

    def init_leveled_info_frame(self,achievement):
        """Creates an info frame for the passed in leveled achievement.
        
        This method works by passing in an achievement, getting
        a reference to the first and last levels of the achievement, 
        and then progressing through each level to create the 
        achievement info frame. This frame is then placed over 
        top of the current category frame, with AchievementFrame 
        as the parent. The info frame is deleted upon clicking 'X'.
        Args:
            achievement (LeveledAchievement): a reference to an instance of
            LeveledAchievement
        """

        # shorten code by extracting attributes first
        category = achievement.shared_attrs.category
        title = achievement.shared_attrs.title
        desc = achievement.shared_attrs.desc
        # input number of tasks needed in level into description string
        desc = desc.format(num_tasks=achievement.num_tasks)
        info = achievement.shared_attrs.info
        # reference to first and last level
        first_lvl = achievement.shared_attrs.first_lvl
        last_lvl = achievement.shared_attrs.last_lvl

        # Initiating achievement info frame
        leveled_achievement_sbf = ScrollableFrame(self, height = 500,
                                                  width = 702, bg='#121111')
        # use info_frame as the parent
        info_frame = leveled_achievement_sbf.scrolled_frame
        leveled_achievement_sbf.place(x=527, y=BACKGROUND_IMG_H/2, 
                                      anchor=CENTER)

        # total columns used in creating the info frame. Used for columnspan
        total_columns = 6

        # initiating information at top for all levels

        # the exit button removes the frame from view and destroys it
        img = AchievementsFrame.exit_x
        exit_button = tk.Label(info_frame, image=img, anchor=E,
                    borderwidth=0, highlightthickness=0)
        exit_button.grid(row=0, column = 5, sticky=E, pady = 10)
        exit_button.bind('<Button-1>', lambda event:[
                        leveled_achievement_sbf.place_forget(),
                        leveled_achievement_sbf.destroy])

        # The collective title for all levels
        text = title
        achievement_title = tk.Label(info_frame, text=text, anchor=W, 
                                     fg='white', height=1, width=20, 
                                     font=AchievementsFrame.big_title_font,
                                     bg='#121111')
        achievement_title.grid(row=1, column=0, sticky=NW)

        # The planned/completed buttons at the top of the info frame use the
        # same variables as the last level of the achievement. If the last
        # level of the achievement is completed, the entire achievement is
        # completed.
        var = last_lvl.planned_var
        planned_btn = tk.Checkbutton(info_frame, variable=var, 
                                     activebackground='#121111', bg='#121111',
                                     command=last_lvl.on_planned_checkbox)
        planned_btn.grid(row=1, column=2, sticky=E)

        text = "Planned"
        checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                 bg='#121111')
        checkbox_text.grid(row=1, column=3, sticky=W)

        var = last_lvl.completed_var
        completed_btn = tk.Checkbutton(info_frame, variable=var, 
                                       activebackground='#121111', bg='#121111', 
                                       command=last_lvl.on_completed_checkbox)
        completed_btn.grid(row=1, column=4, sticky=E)

        text = "Completed"
        checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                 bg='#121111')
        checkbox_text.grid(row=1, column=5, sticky=W)

        # Draws a line under achievement title
        text = "     _________________________________________________________________________"
        line = tk.Label(info_frame, text=text, anchor=W, fg='white',
                    height=1, font=AchievementsFrame.title_font, bg='#121111')
        line.grid(row=2, column=0, columnspan=total_columns, sticky=NW)

        # next_row is the next row for an achievement frame to be placed
        next_row=3

        # Adding a frame for each level, starting with the first level
        cur_lvl_index = first_lvl.list_index
        achievement = AchievementsFrame.achievement_list[cur_lvl_index]
        # set this to True once all levels have been initialized
        last_level_initialized = False
        while (last_level_initialized == False):
            # if reached the last level, exit the loop after this iteration
            if achievement == last_lvl:
                last_level_initialized = True

            achievement_frame = tk.Frame(info_frame, bd=2, 
                                              relief = 'solid', bg='#121111')
            achievement_frame.grid(row=next_row, column=0, columnspan=2, 
                                        sticky=NW)

            text = title + " " + achievement.level_rom_num
            frame_title=tk.Label(achievement_frame, text=text, anchor=W, 
                                 fg='white', height=1, 
                                 font=AchievementsFrame.title_font, 
                                 bg='#121111')
            frame_title.grid(row=0, column=0, sticky=NW)

            text = textwrap.fill(desc, width=44)
            # input number of tasks needed in level into description string
            text = desc.format(num_tasks=achievement.num_tasks)
            frame_desc=tk.Label(achievement_frame, text=text, 
                                justify=LEFT, anchor=W, height=3, width=35, 
                                fg='white', font=AchievementsFrame.desc_font, 
                                bg='#121111')
            frame_desc.grid(row=1, column=0, sticky=NW)
            
            img = achievement.points_img
            frame_points = tk.Label(achievement_frame, image=img, 
                                    anchor=W, borderwidth=0, 
                                    highlightthickness=0)
            frame_points.grid(row=0, rowspan=3, column = 2, sticky=W)

            text = achievement.reward_amount + " x "
            frame_amount=tk.Label(achievement_frame, text=text, anchor=E,
                                  fg='white', height=1, width=9, 
                                  font=AchievementsFrame.desc_font, bg='#121111')
            frame_amount.grid(row=1, column=3, sticky=NW)

            img = achievement.reward_img
            frame_reward = tk.Label(achievement_frame, image=img, 
                                    anchor=W, borderwidth=0,
                                    highlightthickness=0)
            frame_reward.grid(row=0, rowspan=3, column = 4, sticky=W)

            var = achievement.planned_var
            planned_btn = tk.Checkbutton(info_frame, variable=var, 
                                         activebackground='#121111',
                                         bg='#121111',
                                         command=achievement.on_planned_checkbox)
            planned_btn.grid(row=next_row, column=2, sticky=E)

            text = "Planned"
            checkbox_text = tk.Label(info_frame, text=text, anchor=W, 
                                     fg='white', bg='#121111')
            checkbox_text.grid(row=next_row, column=3, sticky=W)

            var = achievement.completed_var
            completed_btn = tk.Checkbutton(info_frame, variable=var, 
                                            activebackground='#121111',
                                            bg='#121111',
                                            command=achievement.on_completed_checkbox)
            completed_btn.grid(row=next_row, column=4, sticky=E)

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
                achievement = AchievementsFrame.achievement_list[cur_lvl_index]
            except IndexError:
                pass

        # draws a line under the achievement frames
        text = "     _________________________________________________________________________"
        line = tk.Label(info_frame, text=text, anchor=W, fg='white',
                    font=AchievementsFrame.title_font, bg='#121111')
        line.grid(row=next_row, column=0, columnspan=total_columns, sticky=NW)
        next_row += 1

        # information on how to get the achievement
        text = textwrap.fill(info, width=101)
        info=tk.Label(info_frame, text=text, justify=LEFT, fg='white',
                    font=AchievementsFrame.desc_font, bg='#121111')
        info.grid(row=next_row, column=0, columnspan=total_columns, sticky=NW)

    def init_list_info_frame(self, achievement):
        """Creates the info frame for the passed in list achievement.
        
        Args:
            achievement (ListAchievement): a reference an instance of
            LeveledAchievement
        """

        # Initiating achievement info frame
        list_achievement_sbf = ScrollableFrame(self, height=500,
                                               width=702, bg='#121111')
        # use info_frame as the parent
        info_frame = list_achievement_sbf.scrolled_frame
        list_achievement_sbf.place(x=527, y=BACKGROUND_IMG_H/2, anchor=CENTER)
        
        # the total columns used in creating the info frame. Used for columnspan
        total_columns = 6

        img = AchievementsFrame.exit_x
        exit_button = tk.Label(info_frame, image=img, anchor=E,
                               borderwidth=0, highlightthickness=0)
        exit_button.grid(row=0, column = 5, sticky=E, pady = 10)
        exit_button.bind('<Button-1>', lambda event:
                         [list_achievement_sbf.place_forget(),
                         list_achievement_sbf.destroy])

        text = achievement.title
        title=tk.Label(info_frame, text=text, anchor=W, fg='white',
                    height=1, font=AchievementsFrame.big_title_font, width=20,
                    bg='#121111')
        title.grid(row=1, column=0, sticky=NW)

        # padding to seperate title from checkboxes
        pad=tk.Label(info_frame, width=5,
                bg='#121111')
        pad.grid(row=1, column=1, sticky=NW)

        var = achievement.planned_var
        planned_btn = tk.Checkbutton(info_frame, variable=var, 
                                     activebackground='#121111',
                                     bg='#121111',
                                     command=achievement.on_planned_checkbox)
        planned_btn.grid(row=1, column=2, sticky=E)

        text = "Planned"
        checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                 bg='#121111')
        checkbox_text.grid(row=1, column=3, sticky=W)

        var = achievement.completed_var
        completed_btn = tk.Checkbutton(info_frame, variable=var, 
                                       activebackground='#121111',
                                       bg='#121111', 
                                       command=achievement.on_completed_checkbox)
        completed_btn.grid(row=1, column=4, sticky=E)

        text = "Completed"
        checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                 bg='#121111')
        checkbox_text.grid(row=1, column=5, sticky=W)

        # Draws a line under achievement title
        text = "     _________________________________________________________________________"
        line = tk.Label(info_frame, text=text, anchor=W, fg='white',
                        height=1, font=AchievementsFrame.title_font,
                        bg='#121111')
        line.grid(row=2, column=0, columnspan=total_columns, sticky=NW)

        # keeps track of which row to place next widget
        next_row=3

        for task in achievement.task_list:
            text = textwrap.fill("- " + task, width=84)
            text = text.replace("\n", "\n   ")
            line = tk.Label(info_frame, text=text, anchor=W, fg='white', justify=LEFT,
                    font=AchievementsFrame.desc_font, bg='#121111')
            line.grid(row=next_row, column=0, columnspan=total_columns, sticky=NW)
            next_row = next_row+1

        # Draws a line under achievement title
        text = "     _________________________________________________________________________"
        line = tk.Label(info_frame, text=text, anchor=W, fg='white',
                    height=1, font=AchievementsFrame.title_font, bg='#121111')
        line.grid(row=next_row, column=0, columnspan=total_columns, sticky=NW)
        next_row += 1

        text = textwrap.fill(achievement.info, width=101)
        desc=tk.Label(info_frame, text=text, justify=LEFT, fg='white',
                    font=AchievementsFrame.desc_font, bg='#121111')
        desc.grid(row=next_row, column=0, columnspan=total_columns, sticky=NW)

    def exit_achievement(self, achievement):
        """Exits achievement and returns to the current category frame"""
        exited_achievement = \
            AchievementsFrame.achievement_list[achievement.list_index]
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
            self.bg_image_label.configure(image=
                                          AchievementsFrame.tk_back_clicked)
            # Go to Main Menu frame and return back-button to yellow
            # 'GM' is turned back to red since it's the default category
            self.bg_image_label.bind('<ButtonRelease-1>', lambda event:
                                     [AchievementsFrame.controller.show_frame(
                                         "MainMenuFrame"), 
                                      self.bg_image_label.configure(image=
                                      self.tk_GM_clicked), 
                                      self.bg_image_label.unbind(
                                          '<ButtonRelease-1>')])
        # if "Glorious Moments" was clicked
        elif 900 <= event.x <= 1100 and 90 <= event.y <= 120:
            self.bg_image_label.configure(image=
                                          AchievementsFrame.tk_GM_clicked)
            self.show_category("GM")
        # if "Matches" was clicked
        elif 900 <= event.x <= 1000 and 155 <= event.y <= 185:
            self.bg_image_label.configure(image=
                                          AchievementsFrame.tk_matches_clicked)
            self.show_category("matches")
        # if "Honor" was clicked
        elif 900 <= event.x <= 975 and 225 <= event.y <= 255:
            self.bg_image_label.configure(image=
                                          AchievementsFrame.tk_honor_clicked)
            self.show_category("honor")
        # if "Progress" was clicked
        elif 900 <= event.x <= 1010 and 295 <= event.y <= 325:
            self.bg_image_label.configure(image=
                                          AchievementsFrame.tk_progress_clicked)
            self.show_category("progress")
        # if "Items" was clicked
        elif 900 <= event.x <= 965 and 365 <= event.y <= 395:
            self.bg_image_label.configure(image=
                                          AchievementsFrame.tk_items_clicked)
            self.show_category("items")
        # if "Social" was clicked
        elif 900 <= event.x <= 975 and 435 <= event.y <= 465:
            self.bg_image_label.configure(image=
                                          AchievementsFrame.tk_social_clicked)
            self.show_category("social")
        # if "General" was clicked
        elif 900 <= event.x <= 995 and 505 <= event.y <= 535:
            self.bg_image_label.configure(image=
                                          AchievementsFrame.tk_general_clicked)
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
    def static_init(achievement_list):
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


class LeveledAttributes():
    """A class for storing shared attributes between every level of 
    an achievement.
    
    These shared attributes include the category, title, description,
    info, frame, and a reference to the first and last levels.
    Achievements levels will be able to access these attributes by 
    storing a reference to the instance of this class.

    Args:
        category (string): achievement category
        title (string): achievement title
        desc (string): achievement description
        info (string): contains tips and tricks about the achievement. Only
            stored in the first level of each achievement.
        frame (Frame): a reference to the frame displaying the achievement.
            This frame can either be in the completed or uncompleted 
            AchievementsFrame. frame is given a value once a frame for
            the achievement has been initialized.
        first_level (LeveledAchievement): a reference to the first level
            of the achievement. This is needed when initializing the achievements
            info frame.
        last_level (LeveledAchievement): a reference to the last level. Needed
            for checking if the achievement has been completed and for
            initializing the info frame.
    """

    def __init__(self, category, title, desc, info, first_lvl, last_lvl, 
                 frame = None):
        self.category = category
        self.title = title
        self.desc = desc
        self.info = info
        self.first_lvl = first_lvl
        self.last_lvl = last_lvl
        self.frame = frame


class LeveledAchievement(Achievement):
    """Contains information and methods needed for each level of 
    an achievement.

    A leveled achievement is any achievement that has multiple levels to it.
    Each level has the player complete an increased amount of tasks from the
    last level (ie. winning once, then 10 times, then 20, and then 50). 
    Therefore each level has an associated number of tasks, a roman numeral
    representing the level, variables for planned and completed checkboxes,
    and the associated reward and achievement points for completing that 
    level.

    To save RAM, there is a seperate class storing shared attributes between
    the levels. A reference to this class is stored in each level.

    Args:
        level_rom_num (string): a roman numeral representing the level of 
            the achievement
        is_planned (int): 1 for planned, 0 for not planned
        is_completed (int): 1 for completed, 0 for not completed
        num_tasks (int): the number of tasks required to complete
            the the level of the achievement. The task is described in
            achievement description.
        points (int): amount of points awarded upon level completion.
        reward_amount (int): amount of reward awarded upon level completion
        reward (string): name of reward.
        list_index (int): the index at which this level will be placed in
            achievement_list.
        shared_attrs (LeveledAttributes): a reference to the achievements
        LeveledAttributes, which stores the attributes shared between every
        level.
        
    """

    def __init__(self, level_rom_num, is_planned, is_completed, num_tasks,
                points, reward_amount, reward, list_index, shared_attrs):
        
        self.level_rom_num = level_rom_num
        # variables for checkboxes
        self.planned_var = IntVar(value=is_planned)
        self.completed_var = IntVar(value=is_completed)
        self.num_tasks = num_tasks
        # initiate points_img and reward_img using static dictionaries
        self.points_img = Achievement.points_images[points]
        self.reward_img = Achievement.reward_images[reward]
        self.reward_amount = reward_amount
        self.list_index = list_index
        # a reference to LeveledAttributes
        self.shared_attrs = shared_attrs

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
                # loop through all levels of achievement
                while (Achievement.achievement_list[cur_lvl_index].shared_attrs \
                    == self.shared_attrs):
                    # check checkboxes
                    next_lower_lvl.completed_var.set(1)
                    cur_lvl_index -= 1
                    next_lower_lvl = Achievement.achievement_list[cur_lvl_index]
            # else, uncheck every higher level
            else:
                # get next higher level
                next_higher_lvl = Achievement.achievement_list[self.list_index+1]
                cur_lvl_index = next_higher_lvl.list_index
                while(Achievement.achievement_list[cur_lvl_index].shared_attrs \
                    == self.shared_attrs):
                    next_higher_lvl.completed_var.set(0)
                    cur_lvl_index += 1
                    next_higher_lvl = Achievement.achievement_list[cur_lvl_index]
        # list may go out of bounds if at the end or beginning of list
        # it may also reach a ListAchievement, which would throw an AttributeError
        except (IndexError, AttributeError):
            pass

    def on_planned_checkbox(self):
        """Automatically checks or unchecks "planned" checkboxes in other 
        levels of achievement.
        See on_completed_checkbox() for a more detailed description of method behaviour.
        """
        try:
            # if checking
            if self.planned_var.get() == 1:
                # get the next lower level of achievement
                next_lower_lvl = Achievement.achievement_list[self.list_index-1]
                cur_lvl_index = next_lower_lvl.list_index
                # loop through all levels of achievement
                while (Achievement.achievement_list[cur_lvl_index].shared_attrs \
                    == self.shared_attrs):
                    # check checkboxes
                    next_lower_lvl.planned_var.set(1)
                    cur_lvl_index -= 1
                    next_lower_lvl = Achievement.achievement_list[cur_lvl_index]
            # else, uncheck every higher level
            else:
                # get next higher level
                next_higher_lvl = Achievement.achievement_list[self.list_index+1]
                cur_lvl_index = next_higher_lvl.list_index
                while(Achievement.achievement_list[cur_lvl_index].shared_attrs \
                    == self.shared_attrs):
                    next_higher_lvl.planned_var.set(0)
                    cur_lvl_index += 1
                    next_higher_lvl = Achievement.achievement_list[cur_lvl_index]
        # list may go out of bounds if at the end or beginning of list
        # it may also reach a ListAchievement, which would throw an AttributeError
        except (IndexError, AttributeError):
            pass


class ListAchievement(Achievement):
    """Contains information and methods related to any achivement
    that requires the user to complete a list of tasks.
    Args:
        category (string): achievement category
        title (string): achievement title
        desc (string): achievement description
        task_list (List of strings): The list of tasks
            to complete the achievement.
        is_planned (int): 1 for planned, 0 for not planned
        is_completed (int): 1 for completed, 0 for not completed
        points (int): amount of points awarded upon level completion
        reward_amount (int): amount of reward awarded upon level completion
        reward (string): name of reward
        list_index (int): the index at which this level will be placed in
            achievement_list.
        info (string): contains tips and tricks about the achievement. Only
            stored in the first level of each achievement.
        frame (Frame): a reference to the frame displaying the achievement.
            This frame can either be in the completed or uncompleted 
            AchievementsFrame.
    """
    def __init__(self, category, title, desc, task_list, is_planned,
                 is_completed, points, reward_amount, reward, list_index, 
                 info, frame):
        
        self.category = category
        self.title = title
        self.desc = desc
        self.task_list = task_list
        # variables for checkboxes
        self.planned_var = IntVar(value=is_planned)
        self.completed_var = IntVar(value=is_completed)
        # initiate points_img and reward_img using static dictionaries
        self.points_img = Achievement.points_images[points]
        self.reward_img = Achievement.reward_images[reward]
        self.reward_amount = reward_amount
        self.list_index = list_index
        self.info = info
        self.frame = frame

    def on_planned_checkbox(self):
        pass

    def on_completed_checkbox(self):
        pass


if __name__ == "__main__":
    root = AppController()
    root.mainloop()