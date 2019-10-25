#import moudles
import os
import random
import re as rep
import sys
import time
import tkinter as tk
import tkinter.filedialog as tkFD
import winsound
from collections import Counter

import itchat
import jieba.analyse
import PIL
from PIL import Image
from pyecharts import WordCloud
from removebg import RemoveBg
from skimage import data, io, transform

from cut_funcs import *
from Cutpro.py import *


#functions
def cut(image_name):
    global choose
    global stbg,statusbar
    statusbar['text'] = 'Cutting Picture...'
    statusbar.update()
    #to make sure is it the type of file that can be cut
    if image_name == '':
        image_name = text.get()
        print(image_name+'done1')
    print(image_name+'done')
    if '.jpg'in image_name or '.jpeg'in image_name or '.png'in image_name or '.gif'in image_name or '.ico'in image_name:
        try:
            image = PIL.Image.open(image_name)
            image = fill_image(image)
            image_list = cut_image(image)
            save_images(image_list, image_name)
            statusbar['text'] = 'Picture Cut Successfully'
            statusbar.update()
        except FileNotFoundError:
            statusbar['text'] = 'File Not Found'
            statusbar.update()
    else:
        statusbar['text'] = 'Failed to Cut Picture'
        statusbar.update()
    time.sleep(2.0)
    statusbar['text'] = 'Ready'
    statusbar.update()
