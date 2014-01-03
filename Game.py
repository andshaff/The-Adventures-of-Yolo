import os, pygame, random, math
from pygame.locals import *
from general import *
from Sprites import *
from level import *
from drones import *
from enemy import *
from weapons import *
from enemproj import *
from various import *

class Game():
    def __init__(self, screen, background, clock):
        self.font = pygame.font.Font(dataname("arial.ttf"), 20)
        self.endless = False
        self.screen = screen
        self.screennum = 1
        self.background = background
        self.clock = clock
        self.mode = 0
        self.shotsfired = 0
        self.shotrecharge = 0
        self.score = 0
        self.diff1 = 1
        self.diff2 = 1

        # system graphics
        self.optiongfx = list()
        self.selectgfx = list()
        self.equipgfx = list()
        self.equiphgfx = list()
        self.weapongfx = list()
        self.soundlist = list()

        # graphics
        print "Loading title gfx..."
        self.bg = pygame.image.load(dataname("space.png")).convert()
        self.title = pygame.image.load(dataname("Title.png")).convert_alpha()
        self.optiongfx.append(pygame.image.load(dataname('NewGame.png')).convert_alpha())
        self.optiongfx.append(pygame.image.load(dataname('EndlessMode.png')).convert_alpha())
        self.optiongfx.append(pygame.image.load(dataname('Options.png')).convert_alpha())
        self.selectgfx.append(pygame.image.load(dataname('NewGameSelected.png')).convert_alpha())
        self.selectgfx.append(pygame.image.load(dataname('EndlessModeSelected.png')).convert_alpha())
        self.selectgfx.append(pygame.image.load(dataname('OptionsSelected.png')).convert_alpha())
        self.orientsel=pygame.image.load(dataname('orient1.png')).convert_alpha()
        self.orientnon=pygame.image.load(dataname('orient2.png')).convert_alpha()
        self.orientbox=pygame.image.load(dataname('orientselector.png')).convert_alpha()
        self.weaponsel=pygame.image.load(dataname('weapon1.png')).convert_alpha()
        self.weaponnon=pygame.image.load(dataname('weapon2.png')).convert_alpha()
        self.weaponbox=pygame.image.load(dataname('weaponselect.png')).convert_alpha()
        self.bulletdata=load_image_alpha(dataname("yellowshot.png"))
        self.meterbox = pygame.image.load(dataname("meterbox.png")).convert_alpha()
        self.meter1 = pygame.image.load(dataname("meter1.png")).convert()
        self.meter2 = pygame.image.load(dataname("meter2.png")).convert()

        # general sound effects
        print "Loading sounds..."
        self.soundlist.append(load_sound( 'explosion.wav' ))
        self.soundlist.append(load_sound( 'l_explosion.wav' ))
        self.soundlist.append(load_sound( 'm_explosion.wav' ))
        self.soundlist.append(load_sound('e_hit.wav'))
        self.soundlist.append(load_sound('s_hit.wav'))
        self.soundlist.append(load_sound('ship_hit.wav'))
        self.soundlist.append(load_sound('ship_explosion.wav'))
        
        # explosion loading
        # this will reduce choppy frames on the playing end
        self.explist = list()
        self.explist.append(load_sliced_sprites(35,35,dataname("explode_small.png"), -1))
        self.explist.append(load_sliced_sprites(50,50,dataname("explode_medium.png"), -1))
        self.explist.append(load_sliced_sprites(75,75,dataname("explode.png"), -1))
        self.explist.append(load_sliced_sprites(35,35,dataname("e_explosion_small.png"), -1, True))
        self.explist.append(load_sliced_sprites(75,75,dataname("e_explosion.png"), -1, True))
        self.explist.append(load_sliced_sprites(125,125,dataname("e_explosion_big.png"), -1, True))
        self.explist.append(load_sliced_sprites(75,75,dataname("starbright.png"), -1, True))
        self.explist.append(load_sliced_sprites(125,125,dataname("starbright_big.png"), -1, True))
        self.explistprop = list()
        self.explistprop.append(35)
        self.explistprop.append(50)
        self.explistprop.append(75)
        self.explistprop.append(35)
        self.explistprop.append(75)
        self.explistprop.append(125)
        self.explistprop.append(75)
        self.explistprop.append(125)

        # just some neat transition stuff
        self.overlays = pygame.sprite.OrderedUpdates()

    def start(self):
        select = 0
        music = dataname("MainTitle.ogg")
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
        while True:
            for event in pygame.event.get():
                # doing it this way prevents key repeat faults
                keys = pygame.key.get_pressed()
                if keys[K_ESCAPE]:
                    return
                if keys[K_RETURN]:
                    self.selectmode(select)
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)
                if keys[K_UP]:
                    select -= 1
                    if select < 0:
                        select = 1
                if keys[K_DOWN]:
                    select += 1
                    if select > 1:
                        select = 0
            self.titledisplay(select)

    def selectmode(self,select):
        if select == 0:
            # setting up equipment
            if self.equipmode() == False:
                return
            self.campaignmode()
        elif select == 1:
            if self.equipmode() == False:
                return
            self.endlessmode()
        elif select == 2:
            self.optionsmode()
        return

    def titledisplay(self,select):
        self.background.blit(self.bg,(0,0))
        self.background.blit(self.title,(100,100))
        y = 300
        for i in range(0,2):
            if select == i:
                self.background.blit(self.selectgfx[i],(250,y))
            else:
                self.background.blit(self.optiongfx[i],(250,y))
            y += 100
        self.screen.blit(self.background,(0,0))
        pygame.display.flip()
        return

    def optionsmode(self):
        pass

    def campaignmode(self):
        o1 = self.background.subsurface(0,0,SCREEN_W/2,SCREEN_H-1)
        o2 = self.background.subsurface(SCREEN_W/2+1,0,SCREEN_W-(SCREEN_W/2+1),SCREEN_H-1)
        o3 = o2.get_rect()
        o3.left += SCREEN_W/2+1
        self.overlays.add(Overlay(o1,o1.get_rect(),-2,0))
        self.overlays.add(Overlay(o2,o3,2,0))
        self.diff1 = 1
        self.diff2 = 1
        self.endless = False
        self.score = 0
        self.shotsfired = 0
        self.shotshit = 0
        self.speed = 5
        self.power = 1
        self.level = 1
        self.extstrength=0
        # variable setup
        while self.level < 5:
            self.Ship = Player(25,self)
            self.shield = Shield(30,self)
            if self.play(self.level) == False:
                return
            #diff1 and diff2 become a ratio to shorten the rate of
            # fire for enemies, to increase their difficulty
            self.level+=1
            self.diff1=(self.level)*5
            self.diff2=(((self.level)**(self.level-1))+1)*5
        self.ending()

    def endlessmode(self):
        o1 = self.background.subsurface(0,0,SCREEN_W/2,SCREEN_H-1)
        o2 = self.background.subsurface(SCREEN_W/2+1,0,SCREEN_W-(SCREEN_W/2+1),SCREEN_H-1)
        o3 = o2.get_rect()
        o3.left += SCREEN_W/2+1
        self.overlays.add(Overlay(o1,o1.get_rect(),-2,0))
        self.overlays.add(Overlay(o2,o3,2,0))
        self.diff1 = 1
        self.diff2 = 1
        self.endless = True
        self.score = 0
        self.shotsfired = 0
        self.shotshit = 0
        self.speed = 5
        self.power = 1
        self.Ship = Player(25,self)
        self.shield = Shield(30,self)
        self.shotsfired = 0
        self.extstrength=0

        # variable setup
        self.counter = 0
        self.boss = False
        self.bossdefeated = False
        self.exitstage = False

        # game loop
        self.play(99)

        return

    def equipmode(self):
        #self.equipgfx
        #   0   standard cannon
        #   1   concussive missle
        #   2   homing missle
        #   3   laser beam
        self.weaponmode = 0
        self.dronemode = 0
        select=0
        orientselect=0
        weaponselect=0
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if keys[K_RETURN]:
                    self.dronemode=orientselect
                    self.weaponmode=weaponselect
                    return True
                if keys[K_UP] or keys[K_DOWN]:
                    select = 1-select
                if keys[K_LEFT]:
                    if select == 0:
                        orientselect-=1
                        if orientselect<0:
                            orientselect=5
                    if select == 1:
                        weaponselect-=1
                        if weaponselect<0:
                            weaponselect=2
                if keys[K_RIGHT]:
                    if select == 0:
                        orientselect+=1
                        if orientselect>5:
                            orientselect=0
                    if select == 1:
                        weaponselect+=1
                        if weaponselect>2:
                            weaponselect=0
                if event.type == KEYUP and event.key == K_ESCAPE:
                    return False
            self.screen.fill(0)
            self.background.fill(0)
            if select==0:
                self.background.blit(self.orientsel,(100,100))
                self.background.blit(self.weaponnon,(100,300))
            else:
                self.background.blit(self.orientnon,(100,100))
                self.background.blit(self.weaponsel,(100,300))
            self.background.blit(self.orientbox,(98+(100*orientselect),98))
            self.background.blit(self.weaponbox,(98+(200*weaponselect),298))
            self.screen.blit(self.background,(0,0))
            pygame.display.flip()
        return True

    def play(self,level):
        # stop previous music
        pygame.mixer.music.stop()
        # load level data
        leveldata = Level(level,self.screen)
        gameover = False
        stageexit = False
        stageexitdone = False
        exitvel = 1.0
        self.introcount = 40
        screenrecharge = 0

        self.generalsetup()

        # game loop
        while True:
            ### i guess we start with the count rather than end with it?
            self.counter+=1
            if self.Ship.health <= 0:
                gameover = True

            # code doesn't seem to work properly unless i put it here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYUP:
                    if event.key == K_ESCAPE:
                        return False
                    if event.key == K_h:
                        # changes some drone orientations
                        for d in self.drones.sprites():
                            if d.change == False:
                                d.changemode()
                    if event.key == K_p:
                        self.power+=1
                        if self.power>10:
                            self.power=10
                    if event.key == K_i:
                        stageexitdone = True

            # we should grab data from stage here
            leveldata.update()
            for f in leveldata.getflags():
                if f[0] == 'e':
                    stageexit = True

            ### invulnerable intro
            if self.introcount > 0:
                self.Ship.rect.top-=5
                self.introcount-=1
                if self.introcount == 0:
                    self.Ship.ctrl=True
            elif stageexit and stageexitdone == False and self.endless == False:
                self.Ship.ctrl = False
                self.Ship.invincible = True
                self.Ship.invtime = 100
                self.Ship.rect.centery -= exitvel
                exitvel += .5
                if self.Ship.rect.bottom < -0:
                    stageexitdone = True
                    for d in self.drones.sprites():
                        if d.rect.bottom > 0:
                            stageexitdone = False
            else:
                self.getcontrols()
                if self.endless:
                    # increasing difficulty on endless
                    self.feedback()
                    if self.counter%500==0:
                        self.diff1+=1
                        self.diff2=(self.diff1**2)/2
                    self.randomenemy()
                else:
                    self.feedback()
                    self.randomenemy()


                    ### things we can do if ship is controllable
                    # originally wanted the leveldata object to bring in enemies here
                    
            # check collision
            self.collisioncheck()
            
            ### updating environments
            # keep in mind: explosion updates should occur before enemy updates
            self.player.update()
            self.shields.update()
            self.drones.update()
            self.lasers.update()
            self.missiles.update()
            self.spray.update()
            self.enemies.update()
            self.enemproj.update()
            self.enemmiss.update()
            self.enemtorp.update()
            self.explosions.update()
            self.powerups.update(self.counter)
            self.overlays.update()

            ### draw everything
            self.screen.fill(0)
            leveldata.draw()
            self.powerups.draw(self.screen)
            self.lasers.draw(self.screen)
            self.missiles.draw(self.screen)
            self.spray.draw(self.screen)
            if self.Ship.blink == 0:
                self.shields.draw(self.screen)
                self.drones.draw(self.screen)
                self.player.draw(self.screen)
            # enemy stuff
            self.enemies.draw(self.screen)
            self.enemproj.draw(self.screen)
            self.enemmiss.draw(self.screen)
            self.enemtorp.draw(self.screen)
            self.explosions.draw(self.screen)
            if gameover:
                self.gameover()
            elif stageexitdone:
                self.background.blit(self.screen,(0,0))
                o1 = self.background.subsurface(0,0,SCREEN_W/2,SCREEN_H-1)
                o2 = self.background.subsurface(SCREEN_W/2+1,0,SCREEN_W-(SCREEN_W/2+1),SCREEN_H-1)
                o3 = o2.get_rect()
                o3.left += SCREEN_W/2+1
                self.overlays.add(Overlay(o1,o1.get_rect(),-2,0))
                self.overlays.add(Overlay(o2,o3,2,0))
                self.player.empty()
                self.drones.empty()
                return True
            else:
                self.drawinterface()
            self.overlays.draw(self.screen)

            # screenshot code (leave this commented out)
            #if screenrecharge > 0:
            #    screenrecharge -= 1
            #if self.keys[K_q] and screenrecharge == 0:
            #    screenname = "screen%d.png" % self.screennum
            #    pygame.image.save(self.background,screenname)
            #    screenrecharge = 120
            #    self.screennum += 1
            
            ### blit
            pygame.display.flip()


            ### synchronize on clock
            self.clock.tick(60)

        # return true if we didn't hit escape or die
        pygame.mixer.music.stop()
        return True

    def gameover(self):
        hs = SCREEN_W/2
        gameoverrender1 = self.font.render("GAME OVER",5,(255,255,255))
        gameoverrender2 = self.font.render("GAME OVER",5,(0,0,0))
        self.screen.blit(gameoverrender2,(hs-gameoverrender2.get_width()/2+1,151))
        self.screen.blit(gameoverrender1,(hs-gameoverrender2.get_width()/2,150))
        
        scoretext = "Final score: %d" % self.score
        scorerender = self.font.render(scoretext,5,(0,0,0))
        self.screen.blit(scorerender,(hs-scorerender.get_width()/2+1,201))
        self.screen.blit(self.font.render(scoretext,5,(255,255,255)),(hs-scorerender.get_width()/2,200))

        acctext = "Shots fired: %d" % self.shotsfired
        accrender = self.font.render(acctext,5,(0,0,0))
        self.screen.blit(accrender,(hs-accrender.get_width()/2+1,251))
        self.screen.blit(self.font.render(acctext,5,(255,255,255)),(hs-accrender.get_width()/2,250))

        if self.shotsfired <= 0:
            accpct = 0.0
        else:
            accpct = 100.0*(float(self.shotshit)/float(self.shotsfired))
        acctext = "Accuracy: %%%.2f (%d/%d)" % (accpct,self.shotshit,self.shotsfired)
        accrender = self.font.render(acctext,5,(0,0,0))
        self.screen.blit(accrender,(hs-accrender.get_width()/2+1,301))
        self.screen.blit(self.font.render(acctext,5,(255,255,255)),(hs-accrender.get_width()/2,300))
        
    
    def ending(self):
        pass

    def addmissile(self,origin):
        self.missiles.add(Missile(origin,self,False))
        self.shotsfired+=1

    def addexplosion(self,choice,x,y):
        # index of explosions:
        # 0 - explode_small.png
        # 1 - explode_medium.png
        # 2 - explode.png
        # 3 - e_explosion_small.png
        # 4 - e_explosion.png
        # 5 - e_explosion_big.png
        # 6 - starbright.png
        # 7 - starbright_big.png
        d = self.explistprop[choice]
        self.explosions.add(Explosion(x,y,d,d,self.explist[choice],self))

    def collisioncheck(self):
        ratio = pygame.sprite.collide_rect_ratio(.9)
        for p in self.powerups.sprites():
            if ratio(self.Ship,p):
                p.kill()
                self.power+=1
                (x,y) = p.rect.center
                if self.power>10:
                    self.score+=1000
                    self.power=10
                    self.extstrength+=1
                    self.overlays.add(PowerupText("Attack Up!",x,y,self))
                else:
                    self.overlays.add(PowerupText("Weapon Up!",x,y,self))
        # check the shield and character sprite
        if self.Ship.invincible == False:
            for e in self.enemies.sprites():
                if self.Ship.health <= 0:
                    break
                if self.shield.health > 0:
                    if ratio(self.shield,e):
                        self.soundlist[4].play()
                        self.shield.health-=1
                        e.explode()
                        e.kill()
                else:
                    if ratio(self.Ship,e):
                        self.soundlist[5].play()
                        damage = e.health
                        e.hit(self.Ship.health,2)
                        self.Ship.hit(damage)
            for e in self.enemproj.sprites():
                if self.Ship.health <= 0:
                    break
                if self.shield.health > 0:
                    if ratio(self.shield,e):
                        self.soundlist[4].play()
                        self.shield.health-=1
                        e.kill()
                else:
                    if ratio(self.Ship,e):
                        self.soundlist[5].play()
                        e.kill()
                        self.Ship.hit(1)
            for e in self.enemtorp.sprites():
                if self.Ship.health <= 0:
                    break
                if self.shield.health > 0:
                    if ratio(self.shield,e):
                        self.soundlist[4].play()
                        self.shield.health-=3
                        e.kill()
                else:
                    if ratio(self.Ship,e):
                        self.soundlist[5].play()
                        e.kill()
                        self.Ship.hit(3)
            for e in self.enemmiss.sprites():
                if self.Ship.health <= 0:
                    break
                if self.shield.health > 0:
                    if ratio(self.shield,e):
                        self.soundlist[4].play()
                        self.shield.health-=5
                        e.kill()
                else:
                    if ratio(self.Ship,e):
                        self.soundlist[5].play()
                        e.kill()
                        self.Ship.hit(5)
        # check if our projectiles hit their projectiles OR the enemy
        # first, laser
        for f in self.lasers.sprites():
            laserhit = False
            for e in self.enemies.sprites():
                if ratio(f,e):
                    if laserhit == False:
                        laserhit = True
                        self.shotshit+=1
                    e.hit(self.power+self.extstrength,2)
        # standard bullet
        for f in self.spray.sprites():
            projectileflag = False
            for e in self.enemies.sprites():
                if ratio(f,e):
                    e.hit(5+self.extstrength,0)
                    f.kill()
                    self.shotshit+=1
            if projectileflag: continue
            for e in self.enemmiss.sprites():
                if ratio(f,e):
                    e.hit(2)
                    f.kill()
                    self.shotshit+=1
                    projectileflag=True
            if projectileflag: continue
            for e in self.enemproj.sprites():
                if ratio(f,e):
                    e.hit(3)
                    f.kill()
                    self.shotshit+=1
                    break
        # missiles
        for f in self.missiles.sprites():
            projectileflag = False
            for e in self.enemies.sprites():
                if ratio(f,e):
                    #explosion
                    e.hit(25+self.extstrength,0)
                    f.explode()
                    self.shotshit+=1
                    projectileflag=True
            if projectileflag: continue
            for e in self.enemmiss.sprites():
                if ratio(f,e):
                    # explosion
                    e.kill()
                    f.explode()
                    self.shotshit+=1
                    projectileflag=True
            if projectileflag: continue
            for e in self.enemproj.sprites():
                if ratio(f,e):
                    #explosion
                    e.kill()
                    f.explode()
                    self.shotshit+=1
                    break
        # drones
        for d in self.drones.sprites():
            for e in self.enemies.sprites():
                if ratio(d,e):
                    e.hit(3,0)
            for e in self.enemmiss.sprites():
                if ratio(d,e):
                    e.hit(10)
            for e in self.enemproj.sprites():
                if ratio(d,e):
                    e.kill()
            for e in self.enemtorp.sprites():
                if ratio(d,e):
                    e.hit(10)

    def randomenemy(self):
        if len(self.enemies.sprites())<20:
            #powerups!
            if self.counter == 1000 or self.counter%3500 == 0:
                #print "added powerup"
                e = EnemyPowerup(random.randint(75,SCREEN_W-75),-50,self)
                self.enemies.add(e)
            #kamikaze 
            if self.counter%150 == 0:
                #print "added drone"
                e = EnemyDrone(random.randint(75,SCREEN_W-75),-50,self)
                self.enemies.add(e)
            #fighter
            if self.counter%250 == 0:
                #print "added fighter"
                e = EnemyFighter(random.randint(75,SCREEN_W-75),-50,self)                
                self.enemies.add(e)
            #gunship
            if self.counter%550 == 0 or self.counter > 3000 and self.counter%250 == 0 :
                #print "added gunship"
                e = EnemyGunship(random.randint(75,SCREEN_W-75),-50,self)
                self.enemies.add(e)
            #missile gunship
            if self.counter > 2000 and self.counter%950 == 0 :
                #print "added missile gunship"
                e = MissileGunship(random.randint(75,SCREEN_W-75),-50,self)                
                self.enemies.add(e)
            #bomber
            if self.counter%750 == 0:
                #print "added bomber"
                e = EnemyBomber(random.randint(75,SCREEN_W-75),-50,self)
                self.enemies.add(e)

    def generalsetup(self):
        # setup our pygame sprites
        self.player = pygame.sprite.OrderedUpdates( )
        self.drones = pygame.sprite.OrderedUpdates( )
        self.lasers = pygame.sprite.OrderedUpdates( )
        self.missiles = pygame.sprite.OrderedUpdates( )
        self.spray = pygame.sprite.OrderedUpdates( )
        self.homing = pygame.sprite.OrderedUpdates( )
        self.enemies = pygame.sprite.OrderedUpdates( )
        self.enemproj = pygame.sprite.OrderedUpdates( )
        self.enemmiss = pygame.sprite.OrderedUpdates( )
        self.enemtorp = pygame.sprite.OrderedUpdates( )
        self.explosions = pygame.sprite.OrderedUpdates( )
        self.powerups = pygame.sprite.OrderedUpdates( )
        self.shields = pygame.sprite.OrderedUpdates( )

        self.counter = 0

        # player setup
        self.shields.add(self.shield)
        self.player.add(self.Ship)
        self.plyrvelx = 0       # these are normalized translations
        self.plyrvely = 0       # ie interval of [-1,1]
        self.Ship.ctrl = False
        self.Ship.setinv(120)
        self.Ship.blinkon
        self.shotrecharge = 0
                
        # drone setup
        if self.dronemode==0:
            # basic mode
            self.drones.add(Drone(65,0,0,self.Ship))
            self.drones.add(Drone(-65,0,0,self.Ship))
            self.drones.add(Drone(0,45,0,self.Ship))
        elif self.dronemode==1:
            # condensed
            self.drones.add(Drone(15,0,0,self.Ship))
            self.drones.add(Drone(-15,0,0,self.Ship))
            self.drones.add(Drone(0,-45,0,self.Ship))
        elif self.dronemode==2:
            # rotation
            self.drones.add(RotDrone(0,self.Ship))
            self.drones.add(RotDrone(120,self.Ship))
            self.drones.add(RotDrone(240,self.Ship))
        elif self.dronemode==3:
            # snake
            d1 = TrailDrone(10,0,self.Ship)
            d2 = TrailDrone(10,0,d1)
            d3 = TrailDrone(10,0,d2)
            d1.rect.center = self.Ship.rect.center
            d2.rect.center = self.Ship.rect.center
            d3.rect.center = self.Ship.rect.center
            self.drones.add(d3)
            self.drones.add(d2)
            self.drones.add(d1)
        elif self.dronemode==4:
            # original(ish) mode
            self.drones.add(LatDrone(65,15,self.Ship))
            self.drones.add(LatDrone(-65,-15,self.Ship))
            self.drones.add(Drone(0,0,0,self.Ship))
        else:
            # wide mode
            self.drones.add(LatDrone(65,150,self.Ship))
            self.drones.add(LatDrone(-65,-150,self.Ship))
            self.drones.add(Drone(0,0,0,self.Ship))
        return

    def getcontrols(self):
        ### get controls
        self.keys = pygame.key.get_pressed()
        # y movement (up and down)
        if self.keys[K_w]: self.plyrvely = -1
        elif self.keys[K_s]: self.plyrvely = 1
        else: self.plyrvely = 0
        # x movement (left and right)
        if self.keys[K_d]: self.plyrvelx = 1
        elif self.keys[K_a]: self.plyrvelx = -1
        else: self.plyrvelx = 0
        # weapon selector (cheating!)
        if self.keys[K_1]: self.weaponmode = 0
        if self.keys[K_2]: self.weaponmode = 1
        if self.keys[K_3]: self.weaponmode = 2
        if self.keys[K_4]: self.weaponmode = 3

    def drawinterface(self):
        liferatio = float(self.Ship.health) / float(self.Ship.max_health)
        shieldratio = float(self.shield.health) / float(self.shield.max_health)
        self.screen.blit(self.meter1.subsurface(0,0,300*liferatio,8),(40,610))
        self.screen.blit(self.meter2.subsurface(0,0,300*shieldratio,8),(40,619))
        self.screen.blit(self.meterbox,(10,609))
        scoretext = "SCORE: %d" % self.score
        self.screen.blit(self.font.render(scoretext,1,(0,0,0)),(11,11))
        self.screen.blit(self.font.render(scoretext,1,(255,255,255)),(10,10))
        if self.power >= 10:
            powertext = "POWER: MAX"
        else:
            powertext = "POWER: %d" % self.power
        self.screen.blit(self.font.render(powertext,1,(0,0,0)),(351,606))            
        self.screen.blit(self.font.render(powertext,1,(255,255,255)),(350,605))            
        if self.endless:
            #self.font.render("SURVIVAL",1,(0,0,0))
            modetext="SURVIVAL" 
            wavetext = "WAVE %d" % ((self.diff1+1)/2)
        else:
            modetext="CAMPAIGN"
            wavetext = "LEVEL %d" % self.level
            pass
        moderender = self.font.render(modetext,1,(0,0,0))
        adjustment = SCREEN_W - 10 - moderender.get_width()
        self.screen.blit(moderender,(adjustment+1,11))
        self.screen.blit(self.font.render(modetext,1,(255,255,255)),(adjustment,10))
        self.screen.blit(self.font.render(wavetext,1,(0,0,0)),(691,606))            
        self.screen.blit(self.font.render(wavetext,1,(255,255,255)),(690,606))                        
        return

    # handles shooting out the weapons
    def feedback(self):
        if self.shotrecharge > 0:
            self.shotrecharge-=1
        if self.Ship.ctrl == True:
            # shooting
            if self.keys[K_SPACE]:
                if self.weaponmode == 0 and self.shotrecharge<=0:
                    self.shotrecharge=15
                    for d in self.drones.sprites():
                        self.bulletgroup(d)
                elif self.weaponmode == 1:
                    # rather than wait for a recharge, we
                    # just count the amount of missiles onscreen
                    if len(self.missiles.sprites()) <= .9*self.power*4:
                        for d in self.drones.sprites():
                            for r in range(0,self.power):
                                self.shotsfired+=1
                                self.addmissile(d)
                elif self.weaponmode == 2:
                    for d in self.drones.sprites():
                        if d.laserready:
                            self.shotsfired+=1
                            self.lasers.add(Laser(d))
        return

    # defines the bullet group for the spray
    def bulletgroup(self,d):
        x = d.rect.centerx
        y = d.rect.centery
        if d.side == 0:
            self.shotsfired += self.power
            if self.power%2==0:
                self.spray.add(Spray(x-7,y-15,0))
                self.spray.add(Spray(x+7,y-15,0))
                for xs in range(1,int(self.power/2)):
                    # we can level up the straight shooter more than
                    # the spread shots
                    self.spray.add(Spray(x-7-(xs*14),y-15,0))
                    self.spray.add(Spray(x+7+(xs*14),y-15,0))
            else:
                self.spray.add(Spray(x,y-15,0))
                for xs in range(1,int((self.power+1)/2)):
                    self.spray.add(Spray(x-(xs*14),y-15,0))
                    self.spray.add(Spray(x+(xs*14),y-15,0))
        else:
            # side shots cannot increase in span beyond level 4 :(
            power = self.power
            if power > 4: power = 4
            self.shotsfired+=power
            if power>=1:
                self.spray.add(Spray(x,y-15,0))
            if power>=2: # 45
                self.spray.add(Spray(x,y-15,45*d.side))
            if power>=3: # 22.5
                self.spray.add(Spray(x,y-15,22.5*d.side))
            if power>=4: # 67.5
                self.spray.add(Spray(x,y-15,67.5*d.side))
        return

