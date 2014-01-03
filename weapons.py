import os, pygame, random, math
from pygame.locals import *
from general import *
from localdata import *
from various import *

class Laser(pygame.sprite.Sprite):
    def __init__(self,ptr):
        pygame.sprite.Sprite.__init__(self)
        self.images = list()
        try:
            sheet = pygame.image.load(dataname("laserpart.png"))
        except pygame.error, message:
            print "laserpart.png not found"
            raise SystemExit, message
        for x in range(0,2):
            self.images.append(sheet.subsurface((3*x,0,3,1)))
        self.rect = self.images[0].get_rect()
        self.image = self.images[0]
        self.swap = 0
        self.size = 0
        self.letgo = False
        self.strength = 20
        self.alive = True
        self.ptr = ptr
        self.ptr.laserready = False
        self.x = self.ptr.rect.centerx
        self.y = self.ptr.rect.centery
    def update(self):
        # increase size and check if we can let go of the laser
        if self.size > 600:
            self.letgo = True
        else:
            self.size +=15
        # transform
        self.image=pygame.transform.scale(self.images[self.swap], (3, self.size))
        self.rect = self.image.get_rect()
        self.x = self.ptr.rect.centerx
        if self.letgo == False:
            self.y = self.ptr.rect.centery
        else:
            self.y-=20
        self.rect.bottom = self.y
        self.rect.centerx = self.x
        # swap value after update
        self.swap = 1 - self.swap
        if self.y < 0:
            self.ptr.laserready = True
            self.alive = 0
            self.kill()
        return
    
class Homing(pygame.sprite.Sprite):
    def __init__(self,origin,targetlist,direction):
        pygame.sprite.Sprite.__init__(self)
        self.images = list()
        try:
            sheet = pygame.image.load(dataname("homing.png")).convert_alpha()
        except pygame.error, message:
            print "laserpart.png not found"
            raise SystemExit, message
        for x in range(0,2):
            self.images.append(sheet.subsurface((16*x,0,16,32)))
        self.rect = self.images[0].get_rect()
        self.image = self.images[0]
        self.swap = 0
        self.rect.centerx = origin.rect.centerx
        self.rect.centery = origin.rect.centery
        self.direction = direction
    def update(self):
        pass

class Spray(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image_alpha(dataname("yellowshot.png"))
        self.image = pygame.transform.rotate(self.image,direction*-1)
        self.direction = math.radians(direction)
        self.rect.centery = y
        self.rect.centerx = x
        # speed of projectile is generally 5
    def update(self):
        self.rect.move_ip(( math.sin(self.direction)*10,-math.cos(self.direction)*10 ))
        if self.rect.right < 0 or self.rect.left >= SCREEN_W:
            self.kill()
        if self.rect.bottom < 0 or self.rect.top >= SCREEN_H:
            self.kill()

# this is my own class, it just reuses the older code
class Missile(pygame.sprite.Sprite):
    def __init__(self,origin,gameptr,straight):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=self.missiledata=load_image_alpha(dataname("missle.png"))
        self.period = 0
        self.speed = random.randint(1,4)
        self.health = 5
        self.rect.centerx = origin.rect.centerx+random.randint(-15,16)
        self.rect.centery = origin.rect.centery
        self.straight=straight
        self.rand1 = random.randrange(1,3)
        self.rand2 = random.randrange(1,3)
        self.rand3 = random.randrange(5,15)
        self.liftTime = 0
        self.ptr = origin
        self.gameptr = gameptr
    def update(self):
        if self.straight:
            if self.period>=25:
                self.period=0
                self.speed+=2
            self.rect.centery-=self.speed
        else:
            if self.liftTime <15:
                if self.rand1 == 1:
                    self.rect.move_ip((-math.sin(self.rand3-90) * self.rand2, -self.speed))
                else:
                    self.rect.move_ip((math.sin(self.rand3-90) * self.rand2,  -self.speed))
                self.liftTime+=1
            else:
                if self.period>=25:
                    if self.rand1 == 1:
                        self.rect.move_ip((math.sin(self.rand3/2-90)*self.rand2,-2*self.speed))
                    else:
                        self.rect.move_ip((-math.sin(self.rand3/2-90)*self.rand2,-2*self.speed))
                self.rect.move_ip((0,-self.speed))
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left >= SCREEN_W:
            self.kill()
            return
        self.period+=1
        return
    def explode(self):
        x=self.rect.centerx
        y=self.rect.centery
        # i'm not gonna change it for now, but it would have been better to
        # store the explosions and pass a new rect() type each time
        self.gameptr.addexplosion(0,x,y)
        self.kill()
