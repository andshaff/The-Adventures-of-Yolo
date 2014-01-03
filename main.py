#!/usr/bin/env python2.7

## Import Modules
import os, pygame, random, math

## put commonly used in global namespace
from pygame.locals import *
from localdata import *

from Game import *
from enemy import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


#------------------------------------------------------------------------

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    ## Initialize Everything
    pygame.init()
    pygame.mixer.init()
    size = SCREEN_W,SCREEN_H
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption( TITLE )
    #pygame.mouse.set_visible(0)

    ## Create The Buffer
    background = pygame.Surface( screen.get_size() )
    background = background.convert()
    background.fill(0)
    screen.fill(0)

    # shouldn't need anything more than this
    game = Game(screen, background, pygame.time.Clock())
    game.start()
    pygame.display.quit()
    pygame.mixer.music.stop()


## call the 'main' function when this script is executed
main()
