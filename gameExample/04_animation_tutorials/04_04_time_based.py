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


class TimedAnimation(Sprite):

    def __init__(self, frames, pos, fps=20):
        Sprite.__init__(self)
        self.frames = frames     # store frames in a list
        self.image = frames[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.current = 0         # current image of the animation
        self.playing = 0         # to know if it is playing
        self._next_update = 0    # next time it has to be updated in ms
        self._inv_period = fps/1000. # 1./period of the animation in ms
        self._start_time = 0     # has to be set when the animation is started
        self._paused_time = 0
        self_pause_start = 0
        self._frames_len = len(self.frames)
        
    def update(self, dt, t):     
    
        # dt: time that has passed in last pass through main loop,  t: current time
        if self.playing:
        
            # period is duration of one frame, so dividing the time the animation
            # is running by the period of one frame on gets the number of frames
            self.current = int((t-self._start_time-self._paused_time)*self._inv_period)
            self.current %= self._frames_len
            # update image
            self.image = self.frames[self.current]
            # only needed if size changes between frames
            self.rect = self.image.get_rect(center=self.rect.center)
            
    def start(self, t):
        self.current = 0
        self.playing = True
        self._start_time = t
        self._paused_time = 0
        
    def stop(self, t):
        self.playing = False
        
    def pause(self, t):
        self.playing = False
        self._pause_start = t
        
    def resume(self, t):
        self.playing = True
        self._paused_time += (t - self._pause_start)
        
class TimedAnimation2(Sprite):

    def __init__(self, frames, pos, fps=20):
        Sprite.__init__(self)
        self.frames = frames     # store frames in a list
        self.image = frames[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.current = 0         # current image of the animation
        self.playing = 0         # to know if it is playing
        self._next_update = 0    # next time it has to be updated in ms
        self._period = 1000./fps # frequency/period of the animation in ms
        
    def update(self, dt, t):
        if self.playing:
        
            # accumulate time since last update
            self._next_update += dt
            
            # if more time has passed as a period, then we need to update
            if self._next_update >= self._period:
            
                # skipping frames if too much time has passed
                # since _next_update is bigger than period this is at least 1
                self.current += int(self._next_update/self._period)
                
                # time that already has passed since last update
                self._next_update %= self._period
                
                # known code
                self.current %= len(self.frames)
                
                # update image
                self.image = self.frames[self.current]
                
                # only needed if size changes between frames
                self.rect = self.image.get_rect(center=self.rect.center)
            
    def start(self, t):
        self.current = 0
        self.playing = True
        
    def stop(self, t):
        self.playing = False
        
    def pause(self, t):
        self.playing = False
        
    def resume(self, t):
        self.playing = True

class TimedAnimation3(Sprite):

    def __init__(self, frames, pos, fps=20):
        Sprite.__init__(self)
        self.frames = frames     # store frames in a list
        self.image = frames[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.current = 0         # current image of the animation
        self.playing = 0         # to know if it is playing
        self._next_update = 0    # next time it has to be updated in ms
        self._period = 1000./fps # period of the animation in ms
        self._inv_period = 1./self._period
        self._paused_time = 0
        self._pause_start = 0
        self._frames_len = len(self.frames)
        
    def update(self, dt, t):
        if self.playing:
            # do only something if the time has come
            if self._next_update <= t:    
            
                # time past since it should have updated
                delta = t - self._paused_time - self._next_update
                
                # calculate if there are any skipped frames
                skipped_frames = int(delta*self._inv_period)
                
                # next time to update
                self._next_update = self._next_update + self._period + skipped_frames * self._period
                
                # update to next image
                self.current += (1+skipped_frames)
                
                # bind it to the length of the animation
                self.current %= self._frames_len
                
                # update image
                self.image = self.frames[self.current]
                
                # only needed if size changes between frames
                self.rect = self.image.get_rect(center=self.rect.center)
            
    def start(self, t):
        self.current = 0
        self.playing = True
        self._paused_time = 0
        self._next_update = t
        
    def stop(self, t):
        self.playing = False
        
    def pause(self, t):
        self.playing = False
        self._pause_start = t
        
    def resume(self, t):
        self.playing = True
        self._paused_time += t - self._pause_start


            
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
    caption_str = os.path.split(__file__)[1]+"  keys: a/q: change fps, space: pause/resume, r: start/stop "
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
    # prepare animation
    anims = AnimationGroup()
    anims.add(TimedAnimation(frames, (100, 300-75)))
    anims.add(TimedAnimation2(frames, (325, 300-75)))
    anims.add(TimedAnimation3(frames, (550, 300-75)))
        
    anims.start(0)
    
    # use a clock to fix the fps of the main loop
    clock = pygame.time.Clock()
    fps = 20
    pygame.key.set_repeat(500, 30)
    font = pygame.font.Font(None, 25)
    screen.blit(font.render("TimedAnimation", 3, (255, 255, 255)), (100, 150))
    screen.blit(font.render("TimedAnimation2", 3, (255, 255, 255)), (325, 150))
    screen.blit(font.render("TimedAnimation3", 3, (255, 255, 255)), (550, 150))
    screen.blit(font.render("The animations always run with 20 fps!", 3, (255, 255, 255)), (275, 400))
    screen.blit(font.render("Change the fps of the main loop (using 'a'/'q') and you will see", 3, (255, 255, 255)), (200, 425))
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
                elif event.key == pygame.K_SPACE:
                    if anims.sprites()[0].playing:
                        anims.pause(t)
                    else:
                        anims.resume(t)
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