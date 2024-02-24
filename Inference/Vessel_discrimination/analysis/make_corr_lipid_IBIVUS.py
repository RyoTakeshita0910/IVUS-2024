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
import pandas as pd
from scipy.stats import pearsonr

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--eval_csv", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--gt_csv", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
#parser.add_argument("--thrs", type=float, required=True, help='path to the folder containing origial pngs')
args = parser.parse_args()

def draw(x,y,name):
    fig = plt.figure(figsize=(7,7))

    # res = pearsonr(x, y)
    # if res[1] < 0.001:
    #     p_txt = 'p<0.001'
    # elif res[1] < 0.005:
    #     p_txt = 'p<0.005'
    # elif res[1] < 0.01:
    #     p_txt = 'p<0.01'
    # elif res[1] < 0.05:
    #     p_txt = 'p<0.05'
    # else:
    #     p_txt = ''
    ax = fig.add_subplot(1,1,1)

    #ax.scatter(x,y, c='orange',marker='o',s=5)
    ax.scatter(x,y,c ='green' ,alpha=0.5)
    # ax.text(5,90,'R={:.3f}, {}'.format(res[0],p_txt),horizontalalignment="left")

    #ax.legend(prop={"family":"MS Gothic"})
    ax.set_title("相関グラフ(脂質プラークの割合)", fontname="MS Gothic")
    # ax.set_xlabel('Label (Blue & Purple Ratio) [%]')
    # ax.set_ylabel('Predict (Blue & Purple Ratio) [%]')
    ax.set_xlabel('正解 脂質プラーク割合 [%]', fontname="MS Gothic")
    ax.set_ylabel('予測 脂質プラーク割合 [%]', fontname="MS Gothic")
    ax.set_xlim([0,100])
    ax.set_ylim([0,100])
    

    fig.savefig(os.path.join(args.dest_dir, name))

def main():

    data_name = os.path.basename(args.eval_csv).split('.')[0]

    pred_ratio = []
    with open(args.eval_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            pred_ratio.append(float(row[1])*100)

    gt_ratio = []
    with open(args.gt_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            gt_ratio.append(float(row[1])*100)

    #print("pred",pred_ratio)
    #print("gt",gt_ratio)

    draw(gt_ratio, pred_ratio, data_name)

    s_gt = pd.Series(gt_ratio)
    s_pred = pd.Series(pred_ratio)
    corr = s_gt.corr(s_pred)
    print("相関係数：",corr)
    res = pearsonr(gt_ratio, pred_ratio)
    print('相関係数：{},p値：{:f}'.format(res[0],res[1]))

main()


