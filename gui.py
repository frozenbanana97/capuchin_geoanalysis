import tkinter as tk
from tkinter import *
from tkinter import filedialog
 
# create root window
root = Tk()
 
# root.directory = tkFileDialog.askdirectory()
# print (root.directory)

# root window title and dimension
root.title('Capuchin Geoanalysis Settings')
# Set geometry (widthxheight)
root.geometry('500x300')

# varibales to be used by functions
Checkbutton1 = IntVar()  
Checkbutton2 = IntVar() 
user_button = IntVar()
# Functions to be used by widgets

# Select working directory
def directory():
    # get a directory path by user
    filepath=filedialog.askdirectory(initialdir=r"F:\python\pythonProject",
                                    title="Dialog box")
    label_path=Label(root,text=filepath,font=('italic 10'))
    label_path.grid(row=6,column=2)
    dir_path = filepath
    print(dir_path)

# Have tab move to next widget
def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

# function to display text when button is clicked
def run():
    print('running...')

def userInput():
    observer = observer_input.get(1.0, 'end-1c')
    group = group_input.get(1.0, 'end-1c')
    weather = weather_input.get(1.0, 'end-1c')

    print(observer)
    print(group)
    print(weather)

def mytoggle1(event=None):
    val = Checkbutton1.get()
    if val == 1:
        print('1 on')
    else:
        print('1 off')

def mytoggle2(event=None):
    val = Checkbutton2.get()
    if val == 1:
        print('2 on')
    else:
        print('2 off')

def usertoggle(event=None):
    val = user_button.get()
    if val == 1:
        print('user on')
    else:
        print('user off')

# all widgets will be here
# adding a label to the root window
lbl = Label(root, text='Time to parse GPX data').grid()

# User Input
user_lbl = Label(root, text='Include user input?')
user_check = Checkbutton(root, text = 'Yes/No', 
                      variable = user_button,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 10,
                      command=usertoggle)
observer_lbl = Label(root, text='Observer')
group_lbl = Label(root, text='Group')
weather_lbl = Label(root, text='Weather')

observer = ''
group = ''
weather = ''

observer_input = Text(root, height=1,width=20)
observer_input.bind('<Tab>', focus_next_window)
group_input = Text(root, height=1,width=20)
group_input.bind('<Tab>', focus_next_window)
weather_input = Text(root, height=1,width=20)
submit_btn = Button(root, text='Submit', fg = 'black', command=userInput)

# Button
# button widget with red color text inside
dir_btn = Button(root, text='Select Directory', command=directory)

btn = Button(root, text = 'Run' ,
             fg = 'black', command=run)

Button1 = Checkbutton(root, text = 'Test 1', 
                      variable = Checkbutton1,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 10,
                      command=mytoggle1)

Button2 = Checkbutton(root, text = 'Test 2', 
                      variable = Checkbutton2,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 5,
                      command=mytoggle2)

# Set Grid
user_lbl.grid(row=1)
user_check.grid(row=1,column=2)
observer_lbl.grid(row=2)
group_lbl.grid(row=3)
weather_lbl.grid(row=4)

observer_input.grid(row=2,column=2)
group_input.grid(row=3,column=2)
weather_input.grid(row=4,column=2)
submit_btn.grid(row=5,column=2)

dir_btn.grid(row=6)

Button1.grid()
Button2.grid()
btn.grid()

# Execute Tkinter
root.mainloop()