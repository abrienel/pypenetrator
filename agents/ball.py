import pygame
from pygame.locals import *
import math

class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ball.png')
        self.rect=self.image.get_rect()
        screen = pygame.display.get_surface()
        #self.area = screen.get_rect()
        self.vector = vector

    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)

    def move(self,dx,dy):
        self.rect=self.rect.move(dx,dy)

    def render(self):
        screen = pygame.display.get_surface()
        screen.blit(self.image,self.rect)

