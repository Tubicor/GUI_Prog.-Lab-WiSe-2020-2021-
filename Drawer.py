import turtle
import math
import tkinter

class Draw:
    drawNr = 0
    def __init__(self,canvas,scales):
        #Variables
        self.nr = Draw.drawNr
        #Init turtle
        pen = turtle.RawTurtle(canvas)
        pen.speed(0)
        pen.color('white','white')
        pen.goto(0,0)
        canvas.delete("all")
        self.drawAxis(canvas)
        smalT = scales[4]
        if scales[1]>scales[4]:
            smalT=scales[1]
        print("test")
        print(0.1/smalT)
        for i in (x * 0.13/smalT for x in range(0, 500*(int(smalT)+1))):
            y = -scales[0]*math.sin(scales[1]*i+scales[2])
            x = scales[3]*math.cos(scales[4]*i+scales[5])
            #print(" {} | {}".format(x,y))
            if self.nr != Draw.drawNr:
                #print("break")
                break
            pen.goto(x*100,y*100)
            pen.color('black','black')
        #print("end draw")

    def drawAxis(self,canvas):
        # draw x and y axes
        canvas.create_line(-300,300,-300,-300,width=2)

        canvas.create_line(-300,300,300,300,width=2)
        #canvas.create_line(10,10,10,610,width=2)

        # markings on x axis
        for i in range(16):
            x = (i * 40)-300
            canvas.create_line(x,300,x,310, width=2)
            canvas.create_text(x,314, text=(x/100.0))
        canvas.create_text(310,300,text="x",font=("Arial",14))
        # markings on y axis
        for i in range(16):
            y = (i * 40)-300
            canvas.create_line(-300,y,-310,y, width=2)
            canvas.create_text(-314,y-10,text=(-y/100.0))
        canvas.create_text(-300,-315,text="y",font=("Arial",14))
