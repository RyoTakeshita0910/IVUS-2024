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
parser.add_argument("--src_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()


def main():
    imgList = sorted(os.listdir(args.src_dir))

    red_path = os.path.join(args.dest_dir,'red')
    if not os.path.isdir(red_path):
        os.mkdir(red_path)

    yel_path = os.path.join(args.dest_dir,'yellow')
    if not os.path.isdir(yel_path):
        os.mkdir(yel_path)

    gre_path = os.path.join(args.dest_dir,'green')
    if not os.path.isdir(gre_path):
        os.mkdir(gre_path)

    pur_path = os.path.join(args.dest_dir,'purple')
    if not os.path.isdir(pur_path):
        os.mkdir(pur_path)
        
    blu_path = os.path.join(args.dest_dir,'blue')
    if not os.path.isdir(blu_path):
        os.mkdir(blu_path)
        
    bla_path = os.path.join(args.dest_dir,'black')
    if not os.path.isdir(bla_path):
        os.mkdir(bla_path)

    gt_path = os.path.join(args.dest_dir,'gt')
    if not os.path.isdir(gt_path):
        os.mkdir(gt_path)
        
    


    for img in imgList:
        imgPath = os.path.join(args.src_dir, img)
        print(img)
        src_im = cv2.imread(imgPath)
        np_im = src_im.astype(int)

        height = src_im.shape[0]
        width = src_im.shape[1]

        np_red = np.zeros((height,width))
        np_yel = np.zeros((height,width))
        np_gre = np.zeros((height,width))
        np_pur = np.zeros((height,width))
        np_blu = np.zeros((height,width))
        np_bla = np.zeros((height,width))
        
        for h in range(height):
            for w in range(width):
                if h > 475:
                    np_im[h][w] = [0, 0, 0]
                if h > 55 and h < 70 and w < 70:
                    np_im[h][w] = [0, 0, 0]
                if w < 10:
                    np_im[h][w] = [0, 0, 0]

        for y in range(height):
            for x in range(width):
                imc = np_im[y][x]
                # red
                if all(imc == [0,0,255]):
                    np_red[y][x] = 255
                # yellow
                elif all(imc == [0,255,255]):
                    np_yel[y][x] = 255
                # green
                elif all(imc == [0,255,0]):
                    np_gre[y][x] = 255
                # purple
                elif all(imc == [170,0,85]):
                    np_pur[y][x] = 255
                # blue
                elif all(imc == [255,0,0]):
                    np_blu[y][x] = 255
                # back ground
                elif all(imc == [255,255,255]):
                    np_bla[y][x] = 255
                elif all(imc == [0,0,0]):
                    np_bla[y][x] = 255
        

        cv2.imwrite(os.path.join(gt_path, img), np_im.astype('uint8'))
        cv2.imwrite(os.path.join(red_path, img), np_red.astype('uint8'))
        cv2.imwrite(os.path.join(yel_path, img), np_yel.astype('uint8'))
        cv2.imwrite(os.path.join(gre_path, img), np_gre.astype('uint8'))
        cv2.imwrite(os.path.join(pur_path, img), np_pur.astype('uint8'))
        cv2.imwrite(os.path.join(blu_path, img), np_blu.astype('uint8'))
        cv2.imwrite(os.path.join(bla_path, img), np_bla.astype('uint8'))

main()


