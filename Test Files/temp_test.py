from tkinter import *

def foo():
    x = chk.get()
    if x:
        print('hello')

root = Tk()
chk = IntVar()

c = Checkbutton(root, text='Check for CSV Instead', variable=chk, bg='#45484c', fg='white')
c.grid(row=3, column=3)
root.mainloop