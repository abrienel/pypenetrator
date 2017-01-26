import pygame
class Agent(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gamestate=0
        self.image=[]
        self.image = dict()
        self.loadimages()
        self.extension="png"
        self.file="media/agent"
        self.taglen=3
        self.active = False
        self.hit=False
        self.screenrect=None

    def loadimages(self):
        pass

    def getimageextension(self):
        return "png"

    def loadimage(self, state):

        file = self.file
        extension = self.extension
        tag = ("%s" % state).zfill(self.taglen)  # 2 digit zero padded number
        filename = "%s%s.%s" % (file, tag, extension)
        try:
            newimage = pygame.image.load(filename)
            self.image[state] = newimage
        except:
            print("Error in loadimage %s" % filename)
        return newimage

    def get_rect(self):
        return self.get_image().get_rect()

    def get_image(self):
        return self.image[self.gamestate]

    def update(self):
        pass

    def move(self,dx,dy):
        self.rect=self.rect.move(dx,dy)