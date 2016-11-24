#!/usr/bin/python

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
import logging

from PIL import Image
import numpy as np
from scipy.misc import imresize

from phue import Bridge #https://github.com/studioimaginaire/phue
# turns out Hue [0, 65535] and Saturation [0, 254] are available
# as properties of the lights
from hueColour import Converter

if __name__ == "__main__":
    logging.basicConfig(filename='/home/pi/hueComposer/hue.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Started')

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default='192.168.0.100', 
                        help='hue hub ip address')
    parser.add_argument("--input", "--i", type=str, default='/home/pi/imgs',
                        help='Input image directory')
    parser.add_argument("--rate", "--r", type=float, default=1/5.,
                        help='Rate in ms to step between pixel values')
    parser.add_argument("--transition", "--t", type=float, default=0,
                        help='Transition time in seconds')
    parser.add_argument("--numlights", "--n", type=float, default=30,
                        help='Number of active lights')


    args = parser.parse_args()

    b = Bridge(args.ip)
    b.username = "Ga3Q2uvDeCQBKt3srFKRolzLRaQkgpIm8tENVY0-"
    b.connect()


    while True:
        try:
            lights = b.lights
        except:
            continue
        break

    conv = Converter()

    #make subset of lights which are active (a map)
    
    #make ordered list of images in directory
    imgs = glob.glob("{}/*.png".format(args.input))

    try:
        while True:
            for i, names in enumerate(imgs):
                logging.info(names)
                for x in lights:
                    x.transitiontime = args.transition
                    x.on = True

                img = Image.open(names)
                img = np.asarray(img)

                #shrink Y-axis to size of array
                step = 1
                if(img.shape[0] > args.numlights):
                    step = img.shape[0] / args.numlights
                elif(img.shape[0] < args.numlights):
                    img = imresize(img, (args.numlights, img.shape[1]))

                # if issue with update rate persists, you probably want to dynamically make groups to that updates can be faster
                    # should probably reduce dynamic range of image to have more common images (or a thresh for closeness?)
                    # may not need dynamic groups but instead somethign like:
                        # b.set_light( [1,2], 'on', True)
                        # where the lights are a list
                        # so make lists and then push out instead of pushing

                for x in np.arange(img.shape[1]):
                    for y in np.arange(0, args.numlights):
                        bri = int(np.average(img[y,x,:]))
                        lights[y].xy = conv.rgbToCIE(img[y*step, x, 0], img[y*step, x, 1], img[y*step, x, 2])
                        lights[y].bri = bri
                    #print(x/float(img.shape[1]))

                    sleep(args.rate)

                for i, x in enumerate(lights):
                    if(i % 2):
                        x.on = False


                sleep(10)

                            #command =  {'xy': conv.rgbToCIE(img[y, x, 0], img[y, x, 1], img[y, x, 2]), 'bri' : bri}
                        # else:
                        #     command = {'On': False}
                        #commands.append(command)
                    # for y, command in enumerate(commands):
                    #     b.set_light(y+1, command) # best to shoot these all out like this?

    except KeyboardInterrupt:
        #some sort of cleanup
        0

    logging.info('Finished')


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
