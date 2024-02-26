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
parser.add_argument("--lumen_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--media_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--wire_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

w = 512
h = 512

lw = 2

def set_branch(ivus, bra):
    for y in range(h):
        for x in range(w):
            if all(bra[y][x] == [0,0,255]):
                ivus[y][x] = [0,0,255]
    
    return ivus


def main():

    if not os.path.isdir(args.dest_dir):
        os.mkdir(args.dest_dir)

    img_list = sorted(os.listdir(args.img_dir))
    lumen_list = sorted(os.listdir(args.lumen_dir))
    media_list = sorted(os.listdir(args.media_dir))
    wire_list = sorted(os.listdir(args.wire_dir))

    for img in img_list:
        # pick = '0034_4581954_000588.png'
        # pick = '0062_04670213_002675.png'
        # pick = '0113_3947173_000233.png'
        # if img != pick:
        #     continue
        # pick = ['0034_4581954_000588', '0062_04670213_002675', '0113_3947173_000233']
        # pick = ['0036_04596528_001244']
        # pick = ['0013_04687639_001117','0013_04687639_001057','0013_04687639_001087','0013_04687639_001147','0013_04687639_001177']
        # pick = ['0087_04625013_001957','0087_04625013_002017','0087_04625013_002077']
        # if not img.split('.')[0] in pick:
        #     continue
        for lumen in lumen_list:
            if img == lumen:
                for media in media_list:
                    if img == media:
                        for wire in wire_list:
                            if img == wire:
                                print(img)
                                ivus_img = cv2.imread(os.path.join(args.img_dir,img))
                                l_img = cv2.imread(os.path.join(args.lumen_dir,lumen), cv2.IMREAD_GRAYSCALE)
                                m_img = cv2.imread(os.path.join(args.media_dir,media),cv2.IMREAD_GRAYSCALE)
                                w_img = cv2.imread(os.path.join(args.wire_dir,wire),cv2.IMREAD_GRAYSCALE)


                                l_con, _ = cv2.findContours(l_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                                m_con, _ = cv2.findContours(m_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                                w_con, _ = cv2.findContours(w_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                                ivus_img = cv2.drawContours(ivus_img, l_con, 0, (0,255,0), lw)
                                ivus_img = cv2.drawContours(ivus_img, m_con, 0, (0,165,255), lw)
                                for i in range(len(w_con)):
                                    ivus_img = cv2.drawContours(ivus_img, [w_con[i]], 0, (255,255,0), lw)

                                cv2.imwrite(os.path.join(args.dest_dir,img), ivus_img)
                                break


main()

