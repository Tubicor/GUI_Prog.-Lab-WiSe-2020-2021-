import pygame
import pygame.freetype

MAXSPEED = 250
MAXRPM = 5300
IDLERPM = 300
MAXFUEL = 60
MAXTEMP = 130
MINTEMP = 50
AVAILABLEMODES =[
    "eco", "normal", "sport",
    ]
BUTTONUP = pygame.USEREVENT+1
BUTTONRIGHT = pygame.USEREVENT+2
BUTTONDOWN = pygame.USEREVENT+3
BUTTONLEFT = pygame.USEREVENT+4
BUTTONMIDDLE = pygame.USEREVENT+5
SECOUND = pygame.USEREVENT+100
#https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
FONTBIG = ('Arial',120)
FONTMEDIUM = ('Arial',60)
FONTSMALL = ('Arial',30)
FONTVERYSMALL= ('Arial',20)
WHITE = (255,255,255)
GREEN = (0,255,0)
GREY = (50,50,50)


speed = 0
rpm = 0
gear = "N"
fuel = 0
engineTemperature = 50
outsideTemperature = 10
carTemperature = 25
battery = 14.5
trip = 0
totalKM = 66600
lights = [False,False]  #[Front,Rear]
turnLights = "out"      #possible = out, left, right, bothBlinking
doors = [False,False,False]#False = door shut | [Driver Door, Co-Driver Door, Tailgate]
mode = AVAILABLEMODES[0]
tirePressure = [2.5,2.5,2.8,2.8] # LeftFront - RightFront LeftRear RightRear