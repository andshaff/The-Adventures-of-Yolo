## Import Modules
import os, pygame, random, math

## put commonly used in global namespace
from pygame.locals import *
from general import *
from enemproj import *
from various import *

class Enemy( pygame.sprite.Sprite ):
    def __init__(self,x,y,ptr,drop= False):
        pass
    def setup(self,x,y,ptr,drop= False):
        self.ptr = ptr
        self.max_health = self.health * (self.ptr.diff2*2.2)/(self.ptr.diff1*2)
        self.health = self.max_health
        self.ratecoefficient = float(self.ptr.diff1) / float(self.ptr.diff2)
        self.drop = drop
        self.rect.center = (x,y)
        self.position = self.rect.center
        self.mid_x = random.randint(50,SCREEN_W)
        self.mid_y = random.randint(100,SCREEN_H/3)
        self.end_x = random.randint(50,SCREEN_W)
        self.set_speed = 2
        self.speed = self.set_speed
        self.frequency = 2
        self.counter = 250
        #xbehavior,ybehavior,firebehavior here
        # health here
        self.max_health = self.health
        self.value = self.health**2*5
        self.firing_frequency = int(float(random.randint(45,100))*self.ratecoefficient)
        if self.firing_frequency <=6:
            self.firing_frequency=6
        self.firing_timer = self.firing_frequency
        self.counter = 250
        self.reached_midpt = False
    def update(self):
        (x_loc,y_loc) = self.rect.center
        (ship_x_loc, ship_y_loc) = self.ptr.Ship.rect.center

        #x loc behavior
        #0 - no x movement
        #1 - move to x midpoint
        #2 - attempt to ram player - speed double when close to y range
        if self.x_behavior == 1:
            if x_loc < self.mid_x - 25:
                x_loc += round(self.speed/2)
            elif x_loc > self.mid_x + 25:
                x_loc -= round(self.speed/2)
        if self.x_behavior == 2:
            if y_loc < ship_y_loc:
                if x_loc < ship_x_loc - 10:
                    x_loc += round(self.set_speed)
                elif x_loc > ship_x_loc + 10:
                    x_loc -= round(self.set_speed)
            if x_loc < abs(ship_x_loc+50):
                self.speed = 4
                self.frequency = 1
                
        #y loc behavior
        #0 - (default) move straight down at constant speed
        #1 - move straight down double speed at certain point
        #2 - move straight down double speed then slow down at certain point
        #3 - move straight down and pauses every 250 pixels for 100 units of time and fires
        #4 - move straight down to random upper y loc and hover in place until shot dead

        if self.y_behavior == 4:
            if y_loc >  self.mid_y:
                self.speed = 0

        if self.y_behavior == 3:
            if self.counter == 15:
                self.speed = 0
                self.counter -= 1
                self.firing_timer = 50
            elif self.counter == -165:
                self.firing_timer = 9999
                if self.y_behavior == 3:
                    self.speed = 2
                self.counter = SCREEN_H/3
            else:
                self.counter -= 1

        if self.y_behavior == 1:
            if y_loc >  self.mid_y:
                self.speed = 4
                self.frequency = 1

        if self.y_behavior == 2:
            if y_loc < self.mid_y:
                self.speed = 4
                self.frequency = 1
            else:
                self.speed = 2
                self.frequency = 2
                
        #move down
        y_loc += self.speed
            
        #control rate of animation
        if(self.ptr.counter%self.frequency == 0):
            self.rect.center = (x_loc,y_loc)

        # fires near current Stuff.ship position
        def homing ():
            adjacent = x_loc-ship_x_loc
            opposite = y_loc-ship_y_loc
        
            if adjacent == 0:
                if opposite > 0:
                    degree = 0
                else:
                    degree = 180
            elif opposite == 0:
                if adjacent > 0:
                    degree = 90
                else:
                    degree = 270
            else:
                degree = math.tanh(opposite/adjacent)                 

            degree = math.degrees(degree) + 90
        
            if(adjacent > 0):
                degree = -180+degree

            return degree        
        
        # fires shots depending on behavior
        # 0 - fires at player ship
        # 1 - fires straight down
        # 2 - fires down at 45 degree angles
        # 3 - fires at 90 degree angles on all four directions
        # 4 - fires at 45 degree angles in four directions 
        # 5 - fires a volley of slugs at player
        # 6 - fires missle straight down
        # 7 - fires missle at player
        # 8 - fires 4 missle down
        # 9 - fires volley of missles at player
        #10 - fires volley of torpedos at player
        #11 - fires torpedo at player
        if self.ptr.counter%self.firing_timer == 0:
            
            #SLUGS
            if self.fire_behavior == 0 or self.fire_behavior == 7: # fires near current Stuff.ship position
                 self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed, homing(),-1,3,False,self.ptr))
            elif self.fire_behavior == 1 : # proj down
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,180,-1,3,False,self.ptr))
            elif self.fire_behavior == 2 :  #fire proj SW and SE
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,135,-1,3,False,self.ptr))
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,225,-1,3,False,self.ptr))
            elif self.fire_behavior == 3: # Fire proj N, E, W, S
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,180,-1,3,False,self.ptr))
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,0,-1,3,False,self.ptr))
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,270,-1,3,False,self.ptr))
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,90,-1,3,False,self.ptr))
            elif self.fire_behavior == 4: # Fire proj N, E, W, S
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,135,-1,3,False,self.ptr))
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,225,-1,3,False,self.ptr))
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,45,-1,3,False,self.ptr))
                self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,-45,-1,3,False,self.ptr))
            elif self.fire_behavior == 5 or self.fire_behavior == 9 or self.fire_behavior == 10:
                if self.counter > 0:
                    if self.fire_behavior == 5:
                        self.ptr.enemproj.add(Animated_Projectile(x_loc-7, y_loc,15,15,"enemy_proj.png", 3 + self.speed,homing(),-1,3,False,self.ptr))        
                    elif self.fire_behavior == 9:
                        self.ptr.enemmiss.add(EnemyMissile("enemy_misslesp2.png", (x_loc, y_loc), 3, homing(),3, self.ptr, True))
                    else:
                        self.ptr.enemtorp.add(Animated_Projectile(x_loc-17, y_loc,50,50,"purple_blob.png", 2 + self.speed, homing(),-1,3,False,self.ptr))
                    self.firing_timer = 45
                    self.counter -= 50
                elif self.counter == 0:
                    self.firing_timer = 250
                    self.counter = 250


            # MISSLES
            if self.fire_behavior == 6:  # fires missle South
                self.ptr.enemmiss.add(EnemyMissile("enemy_misslesp2.png", (x_loc, y_loc), 3, 180,3, self.ptr, True))
            elif self.fire_behavior == 7 : # fires missle at player
                self.ptr.enemmiss.add(EnemyMissile("enemy_misslesp2.png", (x_loc, y_loc), 3, homing(),3, self.ptr, True))
            elif self.fire_behavior == 8 : # fires 4 missles south at player
                self.ptr.enemmiss.add(EnemyMissile("enemy_misslesp2.png", (x_loc+random.randint(5,15), y_loc+random.randint(5,15)), 3, 155,2,self.ptr,True))
                self.ptr.enemmiss.add(EnemyMissile("enemy_misslesp2.png", (x_loc+random.randint(-15,-5), y_loc+random.randint(5,15)), 3, -155,2,self.ptr, True))
                self.ptr.enemmiss.add(EnemyMissile("enemy_misslesp2.png", (x_loc+random.randint(-40,-20), y_loc+random.randint(20,40)), 3, 180,2,self.ptr, True))
                self.ptr.enemmiss.add(EnemyMissile("enemy_misslesp2.png", (x_loc+random.randint(20,40), y_loc+random.randint(5,15)), 3, 180,2,self.ptr,True))

            # TORPEDOS
            if self.fire_behavior == 11:
                self.ptr.enemproj.add(Animated_Projectile(x_loc, y_loc,50,50,"purple_blob.png", 4, homing(),-1,3,False,self.ptr))
          
        # kill Stuff.ship once off bottom of screen    
        if(self.rect.top > SCREEN_H + 50 ):
            self.die()    

    def hit (self, damage, d_type):
        (x_loc,y_loc) = self.rect.center
        self.health -= damage
        if self.health <= 0:
        
            self.ptr.score += self.value
            if d_type == 0:
                self.ptr.soundlist[0].play()
            elif d_type == 1:
                self.ptr.soundlist[2].play()
            elif d_type == 2:
                self.ptr.soundlist[1].play()
            self.explode()

            self.die()
        else:
            self.ptr.soundlist[3].play()
        

    #update enemy health and player shield health after collision
    def shield_hit (self):
        #Stuff.shield.health -= self.health
        self.health -= self.ptr.shield.max_health
        if self.health <= 0:
            self.die()
     
    def die (self):
        if self.drop == True:
            (x_loc,y_loc) = self.rect.center
            self.ptr.powerups.add(Powerup(x_loc-37,y_loc-37,75,75))
        self.kill()

    def explode(self):
        (x_loc,y_loc) = self.rect.center
        if self.max_health < 15:
            self.ptr.addexplosion(4,x_loc,y_loc)
            self.ptr.addexplosion(6,x_loc,y_loc)
            self.ptr.addexplosion(1,x_loc,y_loc)
        else:
            self.ptr.addexplosion(5,x_loc,y_loc)
            self.ptr.addexplosion(7,x_loc,y_loc)
            self.ptr.addexplosion(2,x_loc,y_loc)

class EnemyPowerup( Enemy ):
    def __init__(self,x,y,ptr,drop= True):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(dataname("powerup_ship.png"),-1,True)
        self.health = 10
        self.x_behavior = 0
        self.y_behavior = 3
        self.fire_behavior = -1
        self.setup(x,y,ptr,drop)

class EnemyDrone( Enemy ):
    def __init__(self,x,y,ptr,drop= False):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(dataname("enemy_drone.png"),-1,True)
        self.health = 5
        self.x_behavior = 2
        self.y_behavior = 0
        self.fire_behavior = -1
        self.setup(x,y,ptr,drop)

class EnemyFighter( Enemy ):
    def __init__(self,x,y,ptr,drop= False):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(dataname("fighter.png"),-1,True)
        self.health = 10
        self.x_behavior = random.randint(0,1)
        self.y_behavior = random.randint(0,2)
        self.fire_behavior = random.randint(0,1)
        self.setup(x,y,ptr,drop)

class EnemyGunship( Enemy ):
    def __init__(self,x,y,ptr,drop= False):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(dataname("gunship.png"),-1,True)
        self.health = 25
        self.x_behavior = random.randint(0,1)
        self.y_behavior = random.randint(2,4)
        self.fire_behavior = random.randint(2,11)
        self.setup(x,y,ptr,drop)

class MissileGunship( Enemy ):
    def __init__(self,x,y,ptr,drop= False):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(dataname("gunship.png"),-1,True)
        self.gameptr = ptr
        self.health = 25
        self.x_behavior = random.randint(0,1)
        self.y_behavior = random.randint(3,4)
        self.fire_behavior = random.randint(3,5)
        self.setup(x,y,ptr,drop)

class EnemyBomber( Enemy ):
    def __init__(self,x,y,ptr,drop= False):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(dataname("bomber.png"),-1,True)
        self.health = 35
        self.x_behavior = random.randint(0,1)
        self.y_behavior = 0
        self.fire_behavior = random.randint(8,10)
        self.setup(x,y,ptr,drop)
