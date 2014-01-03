import os
import pygame
from pygame.locals import *

from localdata import *

class ScrollItem():
    def __init__(self,i,x,y):
        self.i=i
        self.x=x
        self.y=y
        self.active = True  # is this active? keep it for next update if true
        self.pz = False     # the "past zero" flag

# scrolling class for creating an object of scrolling data

class ScrollBG():
    def __init__(self,level):
        self.boss = False
        self.bg = level.bg
        self.done = False
        self.iterator = 0
        self.level = level
        self.parent=None
        self.elem=None
        self.sdata=list() # this is command list
        self.gdata=list() # grid data
        self.reset()
        self.flaglist = list()
        return
    
    # used to determine precedence of drawing this background
    def setfloor(self,data):
        self.zlevel=data
        return
    def setboss(self):
        self.sdata.append(('b'))
        return
    def setboss(self):
        self.sdata.append(('B'))
        return
    def addmusic(self,data):
        self.sdata.append(('m',data))
        return
    def addfade(self):
        self.sdata.append(('>'))
        return
    # a grid is defined as a surface and when to draw it
    def addgrid(self,i,l,x,y):
        self.gdata.append((i,l,x,y))
    # velocity command
    def addvel(self,x,y,z):
        self.sdata.append(('v',x,y,z))
        return
    # acceleration command
    def addacc(self,x,y,z):
        self.sdata.append(('a',x,y,z))
        return
    # rate command
    def addrate(self,x,y,z):
        self.sdata.append(('r',x,y,z))
        return
    # how many times to execute acceleration increase/decrease
    def addcount(self,x,y,z):
        self.sdata.append(('c',x,y,z))
        return
    # delta determines coefficient of scrolling rate
    def adddelta(self,x,y):
        # these represent float values which are coefficients to
        # scrolling
        self.sdata.append(('d',x,y))
        return
    # wait command
    def addwait(self,time):
        # this is just a wait processor for the queue purposes
        # it might be good to add a "wait 1" at the start of
        # each stage
        self.sdata.append(('w',time))
        return
    # stop actually resets all velocity/acceleration
    def addstop(self,time):
        # unlike wait, no movement actually takes place, this
        # essentially sets velocity to 0 when it occurs
        self.sdata.append(('s',time))
        return
    # enemy flock data
    def addflock(self,data):
        # this waits for a (mid)boss fight to end (or some kind of flag)
        self.sdata.append(('f',data))
        return
    # stage data has ended so don't iterate through anything more
    def addend(self):
        # sends a flag that the stage has ended
        self.sdata.append(('e'))
        return
    # independence flag (false means scrolling is based SOLELY on parent)
    def addind(self,data):
        if data=="true":
            self.independent=True
        else:
            self.independent=False
        return
    # parent is a ScrollBG type
    def addparent(self,data):
        self.parent = data
        return
    # master loop add
    def addmloop(self,pos,count):
        self.gdata.append((None,0,pos,count))

    # update routine
    def update(self):
        # we can run this part regardless of [s]
        if self.xcount > 0:
            if self.xratecnt > 0:
                self.xratecnt = self.xratecnt - 1
                if self.xratecnt == 0:
                    self.xvel=self.xvel+self.xacc
                    self.xcount = self.xcount - 1
                    self.xratecnt = self.xrate
        if self.ycount > 0:
            if self.yratecnt > 0:
                self.yratecnt = self.yratecnt - 1
                if self.yratecnt == 0:
                    self.yvel=self.yvel+self.yacc
                    self.ycount = self.ycount - 1
                    self.yratecnt = self.yrate

        # iterator through commands
        for cmd in range(self.currcmd,len(self.sdata)):
            self.currcmd = cmd
            sdata = self.sdata[cmd]
            if self.timeactive == True:
                self.time = self.time - 1
                if self.time > 0:
                    break
                else:
                    self.currcmd = self.currcmd + 1
                    self.timeactive = False
                    continue
            if sdata[0]=='w' or sdata[0]=='s':
                if self.timeactive == False:
                    self.time = sdata[1]
                    self.timeactive = True
                if sdata[0]=='s':
                    self.xvel=0
                    self.yvel=0
                    self.zvel=0
                    self.xacc=0
                    self.yacc=0
                    self.xrate=0
                    self.yrate=0
                    self.xcount=0
                    self.ycount=0
                    self.xratecnt=0
                    self.yratecnt=0
                break
            elif sdata[0]=='v':
                self.xvel=sdata[1]
                self.yvel=sdata[2]
            elif sdata[0]=='a':
                self.xacc=sdata[1]
                self.yacc=sdata[2]
            elif sdata[0]=='r':
                self.xrate=sdata[1]
                self.yrate=sdata[2]
                self.xratecnt=sdata[1]
                self.yratecnt=sdata[2]
            elif sdata[0]=='c':
                self.xcount=sdata[1]
                self.ycount=sdata[2]
            elif sdata[0]=='d':
                self.xdelta=sdata[1]
                self.ydelta=sdata[2]
            elif sdata[0]=='f':
                self.flocks.append(sdata[1])
            elif sdata[0]=='e':
                if self.done == False:
                    self.done == True
                    self.flaglist.append(('e',0))
                break
            elif sdata[0]=='m':
                self.flaglist.append(('m',sdata[1]))
            elif sdata[0]=='b':
                self.flaglist.append(('b'))
            elif sdata[0]=='B':
                if self.boss == True:
                    break
            else:
                break
            self.currcmd = self.currcmd + 1

    def postupdate(self):
        # postfix if we are not independent womenz who dont need no man
        if self.independent == False:
            self.xvel = self.parent.xvel * self.xdelta
            self.yvel = self.parent.yvel * self.ydelta
        elif self.parent != None:
            self.xvel = self.xvel + (self.parent.xvel*self.xdelta)
            self.yvel = self.yvel + (self.parent.yvel*self.xdelta)
        # now iterate through list of data and update
        i = 0

        # want to divide this up
        # iterate through and update current grids in the queue
        while i < len(self.cgrids):
            #this can dynamically update based on if we add
            #another grid on the way
            currgrid=self.cgrids[i]
            yoff=currgrid.y
            currgrid.x = currgrid.x + self.xvel
            currgrid.y = currgrid.y + self.yvel
            if currgrid.y > 0 and currgrid.pz == False:
                currgrid.pz = True
                # if this is a loopable, we create a new
                # grid, we do this by checking the current
                # iterator
                # interior loop check
                if self.iterator >= len(self.gdata):
                    break
                gdata = self.gdata[self.iterator]
                if gdata[1] > 0:
                    self.loopcount = self.loopcount - 1
                    if self.loopcount == 0:
                        self.iterator += 1
                while self.iterator < len(self.gdata):
                    gdata = self.gdata[self.iterator]
                    # loop command:
                    # remember tokens are:
                    # [None] [cmd] [loop start pos] [count]
                    if gdata[0] == None:
                        self.mloop += 1
                        # we may have encountered a looping command
                        if gdata[3] == 0 or self.mloop < gdata[3]:
                            if gdata[3] > 0:
                                if self.mloop > gdata[3]:
                                    self.iterator += 1
                                    self.mloop = 0
                                    break
                                else:
                                    self.iterator = gdata[2]
                                    continue
                            else:
                                self.iterator = gdata[2]
                                continue
                        else:
                            self.iterator+=1
                            break
                    self.cgrids.append(ScrollItem(gdata[0],
                                                   gdata[2]+self.xorigin,
                                                   yoff+gdata[3]))
                    if self.loopcount <=0:
                        self.loopcount = gdata[1]
                    break
            if currgrid.y > SCREEN_H:
                currgrid.active = False
            i = i+1
                
        # there's nothing in queue yet, and we're just starting
        if self.iterator < len(self.gdata) and len(self.cgrids) <= 0:
            gdata = self.gdata[0]
            self.cgrids.append(ScrollItem(gdata[0],
                                          gdata[2]+self.xorigin,
                                          gdata[3]))
            self.loopcount = gdata[1]

        # adjustment for horizontal scrolling
        self.xorigin = self.xorigin + self.xvel
        newcgrids = list()
        for c in self.cgrids:
            if c.active == True:
                newcgrids.append(c)
        self.cgrids = newcgrids
        return

    # drawing routine. we don't need to modify this, i think
    def getdrawing(self):
        for e in self.cgrids:
            #if e.i == None: break
            or_w = e.i.get_width()
            or_h = e.i.get_height()
            # checking if past the screen boundaries to the bottom and right
            if e.x > SCREEN_W or e.y > SCREEN_H:
                continue
            if e.x < 0:
                or_x = e.x * (-1)
                if or_x >= e.i.get_width(): continue
                dest_x = 0
                if or_x > 0:
                    or_w = or_w - or_x
                    if or_w > SCREEN_W:
                        or_w = SCREEN_W
            else:
                or_x = 0
                dest_x = e.x
                if dest_x + or_w > SCREEN_W:
                    or_w = SCREEN_W - dest_x

            if e.y < 0:
                or_y = e.y * (-1)
                if or_y >= e.i.get_height(): continue
                dest_y = 0
                if or_y > 0:
                    or_h = or_h - or_y
                    if or_h > SCREEN_H:
                        or_h = SCREEN_H
            else:
                or_y = 0
                dest_y = e.y
                if dest_y + or_h > SCREEN_H:
                    or_h = SCREEN_H - dest_y

            if or_w <= 0 or or_h <= 0:
                continue
            # to make sure it's been put on the screen, yet
            sub = e.i.subsurface(or_x,or_y,or_w,or_h)
            self.bg.subsurface(dest_x,dest_y,or_w,or_h).blit(sub,sub.get_rect())
        return
    
    def reset(self):
        self.flocks = list()
        self.xorigin=0                      # our "up vector"
        self.zlevel=0                       # layer level
        self.timeactive=False
        self.iterator=0
        self.loopcount=0
        self.ddata=list() # drawn data?
        self.cgrids = list()
        self.independent=True
        self.loop=False                     # one grid loop
        self.mloop=0                        # master loop count

        # velocity
        self.xvel=0
        self.yvel=0

        # acceleration
        self.xacc = 0
        self.yacc = 0

        # rate of acceleration
        self.xrate = 0
        self.yrate = 0

        # time interval of rate (we should go up to this #)
        self.xratecnt = 0
        self.yratecnt = 0

        # current count down of rate
        self.xcount = 0
        self.ycount = 0

        # delta
        self.xdelta = 1
        self.ydelta = 1

        # time is used for 'wait' or 'stop'
        self.time = 0

        # used for sdata[index]
        self.currcmd = 0

        # used for boss fight, 1 = wait until flag given
        self.flag = False   
        return

    def getflock(self):
        # delivers the flock
        if len(self.flocks) < 1:
            return None
        t = (self.flocks,self)
        self.flocks = list()
        return t

    def getflags(self):
        t = self.flaglist
        self.flaglist = list()
        return t
    
