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

import sys
import os
import pygame
import glob

# CHANGE THIS TO MERGE YOUR FILES, SORRY NO AGUMENT PROCESSING

name = 'data/ball'          # name of like pic01.png, pic02.png
ext = 'png'                # extension: png, bmp, tiff,...
num = 20                   # number of images to merge
digits = 2                 # width of the number 2: 01   4: 0003
offset = 1                 # start to count at this number
prefix = False             # number before the name? False: name004.png True:004name.png
save_to = "strip.png" # file name where to save

#------------------------------------------------------------------------------
#TODO: arg processing

cache = {} # has to be global (or a class variable)
def get_sequence(frames_names, sequence, optimize=True):
    frames = []
    global cache
    for name in frames_names:
        if not cache.has_key(name): # check if it has benn loaded already
            print "loading", name
            if not os.path.isfile(name):
                raise name+' is not a file or does not exist!'
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

def get_names_list(basename, ext, num, num_digits=1, offset=0, prefix=False):
    names = []
    if prefix:
        # format string basename+zero_padded_number+.+ext
        format = "%0"+str(num_digits)+"d%s.%s"
        for i in range(offset, num+1):
            names.append(format % (i, basename, ext)) 
    else:
        # format string basename+zero_padded_number+.+ext
        format = "%s%0"+str(num_digits)+"d.%s"
        for i in range(offset, num+1):
            names.append(format % (basename, i,ext)) 
    return names

def main():
    

    names = get_names_list(os.path.normpath(name), ext, num, digits, offset, prefix)
    images = get_sequence(names, range(num), False)


    total_width = 0
    max_height = 0
    for image in images:
        w,h = image.get_size()
        total_width += w
        if h > max_height:
            max_height = h
        
        
    blit_rect = pygame.Rect(0,0,images[0].get_width(),max_height)
    big = pygame.Surface((total_width, h), pygame.SRCALPHA, 32)
    big.fill((0,0,0,0))
    for idx, image in enumerate(images[:-1]):
        big.blit(image, blit_rect)
        blit_rect.move_ip((images[idx+1].get_width(), 0))
    big.blit(images[-1], blit_rect)
    pygame.image.save(big, save_to)
    print "saved to:", save_to
    


if __name__=='__main__':
    main()