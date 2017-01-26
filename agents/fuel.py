import pygame
from random import randint
from agents.agent import Agent

EXPLODING=64

class Fuel(Agent):
    """Tower"""
    classimage=None
    def __init__(self,caveslice):
        self.hit=False
        print("Init Fuel:before agent super call")
        Agent.__init__(self)
        print("Init Fuel")
        self.file="media/fuel"
        self.taglen=4
        print("Fuel Add Pictures")
        print("Fuel Done pictures add")
        self.caveslice=caveslice
        print("Done Init Fuel")
        self.counter=0.0
        self.rotationspeed=0.1
        self.loadimages()

    def loadimages(self):
        scale = 1
        self.file="media/fuel"
        self.taglen=4
        self.extension="png"
        if Fuel.classimage is None:
            self.loadimage(0)
            for im in self.image.keys():
                self.image[im] = pygame.transform.smoothscale(self.image[im], (
                int(self.image[im].get_rect().width * scale), int(self.image[im].get_rect().height * scale)))
            Fuel.classimage=self.image
        else:
            self.image=Fuel.classimage




    def render(self,xoffset):
        #print("renderfuel")
        screen = pygame.display.get_surface()
        rr=self.get_rect()
        rect = rr.move(xoffset * self.caveslice.slicewidth, self.caveslice.bottom-rr.height)
        if self.hit==True:
            screen.fill((255,0,0),rect)
            self.hit=False
        screen.blit(self.get_image(),rect)
        self.screenrect = rect

    def update(self,xoffset):
        self.counter+=self.rotationspeed
        #self.gamestate=int(self.counter % 39)
