import sys
import os
import time
import pygame
import pygame.locals
import math

from colour import COLOR_NAME_TO_RGB as color

black = color["black"]
red = color["red"]
orange = color["orange"]
green = color["green"]
blue = color["blue"]
white = color["white"]
yellow = color["yellow"]

standardrect = pygame.Rect(0, 0, 32, 32)


class GameController():
    def __init__(self):

        self.screencolor = green
        self.size = self.width, self.height = 1000, 600
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.currenttime = time.time()
        self.prevtime = self.currenttime
        self.file = "media/fuel"
        self.taglen = 4
        self.extension = "png"
        self.image = self.loadimage(1)
        self.x = 100
        self.y = 100
        self.speedx = 150.0
        self.speedy = 150.0

    def mainloop(self):
        while 1:

            # Code for Input handling (i.e. watching for users hitting keys/mouse buttons),
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            # Code for Updating of Game Variables
            interval = time.time() - self.prevtime

            self.x += self.speedx * interval
            self.y += self.speedy * interval
            rect = self.image.get_rect()
            rect = rect.move((self.x, self.y))
            if (rect.bottom - 4) > self.height:
                self.speedy = -(abs(self.speedy))
            if rect.top < -16:
                self.speedy = (abs(self.speedy))
            if rect.right > self.width:
                self.speedx = -(abs(self.speedx))
            if rect.left < 0:
                self.speedx = (abs(self.speedx))

            # Rendering
            gray1 = int(125 * math.sin(1.05 * time.time()) + 130)
            gray2 = int(125 * math.sin(2.23 * time.time()) + 130)
            gray3 = int(125 * math.sin(3.54 * time.time()) + 130)

            # print(gray)
            self.screen.fill((gray1, gray2, gray3),pygame.Rect(gray3,gray2,10,10))
            self.screen.blit(self.image, rect)

            self.drawstats()
            # Present to Front
            pygame.display.flip()
            self.prevtime = self.currenttime
            # self.sync(1)

    def sync(self, fps):
        # first calculate what delta should be for required fps:
        requiredinterval = 1.0 / fps
        time.sleep(requiredinterval)

    def drawfps(self):
        # Display Text
        self.currenttime = time.time()
        try:
            font = pygame.font.Font(None, 20)
            text = font.render("FPS %s" % int(1 / (self.currenttime - self.prevtime)), 1, (255, 255, 255))
            textpos = text.get_rect()
            textpos.x = 10
            textpos.y = 4
            self.screen.blit(text, textpos)
        except:
            pass

    def drawstats(self):
        self.drawfps()

    def loadimage(self, state):
        file = self.file
        extension = self.extension
        tag = ("%s" % state).zfill(self.taglen)  # 2 digit zero padded number
        filename = "%s%s.%s" % (file, tag, extension)
        try:
            newimage = pygame.image.load(filename)
        except:
            print("Error in loadimage %s" % filename)
        return newimage
