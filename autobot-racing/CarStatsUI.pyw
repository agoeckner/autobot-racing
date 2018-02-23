from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont

class CarStatsUI(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.parent = parent
        self.carDisplayFrames = [] # Used to store the car frames and their info
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the Car Configuration Menu Window
    ##-----------------------------------------------------------------------------
    def createWindow(self): #{
        self.window = Tk()

        #Sets the geometry and title on the window
        self.window.geometry('1500x800+150+50')
        self.window.wm_iconbitmap('../ccs.ico')
        self.window.title('Autobot Racing')

        #Create each frame in the window
        self.createf1()
        self.createf2()

        self.createCarConfigTitle()

        #For Testing Remove Later----------------------------------------------------------------------------------------------------
        self.addNewCarCallback('Car 1', '127.0.0.5', '457')
        self.addNewCarCallback('Car 2', '127.0.0.6', '458')
        #----------------------------------------------------------------------------------------------------------------------------


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
        self.f2 = Frame(self.window, width=(self.window.winfo_width() - 10), height=(self.window.winfo_height() - 100), borderwidth=5,highlightbackground="black", highlightthickness=1)
        self.f2.pack()

        f = tkFont.Font(family='helvetica', size=12)
        s = ttk.Style()
        s.configure('.', font=f)

        CarInfoFrame = Frame(self.f2,width=400, borderwidth=5,highlightbackground="black", highlightthickness=1)
        CameraFeedTitleFrame = Frame(self.f2, borderwidth=5,highlightbackground="red", highlightthickness=1)

        CarInfoFrame.pack(side='left', expand=False, anchor=NW, fill=Y)#grid(row=0,column=0,sticky=N+S)
        CameraFeedTitleFrame.pack(side='right', expand=True, anchor=NE, fill=BOTH, padx=5)

        titleLabel = Label(CarInfoFrame, text='Car Information\t\t\t\t        ')
        titleLabel.config(font=("Tahoma", 12))
        titleLabel.pack(side='top', anchor=NW)

        nb = ttk.Notebook(CarInfoFrame)
        self.CarConfig = Canvas(nb)
        self.LeaderBoard = Canvas(nb)

        nb.add(self.CarConfig, text="Car Configuration Menu")
        nb.add(self.LeaderBoard, text="LeaderBoard")

        nb.pack(fill=X, pady=5)


        LeaderBoardTitleLabel = Label(self.LeaderBoard, text='LeaderBoard')
        LeaderBoardTitleLabel.config(font=("Tahoma", 13))
        LeaderBoardTitleLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates title section in the Car Configuration Tab
    ##-----------------------------------------------------------------------------
    def createCarConfigTitle(self): #{
        titleFrame = Frame(self.CarConfig, height=10)
        titleFrame.pack(side='top', padx=5, pady=3, fill=X)

        titleFrame.columnconfigure(1, weight=3)

        titleFrame1 = Frame(titleFrame)
        carLabel = Label(titleFrame1, text='Car Name')
        carLabel.config(font=("Tahoma", 9))
        carLabel.pack()
        titleFrame1.grid(row=0,column=0,sticky=E)

        titleFrame2 = Frame(titleFrame)
        IPLabel = Label(titleFrame2, text='IP         ')
        IPLabel.config(font=("Tahoma", 9))
        IPLabel.pack()
        titleFrame2.grid(row=0,column=1)

        titleFrame3 = Frame(titleFrame)
        portLabel = Label(titleFrame3, text='Port')
        portLabel.config(font=("Tahoma", 9))
        portLabel.pack(padx=2)
        titleFrame3.grid(row=0,column=2,sticky=W)
    #}

    ##-----------------------------------------------------------------------------
    ## Callback for the AddNewCar UI to update car display frame
    ##-----------------------------------------------------------------------------
    def addNewCarCallback(self, carName, IP, port): #{
        newCarFrame = Frame(self.CarConfig, height=10, borderwidth=5,highlightbackground="green", highlightthickness=1)
        newCarFrame.pack(side='top', padx=5, pady=3, fill=X)
        newCarFrame.bind("<Button-1>", lambda event, arg=carName: self.openEditCarWindow(event, arg))

        newCarFrame.columnconfigure(1, weight=3)

        carFrame1 = Frame(newCarFrame)
        carLabel = Label(carFrame1, text=str(carName))
        carLabel.config(font=("Tahoma", 9))
        carLabel.pack()

        carFrame1.grid(row=0,column=0,sticky=E)

        carFrame2 = Frame(newCarFrame)
        IPLabel = Label(carFrame2, text=str(IP))
        IPLabel.config(font=("Tahoma", 9))
        IPLabel.pack()
        carFrame2.grid(row=0,column=1)

        carFrame3 = Frame(newCarFrame)
        portLabel = Label(carFrame3, text=str(port))
        portLabel.config(font=("Tahoma", 9))
        portLabel.pack()
        carFrame3.grid(row=0,column=2,sticky=W)

        frameInfo = [carName, IP, port, newCarFrame.winfo_id(), newCarFrame]
        self.carDisplayFrames.append(frameInfo)
    #}

    ##-----------------------------------------------------------------------------
    ## Event handler for clicking on a Car frame
    ##-----------------------------------------------------------------------------
    def openEditCarWindow(self, event, arg): #{
        print('')
##        for i in self.carDisplayFrames: #{
##            if arg == i[0]:
##                self.parent.openEditCarUI(i[0], i[1], i[2], i[3])
##        #}
    #}

    ##-----------------------------------------------------------------------------
    ## Tracks size changes in UI to update UI widgets
    ##-----------------------------------------------------------------------------
    def updateWindow(self, event): #{
        #print('')
        self.f2.config(width=(self.window.winfo_width() - 50), height=(self.window.winfo_height() - 100))
    #}
#}










































        
