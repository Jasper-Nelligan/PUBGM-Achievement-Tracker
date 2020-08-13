import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import copy

from scrollable_frame import ScrollbarFrame


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
BACKGROUND_IMAGE_HEIGHT = 625
PC_WIDTH = 1366

class AppController(tk.Tk):
    """This class manages the stacking of frames.
   
    It inherits from tk.Tk so that it can have additional methods 
    such as show_frame This class initializes itself as the root 
    frame onto which all other frames will be placed on.
    """

    def __init__(self):
        """Initializes self as root frame and calls on other frame
        classes to initialize them.
        """

        # Creates the root. Root is referenced using 'self'
        tk.Tk.__init__(self)
        # Users cannot resize the window
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
            self.frames[page_name] = frame  #input frame into dictionary

            # Put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

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
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMAGE_HEIGHT, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        # The root, or AppController is the controller for this frame.
        # The controller is a way for the pages to interact with each other.
        # For this application, the controller is used to bring a particular
        # frame forward when the user requests it
        self.controller = controller

        #assigned in init_image()
        self.tk_background_img = None 
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
        self.main_menu_label = tk.Label(self, image=self.tk_background_img)
        self.main_menu_label.place(height=BACKGROUND_IMAGE_HEIGHT, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to back button

        self.main_menu_label.bind('<Button-1>', self.on_click)

    def init_images(self):
        """Initializes the background image, text, and
        buttons for this frame. 
        """

        # self. is used so that background_image is stored
        # as an instance of this class and can be referenced in other
        # methods. 
        self.background_img = Image.open('./Images/background.png')
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
        for img in (overview_btn_img, 
                   achievements_btn_img,
                   completed_btn_img,
                   credits_btn_img,
                   exit_btn_img,
                   overview_red_btn_img,
                   achievements_red_btn_img,
                   completed_red_btn_img,
                   credits_red_btn_image,
                   exit_red_btn_img):
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
        self.background_img.paste(program_title_img, (150, 40), 
                               program_title_img)
        self.background_img.paste(overview_btn_img, (150, 220), 
                               overview_btn_img)
        self.background_img.paste(achievements_btn_img, (150, 320), 
                               achievements_btn_img)
        self.background_img.paste(completed_btn_img, (150, 420), 
                               completed_btn_img)
        self.background_img.paste(credits_btn_img, (150, 520), 
                               credits_btn_img)
        self.background_img.paste(exit_btn_img, (1300, 40), 
                               exit_btn_img)

        # Convert the Image object into a TkPhoto object

        # Must use self.tk_background_image to save a
        # reference to the image, otherwise this variable
        # will be garbage collected once the class is exited
        self.tk_background_img = ImageTk.PhotoImage(self.background_img)

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
        overview_clicked = copy.deepcopy(self.background_img)
        achievements_clicked = copy.deepcopy(self.background_img)
        completed_clicked = copy.deepcopy(self.background_img)
        credits_clicked = copy.deepcopy(self.background_img)
        exit_clicked = copy.deepcopy(self.background_img)

        # "Overview" is clicked
        overview_clicked.paste(overview_red_btn_img,
                                       (150, 220), 
                                       overview_red_btn_img)
        self.tk_overview_clicked = ImageTk.PhotoImage(overview_clicked)
        # "Achievements" is clicked
        achievements_clicked.paste(achievements_red_btn_img,
                                       (150, 320), 
                                       achievements_red_btn_img)
        self.tk_achievements_clicked = ImageTk.PhotoImage(achievements_clicked)
        # "Completed" is clicked
        completed_clicked.paste(completed_red_btn_img,
                                       (150, 420), 
                                       completed_red_btn_img)
        self.tk_completed_clicked = ImageTk.PhotoImage(completed_clicked)
        # "Credits" is clicked
        credits_clicked.paste(credits_red_btn_image,
                                       (150, 520), 
                                       credits_red_btn_image)
        self.tk_credits_clicked = ImageTk.PhotoImage(credits_clicked)
        # "Exit" is clicked
        exit_clicked.paste(exit_red_btn_img,
                                       (1300, 40), 
                                       exit_red_btn_img)
        self.tk_exit_clicked = ImageTk.PhotoImage(exit_clicked)
  
    def on_click(self, event):
        """Turns the clicked on button to red and raises the corresponding 
        frame. Exits the program if Exit is clicked.
        """

        print(f"Area clicked was ({event.x}, {event.y})")
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
                                       self.tk_background_img)])
        #if "Achievements" was clicked 
        elif 75 <= event.x <= 300 and 320 <= event.y <= 365:
            self.main_menu_label.configure(image=
                                       self.tk_achievements_clicked)
            #Go to Achievements frame and turn button back to yellow
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "AchievementsFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background_img)])
        #if "Completed" was clicked
        elif 75 <= event.x <= 240 and 420 <= event.y <= 465:
            self.main_menu_label.configure(image=
                                       self.tk_completed_clicked)
            #Go to Completed frame and turn button back to yellow
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "CompletedFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background_img)])
        #if "Credits" was clicked
        elif 75 <= event.x <= 197 and 520 <= event.y <= 565:
            self.main_menu_label.configure(image=
                                       self.tk_credits_clicked)
            #Go to Credits frame and turn button back to yellow
            self.main_menu_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "CreditsFrame"), 
                                       self.main_menu_label.configure(image=
                                       self.tk_background_img)])

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
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMAGE_HEIGHT, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

        #assigned in init_image()
        self.tk_background_img = None 
        self.tk_back_clicked = None

        # Initialize the background image with buttons/text
        self.init_images()

        #Place image onto frame
        self.overview_label = tk.Label(self, image=self.tk_background_image)
        self.overview_label.place(height=BACKGROUND_IMAGE_HEIGHT, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to back button
        self.overview_label.bind('<Button-1>', self.on_click)

    def init_images(self):
            """Initializes the background image, text, and
            buttons for this frame. Similar code with further
            explanation can be found in MainMenuFrame class.
            """

            self.background_img = Image.open('./Images/background.png')
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
            self.background_img.paste(back_btn_img, (150, 40), 
                                   back_btn_img)

            # Convert the Image object into a TkPhoto object
            self.tk_background_image = ImageTk.PhotoImage(self.background_img)

            # Placing red buttons over original buttons

            # Create copies of background image so button images
            # aren't pasted over the same image
            back_clicked = copy.deepcopy(self.background_img)
        
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
            self.overview_label.configure(image=
                                       self.tk_back_clicked)
            #Go to Main Menu frame and turn button back to yellow
            self.overview_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "MainMenuFrame"), 
                                       self.overview_label.configure(image=
                                       self.tk_background_img)])

class AchievementsFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        """Creates frame for 'Achievements' section

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
        """
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMAGE_HEIGHT, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

        #assigned in init_image()
        self.tk_background_img = None 
        self.tk_back_clicked = None

        # Initialize the background image with buttons/text
        self.init_images()

        # Place image onto frame using label
        self.achievements_label = tk.Label(self, image=self.tk_background_image)
        self.achievements_label.place(height=BACKGROUND_IMAGE_HEIGHT, 
                               width=PC_WIDTH - SCREEN_OFFSET)

        # Adding functionality to back button
        self.achievements_label.bind('<Button-1>', self.on_click)

        # Create scrollable frame to display achievements
        self.sbf = ScrollbarFrame(self, height = 400, width = 702, 
                                  background = '#121111')
        scroll_frame = self.sbf.scrolled_frame

        # Place at center of parent frame
        self.sbf.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Fonts for achievement information
        title_font = font.Font(family='Helvetica',
                                            size=12, weight='bold')
        desc_font = font.Font(family='Helvetica', 
                                            size=12)

        # Some example data, layed out onto the sbf.scrolled_frame

        points_5 = Image.open('./Images/5_points.png')
        points_30 = Image.open('./Images/30_points.png')
        silver_fragment = Image.open('./Images/silver_fragment.png')
        premium_crate = Image.open('./Images/premium_crate.png')

        # Shrinking images
        for img in (points_5, points_30,
                    silver_fragment, premium_crate):
            img.thumbnail(BUTTON_SIZE, Image.BICUBIC)

        self.points_5 = ImageTk.PhotoImage(points_5)
        self.points_30 = ImageTk.PhotoImage(points_30)
        self.silver_fragment = ImageTk.PhotoImage(silver_fragment)
        self.premium_crate = ImageTk.PhotoImage(premium_crate)

        row = 1
        while row <= 50:
            frame1 = tk.Frame(scroll_frame, bd=2, relief = 'solid', 
                             background=self.sbf.scrolled_frame \
                             .cget('bg'))
            frame1.grid(row=row, column=0, sticky='NW')
            frame1.bind_all('<Button-1>', self.on_click)

            text = "Achievement Title " + str(row)
            title=tk.Label(frame1, text=text, anchor=W, fg='white',
                      height=1, font=title_font,
                      bg=self.sbf.scrolled_frame.cget('bg')) \
                     .grid(row=0, column=0, sticky=NW)

            text = "How to get achievement\npart 2 of how to get achievement"
            desc=tk.Label(frame1, text=text, justify=LEFT, anchor=W,
                     height=2, fg='white',
                     font=desc_font,
                     background=self.sbf.scrolled_frame.cget('bg')) \
                     .grid(row=1, column=0, sticky=NW)

            if (row % 2) == 0:
                # Padding to seperate achievement info from points
                text = ""
                desc=tk.Label(frame1, width=40,
                        bg=self.sbf.scrolled_frame.cget('bg')) \
                        .grid(row=1, column=1, sticky=NW)

                # rowspan=2 is a way of centering a label between two other rows
                img = tk.Label(frame1, image=self.points_5, anchor=W,
                           borderwidth=0, highlightthickness=0) \
                           .grid(row=0, rowspan=2, column = 2, sticky=W)

                text = "3000 x"
                desc=tk.Label(frame1, text=text, anchor=E, fg='white',
                        height=1, width=10,
                        font=desc_font, 
                        bg=self.sbf.scrolled_frame.cget('bg')) \
                        .grid(row=1, column=4, sticky=NW)

                img = tk.Label(frame1, image=self.silver_fragment, anchor=W,
                           borderwidth=0, highlightthickness=0) \
                           .grid(row=0, rowspan=2, column = 5, sticky=W)
            # Same but with different points and reward
            else:
                text = ""
                desc=tk.Label(frame1, width=40,
                        bg=self.sbf.scrolled_frame.cget('bg')) \
                        .grid(row=1, column=1, sticky=NW)

                img = tk.Label(frame1, image=self.points_30, anchor=W,
                           borderwidth=0, highlightthickness=0) \
                           .grid(row=0, rowspan=2, column = 2, sticky=W)

                text = "5 x"
                desc=tk.Label(frame1, text=text, anchor=E, fg='white',
                        height=1, width=10,
                        font=desc_font, 
                        bg=self.sbf.scrolled_frame.cget('bg')) \
                        .grid(row=1, column=4, sticky=NW)

                # rowspan=2 is a way of centering a label between two other rows
                img = tk.Label(frame1, image=self.premium_crate, anchor=W,
                           borderwidth=0, highlightthickness=0) \
                           .grid(row=0, rowspan=2, column = 5, sticky=W)

            row=row+1

    def init_images(self):
            """Initializes images and text for this frame.

            Similar code with further explanation can be found in 
            MainMenuFrame class.
            """

            self.background_img = Image.open('./Images/background.png')
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
            self.background_img.paste(back_btn_img, (150, 40), 
                                   back_btn_img)

            # Convert the Image object into a TkPhoto object
            self.tk_background_image = ImageTk.PhotoImage(self.background_img)

            # Placing red buttons over original buttons

            # Create copies of background image so button images
            # aren't pasted over the same image
            back_clicked = copy.deepcopy(self.background_img)
        
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
            self.achievements_label.configure(image=
                                       self.tk_back_clicked)
            #Go to Main Menu frame and turn button back to yellow
            self.achievements_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "MainMenuFrame"), 
                                       self.achievements_label.configure(image=
                                       self.tk_background_img)])


class CompletedFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        """Creates frame for 'Completed' section

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
        """
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMAGE_HEIGHT, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

        #assigned in init_image()
        self.tk_background_img = None 
        self.tk_back_clicked = None

        # Initialize the background image with buttons/text
        self.init_images()

        #Place image onto frame using label
        self.completed_label = tk.Label(self, image=self.tk_background_image)
        self.completed_label.place(height=BACKGROUND_IMAGE_HEIGHT, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to back button

        self.completed_label.bind('<Button-1>', self.on_click)

    def init_images(self):
            """Initializes the background image, text, and
            buttons for this frame. Similar code with further
            explanation can be found in MainMenuFrame class.
            """

            self.background_img = Image.open('./Images/background.png')
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
            self.background_img.paste(back_btn_img, (150, 40), 
                                   back_btn_img)

            # Convert the Image object into a TkPhoto object
            self.tk_background_image = ImageTk.PhotoImage(self.background_img)

            # Placing red buttons over original buttons

            # Create copies of background image so button images
            # aren't pasted over the same image
            back_clicked = copy.deepcopy(self.background_img)
        
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
                                       self.tk_background_img)])


class CreditsFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        """Creates frame for 'Credits' section

        Args: 
            parent (Frame): the frame onto which this frame will be placed, ie. the root
            controller (Frame): The controller frame is a way for the pages to interact 
                with each other. For this application, the controller is used 
                to bring a particular frame forward when the user requests it.
        """
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMAGE_HEIGHT, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        self.controller = controller

        #assigned in init_image()
        self.tk_background_img = None 
        self.tk_back_clicked = None

        # Initialize the background image with buttons/text
        self.init_images()

        #Place image onto frame using label
        self.credits_label = tk.Label(self, image=self.tk_background_image)
        self.credits_label.place(height=BACKGROUND_IMAGE_HEIGHT, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to back button

        self.credits_label.bind('<Button-1>', self.on_click)

    def init_images(self):
            """Initializes the background image, text, and
            buttons for this frame. Similar code with further
            explanation can be found in MainMenuFrame class.
            """

            self.background_img = Image.open('./Images/background.png')
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
            self.background_img.paste(back_btn_img, (150, 40), 
                                   back_btn_img)

            # Convert the Image object into a TkPhoto object
            self.tk_background_image = ImageTk.PhotoImage(self.background_img)

            # Placing red buttons over original buttons

            # Create copies of background image so button images
            # aren't pasted over the same image
            back_clicked = copy.deepcopy(self.background_img)
        
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
            self.credits_label.configure(image=
                                       self.tk_back_clicked)
            #Go to Main Menu frame and turn button back to yellow
            self.credits_label.bind("<ButtonRelease-1>", lambda event:
                                      [self.controller.show_frame(
                                          "MainMenuFrame"), 
                                       self.credits_label.configure(image=
                                       self.tk_background_img)])


if __name__ == "__main__":
    root = AppController()
    root.mainloop()