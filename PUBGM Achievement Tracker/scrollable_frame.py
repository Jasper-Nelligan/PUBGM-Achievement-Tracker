import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

# Desired sizes for the button images
BUTTON_SIZE = 277, 45

class ScrollableFrame(tk.Frame):
    """Extends class tk.Frame to support a scrollable Frame

    This class is independent from the widgets to be scrolled and 
    can be used to replace a standard tk.Frame. It is scrollable using both
    the scroll bar and using the mousewheel while hovering over the canvas.
    
    Attributes:
        scrolled_frame: this frame will hold the child widgets.
            All widgets to be scrolled have to use this frame as parent
    """
    def __init__(self, parent, height, width, bg):
        """ Initiates a scrollable frame with labels using specified
        height and width. Canvas is scrollable both over canvas and scrollbar.

        Args:
            height (int): height of frame in pixels
            width (int): width of frame in pixels
            bg (string): desired colour of background.
                Color can be passed in by hex code or by name.
        """

        super().__init__(parent)

        # Place the scrollbar on self, layout to the right
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical")
        self.v_scrollbar.pack(side="right", fill="y")

        # The Canvas which supports the Scrollbar Interface, 
        # placed on self and layed out to the left.
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=bg, 
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
        self.scrolled_frame = tk.Frame(self.canvas, bg=self.canvas.cget('bg'))
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

        
    def unbind_mousewheel(self):
        """Unbinds the mouse-wheel to this instance. This needs to be called
        every time another scrolled frame is raised.
        """
        self.canvas.unbind_all('<MouseWheel>')

    def bind_mousewheel(self):
        """Re-binds this instance to the mouse-wheel. After unbinding the
        current scrollable frame shown, this needs to be called on the scrollable
        frame to be shown next.
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

class App(tk.Tk):
    """This was used for testing the scrollable frame with simple example data"""
    def __init__(self):
        #initializes self as root
        tk.Tk.__init__(self)

        # create a black background frame
        self.background_frame = tk.Frame(self, bg='black', 
                                height = 600, width = 1000)
        self.background_frame.grid(row=0, column=0, sticky = 'NW')

        # add a new scrollable frame in center of background frame
        self.first_sbf = ScrollableFrame(self.background_frame, height = 500, 
                             width = 702, bg = 'white')
        self.first_sbf.place(x=500, y=300, anchor=CENTER)
        
        # add the second frame
        self.second_sbf = ScrollableFrame(self.background_frame, height = 500, 
                             width = 702, bg = 'white')
        self.second_sbf.place(x=500, y=300, anchor=CENTER)

        # I want it so that once I click anywhere in the frame,
        # the scrollable canvas in the middle will switch
        self.background_frame.bind('<Button-1>', self.on_click)
        # the first frame is initially behind the second frame
        self.first_frame_raised = False

        # add example data to first frame

        self.first_frame = self.first_sbf.scrolled_frame
        for row in range(50):
            text = "%s" % row
            tk.Label(self.first_frame, text=text,
                     width=3, borderwidth="1", relief="solid") \
                .grid(row=row, column=0)

            text = "This is the first frame"
            tk.Label(self.first_frame, text=text,
                     background=self.second_sbf.scrolled_frame.cget('bg')) \
                .grid(row=row, column=1)

        # add example data to second frame
        self.second_frame = self.second_sbf.scrolled_frame
        tk.Label(self.second_frame, text="Second label",
                 borderwidth='1', relief='solid') \
                 .grid(row=1, column=0)
        tk.Label(self.second_frame, text="First label",
                 borderwidth='0', relief='solid') \
                 .grid(row=1, column=0)

    def on_click(self, event):
        if self.first_frame_raised == False:
            print("First frame being raised")
            self.second_sbf.unbind_mousewheel()
            self.first_sbf.bind_mousewheel()
            self.first_sbf.tkraise()
            self.first_frame_raised = True
        else:
            print("Second frame being raised")
            self.first_sbf.unbind_mousewheel()
            self.second_sbf.bind_mousewheel()
            self.second_sbf.tkraise()
            self.first_frame_raised = False

if __name__ == "__main__":
    root = App()
    root.mainloop()