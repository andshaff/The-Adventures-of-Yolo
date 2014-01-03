import os, pygame, random, math
from pygame.locals import *
from general import *

# grab filename with data path
def dataname(name):
    return os.path.join('data',name)

# load image
def load_image(name, colorkey = None, alpha = False):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha == False:
        image = image.convert()
        if colorkey is not None:
            if colorkey == 01:
                colorkey = image.get_it((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image, image.get_rect()

# load alpha image (png usually, or gif89)
def load_image_alpha(name):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    return image, image.get_rect()

# load sound
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error, message:
        print 'Cannont load Sound:', name
        raise SystemExit, message
    return sound

def load_sliced_sprites(w, h, filename, colorkey = None, alpha = False):
    images = []
    if alpha == False:
        master_image = pygame.image.load(filename).convert()
    else:
        master_image = pygame.image.load(filename).convert_alpha()
    
    master_width, master_height = master_image.get_size()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = master_image.get_at( (0,0) )
        ## accelerate
        master_image.set_colorkey( colorkey, RLEACCEL )
    
    for i in xrange(int(master_width/w)):
    	images.append(master_image.subsurface((i*w,0,w,h)))
    return images
