import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

SCROLL_CANVAS_H = 500
SCROLL_CANVAS_W = 1000

class ScrollbarFrame(tk.Frame):
    """
    Extends class tk.Frame to support a scrollable Frame 
    This class is independent from the widgets to be scrolled and 
    can be used to replace a standard tk.Frame
    """
    def __init__(self, parent, frame_h, frame_w):
        """ Initiates a scrollable canvas with labels using specified
        height and width. Canvas is scrollable both over canvas and scrollbar.
        """

        super().__init__(parent)

        # Place the scrollbar on self, layout to the right
        vsb = tk.Scrollbar(self, orient="vertical")
        vsb.pack(side="right", fill="y")

        # The Canvas which supports the Scrollbar Interface, 
        # placed on self and layed out to the left.
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", 
                                height = frame_h, 
                                width = width_h)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.configure(command=self.canvas.yview)

        # Allow canvas to be scrolled using mousewheel while hovering 
        # over the canvas region.
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Place a frame on the canvas, this frame will hold the child widgets
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = tk.Frame(self.canvas, background=self.canvas.cget('bg'))
        self.canvas.create_window((0, 0), window=self.scrolled_frame, anchor="nw")
        
        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)

        # Reset the scroll region to encompass the inner frame
        self.scrolled_frame.bind("<Configure>", self.onFrameConfigure)

    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_mousewheel(self, event):
        """Allows canvas to be scrolled using mousewheel while hovering
        over canvas.
        """
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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

        # Some data, layout into the sbf.scrolled_frame
        frame = sbf.scrolled_frame
        for row in range(50):
            text = "%s" % row
            tk.Label(frame, text=text,
                     width=3, borderwidth="1", relief="solid") \
                .grid(row=row, column=0)

            text = "this is the second column for row %s" % row
            tk.Label(frame, text=text,
                     background=sbf.scrolled_frame.cget('bg')) \
                .grid(row=row, column=1)

            text = "this is the third column for row %s" % row
            tk.Label(frame, text=text,
                     background=sbf.scrolled_frame.cget('bg')) \
                .grid(row=row, column=2)

if __name__ == "__main__":
    root = App()
    root.mainloop()