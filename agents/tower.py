import pygame
from random import randint
from agents.agent import Agent

EXPLODING=64

class Tower(Agent):
    """Tower"""
    classimage=None

    def __init__(self,caveslice):
        Agent.__init__(self)
        self.caveslice=caveslice
        self.counter=0.0
        self.rotationspeed=0.1
        self.loadimages()
        
    def loadimages(self):
        self.file="media/satellite"
        self.taglen=4
        self.extension="png"
        scale = 0.75
        if Tower.classimage is None:
            for i in range(0, 39):
                self.loadimage(i)
            for im in self.image.keys():
                om=self.image[im]
                #Crop the image a bit
                cropped = pygame.Surface((om.get_rect().width,om.get_rect().height-4), pygame.SRCALPHA, 32)
                cropped.convert_alpha()
                cropped.blit(om, (0, 0))
                self.image[im]=cropped
                #Scale it a bit
                self.image[im] = pygame.transform.smoothscale(self.image[im], (
                int(self.image[im].get_rect().width * scale), int(self.image[im].get_rect().height * scale)))
            Tower.classimage=self.image
        else:
            self.image=Tower.classimage

    def render(self,xoffset):
        #print("rendertower")
        screen = pygame.display.get_surface()
        rr=self.get_rect()
        rect = rr.move(xoffset * self.caveslice.slicewidth, self.caveslice.bottom-rr.height)
        if self.hit==True:
            screen.fill((255,0,0),rect)
            self.hit=False
        screen.blit(self.get_image(),rect)
        self.screenrect=rect

    def update(self,xoffset):
        self.counter+=self.rotationspeed
        self.gamestate=int(self.counter % 39)




