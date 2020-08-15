import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

class ScrollbarFrame(tk.Frame):
    """Extends class tk.Frame to support a scrollable Frame

    This class is independent from the widgets to be scrolled and 
    can be used to replace a standard tk.Frame.

    Attributes:
        scrolled_frame: this frame will hold the child widgets.
            All widgets to be scrolled have to use this frame as parent
    """
    def __init__(self, parent, height, width, background):
        """ Initiates a scrollable frame with labels using specified
        height and width. Canvas is scrollable both over canvas and scrollbar.

        Args:
            height (int): height of frame in pixels
            width (int): width of frame in pixels
            background (string): desired colour of background.
                Color can be passed in by hex code or by name.
        """

        super().__init__(parent)

        # Place the scrollbar on self, layout to the right
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical")
        self.v_scrollbar.pack(side="right", fill="y")

        # The Canvas which supports the Scrollbar Interface, 
        # placed on self and layed out to the left.
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=background, 
                                height = height, width = width)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        self.v_scrollbar.configure(command=self.canvas.yview)

        # Allow canvas to be scrolled using mousewheel while hovering 
        # over the canvas region. bind_all is used because just bind
        # doesn't seem to work for scrolling on the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Place a frame on the canvas, this frame will hold the child widgets
        # All widgets to be scrolled have to use this frame as parent
        # To do this, assign a variable to this attribute after creating
        # an instance of the class
        self.scrolled_frame = tk.Frame(self.canvas, background=self.canvas.cget('bg'))
        self.canvas.create_window((0, 0), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)

        # Reset the scroll region to encompass the inner frame
        self.scrolled_frame.bind("<Configure>", self.on_frame_configure)

    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Allows canvas to be scrolled using mousewheel while hovering
        over canvas. Copied from:
        https://preview.tinyurl.com/stackoverflow162
        """
        scroll_speed = 0.1
        # n is either 1 or -1 and must be inverted
        n = -event.delta / abs(event.delta)
        # Return scrollbar position and adjust it by a fraction
        p = self.v_scrollbar.get()[0] + (n*scroll_speed)
        # Apply new position
        self.canvas.yview_moveto(p)             

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
