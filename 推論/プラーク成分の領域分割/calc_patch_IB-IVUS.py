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
parser.add_argument("--dest_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--csv_name", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

all_dict = {}
for i in range(6):
    all_dict[i] = 0

# image size
h = 512
w = 512

# patch image size 
ph = 32
pw = 32

def check_color(img):
    c_dict = {}
    for i in range(6):
        c_dict[i] = 0

    for y in range(ph):
        for x in range(pw):
            img_c = img[y][x]

            # black or white
            if all(img_c == [0,0,0]) or all(img_c == [255,255,255]):
                c_dict[0] += 1

            # blue
            if all(img_c == [255,0,0]):
                c_dict[1] += 1

            # green
            elif all(img_c == [0,255,0]):
                c_dict[2] += 1

            # purple
            elif all(img_c == [170,0,85]):
                c_dict[3] += 1
            
            # red
            elif all(img_c == [0,0,255]):
                c_dict[4] += 1

            # yellow
            elif all(img_c == [0,255,255]):
                c_dict[5] += 1

    out_c = 0
    c_max = 0
    for i in range(5):
        if c_max < c_dict[i+1]:
            out_c = i+1
            c_max = c_dict[i+1]
    
    all_dict[out_c] += 1

    return out_c

def pick_patch(img,img_name):
    dest_dir = os.path.join(args.dest_dir,img_name)
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)
    
    out_list = [img_name]
    yp_num = int(h/ph)
    xp_num = int(w/pw)

    for yp in range(yp_num):
        for xp in range(xp_num):
            patch_img = img[ph*yp:ph*(yp+1), pw*(xp):pw*(xp+1)]
            patch_class = check_color(patch_img)
            out_list.append(patch_class)
            cv2.imwrite(os.path.join(dest_dir,'{}_{:03}-{:03}.png'.format(img_name,yp,xp)),patch_img)
    
    return out_list

def main():

    if not os.path.isdir(args.dest_dir):
        os.mkdir(args.dest_dir)
    
    img_list = sorted(os.listdir(args.img_dir))

    out_list = []
    for img in img_list:
        img_name = img.split('.')[0]
        print(img_name)
        in_img = cv2.imread(os.path.join(args.img_dir, img))
        img_class = pick_patch(in_img,img_name)
        out_list.append(img_class)
    
    column_row = ['img_name']
    for yp in range(int(h/ph)):
        for xp in range(int(w/pw)):
            column_row.append('{:03}-{:03}'.format(yp,xp))
    
    print(all_dict)

    with open(os.path.join(args.dest_dir,args.csv_name), 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(column_row)
        for out in out_list:
            writer.writerow(out)
        
        # writer.writerow([''])
        # writer.writerow(['Black', 'Blue', 'Green', 'Purple', 'Red', 'Yellow'])
        # writer.writerow([all_dict[0], all_dict[1], all_dict[2], all_dict[3], all_dict[4], all_dict[5]])

main()


