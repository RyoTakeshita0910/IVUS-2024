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
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing IB-IVUS pngs')
parser.add_argument("--out_csv", type=str, required=True, help='path to the output csv ')
args = parser.parse_args()

h = 512
w = 512

# 各プラーク成分の面積を計測するメソッド
def check_seg(fname,img):

    cnt_b = 0
    cnt_g = 0
    cnt_p = 0
    cnt_y = 0
    cnt_r = 0
    
    row_list = []
    for y in range(h):
        for x in range(w):
            img_c = img[y][x]
            # blue
            if all(img_c == [255,0,0]):
                cnt_b += 1
            # green
            elif all(img_c == [0,255,0]):
                cnt_g += 1
            # purple
            elif all(img_c == [170,0,85]):
                cnt_p += 1
            # red
            elif all(img_c == [0,0,255]):
                cnt_r += 1
            # yellow
            elif all(img_c == [0,255,255]):
                cnt_y += 1

    row_list.append(fname)
    row_list.append(cnt_p)
    row_list.append(cnt_b)
    row_list.append(cnt_g)
    row_list.append(cnt_y)
    row_list.append(cnt_r)

    return row_list


def main():
    
    img_list = sorted(os.listdir(args.img_dir))

    out_list = []
    for img in img_list:
        img_name = img.split('.')[0]
        in_img = cv2.imread(os.path.join(args.img_dir, img))
        seg_rate = check_seg(img_name,in_img)
        out_list.append(seg_rate)
        
    # 各プラーク成分の面積をcsvに保存
    with open(args.out_csv, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['img_name', 'purple_PA','blue_PA','green_PA','yellow_PA','Red_PA'])
        for row in out_list:
            writer.writerow(row)

main()


