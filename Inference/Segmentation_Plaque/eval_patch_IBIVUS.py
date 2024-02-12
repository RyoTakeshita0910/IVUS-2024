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
parser.add_argument("--eval_csv", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--gt_csv", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--out_csv", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

def main():
    
    file_list = []
    

    eval_list = []
    row_cnt = 0
    with open(args.eval_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            if row_cnt == 0:
                row_cnt += 1
                continue
            eval_list.append(row[1:])
    
    gt_list = []
    row_cnt = 0
    with open(args.gt_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            if row_cnt == 0:
                row_cnt += 1
                continue
            gt_list.append(row[1:])
    

    c_cnt = np.zeros((6,6))
    
    for i in range(len(gt_list)):
        for j in range(len(gt_list[i])):
            gtc = int(gt_list[i][j])
            if gtc != 0:
                evalc = int(eval_list[i][j])
                c_cnt[evalc][gtc] += 1

    p_list = []
    for i in range(6):
        sum = 0
        for j in range(6):
            sum += c_cnt[j][i]
        p = c_cnt[i][i] / sum * 100
        p_list.append(p)

            
    with open(args.out_csv, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['Black', 'Blue', 'Green', 'Purple', 'Red', 'Yellow'])
        for row in c_cnt:
            writer.writerow(row)
        
        writer.writerow([''])
        writer.writerow(p_list)

main()


