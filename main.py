#!/usr/bin/python
# -*- coding:utf-8 -*-
# basic drafting for the wavseshare 213 to get layout and wording straight
import sys
import os
import hashlib
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback

def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

def layout(draw):
  # Top information lines
  draw.line([(0,14),(250,14)], fill = 0,width = 1)
  draw.line([(0,0),(250,0)], fill = 0,width = 1)
  # vertical bar
  draw.line([(100,14),(100,100)], fill = 0,width = 1)
  return draw

def top_info(draw):
  draw.text((0, 0), 'Baby Psymons', font = font_size(12), fill = 0)
  
  return draw

def top_uptime(draw):
  uptime = time.clock_gettime(time.CLOCK_BOOTTIME)
  display_time = str(chop_microseconds(datetime.timedelta(seconds = uptime)))
  
  position = 250 - (len(display_time) * 6)
  print(position)
  draw.text((position, 0), display_time, font = font_size(12), fill = 0)
  
  return draw
  
def font_size(size):
  return ImageFont.truetype(os.path.join(picdir, 'Fonttwo.ttc'), size)

logging.basicConfig(level=logging.DEBUG)

try:
    # reports only single Wlan info
    # import subprocess

    # arg_list = [ '/sbin/iwgetid', '-r' ]
    # args = ' '.join(arg_list)

    # proc = subprocess.Popen(arg_list, stdout=subprocess.PIPE,
    #                             stderr=subprocess.STDOUT,
    #                             universal_newlines=True)

    # (output, dummy) = proc.communicate()
    # print (output)
  
    logging.info("epd2in13_V2 Demo")
        
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
        
    # intiate a full update of the screen
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    # main data fill
    layout(draw)
    top_info(draw)
    top_uptime(draw)
    
    # draw.line([(0,50),(50,0)], fill = 0,width = 1)
    # draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
    # draw.ellipse((55, 60, 95, 100), outline = 0)
    # draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
    # draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
    # draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
    # draw.polygon([(190,0),(190,50),(150,25)],fill = 0)
    # draw.text((10, 10), '( ^_^)', font = font_size(15), fill = 0)
    # draw.text((10,40),'Hello', font = font_size(15), fill = 0)
    # draw.text((110, 90), u'微雪电子', font = font_size(24), fill = 0)
    epd.display(epd.getbuffer(image))
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
