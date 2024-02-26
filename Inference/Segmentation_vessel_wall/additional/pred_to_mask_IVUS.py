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
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--resize", type=int, default=-1, help='path to the output dataset folder')
parser.add_argument("--dtype", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

def make_dir(path):
    if not os.path.isdir(os.path.join(path,args.dtype)):
        os.mkdir(os.path.join(path,args.dtype))

def pick_label(retval, labels, stats):
    height = labels.shape[0]
    width = labels.shape[1]

    label_num = labels[255][255]

    if label_num == 0:
        label_list = []
        for i in range(retval):
            area = stats[i][-1]
            label_list.append(area)

        #print(label_list)
        max_area = max(label_list)
        max_idx = label_list.index(max_area)

        label_list[max_idx] = 0

        sec_area = max(label_list)
        label_num = label_list.index(sec_area)

    for h in range(height):
        for w in range(width):
            if labels[h][w] == label_num:
                labels[h][w] = 255
            else:
                labels[h][w] = 0

    return labels.astype('uint8')

def set_trace(img,h,w):
    for y in range(512):
        for x in range(512):
            if img[y][x] < 0:
                img[y][x] = 0


# Wireのラベル削除に関するメソッド
def pick_label_wire(retval, labels, stats):
    label_list = []
    # 面積が2000[pixel]以上150000[pixel]以下のラベルのラベル番号を全て取得
    for i in range(retval):
        area = stats[i][-1]
        if area >= 2000 and area < 150000:
            label_list.append(i)

    # 取得したラベル番号以外のラベルを削除
    for y in range(h):
        for x in range(w):
            if labels[y][x] in label_list:
                labels[y][x] = 255
            else:
                labels[y][x] = 0

    return labels.astype('uint8')

def set_input(img,bi):
    h = img.shape[0]
    w = img.shape[1]

    for y in range(h):
        for x in range(w):
            bi_c = bi[y][x]
            if bi_c == 0:
                img[y][x] = [0,0,0]
            elif bi_c == 128:
                img[y][x] = [255,255,0]

    return img

def main():

    assert args.dtype == 'Lumen' or args.dtype == 'Media' or args.dtype == 'Wire'

    img_path = args.img_dir
    img_list = sorted(os.listdir(img_path))
    width = 512
    height = 512

    if args.resize != -1:
        width = args.resize
        height = args.resize

        res_path = os.path.join(args.dest_dir,"resize")
        if not os.path.isdir(res_path):
            os.mkdir(res_path)
        make_dir(res_path)

        for img in img_list:
            im = Image.open(os.path.join(img_path, img))
            im_res = im.resize((width,height))
            im_res.save(os.path.join(res_path,args.dtype,img))

        img_path = os.path.join(res_path,args.dtype)
        img_list = sorted(os.listdir(img_path))


    otsu_path = os.path.join(args.dest_dir,"otsu")
    if not os.path.isdir(otsu_path):
        os.mkdir(otsu_path)
    make_dir(otsu_path)

    cut_path = os.path.join(args.dest_dir,"mask")
    if not os.path.isdir(cut_path):
        os.mkdir(cut_path)
    make_dir(cut_path)

    print(args.dtype, "Otsu & Cut")
    for img in img_list:
        im = cv2.imread(os.path.join(img_path,img),cv2.IMREAD_GRAYSCALE)

        # Otsu
        ret, otsu = cv2.threshold(im, 0, 255, cv2.THRESH_OTSU)
        cv2.imwrite(os.path.join(otsu_path,args.dtype,img), otsu)

        # cut
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(otsu)
        if args.dtype == 'Wire':
            cut = pick_label_wire(ret, labels, stats)
        else:
            cut = pick_label(ret, labels, stats)
        contours, hierarchy = cv2.findContours(cut, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(contours)):
            drawarea = cv2.contourArea(contours[i])
            #print(i, " drawarea:",drawarea)
            out = cv2.drawContours(cut, [contours[i]], 0, 255, -1)
        cv2.imwrite(os.path.join(cut_path,args.dtype,img), out)

main()


