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
import csv

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--out_csv", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

def check_seg(img):
    h = img.shape[0]
    w = img.shape[1]

    cnt_bp = 0
    cnt_all = 0

    for y in range(h):
        for x in range(w):
            img_c = img[y][x]
            
            # blue
            if all(img_c == [255,0,0]):
                cnt_bp += 1
                cnt_all += 1
            # green
            elif all(img_c == [0,255,0]):
                cnt_all += 1

            # purple
            elif all(img_c == [170,0,85]):
                cnt_bp += 1
                cnt_all += 1
            
            # red
            elif all(img_c == [0,0,255]):
                cnt_all += 1

            # yellow
            elif all(img_c == [0,255,255]):
                cnt_all += 1

    bp_rate = float(cnt_bp/cnt_all)

    return bp_rate


def main():
    time_start = time.time()
    
    img_list = sorted(os.listdir(args.img_dir))

    out_list = []
    for img in img_list:
        img_name = img.split('.')[0]
        print(img_name)
        in_img = cv2.imread(os.path.join(args.img_dir, img))
        bp_rate = check_seg(in_img)
        out_list.append([img_name, bp_rate])
        
    with open(args.out_csv, 'w', newline = '') as f:
        writer = csv.writer(f)
        #writer.writerow(['img_name', 'blue & purple ratio'])
        for out in out_list:
            writer.writerow(out)


    time_end = time.time()
    outtime = time_end - time_start
    print(outtime)

main()


