from tkinter import *
from tkinter import ttk
import tkinter as tk

class ConfigUI(): #{

    currentCarRow = 0 #Used for grid when adding new Car Config Frames

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

        self.window.bind("<Configure>", self.updateWindow)
    #}

    def createf1(self): #{
        self.f1 = Frame(self.window)

        self.f1.pack(fill=X)

        blankLabel = Label(self.f1, text=' ')
        blankLabel.config(font=("Tahoma", 10))
        blankLabel.grid(row=0,column=0)
    #}

    def createCarDisplayFrame(self): #{
        self.f2 = Frame(self.window, width=(self.window.winfo_width() - 50), height=(self.window.winfo_height() - 150), borderwidth=5,relief=tk.RIDGE)

        ysb = ttk.Scrollbar(self.f3, orient='vertical', command=self.routingList.yview)
        ysb.grid(row=0,column=2,sticky=N+S)

        self.f2.pack()
    #}

    def updateWindow(self, event): #{
        self.f2.config(width=(self.window.winfo_width() - 50), height=(self.window.winfo_height() - 150))
    #}

#}
