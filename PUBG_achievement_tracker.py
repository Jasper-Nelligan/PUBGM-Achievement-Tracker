import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

#**********************************************************************
# Implements a GUI for users track their PUBG MOBILE achievements.

# I made this as a learning experience on making GUI's and using
# python, and so I've overcommented the code accordingly

# Code structure referenced from: https://tinyurl.com/y3g9ab5q

# (C) 2020 Jasper Nelligan
#**********************************************************************

# Desired sizes for the button images
OVERVIEW_BUTTON_SIZE = 163, 45
ACHIEVEMENTS_BUTTON_SIZE = 227, 45
COMPLETED_BUTTON_SIZE = 163, 45
CREDITS_BUTTON_SIZE = 163, 45

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
        self.init_image()

        #Placing background image onto main menu frame

        # Use self as the parent since we are placing 
        # this label onto the frame
        background_label = tk.Label(self, image=self.tk_background_image)
        background_label.place(height=BACKGROUND_IMAGE_HEIGHT, 
                               width=1366 - SCREEN_OFFSET)

        # Adding functionality to buttons

        background_label.bind('<Button-1>', self. on_click)

    def on_click(self, event):
        """Takes action depending on where the user clicked"""
        print("area clicked was", event.x, event.y, sep=" ")
        if 75 <= event.x <= 240 and 220 <= event.y <= 265:
            print("clicked overview")
        if 75 <= event.x <= 300 and 320 <= event.y <= 365:
            print("clicked achievements")
        if 75 <= event.x <= 240 and 420 <= event.y <= 465:
            print("clicked completed")
        if 75 <= event.x <= 197 and 520 <= event.y <= 565:
            print("clicked credits")

    def init_image(self):
        """Initializes the background image, text, and
        buttons for this frame. 
        """

        #loading main menu images

        # Colour for text gradients was DEDF00 for yellow
        # and DF0D0D for red, using
        # https://fontmeme.com/playerunknowns-battlegrounds-font/
        background_image = Image.open('./Images/PUBG_background_image.png')
        program_title_image = Image.open('./Images/program_title.png')
        overview_button_image = Image.open('./Images/overview.png')
        achievements_button_image = Image.open('./Images/achievements.png')
        completed_button_image = Image.open('./Images/completed.png')
        credits_button_image = Image.open('./Images/credits.png')
        # Red text images are for when the user clicks on the buttons,
        # with the button turning red to indicate a click
        credits_red_button_image = Image.open('./Images/credits_red.png')
        overview_red_button_image = Image.open('./Images/overview_red.png')
        achievements_red_button_image = Image.open('./Images/achievements_red.png')
        completed_red_button_image = Image.open('./Images/completed_red.png')
        credits_red_button_image = Image.open('./Images/credits_red.png')
    
        # Notes from stackoverflow:
        # How to use .paste():
        # First parameter to .paste() is the image to paste.
        # Second are coordinates.
        # Third paramater indicates a mask that will be used to 
        # paste the image.If you pass an image with transparency,
        # then the alpha channel is used as mask.
        # This makes sure that an image with transparent background
        # won't show up with a white background
        background_image.paste(program_title_image, (150, 40), 
                               program_title_image)
        background_image.paste(overview_button_image, (150, 220), 
                               overview_button_image)
        background_image.paste(achievements_button_image, (150, 320), 
                               achievements_button_image)
        background_image.paste(completed_button_image, (150, 420), 
                               completed_button_image)
        background_image.paste(credits_button_image, (150, 520), 
                               credits_button_image)

        # Convert the Image object into a TkPhoto object

        # Must use self.tk_background_image to save a
        # reference to the image, otherwise this variable
        # will be garbage collected once the class is exited
        self.tk_background_image = ImageTk.PhotoImage(background_image)


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