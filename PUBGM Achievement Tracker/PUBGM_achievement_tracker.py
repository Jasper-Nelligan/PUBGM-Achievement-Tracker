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

        # Initializing all frames

        # All frames will be stored in a dictionary for quick access
        self.frames = {}
        for F in (MainMenuFrame, OverviewFrame, AchievementsFrame, 
                  CompletedFrame, CreditsFrame):
            page_name = F.__name__
            # Create an instance of each frame
            frame = F(parent=container, controller=self)
            # Input frame into dictionary
            self.frames[page_name] = frame

            # Put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # Start by showing the Main Menu
        self.show_frame("MainMenuFrame")

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

        # self. is used so that background_image is stored
        # as an instance of this class and can be referenced in other
        # methods. 
        background_img = Image.open('./Images/background.png')
        program_title_img = Image.open('./Images/program_title.png')
        overview_btn_img = Image.open('./Images/overview.png')
        achievements_btn_img = Image.open('./Images/achievements.png')
        completed_btn_img = Image.open('./Images/completed.png')
        credits_btn_img = Image.open('./Images/credits.png')
        exit_btn_img = Image.open('./Images/exit.png')
        # Red buttons will be used to indicate when the user 
        # has clicked a button. These images are used in the 
        # change_button_to_red() method
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


        # Notes from stackoverflow:
        # How to use .paste():
        # First parameter to .paste() is the image to paste.
        # Second are coordinates.
        # Third paramater indicates a mask that will be used to 
        # paste the image.If you pass an image with transparency,
        # then the alpha channel is used as mask.
        # This makes sure that an image with transparent background
        # won't show up with a white background
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

        # Must use self.tk_background_image to save a
        # reference to the image, otherwise this variable
        # will be garbage collected once the class is exited
        self.tk_background = ImageTk.PhotoImage(background_img)

        # Placing red buttons over original buttons

        # When a user clicks a button, the intended effect is for the 
        # button to turn red and then back to yellow upon release.
        # To simulate this, each button has an assosciated 
        # image where only that button is red. Once the user clicks on
        # the button, the corresponding image will be placed over the 
        # frame to give this illusion. The image is then removed to
        # restore the button back to yellow. 
        # Red button images are pasted and stored now to allow for 
        # quicker use later.

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
            #Go to Achievements frame and turn button back to yellow
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "AchievementsFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background)])
        #if "Completed" was clicked
        elif 75 <= event.x <= 240 and 420 <= event.y <= 465:
            self.main_menu_label.configure(image=
                                       self.tk_completed_clicked)
            #Go to Completed frame and turn button back to yellow
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "CompletedFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background)])
        #if "Credits" was clicked
        elif 75 <= event.x <= 197 and 520 <= event.y <= 565:
            self.main_menu_label.configure(image=
                                       self.tk_credits_clicked)
            #Go to Credits frame and turn button back to yellow
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
    def __init__(self, parent, controller):
        """Creates frame for 'Achievements' section

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
        """
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMG_H, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

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
        #Dictionaries containing achievement images
        self.reward_points = {}
        self.reward_images = {}
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
        
        # Contains references to each category frame
        # Initialized in init_categories()
        self.categories = {}

        # fonts for achievement information
        self.title_font = font.Font(family='Helvetica',
                                            size=12, weight='bold')
        self.desc_font = font.Font(family='Helvetica', 
                                            size=12)
        self.big_title_font = font.Font(family='Helvetica',
                                            size=20, weight='bold')

        # Keeps track of which row to place next achievement for each category
        # Initialized in init_categorie()
        self.category_row = {}

        # Initializing categories
        self.init_categories()

        # A list for storing a reference to each achievement
        # Achievements are referenced using an assigned array index
        # Initialized in init_leveled_achievements()
        self.achievement_list = []

        # Initiating achievements
        self.init_leveled_achievements()
        #self.init_list_achievements()
         
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
        """Initializes images and text for this frame.

        Similar code with further explanation can be found in 
        MainMenuFrame class.
        """

        # Initiating background images

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
        
        # Initiating achievement images

        self.reward_points = {}
        for points in ('5','10','15','20','30','40','50','60'):
            img = Image.open('./Images/'+points+'_points.png')
            img.thumbnail((40,40), Image.BICUBIC)
            img = ImageTk.PhotoImage(img)
            self.reward_points[points] = img

        self.reward_images = {}
        for reward in ('bp','silver','classic_scrap','classic_crate',
                       'premium_scrap','premium_crate'):
            img = Image.open('./Images/'+reward+'.png')
            img.thumbnail((50,50), Image.BICUBIC)
            img = ImageTk.PhotoImage(img)
            self.reward_images[reward] = img

        # exit button for achievement frame
        exit_x_img = Image.open('./Images/x.png')
        exit_x_img.thumbnail((30,30))
        self.exit_x = ImageTk.PhotoImage(exit_x_img)

    def init_categories(self):
        """Initializes achievement categories, each as a scrollable frame.

        This method loops through the category names and creates a scrollable frame
        for each. There's two dictionary initialized here:

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

    def init_leveled_achievements(self):
        """Reads in achievement information from csv file and initiates each one.

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
                        achievement = Achievement(category, title, num_tasks_desc, 
                                                  level_rom_num, is_planned,
                                                  is_completed, num_tasks, 
                                                  points_img, reward_amount, 
                                                  reward_img, info)
                        first_level = achievement_index
                    else:
                        achievement = Achievement(category, title, num_tasks_desc, 
                                                  level_rom_num, is_planned,
                                                  is_completed, num_tasks, 
                                                  points_img, reward_amount, 
                                                  reward_img)
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
                        achievement_frame = tk.Frame(category_frame, bd=2, 
                                                     relief='solid', 
                                                     bg='#121111')
                        achievement_frame.grid(row=self.category_row[category],
                                              column=0, sticky='NW')
                        # Create info frame when clicked
                        achievement_frame.bind('<Button-1>', lambda event: 
                                            self.init_info_frame(
                                                first_level))
                        self.category_row[category] += 1

                        text = title + " " + level_rom_num
                        frame_title=tk.Label(achievement_frame, text=text, anchor=W, 
                                       fg='white', height=1, font=self.title_font,
                                       bg='#121111')
                        frame_title.grid(row=0, column=0, sticky=NW)
                        frame_title.bind('<Button-1>', lambda event: 
                                    self.init_info_frame(
                                        first_level))

                        # in-frame achievement description
                        text = desc.format(num_tasks=num_tasks)
                        frame_desc=tk.Label(achievement_frame, text=text, justify=LEFT, anchor=W,
                                    height=2, fg='white',
                                    font=self.desc_font,
                                    background='#121111')
                        frame_desc.grid(row=1, column=0, sticky=NW)
                        frame_desc.bind('<Button-1>', lambda event: 
                                    self.init_info_frame(
                                        first_level))

                        # padding to seperate achievement info from points
                        text = ""
                        frame_pad=tk.Label(achievement_frame, width=40,
                                bg='#121111')
                        frame_pad.grid(row=1, column=1, sticky=NW)
                        frame_pad.bind('<Button-1>', lambda event: 
                                    self.init_info_frame(
                                        first_level))

                        img = points_img
                        frame_points = tk.Label(achievement_frame, image=img, anchor=W,
                                    borderwidth=0, highlightthickness=0)
                        # rowspan=2 is a way of centering a label between two other rows
                        frame_points.grid(row=0, rowspan=2, column = 2, sticky=W)
                        frame_points.bind('<Button-1>', lambda event: 
                                    self.init_info_frame(
                                        first_level))

                        # reward amount
                        text = reward_amount + " x "
                        frame_amount=tk.Label(achievement_frame, text=text, anchor=E, fg='white',
                                height=1, width=10, font=self.desc_font, 
                                bg='#121111')
                        frame_amount.grid(row=1, column=3, sticky=NW)
                        frame_amount.bind('<Button-1>', lambda event: 
                                    self.init_info_frame(
                                        first_level))

                        img = reward_img
                        frame_reward = tk.Label(achievement_frame, image=img, anchor=W,
                                    borderwidth=0, highlightthickness=0)
                        frame_reward.grid(row=0, rowspan=2, column = 4, sticky=W)
                        frame_reward.bind('<Button-1>', lambda event: 
                                    self.init_info_frame(
                                        first_level))

                        achievement_frame.grid(row = self.category_row[category])

                        self.category_row[category] += 1
                        
                        frame_initialized = True
                    # else achievement level has not been completed yet, and a lower level
                    # has already been initialized onto category_frame
                    else:
                        pass
                    
    def init_list_achievement(self):
        pass

    def init_info_frame(self,first_level_index):
        """Creates a frame containing info for the passed in achievement.
        
        This method works by passing in level I of an achievement, getting
        a reference to the last level of the achievement, and then
        progressing through each level to create the achievement info frame.
        This frame is then placed over top of the current 
        category frame, with AchievementFrame as the parent.
        The info frame is deleted upon clicking 'X'.

        Args:
            first_level_index (int): the index to level I of an achievement
        """

        first_level = self.achievement_list[first_level_index]

        # getting a reference to the last level of the achievement
        last_level_index = first_level_index
        last_level = self.achievement_list[last_level_index]

        print(f"Info: {first_level.info}")
        # Checks to see if the next achievement in list has a different title.
        # If it does, the last level has been reached
        # Exits if the end of the list is reached
        try:
            while (self.achievement_list[last_level_index+1].title == last_level.title):
                print("in while loop")
                last_level_index += 1
                last_level = self.achievement_list[last_level_index]
        except IndexError:
            print("exception handled")

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
                                            bg='#121111')
        planned_button.grid(row=1, column=2, sticky=E)

        text = "Planned"
        checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                        bg='#121111')
        checkbox_text.grid(row=1, column=3, sticky=W)

        var = last_level.completed_var
        completed_button = tk.Checkbutton(info_frame,  
                                            variable=var, activebackground='#121111',
                                            bg='#121111')
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
        cur_index = first_level_index
        achievement = first_level
        # set this to True once all levels have been initialized, which exits the loop
        last_level_initialized = False
        print("Before while loop")
        while (last_level_initialized == False):
            # if true, terminate the loop after this iteration
            if achievement == last_level:
                last_level_initialized = True

            achievement_frame = tk.Frame(info_frame, bd=2, relief = 'solid', 
                                background='#121111')
            achievement_frame.grid(row=next_row, column=0, columnspan=2, sticky=NW)

            text = achievement.title + " " + achievement.level_rom_num
            frame_title=tk.Label(achievement_frame, text=text, anchor=W, fg='white',
                        height=1, font=self.title_font,
                        bg='#121111')
            frame_title.grid(row=0, column=0, sticky=NW)

            text = achievement.desc
            frame_desc=tk.Label(achievement_frame, text=text, justify=LEFT, anchor=W,
                        height=2, fg='white',
                        font=self.desc_font,
                        background='#121111')
            frame_desc.grid(row=1, column=0, sticky=NW)

            # Padding to seperate achievement info from points
            text = ""
            pad=tk.Label(achievement_frame, width=5,
                    bg='#121111')
            pad.grid(row=1, column=1, sticky=NW)
            
            img = achievement.points_img
            frame_points = tk.Label(achievement_frame, image=img, anchor=W,
                        borderwidth=0, highlightthickness=0)
            frame_points.grid(row=0, rowspan=2, column = 2, sticky=W)

            text = achievement.reward_amount + " x "
            frame_amount=tk.Label(achievement_frame, text=text, anchor=E, fg='white',
                    height=1, width=9, font=self.desc_font, 
                    bg='#121111')
            frame_amount.grid(row=1, column=3, sticky=NW)

            img = achievement.reward_img
            frame_reward = tk.Label(achievement_frame, image=img, anchor=W,
                        borderwidth=0, highlightthickness=0)
            frame_reward.grid(row=0, rowspan=2, column = 4, sticky=W)

            var = achievement.planned_var
            planned_button = tk.Checkbutton(info_frame,
                                            variable=var,
                                            bg='#121111',
                                            activebackground='#121111')
            planned_button.grid(row=next_row, column=2, sticky=E)

            text = "Planned"
            checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                        bg='#121111')
            checkbox_text.grid(row=next_row, column=3, sticky=W)

            var = achievement.completed_var
            completed_button = tk.Checkbutton(info_frame,
                                            variable=var, 
                                            bg='#121111',
                                            activebackground='#121111')
            completed_button.grid(row=next_row, column=4, sticky=E)

            text = "Completed"
            checkbox_text = tk.Label(info_frame, text=text, anchor=W, fg='white',
                                        bg='#121111')
            checkbox_text.grid(row=next_row, column=5, sticky=W)
            
            # the next achievement will be added to the row below
            next_row += 1

            
            # move pointer to next achievement
            cur_index += 1
            # prevents an index error if at the end of the list
            try:
                achievement = self.achievement_list[cur_index]
            except IndexError:
                pass
        print ("after while loop")
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
    
    def __init__(self, parent, controller):
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

    def __init__(self, category, title, desc, level_rom_num, 
                 is_planned, is_completed, num_tasks, points_img, 
                 reward_amount, reward_img, info = None):
        
        self.category = category
        self.title = title
        self.desc = desc
        self.level_rom_num = level_rom_num
        # variables for checkboxes
        self.planned_var = IntVar(value=is_planned)
        self.completed_var = IntVar(value=is_completed)
        self.num_tasks = num_tasks
        self.points_img = points_img
        self.reward_amount = reward_amount
        self.reward_img = reward_img
        self.info = info

#Updating line in file:
#    Read entire file into memory using file reader. Store as a list so you can access the ith row.
#    If checkboxes are both checked: update the file by writing the same line but with both Ys. For this,
#    a function will need to be created to return the correctly formatted string needed to update the line. 
#    For unchecking, vice versa. I think that there should be some other function that handles the boolean values of
#    the achievements before the create string method is used. In the function, lets try saving immediately and see
#    how much processing power that takes.



if __name__ == "__main__":
    root = AppController()
    root.mainloop()