import argparse
import os
import os.path
from shutil import rmtree, move, copy
import random

import pydicom
from PIL import Image
import numpy as np

import shutil
import datetime
import csv
from pathlib import Path

# コマンドライン引数
parser = argparse.ArgumentParser()
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing dicoms') # 正解ラベルの元画像のフォルダパス ~/GT_src
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder') # 保存先のフォルダのパス ~/GT_img
args = parser.parse_args()


def main():
    img_flist = sorted(os.listdir(args.img_dir)) # 画像フォルダのリストアップ
    for img_folder in img_flist:
        img_list = sorted(os.listdir(os.path.join(args.img_dir, img_folder)))
        for img in img_list:
            img_path = os.path.join(args.img_dir,img_folder,img)
            new_imgname = '{}_{}'.format(img_folder, img)
            copy(img_path, os.path.join(args.dest_dir,new_imgname))

main()
    
   

