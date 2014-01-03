## Import Modules
import os, pygame, random, math, json

## put commonly used in global namespace
from pygame.locals import *
from general import *
from localdata import *

class  EnemyMissile (pygame.sprite.Sprite ):
    def __init__( self, filename, start_loc, speed, angle, health, ptr, alpha = False, Poop = True ):
        '''
            filename - image
            start_loc - position of projectile when spawned
            speed - rate particle moves
            angle - direction it travels, 0 is up
            health - health of projectile - destructable
        '''
        pygame.sprite.Sprite.__init__( self )
        self.ptr = ptr
        self.alpha = alpha
        self.angle = -angle
        if self.alpha == True:
            self.image, self.rect = load_image( dataname(filename), -1, True )
            
        else:
            self.image, self.rect = load_image( dataname(filename), -1 )
        
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect.center = (self.x_loc, self.y_loc) = start_loc
        self.speed = speed
        self.angle = math.radians(angle)
        self.health = health
        self.velocity = ( math.sin(self.angle) * self.speed ,-math.cos(self.angle) * self.speed )
        self.liftTime = 0;
        self.side = random.uniform(1, 2)
        if self.side <= 1.5:
            self.side = 1
        else:
            self.side = 2
        self.randomNum = random.uniform(1, 2)
        if self.side >= 1 and self.side < 2:
            self.side = 1
        elif self.side >= 2 and self.side < 3:
            self.side = 2
        self.poop = Poop
        self.defaultX = self.x_loc
        self.defaultY = self.y_loc
        self.randomAngle = random.randint(5, 15)

    def update( self ):
        (x_loc,y_loc) = self.rect.center       

        if self.ptr.counter %25== 0 and self.poop == True:
            self.speed += 2
            self.velocity = ( math.sin(self.angle) * (self.speed+2) ,-math.cos(self.angle) * (self.speed +2))
        elif self.poop == True:
            self.rect.move_ip( self.velocity )
        if self.poop == False:
            if self.liftTime < 15:
                if self.side == 1:
                    self.rect.move_ip((-math.sin(self.randomAngle) * self.randomNum, -self.speed))
                else:
                    self.rect.move_ip((math.sin(self.randomAngle) * self.randomNum,  -self.speed))
                self.liftTime += 1
            else:
                if self.ptr.counter %25 == 0:
                    self.side = random.uniform(1, 2)
                    if self.side <= 1.5:
                        self.side = 1
                    else:
                        self.side = 2
                if self.side == 1:
                    self.rect.move_ip((math.sin(self.randomAngle/2) * self.randomNum,  -2*self.speed))
                else:
                    self.rect.move_ip((-math.sin(self.randomAngle/2) * self.randomNum,  -2*self.speed))
            self.rect.move_ip((0, -self.speed))
        elif self.poop == False and self.ptr.counter %25 == 0:
            self.speed += 2
        if self.rect.bottom < -50 or self.rect.top > SCREEN_H + 100 \
           or self.rect.left < 0 or self.rect.right > SCREEN_W:
            self.kill()


    # manages health and destruction of Stuff.projectiles by player     
    def hit (self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            #Stuff.score.score += 5
