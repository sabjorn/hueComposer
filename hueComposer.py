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
import glob  # list all images
from time import sleep
from time import strftime
import logging

import yaml
import netifaces

from PIL import Image
import numpy as np
from scipy.misc import imresize

from phue import Bridge  # https://github.com/studioimaginaire/phue
# turns out Hue [0, 65535] and Saturation [0, 254] are available
# as properties of the lights
from hueColour import Converter

adjust_time = 2.5

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default='192.168.1.64',
                        help='hue hub ip address')
    parser.add_argument("--username", "-u", type=str,
                        help="Hue hub username.")
    parser.add_argument("--input", "-i", type=str, default='./',
                        help='Input image directory')
    parser.add_argument("--rate", "--r", type=float, default=1/5.,
                        help='Rate in ms to step between pixel values')
    parser.add_argument("--transition", "--t", type=float, default=0,
                        help='Transition time in seconds')
    parser.add_argument("--numlights", "--n", type=float, default=30,
                        help='Number of active lights')
    parser.add_argument("--config", "-c", type=str,
                        help='run with config files')
    parser.add_argument("--base", "-b", type=str, default="./",
                        help='base directory of images')


    args = parser.parse_args()

    logging.basicConfig(filename='~/hueComposer/log/hue_{0}.log'.format(strftime("%d-%m-%Y-%H-%M")), level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Started')

    config_flag = args.config is not None
    cfg = None
    if(config_flag):
        try:
            with open(args.config, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
                config = cfg['config']
                args.numlights = config['lights']
                args.username = config['username']
                args.ip = config['ip']
        except IOError:
            logging.exception("Could not open file: {}".format(args.config))
            exit(1)
        except yaml.YAMLError as exc:
            logging.exception("yaml file borked. ", exc)
        except:
            logging.exception("Error in config file")

    b = Bridge(args.ip)

    # try is to make sure network is connected
    while True:
        addr = netifaces.ifaddresses("eth0")
        logging.info(addr)
        if(netifaces.AF_INET in addr):
            break
        sleep(1)

    #not fully tested!
    if(args.username is None):
        b.connect()
        args.username = b.username
        logging.info("Username: {}".format(b.username))
    else:
        b.username = args.username

    # while True:
    #     try:
    #         lights = b.lights
    #     except:
    #         continue
    #     break

    conv = Converter()

    # make subset of lights which are active (a map)
    # make ordered list of images in directory
    imgs = []
    images = None
    if(config_flag):
        images = cfg['images']
        for k, v in images.items():
            imgs.append(v['filename'])
    else:
        imgs = glob.glob("{}/*.png".format(args.input))

    try:
        lights = b.lights

        # all lights off
        for x in lights:
            x.on = False
        sleep(5)

        while True:
            for i, names in enumerate(imgs):
                logging.info(names)

                for t, x in enumerate(lights):
                    if(t < args.numlights):
                        x.transitiontime = args.transition
                        x.on = True


                img = Image.open(args.base+names)
                img = np.asarray(img)
                logging.info("playing img: {}".format(args.base+names))
                print "playing img: {}".format(args.base+names)

                if(config_flag):
                    args.transition = images[i]['transition']
                    #args.rate = (images[i]['time'] - (img.shape[1] * float(args.transition)*10.)) / img.shape[1] #fixme
                    args.rate = float(images[i]['time']/adjust_time)/ img.shape[1]
                    logging.info(args.rate)
                    # if(args.rate < 1):
                    #     args.rate = 10
                    #     logging.info("Rate too slow")
                    #     print("rate too slow")

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
                        bri = int(np.average(img[y, x, :]))
                        lights[y].xy = conv.rgbToCIE(img[y*step, x, 0], img[y*step, x, 1], img[y*step, x, 2])
                        lights[y].bri = bri
                    #print(x/float(img.shape[1]))

                    sleep(args.rate)

                # image finished animation
                for i, x in enumerate(lights):
                    x.on = False

                sleep(10)
    except KeyboardInterrupt, e:
        #some sort of cleanup
        logging.info("Keyboard Interrupt")
    except Exception, e:
        logging.exception("message")

    logging.info('Finished')
