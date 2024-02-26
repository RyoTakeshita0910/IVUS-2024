import argparse
import os
import os.path
import ctypes
from shutil import rmtree, move, copy
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from natsort import natsorted
import seaborn as sns
import time
import cv2
import csv
import json

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--json_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--ref_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

width = 512
height = 512


def json2outline(dest,points,num):
    img = Image.new("L", (width, height), "Black")
    draw = ImageDraw.Draw(img)

    for i in range(len(points)):
        if i == len(points)-1:
            sx = int(points[i][0])
            sy = int(points[i][1])
            ex = int(points[0][0])
            ey = int(points[0][1])
        else:
            sx = int(points[i][0])
            sy = int(points[i][1])
            ex = int(points[i+1][0])
            ey = int(points[i+1][1])
        # print([(sx,sy),(ex,ey)])
        draw.line([(sx,sy),(ex,ey)], fill='white', width=1)
    
    dest_path = os.path.join(dest,'{:06}.png'.format(num))
    img.save(dest_path)

    return dest_path


def outline2mask(dest,img_path,name,num):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img = cv2.drawContours(img, [contours[0]], 0, (255,255,255), -1)

    cv2.imwrite(os.path.join(dest,'{}_{:06}.png'.format(name,num)), img)


def set_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def main():

    set_dir(args.dest_dir)

    ivus_path = os.path.join(args.dest_dir,'images')
    set_dir(ivus_path)
    mask_path = os.path.join(args.dest_dir,'masks')
    set_dir(mask_path)
    
    json_dlist = sorted(os.listdir(args.json_dir))
    ref_list = sorted(os.listdir(args.ref_dir))

    for j_dir in json_dlist:
        tmp_dir = os.path.join(args.dest_dir,'tmp')
        set_dir(tmp_dir)
        for ref_dir in ref_list:
            if j_dir == ref_dir:
                # dataname = j_dir.split('-')[0]
                dataname = j_dir.split('_')[0]

                json_path = os.path.join(args.json_dir,j_dir)
                json_list = sorted(os.listdir(json_path))

                ref_path = os.path.join(args.ref_dir,ref_dir)
                rim_list = sorted(os.listdir(ref_path))

                for js in json_list:
                    jnum = int(js.split('.')[0])
                    img_num = int(rim_list[jnum].split('.')[0])

                    json_open = open(os.path.join(json_path,js),'r')
                    json_load = json.load(json_open)
                    if len(json_load['shapes']) != 0:
                        points = json_load['shapes'][0]['points']
                    else:
                        continue

                    tmp_path = json2outline(tmp_dir, points, img_num)
                    outline2mask(mask_path, tmp_path, dataname, img_num)
                    copy(os.path.join(ref_path,rim_list[jnum]),os.path.join(ivus_path,'{}_{:06}.png'.format(dataname,img_num)))
                
                break
        
        rmtree(tmp_dir)
    

main()


