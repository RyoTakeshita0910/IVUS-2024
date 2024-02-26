import argparse
import os
import os.path
import ctypes
from shutil import rmtree, move
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from natsort import natsorted
import seaborn as sns
import time
import cv2

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--top", type=int, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--left", type=int, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--height", type=int, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--width", type=int, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

w = 512
h = 512

c = (0,255,255)
# c = (27,85,237) #オレンジ

def main():

    if not os.path.isdir(args.dest_dir):
        os.mkdir(args.dest_dir)

    img_list = sorted(os.listdir(args.img_dir))

    top = args.top
    left = args.left
    fh = args.height
    fw = args.width

    lw = 5

    for img in img_list:
        # # pick = '0034_4581954_000588.png'
        # # pick = '0062_04670213_002675.png'
        # # pick = '0113_3947173_000233.png'
        # # if img != pick:
        # #     continue
        # # pick = ['0034_4581954_000588.png', '0062_04670213_002675.png', '0113_3947173_000233.png']
        # pick = ['0002_4720237_000661.png']0091_01015265_002799
        # pick = ['0091_01015265_002799.png']
        pick = ['0036_04596528_001244.png']
        if not img in pick:
            continue

        ivus_img = cv2.imread(os.path.join(args.img_dir,img))
        cv2.rectangle(ivus_img,(left,top),(left+fw,top+fh),c,thickness=lw)
        cv2.imwrite(os.path.join(args.dest_dir,img), ivus_img)


main()

