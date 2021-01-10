import variables
import pygame
import math 
from monitors import MultiMediaMonitor
from itertools import cycle

class RotatingImage():
    def __init__(self,x,y,angle,pivotX,pivotY,image):
        self.imgPLine = image
        self.pos =(x,y)
        self.delta = (0,0)
        self.origin =(x,y)
        self.angle = angle
        #Define a pivot and calcualte the translation of the rotated pivot
        self.pivot = pygame.math.Vector2(pivotX,pivotY)
    def rotate(self,angle):     
        #Set up a list with the 4 corner points of the bounding box
        w, h = self.imgPLine.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        #Rotate the vectors to the corner points
        box_rotate = [p.rotate(angle) for p in box]
        #Get the minimum and the maximum of the rotated points
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        
        ##self.pivot = (self.pos[0] + pivot.x,self.pos[1] - pivot.y)
        pivot_rotate = self.pivot.rotate(angle)
        pivot_move   = pivot_rotate - self.pivot

        self.origin = (self.pos[0]+self.delta[0] + min_box[0] - pivot_move[0], self.pos[1]+self.delta[1] - max_box[1] + pivot_move[1])
        return  pygame.transform.rotate(self.imgPLine, angle)
   
    def draw(self,screen):  
        screen.blit(self.rotate(-self.angle),self.origin)
        #pygame.draw.rect(screen, (255, 0, 0), (*self.origin, *self.rotate(self.angle).get_size()),2)
        #pygame.draw.circle(screen, (0, 255, 0),(int(self.pos[0]+self.pivot[0]),int(self.pos[1]+self.pivot[1])), 10, 0)
class Fader:

    def __init__(self, scenes):
        self.scenes = cycle(scenes)
        self.scene = next(self.scenes)
        self.fading = None
        self.alpha = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)
        self.veil.fill((0, 0, 0))

    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self, screen):
        self.scene.draw(screen)
        if self.fading:
            self.veil.set_alpha(self.alpha)
            screen.blit(self.veil, (0, 0))

    def update(self, dt, events):
        self.scene.update(dt, events)

        if self.fading == 'OUT':
            self.alpha += 8
            self.scene.tY += 8
            if self.alpha >= 255:
                self.fading = 'IN'
                self.scene.tY = 0
                self.scene = next(self.scenes)
                self.scene.tY = 255
        elif self.fading == 'IN':
            self.alpha -= 8
            self.scene.tY -= 8
            if self.alpha <= 0:
                self.fading = None

class DriveScene():
    def __init__(self):
        self.tX = 0
        self.tY = 0
        self.background = pygame.image.load("Assets\Background_Neu.png")
        self.textSmallFont = pygame.freetype.SysFont(variables.FONTSMALL[0],variables.FONTSMALL[1])
        self.textMediumFont = pygame.freetype.SysFont(variables.FONTMEDIUM[0],variables.FONTMEDIUM[1])
        self.gear = variables.gear
        self.textGear = "Gear"
        self.averageSpeed = 0;
        self.countedSpeed = 0;

        #Meter Pointer
        self.sPointer = RotatingImage(74,230,0,177,-30,pygame.image.load("Assets\Anzeiger_Neu.png"))
        self.rPointer = RotatingImage(958,230,0,177,-30,pygame.image.load("Assets\Anzeiger_Neu.png"))
        #Fuel Meter
        self.fMeter  =RotatingImage(21,300,0,235,35,pygame.image.load("Assets\MeterFuel.png"))
        self.tempMeter  =RotatingImage(901,300,0,235,35,pygame.image.load("Assets\MeterFuel.png"))
        
        self.mmMonitor = MultiMediaMonitor(555,40,270,450,20)

    def draw(self,screen):
        #update Position is not in updateFunction since it only is important to drawing
        self.sPointer.delta = (self.tX,self.tY)
        self.rPointer.delta = (self.tX,self.tY)
        self.fMeter.delta = (self.tX,self.tY)
        self.tempMeter.delta = (self.tX,self.tY)

        self.fMeter.draw(screen)
        self.tempMeter.draw(screen)
        screen.blit(self.background,(self.tX+0,self.tY+0))
        self.sPointer.draw(screen)
        self.rPointer.draw(screen)
        self.textMediumFont.render_to(screen,(self.tX+870,self.tY+460),self.gear,variables.WHITE,style=pygame.freetype.STYLE_STRONG)
        self.textSmallFont.render_to(screen,(self.tX+840,self.tY+430),self.textGear,variables.WHITE)
        self.mmMonitor.draw(screen)

    def update(self, dt, events):        
        self.sPointer.angle = 4 + 360*45/40*(variables.speed/variables.MAXSPEED)
        if(self.sPointer.angle > 97.5):#different scale start at 100kmh
             self.sPointer.angle = 4 + 97.5 + 360*45/80*((variables.speed-60)/variables.MAXSPEED)
        self.rPointer.angle = 3 + 360*6/10*(variables.rpm/variables.MAXRPM)
        self.fMeter.angle = 112 - 64*(variables.fuel/variables.MAXFUEL);
        if(variables.temp > variables.MINTEMP +2):
            self.tempMeter.angle = 113 - 65*((variables.temp-variables.MINTEMP)/(variables.MAXTEMP-variables.MINTEMP))
        else:
            self.tempMeter.angle = 111
        self.gear = variables.gear
        self.mmMonitor.update(dt,events)

class MultimediaScene:
    def __init__(self):       
        self.tX = 0
        self.tY = 0
        self.background = None


    def update(self):
        pass
    def draw(self,screen):
        if( not self.background == None):
            screen.blit(self.background,(self.tX+0,self.tY+0))
        


def display():    
    screen = pygame.display.set_mode((1383,522))
    pygame.display.set_caption("Driver Display")
    clock = pygame.time.Clock()
    dt = 0
    pygame.init()
    fader = Fader([DriveScene()])

    #Timer for calculating Trip in variables
    pygame.time.set_timer(variables.SECOUND,1000)
    while True:
        dt = clock.tick(60)
        screen.fill((0,0,0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                fader.next()
            if event.type == variables.SECOUND:
                #approx. adding driven distance in one secound
                variables.trip += variables.speed / 3.6 /1000
                pygame.time.set_timer(variables.SECOUND,1000)

        fader.draw(screen)
        fader.update(dt,events)
        pygame.display.update()


if __name__ == "__main__":
    display()


#Icons by Freepik