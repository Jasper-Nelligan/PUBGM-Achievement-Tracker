import tkinter
from tkinter import *
from PIL import Image, ImageTk


root = tkinter.Tk()  #this creates a window onto which all widgets will be placed

#setting up main window
background_image = Image.open('./Images/PUBG_background_image.png')
program_title_image = Image.open('./Images/program_title.png')

background_w, background_h = background_image.size
print(background_image.size)

canvas = tkinter.Canvas(root, height=background_h, width=background_w)
canvas.pack()
#First parameter to .paste() is the image to paste.
#Second are coordinates.
#The secret sauce is the third parameter. It indicates a mask that will be used 
#to paste the image. If you pass a image with transparency, 
#then the alpha channel is used as mask.
background_image.paste(program_title_image, (150,40), program_title_image)

#background_image = Tkinter.PhotoImage(file='./Images/PUBG_background_image.png')
#background_h, background_w = background_image.height(), background_image.width()
#background_label = Tkinter.Label(root, image=background_image, bg='black')
#background_label.pack()

#program_title_image = Tkinter.PhotoImage(file='./Images/program_title.png')
#program_title_label = Tkinter.Label(root, image=program_title_image)
#program_title_label.place(relheight=0.1, relwidth=0.1)

#Convert the Image object into a TkPhoto object
tk_background_image = ImageTk.PhotoImage(background_image)

background_label = Label(root, image=tk_background_image, bg='black')
background_label.place(relheight=1,relwidth=1)


canvas = tkinter.Canvas(root, height=background_h, width=background_w, bg="black", highlightthickness=0)
#canvas.pack(expand ='true', fill ='both')
#canvas.create_image(0, 0, image=background_image)


root.mainloop()


