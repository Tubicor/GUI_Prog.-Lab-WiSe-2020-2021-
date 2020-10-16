import tkinter
import Drawer

class Main:
    def __init__(self):
        #Variables
        #Root
        window = tkinter.Tk() # Create a window
        window.title("Lissajou Number") # Set a title
        #Containers
        drawFrame = tkinter.Frame(master=window,bg='blue',width=620,height=620,pady=3);
        uiFrame = tkinter.Frame(master=window,bg='black',width=100,height=100,pady=3);
        controlFrame = tkinter.Frame(master=uiFrame,bg='black',width=100,height=100,pady=3);
        eqFrame = tkinter.Frame(master=uiFrame,bg='white')
        #layout of main Containers
        window.grid_rowconfigure(1,weight=1)
        window.grid_columnconfigure(0,weight=1)
        drawFrame.grid(column=0,row=0,sticky="ew")
        uiFrame.grid(column=1,row=0,sticky="sewn")
        eqFrame.grid(column=0,sticky="nw")
        controlFrame.grid(column=0,row=1,sticky="sewn")
        ## TODO:
        scaleNames = ["a","b","c","d","e","f"]
        scaleColors = ['red','orange','yellow','green','cyan','blue']
        #widgets and layout
            #canvas to show on
        canvas = tkinter.Canvas(master=drawFrame,bg="white",width=600,height=600)
        canvas.grid(column=0)
            #Label for equation
        labels = [None]*6
        textSnip = ["y = ","*sin(","*t+",")","x = ","*cos(","*t+",")"]
        #x row
        for i in range(0,3):
            text = tkinter.Label(master=eqFrame,text=textSnip[i],font=("Arial",20),bg="white")
            text.grid(row=0,column=i*2)
            labels[i] = tkinter.Label(master=eqFrame,text=scaleNames[i],font=("Arial",20),fg=scaleColors[i],bg="white")
            labels[i].grid(row=0,column=i*2+1)
        text = tkinter.Label(master=eqFrame,text=textSnip[3],font=("Arial",20),bg="white")
        text.grid(row=0,column=6)
        #y row
        for i in range(0,3):
            text = tkinter.Label(master=eqFrame,text=textSnip[i+4],font=("Arial",20),bg="white")
            text.grid(row=1,column=i*2)
            labels[i+3] = tkinter.Label(master=eqFrame,text=scaleNames[i+3],font=("Arial",20),fg=scaleColors[i+3],bg="white")
            labels[i+3].grid(row=1,column=i*2+1)
        text = tkinter.Label(master=eqFrame,text=textSnip[7],font=("Arial",20),bg="white")
        text.grid(row=1,column=6)
            #Scale from a-f
        scales = [None]*10

        for i in range(1,7):
            print(i)
            #lable

            labelVar = tkinter.Label(master=controlFrame,text=scaleNames[i-1],fg=scaleColors[i-1],bd=5,bg='black',font=("Arial", 44))
            labelVar.grid(column=0,row=i)
            #Scale
            scale = tkinter.Scale(length= 150,sliderlength=40,master=controlFrame, from_=0, to=3,orient=tkinter.HORIZONTAL,resolution=0.1,bg=scaleColors[i-1])#highlightcolor='red',highlightbackground='blue',relief=tkinter.FLAT,),command= lambda: print("test"))
            scale.bind("<ButtonRelease-1>", lambda event: self.drawLissajou(canvas,labels,scales))
            scale.grid(column=1,row=i)
            scale.set(i*0.3)
            scales[i-1]=scale

        window.mainloop() # Create an event loop*

    def hello(self):
        print("hello")

    def labelRefresh(self,labels,scales):
        print("label labelRefresh")
        for i in range(0,6):
            labels[i]['text'] = scales[i]
        #label['text'] = "{}*sin({}*t+{}) = {}*cos({}*t+{})".format(scales[0],scales[1],scales[2],scales[3],scales[4],scales[5])

    def drawLissajou(self,canvas,labels,scales):
        #stop the Draw
        Drawer.Draw.drawNr += 1
        #getting Values from Scales
        sValues =[None]*6
        for i in range(0,6):
            sValues[i] = scales[i].get()
        #refresh the lable
        self.labelRefresh(labels,sValues)
        #start drawing
        drawer = Drawer.Draw(canvas,sValues)

Main()


#source https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid
