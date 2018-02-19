from tkinter import *
from tkinter import ttk
import tkinter as tk

class CarStatsUI(): #{
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

        #Sets the geometry and title on the window
        self.window.geometry('1100x500+150+50')
        self.window.wm_iconbitmap('../ccs.ico')
        self.window.title('Car Statistics')

        #Create each frame in the window
        self.createf1()
        self.createf2()


        self.window.bind("<Configure>", self.updateWindow)
        self.window.mainloop()
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f1 at the top
    ##-----------------------------------------------------------------------------
    def createf1(self): #{
        self.f1 = Frame(self.window)

        self.f1.pack(fill=X)

        blankLabel = Label(self.f1, text=' ')
        blankLabel.config(font=("Tahoma", 11))
        blankLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates frame f2
    ##-----------------------------------------------------------------------------
    def createf2(self): #{
        self.f2 = Frame(self.window)
        self.f2.pack(fill=X)

        LeaderBoardTitleFrame = Frame(self.f2)
        CameraFeedTitleFrame = Frame(self.f2)
        
        LeaderBoardTitleLabel = Label(LeaderBoardTitleFrame, text='LeaderBoard')
        LeaderBoardTitleLabel.config(font=("Tahoma", 13))
        LeaderBoardTitleLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Tracks size changes in UI to update UI widgets
    ##-----------------------------------------------------------------------------
    def updateWindow(self, event): #{
        print('')
        #self.f2.config(width=(self.window.winfo_width() - 50), height=(self.window.winfo_height() - 150))
    #}
#}
