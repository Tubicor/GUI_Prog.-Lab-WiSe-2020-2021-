import variables
import pygame
import pygame.freetype
from datetime import datetime

blockFaderMMM = False
#TODO Adopt moving of parent Display
#every Text  in one class for readabillity 
#change constant Events to named Event

class MultiMediaMonitor(object):
    def __init__(self,x,y,width,height,border_radius):
        self.textSmallFont = pygame.freetype.SysFont(variables.FONTVERYSMALL[0],variables.FONTVERYSMALL[1]+5)
        self.rect: pygame.rect.Rect = pygame.rect.Rect(x,y,width,height)
        self.color = pygame.color.Color(0,0,0)
        self.border_radius = border_radius
        self.veil = pygame.Surface(self.rect.size) 
        self.veil.fill((0,0,0))
        self.alpha = 0

        self.fading = None
        self.continousBehaivor = 'Next'

        self.monitors = [StatsMonitor(Rect=self.rect),MusicMonitor(Rect=self.rect),SpeedMonitor(Rect=self.rect)]
        self.iterator = 0

        self.textTime = str(datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        self.textTimeRect = self.textSmallFont.get_rect(self.textTime)
        self.textTimeRect.center = (self.rect.midtop[0],self.rect.midtop[1]+25)

        

    def next(self):
        if not self.fading:
            self.continousBehaivor = 'Next'
            self.fading ='OUT'
            self.alpha = 0

    def previous(self):
        if not self.fading:
            self.continousBehaivor = 'Prev'
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self,screen):        
        pygame.draw.rect(screen,self.color,self.rect,border_radius=self.border_radius)

        self.monitors[self.iterator].draw(screen)
        if self.fading:
            self.veil.set_alpha(self.alpha)
            screen.blit(self.veil,(self.rect.x,self.rect.y))        
        
        self.textSmallFont.render_to(screen,self.textTimeRect,self.textTime,variables.WHITE)

    def update(self,dt,events):
        global blockFaderMMM
        for event in events:
            if event.type == variables.BUTTONUP and not blockFaderMMM:
                self.previous()
            if event.type == variables.BUTTONDOWN and not blockFaderMMM:
                print("fading")
                self.next()
            if event.type == variables.SECOUND:
                self.textTime = str(datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
                self.textTimeRect = self.textSmallFont.get_rect(self.textTime)
                self.textTimeRect.center = (self.rect.midtop[0],self.rect.midtop[1]+25)

        self.monitors[self.iterator].update(dt,events)

        if self.fading == 'OUT':
            self.alpha += 8
            #self.scene.tY += 8
            if self.alpha >= 255:
                self.fading = 'IN'
                #self.scene.tY = 0
                if(self.continousBehaivor == 'Next'):
                    self.iterator += 1
                    if self.iterator >= len(self.monitors):
                        self.iterator = 0
                elif(self.continousBehaivor == 'Prev'):
                    self.iterator -= 1
                    if self.iterator < 0:
                        self.iterator = len(self.monitors)-1
                #self.scene.tY = 255
        elif self.fading == 'IN':
            self.alpha -= 8
            #self.scene.tY -= 8
            if self.alpha <= 0:
                self.fading = None
        

        
class Monitor():
    def __init__(self,*args,**kwargs):

        self._mmmRect = kwargs.get("Rect")
        self._center = self._mmmRect .center
        
        self.textVerySmallFont = pygame.freetype.SysFont(variables.FONTVERYSMALL[0],variables.FONTVERYSMALL[1])
        self.textSmallFont = pygame.freetype.SysFont(variables.FONTSMALL[0],variables.FONTSMALL[1])
        self.textMediumFont = pygame.freetype.SysFont(variables.FONTMEDIUM[0],variables.FONTMEDIUM[1])        
        self.textBigFont = pygame.freetype.SysFont(variables.FONTBIG[0],variables.FONTBIG[1])
        
        pass
    def draw(self,screen):
        pass
    def update(self,dt,events):
        pass

class MusicMonitor(Monitor):
    def __init__(self,*args,**kwargs):        
        super().__init__(*args,**kwargs)
        songs = ["Billy Talent-White Sparrows-3'12","Guns N' Roses-Paradise City-5'12",
                 "HI! Spencer-Nicht raus aber weiter-4'03","Highly Suspect-My Name Is Human-5'02",
                 "Metallica-Moth into the Flame-4'21","Razz-Let it in,Let it out-3'46",
                 "The Beatles-Hey Jude-3'32"]
        self.songPictures = []
        self.songNames = []
        self.songArtists = []
        self.songDurations = []
        for song in songs:
            picture = pygame.image.load("Assets\Music\Songs\{}.jpg".format(song))
            picture = pygame.transform.scale(picture,(160,160))
            pictureRect = picture.get_rect()
            self.songPictures += [[picture,pictureRect]] # not smart just need one rect for left one for middle and one for right
            songSplit = song.split("-")
            self.songArtists += [songSplit[0]]
            self.songNames += [songSplit[1]]
            self.songDurations += [int(songSplit[2].replace("'",""))]
        self.iterator= 0
        
        self.playing=False
        self.playDur = 0
        self.lastPlayTime = 0

        self.textSongName = self.songNames[self.iterator]
        self.textSongNameRect =self.textVerySmallFont.get_rect(self.textSongName)
        self.textSongNameRect.center = (self._center[0],self._center[1]+15)

        self.textArtist = self.songArtists[self.iterator]
        self.textArtistRect =self.textVerySmallFont.get_rect(self.textArtist)
        self.textArtistRect.midtop = (self._center[0],self._center[1]+28)

        self.playImage = pygame.image.load("Assets\Music\MusicPlay.png")
        self.playImage = pygame.transform.scale(self.playImage,(75,75))
        self.playImageRect = self.playImage.get_rect()
        self.playImageRect.center = (self._center[0],self._center[1]+95)

        self.pauseImage = pygame.image.load("Assets\Music\MusicPause.png")
        self.pauseImage = pygame.transform.scale(self.pauseImage,(75,75))
        self.pauseImageRect = self.playImageRect.copy()

        self.nextImageCounter = 0
        self.pressedNext = False
        self.nextImage = pygame.image.load("Assets\Music\MusicNext.png")
        self.nextImage = pygame.transform.scale(self.nextImage,(55,55))
        self.nextImageRect = self.nextImage.get_rect()
        self.nextImageRect.midleft = (self.playImageRect.midright[0] +10,self.playImageRect.midright[1])

        self.prevImageCounter = 0
        self.pressedPrev = False
        self.prevImage = pygame.image.load("Assets\Music\MusicNext.png")
        self.prevImage = pygame.transform.scale(self.prevImage,(55,55))
        self.prevImage = pygame.transform.rotate(self.prevImage,180)
        self.prevImageRect = self.prevImage.get_rect()
        self.prevImageRect.midright = (self.playImageRect.midleft[0] -10,self.playImageRect.midleft[1])

        

        self.progressBarRect = pygame.rect.Rect(0,0,self._mmmRect.width-50,7)
        self.progressBarRect.midleft = (self._mmmRect.midleft[0]+25,self._center[1]+150)
        self.progressBarGreenRect = self.progressBarRect.copy()
        self.progressBarGreenRect.width = 50

        self.textPlayDur = str(int(self.playDur)).zfill(3)
        self.textPlayDur = self.textPlayDur[:1]+":"+self.textPlayDur[1:]
        self.textPlayDurRect = self.textVerySmallFont.get_rect(self.textPlayDur)
        self.textPlayDurRect.topleft = (self.progressBarRect.bottomleft[0],self.progressBarRect.bottomleft[1]+5)
        
        self.textTotalDur = str(self.songDurations[self.iterator])
        self.textTotalDur = self.textTotalDur[:1]+":"+self.textTotalDur[1:]
        self.textTotalDurRect = self.textVerySmallFont.get_rect(self.textTotalDur)
        self.textTotalDurRect.topright = (self.progressBarRect.bottomright[0],self.progressBarRect.bottomright[1]+5)

    def draw(self, screen):
        #left picture
        if(self.iterator-1 >= 0):            
            leftPicture = pygame.transform.scale(self.songPictures[self.iterator-1][0],(120,120))
            leftPictureRect = leftPicture.get_rect()
            leftPictureRect.center = (self._center[0]-70,self._center[1]-80)
            screen.blit(leftPicture,leftPictureRect)
        #right picture
        if(self.iterator + 1 < len(self.songPictures)):
            rightPicture = pygame.transform.scale(self.songPictures[self.iterator+1][0],(120,120))
            rightPictureRect = rightPicture.get_rect()
            rightPictureRect.center = (self._center[0]+70,self._center[1]-80)
            screen.blit(rightPicture,rightPictureRect)
        #middle picture
        self.songPictures[self.iterator][1].center = (self._center[0],self._center[1]-80)
        screen.blit(self.songPictures[self.iterator][0],self.songPictures[self.iterator][1])
        #Song Title
        self.textVerySmallFont.render_to(screen,self.textArtistRect,self.textArtist,variables.WHITE)
        self.textVerySmallFont.render_to(screen,self.textSongNameRect,self.textSongName,variables.WHITE,style=pygame.freetype.STYLE_STRONG)
        # Steering
        if not self.playing:
            screen.blit(self.playImage,self.playImageRect)
        else:
            screen.blit(self.pauseImage,self.pauseImageRect)
        screen.blit(self.nextImage,self.nextImageRect)
        screen.blit(self.prevImage,self.prevImageRect)

        #progressbar
        pygame.draw.rect(screen,variables.WHITE,self.progressBarRect,border_radius=2)
        pygame.draw.rect(screen,variables.GREEN,self.progressBarGreenRect,border_radius=2)
        self.textVerySmallFont.render_to(screen,self.textPlayDurRect,self.textPlayDur,variables.GREEN)
        self.textVerySmallFont.render_to(screen,self.textTotalDurRect,self.textTotalDur,variables.WHITE)

        super().draw(screen)
    def update(self,dt,events):
        for event in events:
            if event.type == variables.BUTTONLEFT:
               self.prevSong()
               if(self.pressedPrev == False and self.prevImageCounter <= 0):
                self.pressedPrev = True
            if event.type == variables.BUTTONRIGHT:
               self.nextSong()
               if(self.pressedNext == False and self.nextImageCounter <= 0):
                self.pressedNext = True
            if event.type == variables.BUTTONMIDDLE:
               self.playing = not self.playing
            if event.type == variables.SECOUND:
               if self.playing :
                   self.advancePlay()
               else:
                   self.lastPlayTime = pygame.time.get_ticks()/1000

        if self.pressedPrev:
            self.prevImageCounter +=3;
            self.prevImageRect.left -=3;
            if self.prevImageCounter >12:
                self.pressedPrev = False
        elif self.prevImageCounter > 0:
            self.prevImageCounter -=3;
            self.prevImageRect.left +=3;

        if self.pressedNext:
            self.nextImageCounter +=3;
            self.nextImageRect.right +=3;
            if self.nextImageCounter >12:
                self.pressedNext = False
        elif self.nextImageCounter > 0:
            self.nextImageCounter -=3;
            self.nextImageRect.right -=3;

        self.textSongName = self.songNames[self.iterator]
        self.textSongNameRect =self.textVerySmallFont.get_rect(self.textSongName)
        self.textSongNameRect.center = (self._center[0],self._center[1]+15)

        self.textArtist = self.songArtists[self.iterator]
        self.textArtistRect =self.textVerySmallFont.get_rect(self.textArtist)
        self.textArtistRect.midtop = (self._center[0],self._center[1]+28)

        self.progressBarGreenRect.width = self.progressBarRect.width * (self.playDur/self.songDurations[self.iterator])
        self.textPlayDur = str(int(self.playDur)).zfill(3)
        self.textPlayDur = self.textPlayDur[:1]+":"+self.textPlayDur[1:]
        self.textTotalDur = str(self.songDurations[self.iterator])
        self.textTotalDur = self.textTotalDur[:1]+":"+self.textTotalDur[1:]
        

        super().update(dt,events)

    def advancePlay(self):
        advancedTime = pygame.time.get_ticks()/1000-self.lastPlayTime
        advancedTime = self.songDurations[self.iterator]-self.playDur-advancedTime
        while(advancedTime<0):
            self.nextSong()
            advancedTime +=self.songDurations[self.iterator]
        self.playDur = self.songDurations[self.iterator]-advancedTime
        self.lastPlayTime = pygame.time.get_ticks()/1000

    def nextSong(self):
        self.iterator +=1
        if(self.iterator >= len(self.songNames)):
                self.iterator = 0
        self.playDur = 0

    def prevSong(self):
        self.iterator -=1
        if(self.iterator < 0):
                self.iterator = len(self.songNames)-1
        self.playDur = 0

class SpeedMonitor(Monitor): 
    def __init__(self,*args,**kwargs):        
        super().__init__(*args,**kwargs)

        #Speed 
        self.speed = "0"        
        self.speedRect = self.textBigFont.get_rect(self.speed)
        self.speedRect.midbottom = (self._center[0],180)
        #Text - KM/H
        self.textKMH = "KM/H"
        self.textKMHRect = self.textVerySmallFont.get_rect(self.textKMH)
        self.textKMHRect.center = (self._center[0],190)
        #Trip 
        self.trip = f"{variables.trip:.1f}"
        self.tripRect = self.textMediumFont.get_rect(self.trip)
        self.tripRect.midtop = (self._center[0],340)
        #Text - Trip
        self.textTrip = "Trip :"
        self.textTripRect = self.textVerySmallFont.get_rect(self.textTrip)
        self.textTripRect.center = (self._center[0],325)
        #TotalKM
        self.totalKM = str(variables.totalKM+int(variables.trip))
        self.totalKMRect = self.textMediumFont.get_rect(self.totalKM)
        self.totalKMRect.midtop = (self._center[0],420)
        #Text - TotalKM
        self.textTotalKM = "Total Kilometers:"
        self.textTotalKMRect = self.textVerySmallFont.get_rect(self.textTotalKM)
        self.textTotalKMRect.center = (self._center[0],405)


    def draw(self, screen):  
        #Speed
        self.textBigFont.render_to(screen,self.speedRect,self.speed,variables.WHITE)  
        #Text - KM/H
        self.textVerySmallFont.render_to(screen,self.textKMHRect,self.textKMH,variables.WHITE,style=pygame.freetype.STYLE_OBLIQUE)
        #Trip
        self.textMediumFont.render_to(screen,self.tripRect,self.trip,variables.WHITE)
        #Text - Trip
        self.textVerySmallFont.render_to(screen,self.textTripRect,self.textTrip,variables.WHITE,style=pygame.freetype.STYLE_OBLIQUE)
        #TotalKM
        self.textMediumFont.render_to(screen,self.totalKMRect,self.totalKM,variables.WHITE)
        #Text - TotalKM
        self.textVerySmallFont.render_to(screen,self.textTotalKMRect,self.textTotalKM,variables.WHITE,style=pygame.freetype.STYLE_OBLIQUE)

        super().draw(screen)
    def update(self,dt,events):
        #Speed
        self.speed = str(int(variables.speed))        
        self.speedRect = self.textBigFont.get_rect(self.speed)
        self.speedRect.midbottom = (self._center[0],180)
        #Text - KM/H
        self.textKMHRect.center = (self._center[0],190)
        #Trip 
        self.trip = f"{variables.trip:.1f}"
        self.tripRect = self.textMediumFont.get_rect(self.trip)
        self.tripRect.midtop = (self._center[0],340)
        #Text - Trip
        self.textTripRect.center = (self._center[0],325)
        #TotalKM
        self.totalKM = str(variables.totalKM+int(variables.trip))
        self.totalKMRect = self.textMediumFont.get_rect(self.totalKM)
        self.totalKMRect.midtop = (self._center[0],420)
        #Text - TotalKM
        self.textTotalKMRect.center = (self._center[0],405)

        super().update(dt,events)

class StatsMonitor(Monitor):
    def __init__(self, *args, **kwargs):        
        super().__init__(*args,**kwargs)
        self.imageSetting = pygame.image.load("Assets\settings.png")
        self.imageSetting = pygame.transform.scale(self.imageSetting,(100,100))
        self.imageSettingRect = self.imageSetting.get_rect()
        self.imageSettingRect.center = (self._center[0],self._center[1]-120)
        self.menuRect = pygame.rect.Rect(self._mmmRect.topleft[0]+25,self._mmmRect.topleft[1]+180,self._mmmRect.width-50,self._mmmRect.height-237)
        self.menuItems = []
        
        iterator = 0
        for item in [">Mode",">Temperature",">Fuel",">Battery",">Tire Pressure"]:
            position = (self.menuRect.topleft[0]+20,self.menuRect.topleft[1]+15+40*iterator)
            rect = pygame.rect.Rect(0,0,200,35)
            rect.topleft = position[0],position[1]
            rect.left -=10
            rect.top -= 7
            self.menuItems += [[Text(lambda item=item:item,self.textSmallFont,position,align="Left",color=variables.WHITE),
                                rect]]
            iterator +=1
        self.insideMenu = False
        self.selectedItem = 0

    def draw(self, screen):
        screen.blit(self.imageSetting,self.imageSettingRect)                  
        color = variables.GREY
        colorMenu = variables.WHITE
        
        if(self.insideMenu):    
            color = variables.WHITE
            colorMenu = variables.GREY

        pygame.draw.rect(screen,colorMenu,self.menuRect,border_radius=2)
        #Draw a white line around if inside
        if self.insideMenu:
            pygame.draw.rect(screen,variables.WHITE,self.menuRect,2,border_radius=2) 
        
        iterator = 0
        for item in self.menuItems:            
            pygame.draw.rect(screen,color,item[1],border_radius=3)
            if self.insideMenu and self.selectedItem == iterator:                
                pygame.draw.rect(screen,colorMenu,item[1],border_radius=3)
            item[0].draw(screen)
            iterator +=1
            

        return super().draw(screen)
    def update(self, dt, events):
        global blockFaderMMM
        for event in events:
            if event.type == variables.BUTTONMIDDLE:
                self.insideMenu = True  
                blockFaderMMM = True
                self.selectedItem = 0
            if event.type == variables.BUTTONLEFT:
                self.insideMenu = False
                blockFaderMMM = False
            if event.type == variables.BUTTONDOWN:
                if self.insideMenu:
                    self.selectedItem+=1
                    if self.selectedItem>= len(self.menuItems):
                        self.selectedItem= 0
            if event.type == variables.BUTTONUP:
                if self.insideMenu:
                    self.selectedItem-= 1
                    if self.selectedItem<0:
                        self.selectedItem= len(self.menuItems)-1
        iterator = 0
        if self.insideMenu:
            for item in self.menuItems:
                item[0].color = variables.GREY
                if iterator == self.selectedItem:
                    item[0].color = variables.WHITE
                iterator += 1
        else:
            for item in self.menuItems:
                item[0].color = variables.WHITE
                iterator += 1
            
        return super().update(dt, events)

class Text:
    def __init__(self,textFunc,font,position,color=variables.WHITE,align="Center"):
        self.textFunc = textFunc
        self.font = font   
        self.position = position        
        self.color = color
        self.rect = self.font.get_rect(self.textFunc())
        self.align = align
        if self.align == "Left":
            self.rect.topleft = self.position
        else:
            self.rect.center = self.position
    def draw(self,screen):
        self.font.render_to(screen,self.rect,self.textFunc(),self.color)
    def update(self):
        self.rect = self.font.get_rect(self.textFunc())
        if self.align == "Left":
            self.rect.topleft = self.position
        else:
            self.rect.center = self.position