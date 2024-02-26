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
parser.add_argument("--mask_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

w = 512
h = 512

# c = (0,0,255)
c = (255,255,0)
# c = (0,255,0)
# c = (0,165,255)
lw = 2

def main():

    if not os.path.isdir(args.dest_dir):
        os.mkdir(args.dest_dir)

    img_list = sorted(os.listdir(args.img_dir))
    mask_list = sorted(os.listdir(args.mask_dir))


    for img in img_list:
        # pick = '0034_4581954_000588.png'
        # pick = '0062_04670213_002675.png'
        # pick = '0113_3947173_000233.png'
        # if img != pick:
        #     continue
        # pick = ['0034_4581954_000588.png', '0062_04670213_002675.png', '0113_3947173_000233.png']
        # pick = ['0013_04687639_001117.png','0020_04709209_001133.png']
        # pick = ['0034_4581954_000618.png']
        # pick = ['0087_04625013_001957.png']
        # pick = ['0033_4667531_002742.png']
        # pick = ['0027_04671422_001531.png']
        # pick = ['0083_04653882_003042.png']
        # pick = ['0062_04670213_002675.png']
        # pick = ['0042_4694406_001266.png']
        # pick = ['0111_04147901_001872.png']
        # if not img in pick:
        #     continue
        for mask in mask_list:
            if img == mask:
                print(img)
                ivus_img = cv2.imread(os.path.join(args.img_dir,img))
                mask_img = cv2.imread(os.path.join(args.mask_dir,mask), cv2.IMREAD_GRAYSCALE)

                con, _ = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                for i in range(len(con)):
                    ivus_img = cv2.drawContours(ivus_img, [con[i]], 0, c, lw)

                cv2.imwrite(os.path.join(args.dest_dir,img), ivus_img)
                break


main()

