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
import math
import random



class AnchoredAnimation(Sprite):

    def __init__(self, frames, pos, fps=20):
        Sprite.__init__(self)
        self.frames = frames       # [(anchp_x, anchp_y, image),...]
        self.current = 0       # idx of current image of the animation
        self.posx = pos[0]          # instead of setting the position to the 
        self.posy = pos[1]          # rect argument set these values, update handles it
        anchx, anchy, self.image = frames[0]  # just to prevent some errors
        self.rect = self.image.get_rect(topleft = (pos[0]-anchx,pos[1]-anchy))    # same here
        self.playing = 0
        
    def update(self, *args):
        if self.playing:    # only update the animation if it is playing
            self.current += 1
            if self.current == len(self.frames):
                self.current = 0
            anchp_x, anchp_y, self.image = self.frames[self.current]
            # moving image to match anchor point, - because it is an anchor point
            self.rect.topleft = (self.posx - anchp_x, self.posy - anchp_y)            
            
    def start(self):
        self.current = 0
        self.playing = True
        
    def stop(self):
        self.playing = False
        
    def pause(self):
        self.playing = False
        
    def resume(self):
        self.playing = True
        

            
class AnimationGroup(pygame.sprite.RenderUpdates):

    def start(self):
        for spr in self.sprites():
            spr.start()
            
    def stop(self):
        for spr in self.sprites():
            spr.stop()
            
    def pause(self):
        for spr in self.sprites():
            spr.pause()
            
    def resume(self):
        for spr in self.sprites():
            spr.resume()


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
    # generate another sequence, here simply 0,1,2,3,...,19,20,20,19,...,1,0
    sequence = range(20)+range(19, -1, -1)  # forward+reverse = pingpong
    # load images
    frames = get_sequence(image_names, sequence)
    # generate some anchor points
    xanchors = []
    yanchors = []
    for angle in range(0,360, 360/40):
        xanchors.append(int(50*math.sin(math.radians(angle))))
        yanchors.append(int(50*math.cos(math.radians(angle))))
    frames3 = zip(xanchors, yanchors, frames)
    # anchors on the ball
    xanchors = [0]*40
    yanchors = [33,33,34,35,36,38,41,44,48,52,55,60,65,71,77,84,91,99,108,117]
    yanchors += reversed(yanchors)
    frames2 = zip(xanchors, yanchors, frames)
    # random anchors
    xanchors = []
    yanchors = []
    for i in range(40):
        xanchors.append(random.randint(-5, 5))
        yanchors.append(random.randint(-5, 5))
    frames1 = zip(xanchors, yanchors, frames)
    # prepare animation
    anims = AnimationGroup()
    anims.add(AnchoredAnimation(frames1, (100, 300-75)))
    anims.add(AnchoredAnimation(frames2, (325, 400-75)))
    anims.add(AnchoredAnimation(frames3, (550, 300-75)))
    anims.start()
    
    # use a clock to fix the fps of the main loop
    clock = pygame.time.Clock()
    fps = 20
    pygame.key.set_repeat(500, 30)
    font = pygame.font.Font(None, 25)
    screen.blit(font.render("random anchors", 3, (255, 255, 255)), (100, 150))
    screen.blit(font.render("anchor on ball", 3, (255, 255, 255)), (325, 150))
    screen.blit(font.render("circled anchors", 3, (255, 255, 255)), (550, 150))
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
                    if anims.sprites()[0].playing:
                        anims.pause()
                    else:
                        anims.resume()
                elif event.key == pygame.K_r:
                    if anims.sprites()[0].playing:
                        anims.stop()
                    else:
                        anims.start()
        # update the caption
        pygame.display.set_caption(caption_str+" set fps: "+str(fps)+"/"+"%2d"%(clock.get_fps()))
        # fix the fps
        clock.tick(fps)
        # erase things
        screen.fill((0,0,0))
        # update anim
        anims.update()
        # draw anim
        dirty_rect = anims.draw(screen)
        # update screen
        pygame.display.update(dirty_rect)
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()