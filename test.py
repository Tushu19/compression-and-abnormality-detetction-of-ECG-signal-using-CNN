
from itertools import count
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from ecgCompression import *
import matplotlib.pyplot as plt
import numpy as np
from ecg_file_display import *
from singleFileConversion import *
import time
from automata import *


# for box
root = Tk()
root.geometry('600x450')
# def initialisation():
#     global flag
#     flag=True

# initialisation()
s= ttk.Style()
s.theme_use("classic")
def lightMode():
    global background
    background = "#D2F2F5"
    global textColor
    textColor="black"
lightMode()
def darkMode():
    global background
    background = "#36394F"
    global textColor
    textColor="#DCD5D2"

# def modeSelect():
#     if(flag):
#         darkMode()
#     else:
#         lightMode()
#     flag=~flag

# modeSelect()
root.title("ECG Compression")
# root.iconbitmap("ECGbitmapImage.ico")

root.config(bg=background)
headLabel = Label(root, text="ECG Compression and Decompression", pady=10,
                  bg=background, fg=textColor, font=("Arial", 25))
# headLabel.pack()
headLabel.grid(row=0,column=0,columnspan=20,padx=20,pady=20)

def inputRecordName():
    global str
    str = entry.get()
    if (len(str) != 0):
        nameRecord(str)

def compress():
        global str
        str = entry.get()
        if (len(str) != 0):
            nameRecord(str)
            begin=time.time()
            compression()
            end=time.time()
            global compTime
            compTime=end-begin
            tkinter.messagebox.showinfo("Compression", "Compression Done")

def decompress():
        begin=time.time()
        Results = decompression()
        end=time.time()
        global decompTime
        decompTime=end-begin-0.5
        timing(str,compTime,decompTime)
        displayPRD = Text(root, font=("Arial", 15), width=30, height=2, pady=5)
        displayPRD.insert(1.0, f"PRD = {Results[0]}")
        displayPRD.configure(state='disabled')
        # displayPRD.pack()
        displayPRD.grid(row=9,column=4,columnspan=2)
        displayCR = Text(root, font=("Arial", 15), width=30, height=2, pady=5)
        displayCR.insert(1.0, f"CR = {Results[1]}")
        displayCR.configure(state='disabled')
        # displayCR.pack()
        displayCR.grid(row=10,column=4,columnspan=2)

def plotOG():
    ogPlot(str)

def plotRE():
    rePlot(str)

def conversionCSV():
    global str
    str = entry.get()
    if (len(str) != 0):
        nameRecord(str)
        conversion(str)
        tkinter.messagebox.showinfo("Convert", "Conversion Done")

# modeButton = Button(root, text="Theme",
#                      command=modeSelect, bg=background, fg=textColor, font=("Arial", 15))  # for submit button
# # entryButton.pack()
# modeButton.grid(row=6,column=10, pady=10)

entryLabel = Label(root, text="Enter Record Number : ",
                   bg=background, fg=textColor, font=("Arial", 15),width=20)  # label of entry box
# entryLabel.pack()
entryLabel.grid(row=5,column=1,columnspan=4)

entry = Entry(root, width=10, bg="white", fg="black",
              borderwidth=3, font=("Arial", 15))  # creates entry box
# entry.pack()
entry.grid(row=5, column=5,pady=10)

entryButton = Button(root, text="Compress",
                     command=compress, bg=background, fg=textColor, font=("Arial", 15))  # for submit button
# entryButton.pack()
entryButton.grid(row=6,column=3, pady=10)

entryButton = Button(root, text="Decompress",
                     command=decompress, bg=background, fg=textColor, font=("Arial", 15))  # for submit button
# entryButton.pack()
entryButton.grid(row=6,column=4, pady=10)

entryButton = Button(root, text="Convert",
                     command=conversionCSV, bg=background, fg=textColor, font=("Arial", 15))  # for submit button
# entryButton.pack()
entryButton.grid(row=6,column=5, pady=10)

plotOG_button = Button(root, text="Plot Original", bg=background, fg=textColor,
                       command=plotOG, height=1, width=10, font=("Arial", 15))
# plotOG_button.pack()
plotOG_button.grid(row=8,column=4,pady=10)

plotRE_button = Button(root, text="Plot Reconstructed", bg=background, fg=textColor,
                       command=plotRE, height=1, width=20, font=("Arial", 15))
# plotOG_button.pack()
plotRE_button.grid(row=8,column=5,pady=10)

# entry.insert(0, "Enter record number")
# myButton=Button(root, text="Enter", padx=50 , pady=50, command=inputRecordName , fg="red", bg="aqua")
# myButton.pack()
root.mainloop()