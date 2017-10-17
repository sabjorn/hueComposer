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
from time import time
import logging
import thread

import yaml
import netifaces

import os
import sys
import subprocess
import signal

from PIL import Image
import numpy as np
from scipy.misc import imresize

from phue import Bridge  # https://github.com/studioimaginaire/phue
# turns out Hue [0, 65535] and Saturation [0, 254] are available
# as properties of the lights
from hueColour import Converter

http_delay = .04 # average time of HTTP transmission per light

def hueMain():
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

    # make ordered list of images in directory
    imgs = []
    images = None
    if(config_flag):
        images = cfg['images']
        for k, v in images.items():
            imgs.append(v['filename'])
    else:
        imgs = glob.glob("{}/*.png".format(args.input))

    while True:
        try:
            lights = b.lights
        except:
            logging.info("can't connect to lights")
            sleep(1)
            continue
        break

    # all lights off
    for x in lights:
        x.on = False
    sleep(5)

    while True:
        for i, names in enumerate(imgs):
            logging.info(names)

            for t, x in enumerate(lights):
                if(t < args.numlights):
                    x.on = True
                    x.bri = 1

            try:
                img = Image.open(args.base+names)
                img = np.asarray(img)
            except:
                continue

            logging.info("playing img: {}".format(args.base+names))
            print "playing img: {}".format(args.base+names)

            if(config_flag):
                args.transition = images[i]['transition']  # to seconds?
                args.rate = ((http_delay * args.numlights) + (args.transition))


            for t, x in enumerate(lights):
                if(t < args.numlights):
                    x.transitiontime = int(args.transition * 10)


            x_step = int(img.shape[1] / float(images[i]['time']/args.rate))
            logging.info("x-step size: {0}".format(x_step))
            #shrink Y-axis to size of array
            y_step = 1
            if(img.shape[0] > args.numlights):
                y_step = img.shape[0] / args.numlights
            elif(img.shape[0] < args.numlights):
                img = imresize(img, (args.numlights, img.shape[1]))

            image_average = 0
            image_start_time = time()
            for x in np.arange(0, img.shape[1], x_step):
                start_time = time()
                for y in np.arange(0, args.numlights):
                    bri = int(np.average(img[y, x, :]))
                    lights[y].xy = conv.rgbToCIE(img[y*y_step, x, 0], img[y*y_step, x, 1], img[y*y_step, x, 2])
                    lights[y].bri = bri
                image_average += time() - start_time
                sleep(args.transition)
            logging.info("time elapsed average image {0}, {1}".format(i, image_average/(img.shape[1]/x_step)))
            logging.info("total image {0} elapsed time: {1}".format(i, time() - image_start_time))

            # image finished animation
            for m, light in enumerate(lights):
                light.on = False
                light.bri = 1

            sleep(10)

def audio(audio_file):
    if audio_file is not None:
        try:
            return subprocess.Popen(["omxplayer", "--loop", "--vol", "352", audio_file], preexec_fn=os.setsid)
        except Exception, e:
            logging.exception(e)
    else:
        return None

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
    parser.add_argument("--log", "-l", type=str, default="/var/log"
                        help='log location')
    parser.add_argument("--audio", "-a", type=str,
                        help='Audio File to Play')


    args = parser.parse_args()
    
    logging.basicConfig(filename='{0}/hue_{1}.log'.format(args.log, strftime("%d-%m-%Y-%H-%M")), level=logging.INFO, format='%(asctime)s %(message)s')
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
                args.audio = config['audio']
        except IOError:
            logging.exception("Could not open file: {}".format(args.config))
            exit(1)
        except:
            logging.exception("Error in config file")
    try:
        proc = audio(args.audio)
        hueMain()

    except KeyboardInterrupt, e:
        #some sort of cleanup
        if proc is not None:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        logging.info("Keyboard Interrupt")
    except Exception, e:
        if proc is not None:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        logging.exception(e)

    logging.info('Finished')
