import pygame
from agents.missile import Missile
from agents.tower import Tower
from agents.fuel import Fuel
import random

class CaveSlice():
    def __init__(self,max,sy,slicewidth,top,bottom,objcode,prev):
        self.hit=False
        linewidth=2
        self.sy=sy
        self.max=max*sy
        #print(max)
        #print(sy)
        #print(max*sy)
        self.slicewidth=slicewidth
        self.top=int(top)*self.sy
        self.bottom=int(bottom)*self.sy
        self.color1=(200,200,200)
        self.color2=(10,10,10)
        self.color3=(200,0,0)
        if prev is None:
            self.prev=self
        else:
            self.prev=prev
        obj=None
        if objcode ==1:
            #print(("%s " %objcode) *10)
            #print("Add Tower")
            obj = Tower(self)
            if random.random()>0.5:
                obj.rotationspeed=obj.rotationspeed/2
            if random.random() > 0.5:
                obj.rotationspeed=-obj.rotationspeed
        if objcode == 2:
            #print(("%s " % objcode) * 10)
            #print("Add Missile")
            obj = Missile(self)
        if objcode == 3:
            #print(("%s " % objcode) * 10)
            #print("Add Fuel")
            obj = Fuel(self)

        self.obj=obj
        self.rt = pygame.Rect(0, 0,  self.slicewidth, int(self.top))
        self.rtb = pygame.Rect(0, self.top, self.slicewidth, linewidth)
        if self.prev.top>self.top:
            self.rtl = pygame.Rect(0, self.top,linewidth,self.prev.top-self.top)
        else:
            self.rtl = pygame.Rect(0, self.prev.top, linewidth, self.top - self.prev.top)

        self.rb = pygame.Rect(0, int(self.bottom), self.slicewidth,self.max-self.bottom)
        self.rbt = pygame.Rect(0, self.bottom, self.slicewidth, linewidth)
        if self.prev.bottom > self.bottom:
            self.rbl = pygame.Rect(0, self.bottom, linewidth, self.prev.bottom - self.bottom+linewidth)
        else:
            self.rbl = pygame.Rect(0, self.prev.bottom, linewidth, self.bottom - self.prev.bottom+linewidth)

    def renderrect(self,rect,xoffset,color):
        screen = pygame.display.get_surface()
        screen.fill(color, rect=rect.move(xoffset * self.slicewidth, 0))

    def render(self,xoffset):
        screen = pygame.display.get_surface()
        self.renderrect(self.rt,xoffset,self.color1)
        self.renderrect(self.rtb,xoffset,self.color2)
        self.renderrect(self.rtl,xoffset,self.color2)
        self.renderrect(self.rb,xoffset,self.color1)
        if self.hit==True:
            self.renderrect(self.rb, xoffset, self.color3)
            self.hit=False
        self.renderrect(self.rbt ,xoffset,self.color2)
        self.renderrect(self.rbl,xoffset,self.color2)
        # Interact with ship render red

            # if the caveslice has an object render that
        if not (self.obj is None):
            self.obj.render(xoffset)

    def update(self,xoffset):
        if not (self.obj is None):
            self.obj.update(xoffset)


class Cave():
    def __init__(self,filename,max,slicewidth,sy,gamecontroller):
        self.gt=gamecontroller
        self.max=max
        self.sy=sy
        self.slicewidth=slicewidth
        self.filename=filename
        cave = []
        import csv
        pcs=None
        with open(self.filename, 'r') as csvfile:
            cavereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in cavereader:
                #print("xxxx")
                try:
                    #print(sy)
                    #print(self.sy)
                    cs=CaveSlice(self.max,self.sy,self.slicewidth,int(row[2]), int(row[4]),int(row[3]),pcs)
                    cave.append(cs)
                    pcs=cs
                except:
                    print("error in load cave")
        #print(len(cave))
        self.cave=cave
        self.nrofslices=50

    def update(self, xoffset):
        i = 0
        index = int(xoffset) % len(self.cave)
        for caveslice in self.cave[index:index + self.nrofslices]:
            caveslice.update(i - xoffset % 1)
            i += 1

    def render(self, xoffset):
        i=0
        index=int(xoffset) % len(self.cave)
        for caveslice in self.cave[index:index+self.nrofslices]:
            caveslice.render(i-xoffset%1)
            i+=1
