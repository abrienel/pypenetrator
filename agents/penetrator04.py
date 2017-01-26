import pygame
from agents.agent import Agent

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


class Penetrator(Agent):
    """The main penetrator rocket ship"""

    def __init__(self, cave):
        Agent.__init__(self)
        self.cave = cave
        self.gamestate = NOTHRUST

        self.file = "penetrator"
        self.taglen = 2
        #SINGLE STATE STATES
        self.loadimage(NOTHRUST)
        self.loadimage(EXPLODING)

        #COMBINATION STATES
        self.loadimage(UPWARD)
        self.loadimage(DOWNWARD)
        self.loadimage(FORWARD)
        self.loadimage(BACKWARD)
        self.loadimage(UPWARD | DOWNWARD)
        self.loadimage(UPWARD | FORWARD)
        self.loadimage(UPWARD | BACKWARD)
        self.loadimage(FORWARD | BACKWARD)
        self.loadimage(DOWNWARD | UPWARD)
        self.loadimage(DOWNWARD | FORWARD)
        self.loadimage(DOWNWARD | BACKWARD)
        self.x=100
        self.y=100
        self.speedx=0
        self.speedy=0
        self.thrust=0.005
        self.maxspeed=1

    def render(self):
        screen = pygame.display.get_surface()
        r=self.get_rect().move(self.x,self.y)

        screen.blit(self.image[self.gamestate], r)

    def thrustUp(self):
        self.gamestate = self.gamestate | UPWARD

    def thrustDown(self):
        self.gamestate = self.gamestate | DOWNWARD

    def thrustBackward(self):
        self.gamestate = self.gamestate | BACKWARD

    def thrustForward(self):
        self.gamestate = self.gamestate | FORWARD

    def zeroThrust(self):
        self.gamestate = NOTHRUST

    def explode(self):
        self.gamestate = EXPLODING

    def update(self):
        if (self.gamestate & UPWARD)>0:
            self.speedy-=self.thrust
        if self.gamestate & DOWNWARD > 0:
            self.speedy += self.thrust
        if self.gamestate & FORWARD > 0:
            self.speedx += self.thrust
        if self.gamestate & BACKWARD > 0:
            self.speedx -= self.thrust
        self.x+=self.speedx
        self.y+=self.speedy
        if self.speedx<-self.maxspeed:
            self.speedx=-self.maxspeed
        if self.speedy < -self.maxspeed:
            self.speedy = -self.maxspeed
        if self.speedx > self.maxspeed:
            self.speedx = self.maxspeed
        if self.speedy > self.maxspeed:
            self.speedy = self.maxspeed
        gravity=self.thrust/4
        self.speedy+=gravity

    def processinput(self):
        self.zeroThrust()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q]:
            self.thrustUp()
            return
        if pressed[pygame.K_a]:
            self.thrustDown()
            return
        if pressed[pygame.K_o]:
            self.thrustBackward()
            return
        if pressed[pygame.K_p]:
            self.thrustForward()
            return
