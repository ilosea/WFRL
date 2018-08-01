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

    def __init__(self, frames, pos, fps=40):
        Sprite.__init__(self)
        self.image = frames
        self.rect = pygame.Rect(pos, (150,150))
        self.source_rect = pygame.Rect(0,0,150,150)
        self.current = 0
        self.playing = 0         # to know if it is playing
        self._next_update = 0    # next time it has to be updated in ms
        self._period = 1000./fps # frequency/period of the animation in ms
        self._frame_w = 150
        self._len = 40
        # movement
        self.speed = 0 # [px/s]
        self.optimal_speed = 80. # [px/s] assuming at 40 [frames/s]
        self.optimal_fps = 40. # [frames/s]
        self.x, self.y = pos
        
        
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
                self.current %= self._len
                # update image
                self.source_rect.x = self.current*self._frame_w
                
            
            # updating movement
##            self.x += (self.speed * self._len * dt/1000.) # [px/s]/[ms/s]*[ms]
            self.x += (self.speed * dt/1000.) # [px/s]*[ms]/[ms/s]
            self.rect.x = int(self.x)
            # dont let it vanish from screen
            if self.x > 800-75:
                self.x = -75
                self.current = 0
            
    def start(self, t):
        self.current = 0
        self.playing = True
        
    def stop(self, t):
        self.playing = False
        
    def pause(self, t):
        self.playing = False
        
    def resume(self, t):
        self.playing = True

    def set_fps(self, fps):
        self._period = 1000./fps
        
    def set_speed1(self, speed):
        if speed > 0:
            self.playing = True
            self.speed = speed
        else:
            self.stop(0)
            self.speed = 0
        print '-------------------'
        print 'speed', speed
        print 'fps1:',1000./self._period

    def set_speed2(self, speed):
        if speed > 0:
            self.playing = True
            self.speed = speed
            self._period = 1000./(speed/self.optimal_speed*self.optimal_fps) # 1000[ms/s]/([px/s]/[px/s]*[frames/s])= ms
        else:
            self.stop(0)
            self.speed = 0
        print 'real speed:', speed
        print 'fps2',1000./self._period
            
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
    bgd.fill((255,255,255))
    
    # define a variable to control the main loop
    running = True
    
    # generate a list of names    
##    frames = pygame.image.load(os.path.normpath('data/locomotive.png'))
    frames = pygame.image.load(os.path.normpath('data/locomotive.png'))
    # prepare animation
    anims = AnimationGroup()
    anim_faulty = TimedAnimation(frames, (-75, 150))
    anim_ok = TimedAnimation(frames, (-75, 450))
    anims.add(anim_faulty)
    anims.add(anim_ok)
        
    
    # use a clock to fix the fps of the main loop
    clock = pygame.time.Clock()
    fps = 100
    pygame.key.set_repeat(500, 30)
    font = pygame.font.Font(None, 25)
    screen.blit(font.render("The animations run with fps depending on speed!", 3, (255, 255, 255)), (200, 300))
    screen.blit(font.render("change speed of steamer using 'a'/'q'", 3, (255, 255, 255)), (200, 325))
    screen.blit(font.render("upper is wrong (because wheels slip), beneath its good", 3, (255, 255, 255)), (200, 350))
    pygame.display.flip()
    dt = 0
    t = 0
    speed = 0
    last_x1 = 0
    last_x2 = 0
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
                    speed -= 1
                    speed = max(speed, 0)
##                    fps -= 1
##                    fps = max(fps, 1)
                elif event.key == pygame.K_q:
                    speed += 1
##                    fps += 1
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
                # update speed
                anim_faulty.set_speed1(speed)
                anim_ok.set_speed2(speed)
                
        # update the caption
        pygame.display.set_caption(caption_str+" set fps: "+str(fps)+"/"+"%2d"%(clock.get_fps()))
        # fix the fps
        dt = clock.tick(fps)
        t = pygame.time.get_ticks()
        # erase things
##        screen.fill((0,0,0))
##        screen.blit(bgd, (0,0))
        # update anim
        anims.update(dt, t)
        # draw anim
        dirty1 = screen.blit(anim_faulty.image, anim_faulty.rect, anim_faulty.source_rect)
        dirty2 = screen.blit(anim_ok.image, anim_ok.rect, anim_ok.source_rect)
        if anim_faulty.current == 0:
##            print 'faulty:',anim_faulty.x-last_x1
            last_x1 = anim_faulty.x
            pygame.draw.line(screen, (0,255,0), (anim_faulty.x, 125), ((anim_faulty.x, 175)))
        if anim_ok.current == 0:
##            print 'good:',anim_ok.x-last_x2
            last_x2 = anim_ok.x
            pygame.draw.line(screen, (255,0,0), (anim_ok.x, 425), ((anim_ok.x, 600)))
        # update screen
        pygame.display.update()
        screen.blit(bgd, dirty1, dirty1)
        screen.blit(bgd, dirty2, dirty2)
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()