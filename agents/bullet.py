import pygame
from agents.agent import Agent
from agents.fuel import Fuel

NOTHRUST = 0
FORWARD = 1
BACKWARD = 2
UPWARD = 4
DOWNWARD = 8
FORWARDUP = 5
FORWARDDOWN = 9
BACKWARDUP = 3
BACKWARDDOWN = 10
OVERHEATING = 16
WARM = 32
EXPLODING = 64
FIRINGBULLET = 128
DROPPINGBOMB = 256


class Bullet(Agent):
    """The main penetrator rocket ship"""

    def __init__(self, cave):
        Agent.__init__(self)
        self.cave = cave
        self.gamestate = NOTHRUST
        self.lifetime=100
        self.thrust=2
        self.speedx=0
        self.speedy=0
        self.x=0
        self.y=0

    def get_rect(self):
        return pygame.Rect(0,0,12,4)
    def render(self):
        try:
            if self.gamestate == NOTHRUST:
                self.screenrect=None
                return
            screen = pygame.display.get_surface()
            r=self.get_rect().move(self.x,self.y)
            screen.fill((255,255,255),r)
            self.screenrect=r
            #print("BULLETRENDER")
        except:
            print("Render error")
    def update(self):
        #print("UPDATE %s" % self.x)
        try:
            if (self.gamestate == NOTHRUST):
                self.speedx=0
                self.speedy=0
                return
            if self.gamestate == FORWARD:
                #print("FORWARD")
                self.lifetime-=1
                #print(self.lifetime)
                self.speedx = self.thrust
                if self.lifetime<=0:
                    #print("BULLET EXPIRE")
                    self.lifetime=100
                    self.speedx=0
                    self.speedy=0
                    self.gamestate=NOTHRUST
                    return
                self.x += self.speedx
                #self.y += self.speedy
                gravity=self.thrust/40
                #self.speedy+=gravity
            #print(self.gamestate)
        except:
            print("Update render")
