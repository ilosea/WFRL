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




class StripAnimation(Sprite):

    def __init__(self, strip, size, pos):
        Sprite.__init__(self)
        self.image = strip # save the imagestrip here
        self._frame_w = size[0]       # width of single frame
        self._frame_h = size[1]       # height of single frame
        self.source_rect = pygame.Rect((0,0), size) # source rect
        # topleft is the position where it gets blit
        self.rect = pygame.Rect(pos, size)
        self.playing = 0
        
    def update(self, *args):
        if self.playing:    # only update the animation if it is playing
            self.source_rect.x += self._frame_w    # move the rect to the next frame
            self.source_rect.x %= self.image.get_width()
            
    def start(self):
        self.current = 0
        self.playing = True
        
    def stop(self):
        self.playing = False
        
    def pause(self):
        self.playing = False
        
    def resume(self):
        self.playing = True
        

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
    
    # define animation
    strip = pygame.image.load(os.path.normpath('data/strip.png')).convert()
    anims = StripAnimation(strip, (150, 150), (325, 300-75))
    anims.start()
    
    # use a clock to fix the fps of the main loop
    clock = pygame.time.Clock()
    fps = 20
    pygame.key.set_repeat(500, 30)
    font = pygame.font.Font(None, 25)
    screen.blit(font.render("image strip animation", 3, (255, 255, 255)), (325, 150))
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
                    if anims.playing:
                        anims.pause()
                    else:
                        anims.resume()
                elif event.key == pygame.K_r:
                    if anims.playing:
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
        dirty_rect = screen.blit(anims.image, anims.rect, anims.source_rect)
        # update screen
        pygame.display.update(dirty_rect)
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()