## Import Modules
import os, pygame, random, math

## put commonly used in global namespace
from pygame.locals import *
from general import *
from localdata import *

class Drone(pygame.sprite.Sprite):
    def __init__(self,x_offset,y_offset,side,ptr):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image_alpha( dataname("drone.png"))
        self.x_off = x_offset
        self.y_off = y_offset
        self.oldx = x_offset
        self.oldy = y_offset
        self.shipptr = ptr
        self.change = False
        self.changeacc = 0
        self.laserready = True
        self.side = side
    def changemode(self):
        pass
    def update(self):
        self.rect.center = (self.shipptr.rect.center[0]+self.x_off,
                             self.shipptr.rect.center[1]+self.y_off)
        return

class LatDrone(pygame.sprite.Sprite):
    def __init__(self,x1,x2,ptr):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image_alpha( dataname("drone.png"))
        self.x_off = x1
        self.y_off = 0
        self.shipptr = ptr
        # used for orientation change
        self.change = False
        self.changeacc = 0
        self.changepct = 0
        # transient code
        self.oldx = x2
        if x1 < 0:
            self.side = -1
        elif x1 > 0:
            self.side = 1
        else:
            self.side = 0
        self.laserready = True
    def changemode(self):
        self.change = True
        self.changepct = 1.0
        self.changeacc = 0.0
        tempx = self.oldx
        self.oldx = self.x_off
        self.x_off = tempx
        return
    def update(self):
        # this code animates the mode change
        if self.change == True:
            self.changeacc+=0.002
            if self.changeacc > 0.7:
                self.changeacc = 0.7
            self.changepct-=self.changeacc
            if self.changepct < 0:
                self.changepct = 0
                self.change = False
            x = ((self.x_off - self.oldx)*self.changepct)
        else:
            x = 0
        self.rect.centerx = self.shipptr.rect.centerx + self.x_off - x
        self.rect.centery = self.shipptr.rect.centery
        return

class RotDrone(pygame.sprite.Sprite):
    def __init__(self,rot,ptr):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image_alpha( dataname("drone.png"))
        self.rot = rot
        self.shipptr = ptr
        self.change = False
        self.speed = 5
        self.side = 0
        self.laserready = True
    def changemode(self):
        pass
    def update(self):
        self.rot += self.speed
        if self.rot >= 360:
            self.rot-=360
        angle = self.rot * math.pi / 180
        self.rect.centerx = self.shipptr.rect.centerx+(-math.cos(angle) * 65)
        self.rect.centery = self.shipptr.rect.centery+(math.sin(angle) * 65)
        return

class TrailDrone(pygame.sprite.Sprite):
    def __init__(self,delay,mode,ptr):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image_alpha( dataname("drone.png"))
        # unlike the other drones, this actually doesn't
        # want only the ship pointer as ptr
        self.ptr = ptr
        self.delay = delay
        self.mode = mode
        self.steps = list()
        self.change = False
        self.side = 0
        self.laserready = True
    def changemode(self):
        self.mode = 1 - self.mode
    def update(self):
        if len(self.steps) <= self.delay:
            # record more steps
            if self.mode == 1:
                self.steps.append(self.ptr.rect.center)
            elif self.mode == 0:
                if len(self.steps)<=0:
                    self.steps.append(self.ptr.rect.center)
                elif self.ptr.rect.center !=self.steps[-1]:                    
                    self.steps.append(self.ptr.rect.center)
        else:
            self.steps = self.steps[1:]
        self.rect.center = self.steps[0]
        return

class CenterDrone(pygame.sprite.Sprite):
    def __init__(self,y1,y2,ptr):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image_alpha( dataname("drone.png"))
        self.x_off = 0
        self.y_off = y1
        self.oldy = y2
        self.shipptr = ptr
        self.change = False
        self.changeacc = 0
        self.changepct = 0
        self.side = 0
        self.laserready = True
    def changemode(self):
        self.change = True
        tempy = self.oldy
        self.oldy = self.y_off
        self.y_off = tempy
        self.changeacc = 0.0
        self.changepct = 1.0
        return
    def update(self):
        if self.change == True:
            self.changeacc+=0.002
            if self.changeacc > 0.7:
                self.changeacc = 0.7
            self.changepct-=self.changeacc
            if self.changepct < 0:
                self.changepct = 0
                self.change = False
            y = ((self.y_off - self.oldy)*self.changepct)
        else:
            y = 0
        self.rect.centery = self.shipptr.rect.centery + self.y_off - y
        self.rect.centerx = self.shipptr.rect.centerx
        return
