# Copyright (c) 2016 Steven A. Bjornson
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights to 
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
# the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies 
# or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Info
# The goal of this software is to fascilitate the creation
# of complex light patterns using a large array of 
# Philips Hue bulbs.
# 
# An image is imported with PIL and the pixels are mapped
# to the bulbs.
# The x-axis being time and y-axis being bulb index

import argparse
from time import sleep

import PIL
import numpy as np
from phue import Bridge #https://github.com/studioimaginaire/phue
from hueColour import Converter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default='Philips-hue.local', 
                        help='hue hub ip address')
    parser.add_argument("--input", "--i", type=str, default='./',
                        help='Input image directory')

    args = parser.parse_args()
    
    #make ordered list of images in direcory
    
    try:
        while 1:
            #load image

            #step through image

            #back to load image

    except KeyboardInterrupt:
        #some sort of cleanup
        0
