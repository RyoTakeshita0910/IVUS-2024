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
parser.add_argument("--lumen_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--media_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--wire_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()


h=512
w=512

def make_dir(path):
    if not os.path.isdir(os.path.join(path,"Lumen")):
        os.mkdir(os.path.join(path,"Lumen"))

    if not os.path.isdir(os.path.join(path,"Media")):
        os.mkdir(os.path.join(path,"Media"))


def set_trace(img):
    for y in range(h):
        for x in range(w):
            if img[y][x] < 0:
                img[y][x] = 0


def set_input(img,bi):
    h = img.shape[0]
    w = img.shape[1]

    for y in range(h):
        for x in range(w):
            bi_c = bi[y][x]
            if bi_c == 0:
                img[y][x] = [255,255,0]

    return img


def main():

    if not os.path.isdir(args.dest_dir):
        os.mkdir(args.dest_dir)
    
    lumen_list = sorted(os.listdir(args.lumen_dir))
    media_list = sorted(os.listdir(args.media_dir))
    wire_list = sorted(os.listdir(args.wire_dir))

    img_list = sorted(os.listdir(args.img_dir))

    for l in lumen_list:
        for m in media_list:
            if l == m:
                for w in wire_list:
                    if l == w:
                        l_img = cv2.imread(os.path.join(args.lumen_dir,l), cv2.IMREAD_GRAYSCALE)
                        m_img = cv2.imread(os.path.join(args.media_dir,m), cv2.IMREAD_GRAYSCALE)
                        w_img = cv2.imread(os.path.join(args.wire_dir,w), cv2.IMREAD_GRAYSCALE)

                        trace_mask = m_img.astype(float) - l_img.astype(float) - w_img.astype(float)
                        set_trace(trace_mask)

                        for img in img_list:
                            if l == img:
                                ivus_img = cv2.imread(os.path.join(args.img_dir, img))
                                ib_input = set_input(ivus_img, trace_mask)
                                cv2.imwrite(os.path.join(args.dest_dir,img), ib_input)
                                break
                        break
                break

main()


