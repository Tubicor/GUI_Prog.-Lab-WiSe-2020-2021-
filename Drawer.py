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

        for i in (x * 0.1 for x in range(0, 800)):
            y = scales[0]*math.sin(scales[1]*i+scales[2])
            x = scales[3]*math.cos(scales[4]*i+scales[5])
            #print(" {} | {}".format(x,y))
            if self.nr != Draw.drawNr:
                #print("break")
                break
            pen.goto(x*100,y*100)
            pen.color('black','black')
        #print("end draw")
