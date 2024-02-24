import argparse
import os
import os.path
from shutil import rmtree, move, copy
import random

import pydicom
from PIL import Image
import numpy as np

import shutil
import datetime
import csv
from pathlib import Path
import cv2

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing dicoms')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

h = 512
w = 512

def set_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def set_img(img):
    new_img = img
    for y in range(h):
        for x in range(w):
            img_c = img[y][x]
            area = (x-255)**2 + (y-255)**2
            if area > 255**2 and img_c == 255:
                new_img[y][x] = 0
    
    return new_img

def main():
    
    # setting output folder
    set_dir(args.dest_dir)

    img_list = sorted(os.listdir(args.img_dir))
    for img in img_list:
        im = cv2.imread(os.path.join(args.img_dir,img), cv2.IMREAD_GRAYSCALE)
        new_im = set_img(im)
        cv2.imwrite(os.path.join(args.dest_dir,img),new_im)

main()
    
   

