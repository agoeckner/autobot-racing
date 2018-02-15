from tkinter import *
from tkinter import ttk
import tkinter as tk

class ConfigUI(): #{

    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.parent = parent
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the main window for the program
    ##-----------------------------------------------------------------------------
    def createWindow(self): #{
        self.window = Tk()

        #Maximizes the window on the screen
        self.window.geometry('1100x500+150+50')
        self.window.wm_iconbitmap('../ccs.ico')
        self.window.title('Car Configuration Menu')

        #Frames
        self.f1 = Frame(self.window)
        self.f2 = Frame(self.window)
        self.f3 = Frame(self.window)
        self.f4 = Frame(self.window)
        self.f5 = Frame(self.window)
        self.f6 = Frame(self.window)
        self.f7 = Frame(self.window)
        self.f8 = Frame(self.window)
        self.f9 = Frame(self.window)

        
    #}

#}
