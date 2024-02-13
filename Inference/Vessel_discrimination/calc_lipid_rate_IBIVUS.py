import argparse
import os
import os.path
import ctypes
from shutil import rmtree, move
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import csv

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing IB-IVUS pngs')
parser.add_argument("--out_csv", type=str, required=True, help='path to the output csv')
args = parser.parse_args()

h = 512
w = 512

# 脂質プラークの割合を計測するメソッド
def check_seg(img):
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

    # 脂質プラークの割合
    bp_rate = float(cnt_bp/cnt_all)

    return bp_rate


def main():
    
    img_list = sorted(os.listdir(args.img_dir))

    out_list = []
    for img in img_list:
        img_name = img.split('.')[0]
        print(img_name)
        in_img = cv2.imread(os.path.join(args.img_dir, img))
        bp_rate = check_seg(in_img)
        out_list.append([img_name, bp_rate])
        
    # csvに脂質プラークの割合を書き込み保存
    with open(args.out_csv, 'w', newline = '') as f:
        writer = csv.writer(f)
        for out in out_list:
            writer.writerow(out)

main()


