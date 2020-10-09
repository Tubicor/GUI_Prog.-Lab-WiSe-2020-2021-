from tkinter import * # Import tkinter
import math

class Main:
    def __init__(self):
        window = Tk() # Create a window
        window.title("Lissajou Number") # Set a title
        self.width = 800
        self.height = 800

        #self.degreeToRadiant = 0.0174533 # ~1Grad in Bogenmaß
        self.canvas = Canvas(window,width = self.width, height = self.height,bg="white")
        self.canvas.pack()

        frame1 = Frame(window) # Create and add a frame to window
        frame1.pack()


        #Scales
        '''
        self.angleScale = Scale(frame1, from_=0, to=180, orient=VERTICAL,labe="angel between branches",resolution=5)
        self.angleScale.pack(side = LEFT)
        self.angleScale.set(30)
        #sizeFactor
        self.sFScale = Scale(frame1, from_=0.5, to=0.9, orient=VERTICAL,labe="sizeFac",resolution=0.05)
        self.sFScale.pack(side = LEFT)
        self.sFScale.set(0.75)
        #Startsize
        self.sSizeScale = Scale(frame1, from_=0, to=130, orient=VERTICAL,labe="startSize",resolution=5)
        self.sSizeScale.pack(side = LEFT)
        self.sSizeScale.set(130)
        #Number of Branches
        self.numOfBranches = Scale(frame1, from_=1, to=5, orient=VERTICAL,labe="Number of Branches",resolution=1)
        self.numOfBranches.pack(side = LEFT)
        self.numOfBranches.set(4)
        '''
        #Button
        Button(frame1,text="grow Tree",command=self.display).pack(side = LEFT)
        self.display
        window.mainloop() # Create an event loop*

    def drawLine(self,breite, x1,y1, x2,y2):
        self.canvas.create_line(x1,y1, x2,y2, tags = "line",width=breite)

    def display(self):
        self.canvas.delete("line")
        self.bFac = 1.8/self.numOfBranches.get()
        breite =self.sSizeScale.get()/6
        return self.paintBranch(breite,self.width/2, self.height, self.sSizeScale.get(), math.pi/2,1)

    def paintBranch(self,breite, x1, y1, length, angle,counter):
        if length >= 1 and counter < 15-(self.numOfBranches.get()*1.5) :
            x2 = x1 + int(math.cos(angle) * length)
            y2 = y1 - int(math.sin(angle) * length)
            breite2 = breite*self.bFac
            #linkester Ast = abstand zwischen Branches*(anzahl Branches -1)/2
            leftestBranch = angle + self.angleScale.get()*self.degreeToRadiant*(self.numOfBranches.get()-1)/2
            # Draw the line
            self.drawLine(breite,x1,y1, x2,y2)
            for x in range(1, self.numOfBranches.get()+1):
                self.paintBranch(breite2, x2, y2, length * self.sFScale.get(), leftestBranch,counter+1)
                leftestBranch = leftestBranch - self.angleScale.get()*self.degreeToRadiant
Main()
