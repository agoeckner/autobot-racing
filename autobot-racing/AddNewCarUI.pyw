from tkinter import *
from tkinter import ttk
import tkinter as tk

class AddNewCarUI(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.parent = parent
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the Add New Car Window
    ##-----------------------------------------------------------------------------
    def createWindow(self): #{
        self.window = Tk()

        #Sets the geometry and title on the window
        self.window.geometry('500x200+200+50')
        self.window.wm_iconbitmap('../ccs.ico')
        self.window.title('Add New Car')
        self.window.resizable(0, 0)

        self.createf1()
        self.createf2()
        self.createf3()
        self.createf4()
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f1
    ##-----------------------------------------------------------------------------
    def createf1(self): #{
        self.f1 = Frame(self.window)
        self.f1.pack(fill=X)

        blankLabel = Label(self.f1, text=' ')
        blankLabel.config(font=("Tahoma", 11))
        blankLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f2
    ##-----------------------------------------------------------------------------
    def createf2(self): #{
        self.f2 = Frame(self.window)
        self.f2.pack(fill=X)

        carNameLabel = Label(self.f2, text='   Enter Car Name:  ')
        carNameLabel.config(font=("Tahoma", 11))
        carNameLabel.pack(side='left')

        carNameEntry = Entry(self.f2, width=55)
        carNameEntry.pack(side='left')
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f3
    ##-----------------------------------------------------------------------------
    def createf3(self): #{
        self.f3 = Frame(self.window)
        self.f3.pack(fill=X)

        blankLabel = Label(self.f3, text=' ')
        blankLabel.config(font=("Tahoma", 4))
        blankLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f4
    ##-----------------------------------------------------------------------------
    def createf4(self): #{
        self.f4 = Frame(self.window)
        self.f4.pack(fill=X)

        IPLabel = Label(self.f4, text='   Enter Car IP:       ')
        IPLabel.config(font=("Tahoma", 11))
        IPLabel.pack(side='left')

        IPEntry = Entry(self.f4, width=25)
        IPEntry.pack(side='left')
    #}
#}

















