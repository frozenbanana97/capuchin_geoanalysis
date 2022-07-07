# Import Module
import tkinter as tk
from tkinter import *
 
# create root window
root = Tk()
 
# root window title and dimension
root.title("hallo")
# Set geometry (widthxheight)
root.geometry('450x300')

# Functions to be used by widgets
# function to display text when button is clicked
def clicked():
    print('click')

# all widgets will be here
# adding a label to the root window
lbl = Label(root, text='Time to parse GPX data')
lbl.grid()

# Button
# button widget with red color text inside
btn = Button(root, text = 'Run' ,
             fg = 'blue', command=clicked)

Checkbutton1 = IntVar()  

Button1 = Checkbutton(root, text = "Tutorial", 
                      variable = Checkbutton1,
                      onvalue = 1,
                      offvalue = 0,
                      height = 2,
                      width = 10)
Button1.grid()
# Set Button Grid
btn.grid(column=10, row=5)

# Execute Tkinter
root.mainloop()