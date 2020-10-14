import tkinter
import Drawer

class Main:
    def __init__(self):
        #Variables
        #Root
        window = tkinter.Tk() # Create a window
        window.title("Lissajou Number") # Set a title
        #Containers
        drawFrame = tkinter.Frame(bg='blue',width=620,height=620,pady=3);
        controlFrame = tkinter.Frame(bg='red',width=100,height=100,pady=3);
        #layout of main Containers
        window.grid_rowconfigure(1,weight=1)
        window.grid_columnconfigure(0,weight=1)
        drawFrame.grid(column=0,row=0,sticky="ew")
        controlFrame.grid(column=1,row=0,sticky="sewn")
        #widgets and layout
            #canvas to show on
        canvas = tkinter.Canvas(master=drawFrame,bg="white",width=600,height=600)
        canvas.grid(column=0)
            #Label """a*sin(b*t+c) = d*cos(e*t+f)"""
        label = tkinter.Label(master=controlFrame,text="a*sin(b*t+c) = d*cos(e*t+f)")
        label.grid(column=0)
        """    #startButton
        startButton = tkinter.Button(master=controlFrame,text="grow Tree",command= lambda: self.drawLissajou(canvas,label,scales))
        startButton.grid(column=0)"""
            #Scale from a-f
        scales = [None]*10
        scaleNames = ["a","b","c","d","e","f"]
        for i in range(1,7):
            print(i)
            #Scale
            scale = tkinter.Scale(master=controlFrame, from_=0, to=3,orient=tkinter.HORIZONTAL,label=scaleNames[i-1],resolution=0.1,activebackground='blue' )#highlightcolor='red',highlightbackground='blue',relief=tkinter.FLAT,),command= lambda: print("test"))
            scale.bind("<ButtonRelease-1>", lambda event: self.drawLissajou(canvas,label,scales))
            scale.grid(column=0)
            scale.set(i*0.3)
            scales[i-1]=scale

        window.mainloop() # Create an event loop*

    def hello(self):
        print("hello")

    def labelRefresh(self,label,scales):
        print("label labelRefresh")
        label['text'] = "{}*sin({}*t+{}) = {}*cos({}*t+{})".format(scales[0],scales[1],scales[2],scales[3],scales[4],scales[5])

    def drawLissajou(self,canvas,label,scales):
        #stop the Draw
        Drawer.Draw.drawNr += 1
        #getting Values from Scales
        sValues =[None]*6
        for i in range(0,6):
            sValues[i] = scales[i].get()
        #refresh the lable
        self.labelRefresh(label,sValues)
        #start drawing
        drawer = Drawer.Draw(canvas,label,sValues)

Main()


#source https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid
