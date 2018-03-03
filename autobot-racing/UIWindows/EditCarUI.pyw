from tkinter import *
from tkinter import ttk
import tkinter as tk

##TODO: Add dropdowns to select control and guidance system

class EditCarUI(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.parent = parent
    #}

    ##-----------------------------------------------------------------------------
    ## Creates the Add New Car Window
    ##-----------------------------------------------------------------------------
    def createWindow(self, car): #{
        self.car = car
        self.destroyWindow() #Called in case the user tries to open multiple windows
        self.window = Tk()

        #Sets the geometry and title on the window
        self.window.geometry('500x300+200+50')
        self.window.wm_iconbitmap('../ccs.ico')
        self.window.title('Edit Car')
        self.window.resizable(0, 0)

        self.createf1()
        self.createf2(car.carName)
        self.createf3()
        self.createf4(car.IP)
        self.createf5()
        self.createf6(car.port)
        self.createf7()
        self.createf8(car.controlSystem)
        self.createf9()
        self.createf10(car.guidanceSystem)
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
    def createf2(self, carName): #{
        self.f2 = Frame(self.window)
        self.f2.pack(fill=X)

        carNameLabel = Label(self.f2, text='   Enter Car Name:  ')
        carNameLabel.config(font=("Tahoma", 11))
        carNameLabel.pack(side='left')

        self.carNameEntry = Entry(self.f2, width=55)
        self.carNameEntry.insert(0, str(carName))
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
    def createf4(self, IP): #{
        self.f4 = Frame(self.window)
        self.f4.pack(fill=X)

        IPLabel = Label(self.f4, text='   Enter Car IP:       ')
        IPLabel.config(font=("Tahoma", 11))
        IPLabel.pack(side='left')

        self.IPEntry = Entry(self.f4, width=25)
        self.IPEntry.insert(0, str(IP))
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
    def createf6(self, port): #{
        self.f6 = Frame(self.window)
        self.f6.pack(fill=X)

        portLabel = Label(self.f6, text='   Enter Car Port:    ')
        portLabel.config(font=("Tahoma", 11))
        portLabel.pack(side='left')

        self.portEntry = Entry(self.f6, width=25)
        self.portEntry.insert(0, str(port))
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
    def createf8(self, controlSystem): #{
        self.f8 = Frame(self.window)
        self.f8.pack(fill=X)

        controlSystemLabel = Label(self.f8, text='   Select Control System:     ')
        controlSystemLabel.config(font=("Tahoma", 11))
        controlSystemLabel.grid(row=0,column=0)

        #self.controlOptions = StringVar()
        #self.controlOptions['values'] = self.parent.getControlSystems()

        vals = self.parent.getControlSystems()
        index = 0
        for i in range(0, len(vals)):
            if vals[i] == controlSystem:
                index = i
        
        self.controlOptionList = ttk.Combobox(self.f8, values=vals)
        self.controlOptionList.grid(row=0,column=1)
        self.controlOptionList.current(index)
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
    def createf10(self, guidanceSystem): #{
        self.f10 = Frame(self.window)
        self.f10.pack(fill=X)

        guidanceSystemLabel = Label(self.f10, text='   Select Guidance System:  ')
        guidanceSystemLabel.config(font=("Tahoma", 11))
        guidanceSystemLabel.grid(row=0,column=0)

        vals = self.parent.getGuidanceSystems()
        index = 0
        for i in range(0, len(vals)):
            if vals[i] == guidanceSystem:
                index = i
        
        self.guidanceOptionList = ttk.Combobox(self.f10, values=vals)
        self.guidanceOptionList.grid(row=0,column=1)
        self.guidanceOptionList.current(index)
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

        blankLabel = Label(self.f12, text='\t\t  ')
        blankLabel.config(font=("Tahoma", 8))
        blankLabel.grid(row=0,column=0)

        self.saveChangesButton = Button(self.f12, text='Save Changes', command=self.saveCarSettings, width=15)
        self.saveChangesButton.config(font=("Tahoma", 10))
        self.saveChangesButton.grid(row=0,column=1)

        blankLabel1 = Label(self.f12, text='\t')
        blankLabel1.config(font=("Tahoma", 8))
        blankLabel1.grid(row=0,column=2)

        self.deleteCarButton = Button(self.f12, text='Delete Car', command=self.deleteCarFrame, width=15)
        self.deleteCarButton.config(font=("Tahoma", 10))
        self.deleteCarButton.grid(row=0,column=3)
    #}

    ##-----------------------------------------------------------------------------
    ## Collects info from entries and sends back to config UI
    ##-----------------------------------------------------------------------------
    def saveCarSettings(self): #{
        self.car.carName = self.carNameEntry.get()
        self.car.IP = self.IPEntry.get()
        self.car.port = self.portEntry.get()

        self.parent.updateCarFrame(self.car)

        self.destroyWindow()
    #}

    ##-----------------------------------------------------------------------------
    ## Sends back the car frame to delete
    ##-----------------------------------------------------------------------------
    def deleteCarFrame(self): #{
        self.parent.deleteCarFrame(self.car)
        self.destroyWindow()
    #}

    ##-----------------------------------------------------------------------------
    ## Deletes the editCar Window
    ##-----------------------------------------------------------------------------
    def destroyWindow(self): #{
        try:
            self.window.destroy()
        except:
            print('Error destroying editCar UI')
    #}
#}

















