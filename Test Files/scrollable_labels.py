import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

SCROLL_CANVAS_H = 500
SCROLL_CANVAS_W = 1000

# Desired sizes for the button images
BUTTON_SIZE = 100, 40

class ScrollbarFrame(tk.Frame):
    """Extends class tk.Frame to support a scrollable Frame

    This class is independent from the widgets to be scrolled and 
    can be used to replace a standard tk.Frame.

    """
    def __init__(self, parent, height, width):
        """ Initiates a scrollable frame with labels using specified
        height and width. Canvas is scrollable both over canvas and scrollbar.

        Args:
            height (int): height of frame in pixels
            width (int): width of frame in pixels
        """

        super().__init__(parent)

        self.height = height
        self.width = width

        # Place the scrollbar on self, layout to the right
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical")
        self.v_scrollbar.pack(side="right", fill="y")

        # The Canvas which supports the Scrollbar Interface, 
        # placed on self and layed out to the left.
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", 
                                height = height, 
                                width = width)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        self.v_scrollbar.configure(command=self.canvas.yview)

        # Allow canvas to be scrolled using mousewheel while hovering 
        # over the canvas region.
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Place a frame on the canvas, this frame will hold the child widgets
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = tk.Frame(self.canvas, background=self.canvas.cget('bg'))
        self.canvas.create_window((0, 0), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)

        # Reset the scroll region to encompass the inner frame
        self.scrolled_frame.bind("<Configure>", self.on_frame_configure)

        #For testing and debugging
        self.canvas.bind("<Button-1>", self.on_click)

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

    def on_click(self, event):
        """For testing and debugging"""

        print("Area clicked was (" + str(event.x) + ", " + str(event.y) + ")")


class App(tk.Tk):
    def __init__(self):
        #initializes self as root
        tk.Tk.__init__(self)

        # add a new scrollable frame
        sbf = ScrollbarFrame(self, height = 500, width = 1000)
        #self.grid_rowconfigure(0, weight=1)    # not sure what these do
        #self.grid_columnconfigure(0, weight=1) 
        sbf.grid(row=0, column=0, sticky='nsew')
        #sbf.pack(side="top", fill="both", expand=True)

        
        example_img = Image.open('./Images/background.png')
        example_img.thumbnail(BUTTON_SIZE, Image.BICUBIC)
        self.tk_example_img = ImageTk.PhotoImage(example_img)

        achievement_title_font = font.Font(family='Helvetica',
                                            size=8, weight='bold')
        achievement_desc_font = font.Font(family='Helvetica', 
                                            size=8)

        # Some data, layout into the sbf.scrolled_frame
        frame = sbf.scrolled_frame
        row = 0
        title=None
        desc=None

        CheckVar1 = IntVar()
        CheckVar2 = IntVar()
        while row < 50:
            # Image on left
            #tk.Label(frame, image=self.tk_example_img,
            #         borderwidth="1", relief="solid") \
            #    .grid(row=row, column=0)
            frame1 = tk.Frame(frame, bd=2, relief = 'solid', 
                              background=sbf.scrolled_frame.cget('bg'))
            frame1.grid(row=row, column=0, sticky='NW')
            frame1.bind_all('<Button-1>', self.on_click)

            text = "Achievement Title " + str(row)
            title=tk.Label(frame1, text=text, anchor=W, justify=LEFT,
                     relief='solid', height=1,
                     font=achievement_title_font, state=DISABLED,
                     background=sbf.scrolled_frame.cget('bg')) \
                     .grid(row=0, column=0, sticky=NW)
            #frame.columnconfigure(0, minsize=20)

            text = "How to get achievement\npart 2 of how to get achievement"
            desc=tk.Label(frame1, text=text, anchor=W, justify=LEFT,
                     relief='solid', height=2,
                     font=achievement_desc_font,
                     background=sbf.scrolled_frame.cget('bg')) \
                     .grid(row=1, column=0, sticky=NW)
            #frame.columnconfigure(0, minsize=20)

            text = "Reward from this achievement:"
            desc=tk.Label(frame1, text=text, anchor=W, justify=LEFT,
                     relief='solid', height=1,
                     font=achievement_desc_font,
                     background=sbf.scrolled_frame.cget('bg')) \
                     .grid(row=1, column=1, sticky=NW)
            #frame.columnconfigure(0, minsize=20)

            C1 = Checkbutton(frame, text = "Completed", variable = CheckVar1,
                            background=sbf.scrolled_frame.cget('bg'))
            C1.grid(row=row+1, column=2,sticky=NW)

            C2 = Checkbutton(frame, text = "Planned", variable = CheckVar2,
                            background=sbf.scrolled_frame.cget('bg'))
            C2.grid(row=row+1, column=3,sticky=NW)

            row=row+2

            frame1.bind('<Button-1>', self.on_click)
            #text = "this is the third column for row %s" % row
            #tk.Label(frame, text=text,
            #         background=sbf.scrolled_frame.cget('bg')) \
            #    .grid(row=row, column=2)

            
    def on_click(self, event):
        """For testing and debugging"""

        print("Area clicked was (" + str(event.x) + ", " + str(event.y) + ")")
        print(str(event.widget))

if __name__ == "__main__":
    root = App()
    root.mainloop()