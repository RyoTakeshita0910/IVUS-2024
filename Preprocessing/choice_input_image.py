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
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing dicoms') # 画像フォルダが入っているフォルダのパス
parser.add_argument("--gt_dir", type=str, required=True, help='path to the folder containing dicoms') # 正解ラベルの元画像が入っているパス
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder') # 保存先のフォルダのパス
args = parser.parse_args()


def main():
    img_flist = sorted(os.listdir(args.img_dir)) # 画像フォルダのリストアップ
    gt_list = sorted(os.listdir(args.gt_dir)) # 正解ラベルの元画像のリストアップ
    for gt in gt_list:
        dir_name = gt.split('_')[0]
        img_name = gt.split('_')[1]
        for img_folder in img_flist:
            if img_folder == dir_name:
                img_list = sorted(os.listdir(os.path.join(args.img_dir, img_folder)))
                if img_name in img_list:
                    img_path = os.path.join(args.img_dir,img_folder,img_name)
                    # Write : img_pathの画像をdest_dirにコピーするプログラムを書いてください。
                    # ただし、コピー先のファイル名はgtと同じになるようにしてください。
                    copy(img_path,os.path.join(args.dest_dir,gt))

main()
    
   

