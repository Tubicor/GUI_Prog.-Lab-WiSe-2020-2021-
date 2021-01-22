import variables
import tkinter as tk
from tkinter import font as tkFont
import pygame


def controlWindow():
    controller = Controller()
    controller.loop()


class Controller():
    def __init__(self):        
        self.root = tk.Tk()        
        self.speedVar = tk.DoubleVar()
        self.radioVar = tk.IntVar()
      

        self.radioFrame = tk.Frame(master=self.root);
        self.radioFrame.grid()
        r1 = tk.Radiobutton(self.radioFrame,text=variables.AVAILABLEMODES[0],variable =self.radioVar,value=0, command=self.setMode)
        r1.grid()
        r2 = tk.Radiobutton(self.radioFrame,text=variables.AVAILABLEMODES[1],variable =self.radioVar,value=1, command=self.setMode)
        r2.grid()
        r3 = tk.Radiobutton(self.radioFrame,text=variables.AVAILABLEMODES[2],variable =self.radioVar,value=2, command=self.setMode)
        r3.grid()

        self.navButtonFrame = tk.Frame(master=self.root)
        self.navButtonFrame.grid(row=0,column=2)
        up = tk.Button(self.navButtonFrame,text="^",font=("Arial", 25),command = lambda :pygame.event.post(pygame.event.Event(variables.BUTTONUP)))
        up.grid(row=0,column=1)
        left = tk.Button(self.navButtonFrame,text="<",font=("Arial", 25),command = lambda :pygame.event.post(pygame.event.Event(variables.BUTTONLEFT)))
        left.grid(row=1,column=0)
        middle = tk.Button(self.navButtonFrame,text="0",font=("Arial", 25),command = lambda :pygame.event.post(pygame.event.Event(variables.BUTTONMIDDLE)))
        middle.grid(row=1,column=1)
        right = tk.Button(self.navButtonFrame,text=">",font=("Arial", 25),command = lambda :pygame.event.post(pygame.event.Event(variables.BUTTONRIGHT)))
        right.grid(row=1,column=2)
        down = tk.Button(self.navButtonFrame,text="v",font=("Arial", 25),command = lambda :pygame.event.post(pygame.event.Event(variables.BUTTONDOWN)))
        down.grid(row=2,column=1)

        self.sliderFrame = tk.Frame(master= self.root)
        self.sliderFrame.columnconfigure(0,minsize=200)
        self.sliderFrame.columnconfigure(1,minsize=100)
        self.sliderFrame.columnconfigure(2,minsize=200)
        self.sliderFrame.grid(columnspan=2)
        self.speedLabel = tk.Label(master=self.sliderFrame,text="Speed : 0",font=("Arial", 16))
        self.speedLabel.grid(row=0)
        self.speedSlider = tk.Scale(master=self.sliderFrame,length = 300,variable = self.speedVar, from_=0,showvalue =0,to=variables.MAXSPEED,resolution =0.1,orient=tk.VERTICAL,command=self.calcRPMandGear)
        self.speedSlider.grid(row=1)
        self.fuelLable = tk.Label(master=self.sliderFrame,text="Fuel : 0%",font=("Arial", 16))
        self.fuelLable.grid(column=1,row=0)
        self.fuelSlider = tk.Scale(master=self.sliderFrame,length = 300, from_=0,showvalue =0,to=variables.MAXFUEL,resolution =1,orient=tk.VERTICAL,command=self.variables)
        self.fuelSlider.set(100)
        self.fuelSlider.grid(column=1,row=1)
        self.engineTemperatureLable = tk.Label(master=self.sliderFrame,text="engineTemp : 0 C",font=("Arial", 16))
        self.engineTemperatureLable.grid(column=2,row=0)
        self.engineTemperatureSlider = tk.Scale(master=self.sliderFrame,length = 300, from_=0,showvalue =0,to=variables.MAXTEMP,resolution =1,orient=tk.VERTICAL,command=self.variables)
        self.engineTemperatureSlider.grid(column=2,row=1)
        
        self.neutralButton = tk.Button(master=self.root,text="Neutral Gear",command=self.neutral)
        self.neutralButton.grid(column=1,row=0)
    def loop(self):
        tk.mainloop()

        #called everytime anthing changes so all Lables and variables are refreshed
    def variables(self,event=None):
        variables.speed = (self.speedVar.get())**2/variables.MAXSPEED
        variables.fuel = self.fuelSlider.get()
        variables.engineTemperature = self.engineTemperatureSlider.get()
        self.speedLabel["text"] = "Speed : {}".format(int(variables.speed))
        self.fuelLable["text"] = "Fuel : {}%".format(int(variables.fuel/variables.MAXFUEL*100))
        self.engineTemperatureLable["text"] = "engineTemp : {} C".format(int(variables.engineTemperature))
        self.radioVar.set( variables.AVAILABLEMODES.index(variables.mode))

    def calcRPMandGear(self,event=None):
        self.variables()
        nRPM = variables.IDLERPM
        mode = 0
        if(variables.mode == "eco"):
            mode = 3/10
        elif(variables.mode == "normal"):
            mode = 1/2
        elif(variables.mode == "sport"):
            mode = 7/10
        else:
            raise Exception("missing Mode")
        if(variables.speed <= 0):
            variables.rpm = nRPM 
            variables.gear = "N"
        elif(variables.speed <= 10):
            variables.rpm = nRPM + variables.MAXRPM*mode*(variables.speed/10)
            variables.gear = "1"
        elif(variables.speed <= 30):
            variables.rpm = nRPM + variables.MAXRPM*mode*((variables.speed-10)/20)
            variables.gear = "2"
        elif(variables.speed <= 50):
            variables.rpm = nRPM + variables.MAXRPM*mode*((variables.speed-30)/20)
            variables.gear = "3"
        elif(variables.speed <= 80):
            variables.rpm = nRPM + variables.MAXRPM*mode*((variables.speed-50)/30)
            variables.gear = "4"
        elif(variables.speed <= 130):
            variables.rpm = nRPM + variables.MAXRPM*mode*((variables.speed-80)/50)
            variables.gear = "5"
        elif(variables.speed ):
            variables.rpm = nRPM + variables.MAXRPM*((variables.speed-130)/120)
            variables.gear = "6"   
    def neutral(self):        
        variables.rpm = variables.IDLERPM
        variables.gear = "N"
        self.neutralButton["state"] = "disable"
        self.neutralRepeat()
    def neutralRepeat(self):
        if(variables.gear == "N" and variables.speed >= 0):
            self.neutralButton.after(100,self.neutralRepeat)
            self.speedVar.set(self.speedVar.get()-1.2)
            self.variables()
        else:
            self.neutralButton["state"] = "normal"
    def setMode(self):
        variables.mode = variables.AVAILABLEMODES[self.radioVar.get()]
        self.calcRPMandGear();
        
if __name__ == "__main__":
    controlWindow()