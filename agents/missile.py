import pygame
from agents.agent import Agent
from pygame.locals import *
import math
from random import randint
NOTHRUST=0
UPWARD=4
EXPLODING=64

class Missile(Agent):
    """Missile"""

    def __init__(self,caveslice):
        Agent.__init__(self)
        self.v = 0
        self.gamestate=NOTHRUST
        self.active = False
        self.activity=40000
        self.file = "media/missile"
        self.taglen = 4
        self.loadimage(NOTHRUST)
        self.caveslice=caveslice
        self.speedy=0
        scale = 0.75
        self.thrust=0.005
        for im in self.image.keys():
            self.image[im] = pygame.transform.smoothscale(self.image[im], (
            int(self.image[im].get_rect().width * scale), int(self.image[im].get_rect().height * scale)))

    def render(self,xoffset):
        #print("rendermissile")
        screen = pygame.display.get_surface()
        rr=self.get_rect()
        rect = rr.move(xoffset * self.caveslice.slicewidth, self.caveslice.bottom-rr.height+self.v)
        if self.hit==True:
            screen.fill((255,0,0),rect)
            self.hit=False
        screen.blit(self.get_image(),rect)
        self.screenrect=rect

    def update(self,xoffset):
        if randint(0,self.activity)==1:
            self.active=True
        if self.active==True:
            self.speedy-=self.thrust
        self.v+=self.speedy
        

