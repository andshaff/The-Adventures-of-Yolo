import os, pygame,sys,string,math, random
from pygame.locals import *
from general import *
from localdata import *

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, width, height):
        pygame.sprite.Sprite.__init__( self )
        self.images = load_sliced_sprites(width,height,dataname('Blue_Pow.png'), None,True)
        # assuming both images are 64x64 pixels
        self.x_loc = x_loc
        self.y_lox = y_loc
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x_loc, y_loc, width, height)
    def update(self, counter):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''        
        if self.index >= len(self.images):
            self.index = 0
        elif counter%5 == 0:
            self.image = self.images[self.index]
            self.index += 1

        (x_loc,y_loc) = self.rect.center
        self.rect.center = ( x_loc, y_loc + 1)

        if self.rect.top > SCREEN_H:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, width, height, imageset, ptr):
        pygame.sprite.Sprite.__init__( self )
        self.images = imageset
        # assuming both images are 64x64 pixels
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x_loc, y_loc, width, height)
        self.rect.center = (x_loc,y_loc)
        self.ptr = ptr
    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        if self.ptr.counter%4 == 0:
            (x_loc,y_loc) = self.rect.center
            self.rect.center = ( x_loc, y_loc + 1)           
        if self.index >= len(self.images):
            self.kill()
        elif self.ptr.counter%3 == 0:
            self.image = self.images[self.index]
            self.index += 1
            
class Animated_Projectile(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, width, height, filename, speed, angle, life, health, faster, ptr, x_off = 0, y_off = 0):
        #super(MovingAnimation, self).__init__()
        pygame.sprite.Sprite.__init__( self )
        self.images = load_sliced_sprites(width,height,dataname(filename), None,True)
        # assuming both images are 64x64 pixels
        self.ptr = ptr
        self.x_loc = x_loc
        self.y_lox = y_loc
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x_loc, y_loc, width, height)
        self.width = width
        self.height = height
        self.x_offset = x_off
        self.y_offset = y_off
        self.speed = speed
        self.faster = faster
        self.angle = math.radians(angle)
        self.health = health
        self.life = life
        self.velocity = ( math.sin(self.angle) * self.speed ,-math.cos(self.angle) * self.speed )
    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        
        if self.index >= len(self.images):
            self.index = 0;
        elif self.ptr.counter%3 == 0:
            self.image = self.images[self.index]
            self.index += 1

        if self.faster and self.ptr.counter %25== 0:
            self.speed += 2
            self.velocity = ( math.sin(self.angle) * self.speed ,-math.cos(self.angle) * self.speed )
        if self.rect.bottom < 0 or self.rect.top > SCREEN_H \
           or self.rect.left < 0 or self.rect.right > SCREEN_W or self.life == 0:
            self.kill()
        else:    
            self.rect.move_ip( self.velocity )
            if self.life > 0:
                self.life -= 1
    # manages health and destruction of Stuff.projectiles by player     
    def hit (self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            #Stuff.score.score += 5

class MovingAnimation(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, width, height, filename, ptr, x_off = 0, y_off = 0):
        #super(MovingAnimation, self).__init__()
        pygame.sprite.Sprite.__init__( self )
        self.images = load_sliced_sprites(width,height,dataname(filename), None,True)
        # assuming both images are 64x64 pixels
        self.x_loc = x_loc
        self.y_lox = y_loc
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x_loc, y_loc, width, height)
        self.width = width
        self.height = height
        self.x_offset = x_off
        self.y_offset = y_off
        self.ptr = ptr
    def update(self, loc):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''        
        if self.index >= len(self.images):
            self.kill()
        elif self.ptr.counter%3 == 0:
            self.image = self.images[self.index]
            self.index += 1
        (x_loc,y_loc) = loc
        self.rect.center = (x_loc + self.x_offset, y_loc + self.y_offset)

class Shield (pygame.sprite.Sprite ):
    '''
        used to track shield info, health is max health for shield
    '''
    def __init__( self, health, ptr ):
        pygame.sprite.Sprite.__init__( self )
        self.image, self.rect = load_image( dataname("shipshield.png"), -1, True )
        self.max_health = health
        self.health = health
        self.respawn = True
        self.respawn_count = 500
        self.respawn_timer = self.respawn_count
        self.ptr = ptr        
    def update ( self ):
        #shield should not be viewable
        if self.respawn == True and (self.health <= 0):
            self.remove(self.ptr.shields) # removes shield if not right role or Stuff.ship destroyed
            if self.health <= 0: # shield has been destroyed
                self.respawn = False
        #shield is now regenerating
        elif self.respawn == False:  
            self.respawn_timer -= 1
            #shield has regenerated
            if self.respawn_timer <= 0:
                  self.ptr.shields.add(MovingAnimation(200,300,150,150,'heal_strip17.png',self.ptr ))
                  self.respawn = True
                  self.respawn_timer = self.respawn_count
                  self.health = self.max_health
        else:
            #deploy shield
            self.add(self.ptr.shields)
            (x_loc,y_loc) = self.ptr.Ship.rect.center
            self.rect.center = ( x_loc, y_loc-1)
        if self.ptr.counter%250 == 0:
            if self.health < self.max_health and self.respawn == True:
                self.health += 1

class Overlay (pygame.sprite.Sprite):
    def __init__(self,image,rect,xacc,yacc):
        pygame.sprite.Sprite.__init__( self )
        self.image = image
        self.rect = rect
        self.xacc = xacc
        self.yacc = yacc
        self.xvel = 0
        self.yvel = 0
    def update(self):
        self.xvel += self.xacc
        self.yvel += self.yacc
        self.rect.centerx += self.xvel
        self.rect.centery += self.yvel
        if self.rect.left >= SCREEN_W or self.rect.right < 0:
            self.kill()
        if self.rect.top >= SCREEN_H or self.rect.bottom < 0:
            self.kill()
            
class PowerupText (pygame.sprite.Sprite):
    def __init__(self,text,x,y,ptr):
        pygame.sprite.Sprite.__init__(self)
        self.ptr = ptr
        self.c = 255
        self.image = self.ptr.font.render(text,1,(255,self.c,self.c))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.timer = 0
        self.text = text
    def update(self):
        self.timer+=1
        if self.timer > 50:
            self.kill()
        if self.timer%5==0:
            self.c = 255 - self.c
        if self.timer <= 10:
            self.rect.centery -= 5
        self.image = self.ptr.font.render(self.text,2,(255,self.c,self.c))
        
