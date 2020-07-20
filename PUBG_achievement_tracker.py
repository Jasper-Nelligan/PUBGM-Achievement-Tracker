import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

#**********************************************************************
# Implements a GUI for users track their PUBG MOBILE achievements.

# I made this as a learning experience on making GUI's and using
# python, and so I've overcommented the code accordingly

# Code structure referenced from: https://tinyurl.com/y3g9ab5q

# Helpful links:
# 
# Tkinter events and bindings:
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm

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
    """This class manages the stacking of frames. It inherits from
    tk.Tk so that it can have additional methods such as show_frame.
    This class initializes itself as the root frame onto which all
    other frames will be placed on.
    """

    def __init__(self):
        """Initializes self as root frame, and calls on the other frame
        classes to initialize them.
        """

        # Creates the root. Root is referenced using 'self'
        tk.Tk.__init__(self)
        # Users cannot resize the window
        self.resizable(width=False, height=False)
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
        for F in (MainMenu, Overview, Achievements, Completed, Credits):
            page_name = F.__name__
            # Create an instance of each frame
            frame = F(parent=container, controller=self)
            # Input frame into dictionary
            self.frames[page_name] = frame  #input frame into dictionary

            # Put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        """Shows a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        "Creates frame for Main menu"

        # tk.Frame.__init__ is used since this class inherits from
        # tk.Frame, meaning the constructor of the parent
        # class must be used.
        # Frame width is set to the max width of my PC since the
        # background image is wider than my PC allows. This means
        # that frame width is hard coded to my PC's width.
        # Therefore, button clicks are calculated based on this fixed size.
        # Allowing variable window sizes for different screens is a feature that
        # needs to be added.
        tk.Frame.__init__(self, parent, height=BACKGROUND_IMAGE_HEIGHT, 
                          width=PC_WIDTH - SCREEN_OFFSET)

        tk_background_image = None  #assigned in init_image()

        # The root, or AppController is the controller for this frame.
        # The controller is a way for the pages to interact with each other.
        # For this application, the controller is used to bring a particular
        # frame forward when the user requests it
        self.controller = controller

        # Initialize the background image with buttons/text
        self.init_images()

        #Placing background image onto main menu frame

        # Use self as the parent since we are placing 
        # this label onto the frame
        self.main_menu_label = tk.Label(self, image=self.tk_background_image)
        self.main_menu_label.place(height=BACKGROUND_IMAGE_HEIGHT, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to buttons

        self.main_menu_label.bind('<Button-1>', self.on_click)

    def init_images(self):
        """Initializes the background image, text, and
        buttons for this frame. 
        """
        # Loading main menu images

        # Colour for text gradients was DEDF00 for yellow
        # and DF0D0D for red, using
        # https://fontmeme.com/playerunknowns-battlegrounds-font/
        # self. is used so that these images are stored
        # as an instance of this class and can be referenced in other
        # methods.
        self.background_image = Image.open('./Images/background.png')
        self.program_title_image = Image.open('./Images/program_title.png')
        self.overview_button_image = Image.open('./Images/overview.png')
        self.achievements_button_image = Image.open('./Images/achievements.png')
        self.completed_button_image = Image.open('./Images/completed.png')
        self.credits_button_image = Image.open('./Images/credits.png')
        # Red buttons will be used to indicate when the user 
        # has clicked a button. These images are used in the 
        # change_button_to_red() method
        self.overview_red_button_image = Image.open('./Images/overview_red.png')
        self.achievements_red_button_image = Image.open('./Images/achievements_red.png')
        self.completed_red_button_image = Image.open('./Images/completed_red.png')
        self.credits_red_button_image = Image.open('./Images/credits_red.png')

        # Shrinking button images
        for img in (self.overview_button_image, 
                   self.achievements_button_image,
                   self.completed_button_image,
                   self.credits_button_image,
                   self.overview_red_button_image,
                   self.achievements_red_button_image,
                   self.completed_red_button_image,
                   self.credits_red_button_image):
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
        self.background_image.paste(self.program_title_image, (150, 40), 
                               self.program_title_image)
        self.background_image.paste(self.overview_button_image, (150, 220), 
                               self.overview_button_image)
        self.background_image.paste(self.achievements_button_image, (150, 320), 
                               self.achievements_button_image)
        self.background_image.paste(self.completed_button_image, (150, 420), 
                               self.completed_button_image)
        self.background_image.paste(self.credits_button_image, (150, 520), 
                               self.credits_button_image)

        # Convert the Image object into a TkPhoto object

        # Must use self.tk_background_image to save a
        # reference to the image, otherwise this variable
        # will be garbage collected once the class is exited
        self.tk_background_image = ImageTk.PhotoImage(self.background_image)
    
    def on_click(self, event):
        """Takes action depending on where the user clicked"""
        print("area clicked was", event.x, event.y, sep=" ")
        #if "Overview" was clicked
        if 75 <= event.x <= 240 and 220 <= event.y <= 265:
            print("clicked overview")
            self.change_button_to_red("Overview")
        #if Achievements was clicked 
        elif 75 <= event.x <= 300 and 320 <= event.y <= 365:
            print("clicked achievements")
            self.change_button_to_red("Achievements")
        #if Completed was clicked
        elif 75 <= event.x <= 240 and 420 <= event.y <= 465:
            print("clicked completed")
            self.change_button_to_red("Completed")
        #if Credits was clicked
        elif 75 <= event.x <= 197 and 520 <= event.y <= 565:
            print("clicked credits")
            self.change_button_to_red("Credits")

    def change_button_to_red(self, button_name):
        """Updates background_image so that passed in button will flicker
        red to indicate the user has clicked on that button.
        """
        # Red button will be placed over a copy of the background image
        self.background_image_clicked = self.background_image.copy()

        if button_name == "Overview":
            self.background_image_clicked.paste(self.overview_red_button_image,
                                       (150, 220), 
                                       self.overview_red_button_image)
        elif button_name == "Achievements":
            self.background_image_clicked.paste(self.achievements_red_button_image,
                                       (150, 320), 
                                       self.achievements_red_button_image)
        elif button_name == "Completed":
            self.background_image_clicked.paste(self.completed_red_button_image,
                                       (150, 420), 
                                       self.completed_red_button_image)
        elif button_name == "Credits":
            self.background_image_clicked.paste(self.credits_red_button_image,
                                       (150, 520), 
                                       self.credits_red_button_image)

        self.tk_background_clicked = ImageTk.PhotoImage(self.background_image_clicked)
        #switch images
        self.main_menu_label.configure(image=
                                       self.tk_background_clicked)
        self.main_menu_label.bind("<ButtonRelease-1>", lambda event: 
                                  self.main_menu_label.configure(image=
                                  self.tk_background_image))

class Overview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class Achievements(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class Completed(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class Credits(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    root = AppController()
    root.mainloop()