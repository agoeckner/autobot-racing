from tkinter import *
from tkinter import ttk
import tkinter as tk

class ConfigUI(): #{

    currentCarRow = 0 #Used for grid when adding new Car Config Frames
    carDisplayFrames = [] # Used to store the frames inside the car display frame

    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.parent = parent
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the Car Configuration Menu Window
    ##-----------------------------------------------------------------------------
    def createWindow(self): #{
        self.window = Tk()

        #Maximizes the window on the screen
        self.window.geometry('1100x500+150+50')
        self.window.wm_iconbitmap('../ccs.ico')
        self.window.title('Car Configuration Menu')

        self.createf1()
        self.createCarDisplayFrame()
        self.createf3()
        self.createf4()

        self.window.bind("<Configure>", self.updateWindow)
    #}

    def createf1(self): #{
        self.f1 = Frame(self.window)

        self.f1.pack(fill=X)

        blankLabel = Label(self.f1, text=' ')
        blankLabel.config(font=("Tahoma", 11))
        blankLabel.grid(row=0,column=0)
    #}

    def createCarDisplayFrame(self): #{
        self.f2 = Frame(self.window, width=(self.window.winfo_width() - 50), height=(self.window.winfo_height() - 150), borderwidth=5,highlightbackground="black", highlightthickness=1)

        #Frame Scrollbar
        scrollY = ttk.Scrollbar(self.f2)
        scrollY.pack(side='right', fill=Y)

        
        
        self.f2.pack()
    #}

    def createf3(self): #{
        self.f3 = Frame(self.window)

        self.f3.pack(fill=X)

        blankLabel = Label(self.f3, text=' ')
        blankLabel.config(font=("Tahoma", 11))
        blankLabel.grid(row=0,column=0)
    #}

    def createf4(self): #{
        self.f4 = Frame(self.window)

        self.f4.pack(fill=X)
        
        self.addCarButton = Button(self.f4, text='Add Car', command=self.addNewCar, width=12)
        self.addCarButton.config(font=("Tahoma", 12))
        self.addCarButton.pack()
    #}

    def addNewCar(self): #{
        print('')
    #}

    def updateWindow(self, event): #{
        self.f2.config(width=(self.window.winfo_width() - 50), height=(self.window.winfo_height() - 150))
    #}

#}
