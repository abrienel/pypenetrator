import sys
import os
import time
import pygame
import pygame.locals
from cave import Cave
from agents.penetrator import Penetrator

from colour import COLOR_NAME_TO_RGB as color

black = color["black"]
red = color["red"]
orange = color["orange"]
green = color["green"]
blue = color["blue"]
white = color["white"]
yellow = color["yellow"]

standardrect=pygame.Rect(0,0,32,32)

class GameController():
    def __init__(self):

        self.screencolor = green
        self.size = self.width, self.height = 1000, 600
        self.sy = (self.height+0.0001) / 192.0  # vertical scale factor
        # initialise sound
        # setup mixer to avoid sound lag
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        #initialize pygame
        pygame.init()
        self.bulletsound = pygame.mixer.Sound(os.path.join('media','bullet.wav'))  #load sound
        self.explosionsound = pygame.mixer.Sound(os.path.join('media','explosion.wav'))  #load sound
        self.destroysound=pygame.mixer.Sound(os.path.join('media','destroy.wav'))  #
        self.screen = pygame.display.set_mode(self.size)
        self.initcave()
        print("BEFOREGAME")
        print(self.sy)
        self.cave.width=self.width
        self.cave.height=self.height

    def initcave(self):
        '''
        Resource handling classes
        '''
        #each slice is 32 pixels wide
        self.cave = Cave("cavedata4.csv",192,32,self.sy,self)
        self.ship = Penetrator(self.cave)

    def mainloop(self):
        ii = 0
        while 1:
            # Code for Input handling (i.e. watching for users hitting keys/mouse buttons),
            self.ship.processinput()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            # Code for Updating of Game Variables
            self.cave.update(ii)
            self.ship.update()
            self.ship.interactwithcave(ii)
            
            # Rendering
            self.screen.fill(self.screencolor)
            self.cave.render(ii)
            self.ship.render()
            #self.drawtext()
            self.drawstats()

            #Present to Front
            pygame.display.flip()
            ii=ii+1.0/32.0
            time.sleep(0.005 )

    def drawtext(self):
        # Display Text
        font = pygame.font.Font(None, 28)
        text = font.render("Cave Master.  Fuel=%s" % int(self.ship.fuel), 1,
                           (10, 10, 10))
        textpos = text.get_rect()
        textpos.x = 10
        textpos.y = 4
        self.screen.blit(text, textpos)

    def drawfuel(self,x,y,fwidth,fheight,gap=2,line=1):
        font = pygame.font.Font(None,18)
        text = font.render("Fuel: ", 1,
                           (10, 10, 10))
        textpos = text.get_rect()
        textpos.x = x
        textpos.y = y
        self.screen.blit(text, textpos)
        rw=fwidth-(textpos.width+gap)
        dy=(textpos.height-fheight)/2
        fuelrt = pygame.Rect(x+textpos.width+gap,y+dy,rw*self.ship.fuel/100.0,fheight)
        fuelbackgroundrt=pygame.Rect(fuelrt.x-line,fuelrt.y-line,fuelrt.width+line+line,fuelrt.height+line+line)
        self.screen.fill((24,24,24),rect=fuelbackgroundrt)
        if self.ship.fuel > 45:
            self.screen.fill((128, 255, 128), rect=fuelrt)
        elif self.ship.fuel > 25:
            self.screen.fill((255, 255, 40), rect=fuelrt)
        else:
            self.screen.fill((255, 40, 40), rect=fuelrt)
        if self.ship.fuel < 0:
            self.ship.fuel = 0.0
    def drawscore(self):
        # Display Text
        font = pygame.font.Font(None, 18)
        text = font.render("Score:  %s Ships Lost: %s" % (self.ship.score,self.ship.shipslost), 1,
                           (10, 10, 10))
        textpos = text.get_rect()
        textpos.x = 300
        textpos.y = self.height-18
        self.screen.blit(text, textpos)
    def drawstats(self):
        self.drawfuel(8,self.height-18,200,10)
        self.drawscore()

