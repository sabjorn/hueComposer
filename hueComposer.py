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
import glob #list all images
from time import sleep

from PIL import Image
import numpy as np
from phue import Bridge #https://github.com/studioimaginaire/phue

# turns out Hue [0, 65535] and Saturation [0, 254] are available
# as properties of the lights
from hueColour import Converter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default='Philips-hue.local', 
                        help='hue hub ip address')
    parser.add_argument("--input", "--i", type=str, default='/home/pi/imgs',
                        help='Input image directory')
    parser.add_argument("--rate", "--r", type=float, default=1/25.,
                        help='Rate in ms to step between pixel values')
    parser.add_argument("--transition", "--t", type=float, default=0,
                        help='Transition time in seconds')

    args = parser.parse_args()

    b = Bridge(args.ip)
    b.connect()

    lights = b.lights

    for x in lights:
        x.transitiontime = args.transition

    conv = Converter()

    #make subset of lights which are active (a map)
    
    #make ordered list of images in directory
    imgs = glob.glob("{}/*.png".format(args.input))

    try:
        for i, names in enumerate(imgs):
            img = Image.open(names)
            img = np.asarray(img)

            for x in np.arange(img.shape[1]):
                lights[1].xy = conv.rgbToCIE(img[0, x, 0], img[0, x, 1], img[0, x, 2])
                lights[1].brightness = np.average(img[0,x,:])
                lights[2].xy = conv.rgbToCIE(img[1, x, 0], img[1, x, 1], img[1, x, 2])
                lights[2].brightness = np.average(img[1,x,:])
                sleep(args.rate)

    except KeyboardInterrupt:
        #some sort of cleanup
        0


    # try:
    #     while 1:
    #         #load image

    #         #step through image
    #         """
    #         set_light(self, light_id, parameter, value=None, transitiontime=None):
    #         Adjust properties of one or more lights.
    #         light_id can be a single lamp or an ARRAY of lamps!
    #         parameters: 'on' : True|False , 'bri' : 0-254, 'sat' : 0-254, 'ct': 154-500
    #         """

    #         #back to load image

    # except KeyboardInterrupt:
    #     #some sort of cleanup
    #     0
