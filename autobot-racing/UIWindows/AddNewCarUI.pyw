from tkinter import *
from tkinter import ttk
import tkinter as tk

##TODO: Add dropdowns to select control and guidance system

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
        self.destroyWindow() #Called in case the user tries to open multiple windows
        self.window = Tk()

        #Sets the geometry and title on the window
        self.window.geometry('500x300+300+150')
        self.window.wm_iconbitmap('../ccs.ico')
        self.window.title('Add New Car')
        self.window.resizable(0, 0)

        self.createf1()
        self.createf2()
        self.createf3()
        self.createf4()
        self.createf5()
        self.createf6()
        self.createf7()
        self.createf8()
        self.createf9()
        self.createf10()
        self.createf11()
        self.createf12()

        self.carNameEntry.focus_force()
        self.window.mainloop()
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

        self.carNameEntry = Entry(self.f2, width=55)
        self.carNameEntry.pack(side='left')
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

        self.IPEntry = Entry(self.f4, width=25)
        self.IPEntry.pack(side='left')
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f5
    ##-----------------------------------------------------------------------------
    def createf5(self): #{
        self.f5 = Frame(self.window)
        self.f5.pack(fill=X)

        blankLabel = Label(self.f5, text=' ')
        blankLabel.config(font=("Tahoma", 4))
        blankLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f6
    ##-----------------------------------------------------------------------------
    def createf6(self): #{
        self.f6 = Frame(self.window)
        self.f6.pack(fill=X)

        portLabel = Label(self.f6, text='   Enter Car Port:    ')
        portLabel.config(font=("Tahoma", 11))
        portLabel.pack(side='left')

        self.portEntry = Entry(self.f6, width=25)
        self.portEntry.pack(side='left', padx=3)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f7
    ##-----------------------------------------------------------------------------
    def createf7(self): #{
        self.f7 = Frame(self.window)
        self.f7.pack(fill=X)

        blankLabel = Label(self.f7, text=' ')
        blankLabel.config(font=("Tahoma", 11))
        blankLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f8
    ##-----------------------------------------------------------------------------
    def createf8(self): #{
        self.f8 = Frame(self.window)
        self.f8.pack(fill=X)

        controlSystemLabel = Label(self.f8, text='   Select Control System:     ')
        controlSystemLabel.config(font=("Tahoma", 11))
        controlSystemLabel.grid(row=0,column=0)

        #self.controlOptions = StringVar()
        #self.controlOptions['values'] = self.parent.getControlSystems()
        
        self.controlOptionList = ttk.Combobox(self.f8, values=self.parent.getControlSystems())
        self.controlOptionList.grid(row=0,column=1)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f9
    ##-----------------------------------------------------------------------------
    def createf9(self): #{
        self.f9 = Frame(self.window)
        self.f9.pack(fill=X)

        blankLabel = Label(self.f9, text=' ')
        blankLabel.config(font=("Tahoma", 11))
        blankLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f10
    ##-----------------------------------------------------------------------------
    def createf10(self): #{
        self.f10 = Frame(self.window)
        self.f10.pack(fill=X)

        guidanceSystemLabel = Label(self.f10, text='   Select Guidance System:  ')
        guidanceSystemLabel.config(font=("Tahoma", 11))
        guidanceSystemLabel.grid(row=0,column=0)

        #self.guidanceOptions = StringVar()
        #self.guidanceOptions['values'] = self.parent.getGuidanceSystems()
        
        self.guidanceOptionList = ttk.Combobox(self.f10, values=self.parent.getGuidanceSystems())
        self.guidanceOptionList.grid(row=0,column=1)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f11
    ##-----------------------------------------------------------------------------
    def createf11(self): #{
        self.f11 = Frame(self.window)
        self.f11.pack(fill=X)

        blankLabel = Label(self.f11, text=' ')
        blankLabel.config(font=("Tahoma", 11))
        blankLabel.grid(row=0,column=0)
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the frame f12
    ##-----------------------------------------------------------------------------
    def createf12(self): #{
        self.f12 = Frame(self.window)
        self.f12.pack(fill=X)

        blankLabel = Label(self.f12, text='\t\t\t                ')
        blankLabel.config(font=("Tahoma", 8))
        blankLabel.grid(row=0,column=0)

        self.addNewCarButton = Button(self.f12, text='Add Car', command=self.addCar, width=15)
        self.addNewCarButton.config(font=("Tahoma", 10))
        self.addNewCarButton.grid(row=0,column=1)
    #}

    ##-----------------------------------------------------------------------------
    ## Collects info from entries and sends back to config UI
    ##-----------------------------------------------------------------------------
    def addCar(self): #{
        carName = self.carNameEntry.get()
        IP = self.IPEntry.get()
        port = self.portEntry.get()
        #controlSystem = 

        self.parent.addNewCarFrame(carName,IP,port)

        self.destroyWindow()
    #}

    ##-----------------------------------------------------------------------------
    ## Deletes the addNewCar Window
    ##-----------------------------------------------------------------------------
    def destroyWindow(self): #{
        try:
            self.window.destroy()
        except:
            print('Error destroying AddNewCar UI')
    #}
#}

















