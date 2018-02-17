from tkinter import *
from tkinter import ttk
import tkinter as tk

class ConfigUI(): #{

    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.parent = parent
        self.carDisplayFrames = [] # Used to store the frames inside the car display frame
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
        self.addCarDisplayTitle()

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
    ## Creates the frame to display the list of cars
    ##-----------------------------------------------------------------------------
    def createCarDisplayFrame(self): #{
        self.f2 = Frame(self.window, width=(self.window.winfo_width() - 50), height=(self.window.winfo_height() - 150), borderwidth=5,highlightbackground="black", highlightthickness=1)

        #Frame Scrollbar
        scrollY = ttk.Scrollbar(self.f2)
        scrollY.pack(side='right', fill=Y)

        
        
        self.f2.pack()
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f3 below the car display
    ##-----------------------------------------------------------------------------
    def createf3(self): #{
        self.f3 = Frame(self.window)

        self.f3.pack(fill=X)

        blankLabel = Label(self.f3, text=' ')
        blankLabel.config(font=("Tahoma", 11))
        blankLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame that holds the add car button
    ##-----------------------------------------------------------------------------
    def createf4(self): #{
        self.f4 = Frame(self.window)

        self.f4.pack(fill=X)
        
        self.addCarButton = Button(self.f4, text='Add Car', command=self.addNewCar, width=12)
        self.addCarButton.config(font=("Tahoma", 12))
        self.addCarButton.pack()
    #}

    ##-----------------------------------------------------------------------------
    ## Adds a Title section for the Car List
    ##-----------------------------------------------------------------------------
    def addCarDisplayTitle(self): #{
        titleFrame = Frame(self.f2, width=(self.window.winfo_width() - 150), height=10)
        titleFrame.pack(side='top', padx=5, pady=3, fill=X)

        titleFrame.columnconfigure(1, weight=3)

        titleFrame1 = Frame(titleFrame)
        carLabel = Label(titleFrame1, text='Car Name')
        carLabel.config(font=("Tahoma", 12))
        carLabel.pack()
        titleFrame1.grid(row=0,column=0,sticky=E)

        titleFrame2 = Frame(titleFrame)
        IPLabel = Label(titleFrame2, text='IP    ')
        IPLabel.config(font=("Tahoma", 12))
        IPLabel.pack()
        titleFrame2.grid(row=0,column=1)

        titleFrame3 = Frame(titleFrame)
        portLabel = Label(titleFrame3, text='Port')
        portLabel.config(font=("Tahoma", 12))
        portLabel.pack(padx=2)
        titleFrame3.grid(row=0,column=2,sticky=W)
    #}

    ##-----------------------------------------------------------------------------
    ## Opens the AddNewCar UI
    ##-----------------------------------------------------------------------------
    def addNewCar(self): #{
        #Open new car UI
        print('')
    #}

    ##-----------------------------------------------------------------------------
    ## Callback for the AddNewCar UI to update car display frame
    ##-----------------------------------------------------------------------------
    def addNewCarCallback(self, carName, IP, port): #{
        newCarFrame = Frame(self.f2, width=(self.window.winfo_width() - 150), height=10, borderwidth=5,highlightbackground="black", highlightthickness=1)
        newCarFrame.pack(side='top', padx=5, pady=3, fill=X)
        newCarFrame.bind("<Button-1>", lambda event, arg=carName: self.openEditCarWindow(event, arg))

        newCarFrame.columnconfigure(1, weight=3)

        carFrame1 = Frame(newCarFrame)
        carLabel = Label(carFrame1, text=str(carName))
        carLabel.config(font=("Tahoma", 12))
        carLabel.pack()
        carFrame1.grid(row=0,column=0,sticky=E)

        carFrame2 = Frame(newCarFrame)
        IPLabel = Label(carFrame2, text=str(IP))
        IPLabel.config(font=("Tahoma", 12))
        IPLabel.pack()
        carFrame2.grid(row=0,column=1)

        carFrame3 = Frame(newCarFrame)
        portLabel = Label(carFrame3, text=str(port))
        portLabel.config(font=("Tahoma", 12))
        portLabel.pack()
        carFrame3.grid(row=0,column=2,sticky=W)

        frameInfo = [carName, newCarFrame]
        self.carDisplayFrames.append(frameInfo)
    #}

    ##-----------------------------------------------------------------------------
    ## Tracks size changes in UI to update UI widgets
    ##-----------------------------------------------------------------------------
    def updateWindow(self, event): #{
        self.f2.config(width=(self.window.winfo_width() - 50), height=(self.window.winfo_height() - 150))
    #}

    #lambda event, arg=data: self.on_mouse_down(event, arg)
    def openEditCarWindow(self, event, arg): #{
        print('Event: ' + str(event) + '\nArg: ' + str(arg))
        
    #}
#}

























