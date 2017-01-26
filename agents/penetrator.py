import pygame
from agents.agent import Agent
from agents.fuel import Fuel
from agents.bullet import Bullet
from agents.missile import Missile
from agents.tower import Tower

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

        self.file = "media/penetrator"
        self.taglen = 2
        #SINGLE STATE STATES
        self.loadimage(NOTHRUST)
        self.loadimage(EXPLODING)

        #COMBINATION STATES
        self.loadimage(UPWARD)
        self.loadimage(DOWNWARD)
        self.loadimage(FORWARD)
        self.loadimage(BACKWARD)
        self.loadimage(UPWARD | FORWARD)
        self.loadimage(UPWARD | BACKWARD)
        self.loadimage(DOWNWARD | UPWARD)
        self.loadimage(DOWNWARD | FORWARD)
        self.loadimage(DOWNWARD | BACKWARD)
        scale=0.75
        for im in self.image.keys():
            self.image[im]=pygame.transform.smoothscale(self.image[im], (int(self.image[im].get_rect().width*scale),int(self.image[im].get_rect().height*scale)))
        self.x=100
        self.y=100
        self.speedx=0.0
        self.speedy=0.0
        self.thrust=0.05
        self.maxspeed=1
        self.fuel=100.0
        self.fuelconsumption=0.02
        self.bullets=[]
        for i in range(0,12):
            self.bullets.append(Bullet(cave))
        self.score=0
        self.shipslost=0
        self.bulletinterval = 0
        self.wait=0
        
    def render(self):
        screen = pygame.display.get_surface()
        for bullet in self.bullets:
            if bullet.gamestate!=NOTHRUST:
                bullet.render()
        r=self.get_rect().move(self.x,self.y)
        screen.blit(self.image[self.gamestate], r)
        self.screenrect=r


    def thrustUp(self):
        self.gamestate = self.gamestate | UPWARD
        if (self.gamestate & DOWNWARD) > 0:
            self.gamestate-=DOWNWARD
        self.fuel -= self.fuelconsumption

    def thrustDown(self):
        self.gamestate = self.gamestate | DOWNWARD
        if (self.gamestate & UPWARD) > 0:
            self.gamestate-=UPWARD
        self.fuel -= self.fuelconsumption

    def thrustBackward(self):
        self.gamestate = self.gamestate | BACKWARD
        if (self.gamestate &FORWARD) > 0:
            self.gamestate-=FORWARD
        self.fuel -= self.fuelconsumption

    def thrustForward(self):
        self.gamestate = self.gamestate | FORWARD
        if (self.gamestate & BACKWARD) > 0:
            self.gamestate-=BACKWARD
        self.fuel -= self.fuelconsumption

    def zeroThrust(self):
        self.gamestate = NOTHRUST

    def explode(self):
        self.gamestate = EXPLODING

    def update(self):
        if self.wait>0:
            return
        if (self.gamestate & EXPLODING):
            self.wait=200
            
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
        for bullet in self.bullets:
            bullet.update()

            
        #print(self.gamestate)

    def fireBullet(self):
        if self.bulletinterval>0:
            self.bulletinterval-=1
            return
        for bullet in self.bullets:
            if bullet.gamestate==NOTHRUST:
                bullet.gamestate=FORWARD
                bullet.lifetime=200
                self.cave.gt.bulletsound.play()
                bullet.x=self.x+self.get_rect().width
                bullet.y=self.y+self.get_rect().height/2-2
                bullet.speedx=self.speedx+bullet.thrust
                bullet.speedy=self.speedy
                #print("Fire!")
                self.bulletinterval=10
                break


    def processinput(self):
        self.zeroThrust()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_i]:
            self.fireBullet()
        if self.fuel<=0:
            self.gamestate=NOTHRUST
            return

        if pressed[pygame.K_q]:
            self.thrustUp()
        if pressed[pygame.K_a]:
            self.thrustDown()
        if pressed[pygame.K_o]:
            self.thrustBackward()
        if pressed[pygame.K_p]:
            self.thrustForward()


            #self.fireBullet()

    def interactwithcave(self,xoffset):
        if self.wait>0:
            self.wait=self.wait-1
            if self.wait==0:
                self.gamestate=NOTHRUST
            else:
                return
            
        cave=self.cave
        sw=cave.slicewidth
        nrofslices=cave.nrofslices
        i = 0
        activeslices=[]
        index = int(xoffset) % len(cave.cave)
        r=self.get_rect().move(self.x,self.y)
        missiles=[]
        towercount=0
        for slice in cave.cave[index:index + self.cave.nrofslices]:
            #check if there is cave collision
            if self.y<slice.top and self.x>i*sw and self.x>i*sw and self.x<(i+1)*sw:
                self.gamestate=EXPLODING
                self.speedy=1
                self.y=slice.top+1
                self.shipslost+=1
                self.cave.gt.explosionsound.play()
                break
            if self.y>slice.bottom and self.x>i*sw and self.x<(i+1)*sw:
                self.gamestate=EXPLODING
                self.speedy=-1
                self.y=slice.bottom-self.get_rect().height-1
                self.shipslost+=1
                self.cave.gt.explosionsound.play()
                break

            if self.x<0:
                self.speedx=1
                self.gamestate=EXPLODING
                self.shipslost+=1
                self.cave.gt.explosionsound.play()
                self.x=1
                break

            if self.x+self.get_rect().width>cave.width:
                self.speedx=-1
                self.gamestate=EXPLODING
                self.shipslost+=1
                self.cave.gt.explosionsound.play()
                self.x=cave.width-self.get_rect().width-10
                break

            if not slice.obj is None:
                if type(slice.obj) is Missile:
                    missiles.append(slice.obj)
                    slice.obj.proximity=abs(self.cave.width-(self.x-i*sw))
                if type(slice.obj) is Tower:
                    towercount+=1
                    
                if slice.obj.screenrect:
                    if slice.obj.screenrect.collidepoint((r.x, r.y)) == True or \
                                        slice.obj.screenrect.collidepoint((r.x+r.width, r.y+r.height)) == True:
                        slice.obj.hit=True
                        if type(slice.obj) is Fuel:
                                self.fuel=100
                                slice.obj = None
                                self.cave.gt.destroysound.play()
                    for bullet in self.bullets:
                        if bullet.gamestate==FORWARD:
                            if not slice.obj is None:
                                r=bullet.get_rect().move(bullet.x,bullet.y)
                                if slice.obj.screenrect.collidepoint((r.x, r.y)) == True or \
                                        slice.obj.screenrect.collidepoint((r.x+r.width, r.y+r.height)) == True:
                                    slice.obj.hit=True
                                    if type(slice.obj) is Fuel:
                                        self.fuel=100
                                    slice.obj = None
                                    self.cave.gt.destroysound.play()
                                    self.score+=10
                                    bullet.gamestate=NOTHRUST
                                    bullet.lifetime=0
            i+=1
        #print("len(missiles)=%s" %len(missiles))
        if towercount>0:
            #print("towercount=%s" %towercount)
            for missile in missiles:
                missile.activity=int(missile.proximity/towercount)
                                    

