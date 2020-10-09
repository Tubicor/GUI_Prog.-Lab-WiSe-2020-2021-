import tkinter
import turtle
import math

class Main:
    def __init__(self):


        #Root
        window = tkinter.Tk() # Create a window
        window.title("Lissajou Number") # Set a title
        #Containers
        drawFrame = tkinter.Frame(bg='blue',width=100,height=100,pady=3);
        controlFrame = tkinter.Frame(bg='red',width=100,height=100,pady=3);
        #layout of main Containers
        window.grid_rowconfigure(1,weight=1)
        window.grid_columnconfigure(0,weight=1)

        drawFrame.grid(column=0,row=0,sticky="ew")
        controlFrame.grid(column=1,row=0,sticky="sewn")
        #widgets and layout
        startButton = tkinter.Button(master=controlFrame,text="grow Tree")
        startButton.grid(column=0)

        canvas = tkinter.Canvas(master=drawFrame,width =60, height = 60,bg="white")
        canvas.grid(column=0)


        #source https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid
        #frame1 = tkinter.Frame(window) # Create and add a frame to window for the Scales
        '''
        pen = turtle.RawTurtle(canvas)
        pen.speed(10)
        pen.color('white','white')
        a,b,c = 1,1,1
        d,e,f = 1,2,1
        for i in (x * 0.2 for x in range(0, 1000)):
            y = a*math.cos(b*i)
            x = c*math.sin(d*i)
            print(" {} | {}".format(x,y))
            pen.goto(x*200,y*200)
            pen.color('black','black')
        '''
        #Scales
        """
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
        """




        window.mainloop() # Create an event loop*
    '''
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
    '''
Main()
