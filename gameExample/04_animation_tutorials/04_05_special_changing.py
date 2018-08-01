#!/usr/bin/env python
#
#
#
#
#

# documentation string of this module
"""
Animation tutorials.
"""
# some informational variables
__author__    = "$Author: DR0ID $"
__version__   = "$Revision: 184 $"
__date__      = "$Date: 2007-08-24 19:22:06 +0200 (Fr, 24 Aug 2007) $"
__license__   = 'GPL2, see: gpl-2.0.txt'
__copyright__ = "DR0ID (c) 2006-2007   http://dr0id.ch.vu"

#----------------------------- actual code --------------------------------

# import the modules used
import pygame
import os
from pygame.sprite import Sprite




class Pow2Animation(Sprite):

    def __init__(self, frames):
        Sprite.__init__(self)
        if len(frames) not in [2**i for i in range(20)]:
            raise "number of frames must be 2**n number!"
        self.frames = frames       # save the images in here
        self.current = 0       # idx of current image of the animation
        self.image = frames[0]  # just to prevent some errors
        self.rect = self.image.get_rect()    # same here
        self.playing = 0
        self._modulo = len(frames)-1
        
    def update(self, *args):
        if self.playing:    # only update the animation if it is playing
            self.current += 1
            self.current &= self._modulo
            self.image = self.frames[self.current]
            # only needed if size changes within the animation
            self.rect = self.image.get_rect(center=self.rect.center)
            
    def start(self):
        self.current = 0
        self.playing = True
        
    def stop(self):
        self.playing = False
        
    def pause(self):
        self.playing = False
        
    def resume(self):
        self.playing = True


cache = {} # has to be global (or a class variable)
def get_sequence(frames_names, sequence, optimize=True):
    frames = []
    global cache
    for name in frames_names:
        if not cache.has_key(name): # check if it has benn loaded already
            image = pygame.image.load(name) # not optimized
            if optimize:
                if image.get_alpha() is not None:
                    image = image.convert_alpha()
                else:
                    image = image.convert()
            cache[name] = image
            
        # constructs a sequence of frames equal to frames_names
        frames.append(cache[name]) 
    frames2 = []
    for idx in sequence:
        # constructing the animation sequence according to sequence
        frames2.append(frames[idx]) 
    return frames2

def get_names_list(basename, ext, num, num_digits=1, offset=0):
    names = []
    # format string basename+zero_padded_number+.+ext
    format = "%s%0"+str(num_digits)+"d.%s"
    for i in range(offset, num+1):
        names.append(format % (basename, i,ext)) 
    return names




# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    
    # load and set the logo
    logo = pygame.image.load(os.path.normpath("data/logo32x32.png"))
    pygame.display.set_icon(logo)
    caption_str = os.path.split(__file__)[1]+"  keys: a/q: change fps, space: pause/resume, r: start/stop "
    pygame.display.set_caption(caption_str)
    
    # create a surface on screen that has the size of 800 x 600
    screen = pygame.display.set_mode((800,600))
    
    # define a variable to control the main loop
    running = True
    
    # generate a list of names    
    image_names = get_names_list(os.path.normpath("data/ball"), "png", 20, 2, 1)
    # generate a sequence, here simply 0,1,2,3...
    sequence = range(20)
    # load images
    frames = get_sequence(image_names, sequence) # [0,1,2,3,2,1]
    sequence.reverse()
    frames += get_sequence(image_names, sequence) # [0,1,2,3,2,1]
    # remove some frames to make it fit into 32 frames
    frames.pop(5)
    frames.pop(9)
    frames.pop(13)
    frames.pop(17)
    frames.pop(21)
    frames.pop(25)
    frames.pop(29)
    frames.pop(32)
    # prepare animation
    anim = Pow2Animation(frames)
    anim.rect.topleft = (400-75,300-75) 
    anim.start()
    
    # use a clock to fix the fps of the main loop
    clock = pygame.time.Clock()
    fps = 20
    pygame.key.set_repeat(500, 30)
    font = pygame.font.Font(None, 25)
    screen.blit(font.render("special frame changing: bitwise & used as modulo", 1, (255,255,255)), (200, 150))
    pygame.display.flip()
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_a:
                    fps -= 1
                    fps = max(fps, 1)
                elif event.key == pygame.K_q:
                    fps += 1
                elif event.key == pygame.K_SPACE:
                    if anim.playing:
                        anim.pause()
                    else:
                        anim.resume()
                elif event.key == pygame.K_r:
                    if anim.playing:
                        anim.stop()
                    else:
                        anim.start()
        # update the caption
        pygame.display.set_caption(caption_str+" set fps: "+str(fps)+"/"+"%2d"%(clock.get_fps()))
        # fix the fps
        clock.tick(fps)
        # erase things
        screen.fill((0,0,0))
        # update anim
        anim.update()
        # draw anim
        dirty_rect = screen.blit(anim.image, anim.rect)
        # update screen
        pygame.display.update(dirty_rect)
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()