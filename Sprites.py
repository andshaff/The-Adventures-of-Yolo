import os, pygame, random, math
from pygame.locals import *
from general import *
from localdata import *

class Player(pygame.sprite.Sprite):
    def __init__(self,health,ptr):
        pygame.sprite.Sprite.__init__( self )
        self.tempimage, self.rect = load_image_alpha(dataname("ship.png"))
        self.zeroimage = pygame.Surface((1,1)).convert_alpha()
        self.zeroimage.fill(0)
        self.image = self.tempimage
        self.max_health = health
        self.health = health
        self.rect.midtop = (400,SCREEN_H)
        self.gamedata = ptr
        self.blinkon = False
        self.blink = 0          # this is just an alternation b/w blinking states
        self.blinkcount = 0     # intervals between blinking states
        self.invincible = True  # we only blink when invincible however
        self.invtime = 0
        self.speed = ptr.speed
        self.ctrl = False
        self.laserready = True
        self.alive = True
    def setinv(self,time,blink=True):
        self.invtime = 120
        self.invincible = True
        self.blinkon = blink
    def update(self):
        # blinking the ship for invulnerability
        if self.invincible == True:
            if self.blinkon == True:
                self.blinkcount += 1
                if self.blinkcount >= 2:
                    self.blink = 1-self.blink
                    self.blinkcount = 0
                if self.blink == 1:
                    self.image = self.zeroimage
                else:
                    self.image = self.tempimage
            self.invtime -= 1
            if self.invtime <= 0:
                self.invincible = False
                self.image = self.tempimage
                self.blinkon = False
        if self.ctrl:
            # moving the ship
            self.rect.top += self.speed*self.gamedata.plyrvely
            self.rect.left += self.speed*self.gamedata.plyrvelx
            if self.rect.top < 0: self.rect.top = 0
            # constricting the ship
            if self.rect.bottom >= SCREEN_H: self.rect.bottom = SCREEN_H-1
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.right >= SCREEN_W: self.rect.right = SCREEN_W-1
        return
    def hit(self,damage):
        self.health-=damage
        if self.health<=0:
            x = self.rect.centerx
            y = self.rect.centery
            self.gamedata.addexplosion(6,x,y)
            self.gamedata.soundlist[6].play()
            self.kill()
            self.gamedata.drones.empty()
        else:
            self.gamedata.soundlist[5].play()
    
