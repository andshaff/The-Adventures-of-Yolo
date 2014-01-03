import os
import pygame
from pygame.locals import *

from ScrollBG import *
from various import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from localdata import *

class Level():
    def __init__(self,levelnum,bg):
        #now get the data file
        datafile = "data%s%d%s" % (os.sep,levelnum,".dat")
        mode = 0

        self.bg = bg
        self.images = list()
        self.elemdata = list()
        self.scrolldata = list()
        self.controldata = list()
        self.flockdata = list()
        self.flockq = list()
        self.controlcnt = 0
        self.xorigin = 0
        self.musiclist = list()
        self.outerflags = list()
        self.flaglist = list()

        with open(datafile) as data:
            print "Opening",datafile
            # now we read contents of file
            while(True):
                # read in a line of data
                line = data.readline()
                if len(line) == 1:
                    continue
                if len(line) == 0:
                    break
                if line[0] == '#':
                    continue
                tokens = list()
                for e in line.split(' '):
                    tokens.append(self.valueproc(e))
                if line[0] == "[":
                    if tokens[0]=="[Elements]":
                        print "Loading elements and animations"
                        mode=1
                    elif tokens[0]=="[Flock]":
                        print "Loading enemy data"
                        mode=2
                    elif tokens[0]=="[Scrolling]":
                        # most important part
                        print "Loading scrolling and event data"
                        mode=3
                    elif tokens[0]=="[Controller]":
                        # for now, this doesn't actually do shit, maybe it won't ever
                        # since there's no point yet
                        print "Loading sequential data"
                        mode=4
                    if len(tokens)>1:
                        print "Syntax error found"
                        return
                    continue
                if tokens[0] == "END":
                    # return to mode 0 if END is encountered
                    mode = 0
                    if len(tokens)>1:
                        print "Syntax error found"
                        return
                    continue
                if mode == 0:
                    # this is import and tile mode (our default mode)
                    if tokens[0] == "import":
                        impfilename = "data%s%s" % (os.sep,tokens[1])
                        try:
                            image = pygame.image.load(impfilename)
                        except pygame.error, message:
                            print tokens[1],"not found"
                            raise SystemExit, message
                        image = image.convert_alpha()
                        self.images.append(image)
                        print tokens[1],"loaded"
                    if tokens[0] == "music":
                        musfilename = dataname(tokens[1])
                        self.musiclist.append(musfilename)
                    if tokens[0] == "resize":
                        self.images[tokens[1]] = pygame.transform.scale(self.images[tokens[1]],(tokens[2],tokens[3]))
                    continue
                elif mode == 1:
                    # elements mode, defining any animated elements that appear onscreen
                    if tokens[0] == "addelem":
                        self.addelem = list()
                    elif tokens[0] == "elem":
                        # cmd imagedata xoffset yoff zoff frameval
                        self.addelem.append(('i',self.images[tokens[1]],tokens[2],tokens[3],tokens[4],tokens[5]))
                    elif tokens[0] == "endelem":
                        self.elemdata.append(self.addelem)
                    continue
                elif mode == 2:
                    # enemies mode aka "flock"
                    if tokens[0] == "addflock":
                        self.addflock = list()
                    elif tokens[0] == "endflock":
                        self.flockdata.append(self.addflock)
                    else:
                        # indice of enemy, x start, y start, z start
                        self.addflock.append((tokens[0],tokens[1],tokens[2],tokens[3]))
                    continue
                elif mode == 3:
                    # scrolling definition mode
                    if tokens[0] == "addbg":
                        self.addbg = ScrollBG(self)
                    elif tokens[0] == "grid":
                        # [elem] [loop] [initx] [inity] [initz]
                        self.addbg.addgrid(self.images[tokens[1]],tokens[2],tokens[3],tokens[4])
                    elif tokens[0] == "vel":
                        # velocity [x] [y] [z]
                        self.addbg.addvel(tokens[1],tokens[2],tokens[3])
                    elif tokens[0] == "acc":
                        self.addbg.addacc(tokens[1],tokens[2],tokens[3])
                    elif tokens[0] == "rate":
                        self.addbg.addrate(tokens[1],tokens[2],tokens[3])
                    elif tokens[0] == "count":
                        self.addbg.addcount(tokens[1],tokens[2],tokens[3])
                    elif tokens[0] == "delta":
                        self.addbg.adddelta(tokens[1],tokens[2])
                    elif tokens[0] == "wait":
                        self.addbg.addwait(tokens[1])
                    elif tokens[0] == "stop":
                        self.addbg.addstop(tokens[1])
                    elif tokens[0] == "flock":
                        self.addbg.addflock(tokens[1])
                    elif tokens[0] == "independent":
                        self.addbg.addind("tokens[1]")
                    elif tokens[0] == "end":
                        self.addbg.addend()
                    elif tokens[0] == "floor":
                        self.addbg.setfloor(tokens[1])
                    elif tokens[0] == "boss":
                        self.addbg.setboss()
                    elif tokens[0] == "waitboss":
                        self.addbg.setwaitboss()
                    elif tokens[0] == "parent":
                        self.scrolldata[tokens[1]].addparent(
                            self.scrolldata[tokens[2]])
                    elif tokens[0] == "endbg":
                        self.scrolldata.append(self.addbg)
                    elif tokens[0] == "loop":
                        self.addbg.addmloop(tokens[1],tokens[2])
                    elif tokens[0] == "music":
                        self.addbg.addmusic(tokens[1])
                    elif tokens[0] == "fade":
                        self.addbg.addfade()
                    continue
        return
    def valueproc(self,token):
        token = token.strip('\n').strip('\r')
        if token[0] in "0123456789-":
            if '.' in token:
                return float(token)
            else:
                return int(token)
        return token
    def drawto(self,bg):
        for e in self.scrolldata:
            e.getdrawing()
        return
    def draw(self):
        for e in self.scrolldata:
            e.getdrawing()
        return
    def update(self):
        for f in self.outerflags:
            # boss fight is done
            if f[0] == 'b':
                for s in self.scrolldata:
                    if s.boss:
                        s.boss==False
        self.outerflags = list()
        for s in self.scrolldata:
            s.update()
        for s in self.scrolldata:
            s.postupdate()
            f = s.getflock()
            if f != None:
                for s in f[0]:
                    for t in self.flockdata[s]:
                        tup = (t,f[1])
                        self.flockq.append(tup)
            for gf in s.getflags():
                if gf[0] == 'm':
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.musiclist[gf[1]])
                    pygame.mixer.music.play(-1)
                else:
                    self.flaglist.append(gf)
    def getflock(self):
        # pops flock queue out and destroys list, making a new one
        # each item in the list is tuple of the
        if len(self.flockq) < 1:
            return None
        t = self.flockq
        self.flockq = list()
        return t
    def getflags(self):
        t = self.flaglist
        self.flaglist = list()
        return t
    def pushflags(self,flagdata):
        self.outerflags.append(flagdata)
        return
