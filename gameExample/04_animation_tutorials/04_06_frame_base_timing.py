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


class FrameTimedAnimation(Sprite):

    def __init__(self, frames, pos, fps=20):
        Sprite.__init__(self)
        self.frames = frames     # stores tuples (duration in ms, image-surf)
        self.current = 0     # index, which frame to show
        self._next_update = 0# next time to update
        self.image = frames[0][1]
        self.rect = self.image.get_rect(topleft=pos)
        self.playing = True
        
    def update(self, dt, t):
        if self.playing:
            if self._next_update <= t:
                while self._next_update <= t: # for frame skipping, at least once
                    self.current += 1
                    self.current %= len(self.frames)
                    duration, next_image = self.frames[self.current]
                    
                    # summing the durations and calculating the new time when to change
                    self._next_update += duration 
                    
                self.image = next_image
                # only needed if size of frames can change
                self.rect = self.image.get_rect(center=self.rect.center)

            
    def start(self, t):
        self.current = 0
        duration, self.image = self.frames[self.current]
        self.rect = self.image.get_rect(center=self.rect.center)
        self._next_update = t+duration
        self.playing = True
        
    def stop(self, t):
        self.playing = False
        
    def pause(self, t):
        raise NotImplementedError
        
    def resume(self, t):
        raise NotImplementedError
        

            
class AnimationGroup(pygame.sprite.RenderUpdates):

    def start(self, t):
        for spr in self.sprites():
            spr.start(t)
            
    def stop(self, t):
        for spr in self.sprites():
            spr.stop(t)
            
    def pause(self, t):
        for spr in self.sprites():
            spr.pause(t)
            
    def resume(self, t):
        for spr in self.sprites():
            spr.resume(t)
            
    def update(self, dt, t):
        for spr in self.sprites():
            spr.update(dt, t)


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
    caption_str = os.path.split(__file__)[1]+"  keys: a/q: change fps, r: start/stop "
    pygame.display.set_caption(caption_str)
    
    # create a surface on screen that has the size of 800 x 600
    screen = pygame.display.set_mode((800,600))
    bgd = pygame.Surface(screen.get_size()).convert()
    bgd.fill((0,0,0))
    
    # define a variable to control the main loop
    running = True
    
    # generate a list of names    
    image_names = get_names_list(os.path.normpath("data/ball"), "png", 20, 2, 1)
    # generate a sequence, here simply 0,1,2,3...
    sequence = range(20)+range(19, -1, -1)
    # load images
    frames = get_sequence(image_names, sequence) # [0,1,2,3,2,1]
    frame_times = [50]*39
    frame_times.insert(0, 2000)
    frames = zip(frame_times, frames) # makes [(time, image), ...]
    # prepare animation
    anims = AnimationGroup()
    anims.add(FrameTimedAnimation(frames, (325, 300-75)))
        
    anims.start(0)
    
    # use a clock to fix the fps of the main loop
    clock = pygame.time.Clock()
    fps = 20
    pygame.key.set_repeat(500, 30)
    font = pygame.font.Font(None, 25)
    screen.blit(font.render("FrameTimedAnimation", 3, (255, 255, 255)), (325, 150))
    screen.blit(font.render("it waits 2 seconds at frame 1", 3, (255, 255, 255)), (325, 175))
    pygame.display.flip()
    dt = 0
    t = 0
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
                elif event.key == pygame.K_r:
                    if anims.sprites()[0].playing:
                        anims.stop(t)
                    else:
                        anims.start(t)
        # update the caption
        pygame.display.set_caption(caption_str+" set fps: "+str(fps)+"/"+"%2d"%(clock.get_fps()))
        # fix the fps
        dt = clock.tick(fps)
        t = pygame.time.get_ticks()
        # erase things
##        screen.fill((0,0,0))
        anims.clear(screen, bgd)
        # update anim
        anims.update(dt, t)
        # draw anim
        dirty_rect = anims.draw(screen)
        # update screen
        pygame.display.update(dirty_rect)
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()