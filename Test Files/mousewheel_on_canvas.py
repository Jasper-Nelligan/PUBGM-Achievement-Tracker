import tkinter as tk
from tkinter import *
import time


root = Tk()


root.state('zoomed')  # full screen -windowed

# ------------------INTRODUCTION BLOCK--------------
f1 = Frame(root, width=900, height=700, relief=SUNKEN)
f1.grid_rowconfigure(1, weight=1)
f1.grid_columnconfigure(2, weight=1)
f1.pack(fill=BOTH, expand=1, side=BOTTOM)

root.title("Diagram Scroll Test")

Tops = Frame(root, width=1600, height=50, relief=SUNKEN)
Tops.pack(side=TOP)

# ------------------TIME--------------
localtime = time.asctime(time.localtime(time.time()))
# -----------------INFO TOP------------
lblinfo = Label(Tops, font=('aria', 30, 'bold'), text="My Diagram Scroll Test",
                fg="steel blue", bd=10, anchor='w')
lblinfo.grid(row=0, column=0)
lblinfo = Label(Tops, font=('aria', 20,), text=localtime, fg="steel blue", anchor=W)
lblinfo.grid(row=1, column=0)
lblinfo = Label(Tops, font=('aria', 15, 'bold'), text="Please help", fg="steel blue", bd=10,
                anchor='w')
lblinfo.grid(row=2, column=0)

# ------------------CANVAS DEFINITION-------------

class CanvasDemo(Frame):


    def __init__(self,root):
        Frame.__init__(self,root)


        self.canvas = tk.Canvas(root, borderwidth=0)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        root.state('zoomed')
        self.vsb.pack(side="right", fill="y")
        self.canvas.config(width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        # self.canvas.pack(side="left", fill="both", expand="1")
        self.canvas.pack(fill="both", expand="1")
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                    tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    # ------------------CODE TO CREATE BLOCK DIAGRAMS-------------

    def populate(self):


        i = 0
        turnCount = 0  # Keeps track of how many boxes is used to trigger a turn

        # Create Small starter box
        lineVarx1 = 70
        lineVary1 = 50
        lineVarx2 = 120
        lineVary2 = 50

        varx1 = 120
        vary1 = 25
        varx2 = 220
        vary2 = 75

        varblk = 1
        varline = 1

        self.canvas.create_rectangle(20, 40, 70, 60, fill="green", tags="start")



        while i < 200:  # Provides 104 blocks

            # ------------------IF STATEMENT TO CONTROL WHEN
            # DIAGRAM TURNS-------------

            if turnCount == 12:  # At Turn Point, initiating turn sequence
                lineVarx2 = lineVarx2 - 25
                self.canvas.create_line(lineVarx1, lineVary1, lineVarx2, lineVary2, arrow="last", tags="to_r1")
                # Downward line
                lineVarx1 = lineVarx2
                lineVary1 = lineVary2
                lineVary2 = lineVary2 + 50
                self.canvas.create_line(lineVarx1, lineVary1, lineVarx2, lineVary2, arrow="last", tags="to_r1")

                # long line to left
                lineVarx1 = lineVarx2
                lineVary1 = lineVary2
                lineVarx2 = lineVarx2 - 1825
                self.canvas.create_line(lineVarx1, lineVary1, lineVarx2, lineVary2, arrow="last", tags="to_r1")

                # Downward line
                lineVarx1 = lineVarx2
                lineVary1 = lineVary2
                lineVary2 = lineVary2 + 50
                self.canvas.create_line(lineVarx1, lineVary1, lineVarx2, lineVary2, arrow="last", tags="to_r1")

                lineVary1 = lineVary2
                lineVarx2 = lineVarx2 + 50

                varx1 = lineVarx2
                vary1 = lineVary2 - 25
                varx2 = lineVarx2 + 100
                vary2 = lineVary2 + 25
                turnCount = 0

            self.canvas.create_line(lineVarx1, lineVary1, lineVarx2, lineVary2, arrow="last", tags="to_r1")
            self.canvas.create_rectangle(varx1, vary1, varx2, vary2, fill="bisque", tags="r1")
            self.canvas.create_text(varx1 + 20, vary1, fill="darkblue", anchor=NW,
                                    text="Hi")
            self.canvas.create_text(varx1 + 20, vary1 + 10, fill="darkblue", anchor=NW,
                                    text="bye")
            self.canvas.create_text(varx1 + 20, vary1 + 20, fill="darkblue", anchor=NW,
                                    text="fly")
            lineVarx1 = lineVarx1 + 150
            lineVarx2 = lineVarx2 + 150
            varx1 = varx1 + 150
            varx2 = varx2 + 150
            i += 1
            turnCount += 1

        # "End" Block
        lineVarx1 = varx2 - 150
        lineVarx2 = lineVarx1 + 50

        varx1 = lineVarx2
        vary1 = lineVary1 - 10
        varx2 = varx1 + 50
        vary2 = lineVary1 + 10

        self.canvas.create_line(lineVarx1, lineVary1, lineVarx2, lineVary2, arrow="last", tags="to_r1")
        self.canvas.create_rectangle(varx1, vary1, varx2, vary2, fill="red", tags="r1")






    def _on_mousewheel(self, event):
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")



    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



def qexit():
    root.destroy()


btnexit = Button(f1, padx=16, pady=7, bd=10, fg="black", font=('ariel', 12, 'bold'), width=8, text="EXIT",
                    bg="powder blue", command=qexit)
btnexit.grid(row=15, column=2)





canvas = CanvasDemo(root)
canvas.pack()

mainloop()