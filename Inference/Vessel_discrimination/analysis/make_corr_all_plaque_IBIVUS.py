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

def draw(x,y,name,color):
    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(1,1,1)

    #ax.scatter(x,y, c='orange',marker='o',s=5)
    ax.scatter(x,y, c='orange')

    #ax.legend(prop={"family":"MS Gothic"})
    ax.set_title("相関グラフ()".format(color), fontname="MS Gothic")
    # ax.set_xlabel('Label (Blue & Purple Ratio) [%]')
    # ax.set_ylabel('Predict (Blue & Purple Ratio) [%]')
    ax.set_xlabel('Label ({} Area) [pixels]'.format(color))
    ax.set_ylabel('Predict ({} Area) [pixels]'.format(color))
    # ax.set_xlim([0,100])
    # ax.set_ylim([0,100])

    fig.savefig(os.path.join(args.dest_dir, name+'_'+color))


def draw_all(x,y,name,color):
    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(1,1,1)

    #ax.scatter(x,y, c='orange',marker='o',s=5)
    for i in range(len(color)):
        if color[i] == 'yellow':
            ax.scatter(x[i],y[i],c='#fcc800',alpha=0.2)
            continue
        ax.scatter(x[i],y[i], c=color[i], alpha=0.2)

    #ax.legend(prop={"family":"MS Gothic"})
    ax.set_title("相関グラフ(プラークの面積)", fontname="MS Gothic")
    # ax.set_xlabel('Label (Blue & Purple Ratio) [%]')
    # ax.set_ylabel('Predict (Blue & Purple Ratio) [%]')
    ax.set_xlabel('正解 プラークの面積 [pixels]'.format(color), fontname="MS Gothic")
    ax.set_ylabel('予測 プラークの面積 [pixels]'.format(color), fontname="MS Gothic")
    # ax.set_xlim([0,100])
    # ax.set_ylim([0,100])

    fig.savefig(os.path.join(args.dest_dir, name+'_all'))

def main():

    data_name = os.path.basename(args.eval_csv).split('.')[0]

    color_list = ['purple','blue','green','yellow','red']

    pred_all = []
    pred_area = [[],[],[],[],[]]
    with open(args.eval_csv) as f:
        reader = csv.reader(f)
        row_cnt = 0
        for row in reader:
            if row_cnt == 0:
                row_cnt += 1
                continue
            else:
                for i in range(5):
                    pred_area[i].append(int(row[i+1]))
                    pred_all.append(int(row[i+1]))
                row_cnt += 1

    gt_all = []
    gt_area = [[],[],[],[],[]]
    with open(args.gt_csv) as f:
        reader = csv.reader(f)
        row_cnt = 0
        for row in reader:
            if row_cnt == 0:
                row_cnt += 1
                continue
            else:
                for i in range(5):
                    gt_area[i].append(int(row[i+1]))
                    gt_all.append(int(row[i+1]))
                row_cnt += 1

    print("pred",pred_area)
    print("gt",gt_area)


    corr_list = []
    for i in range(5):
        draw(gt_area[i],pred_area[i],data_name,color_list[i])
        # s_gt = pd.Series(gt_area[i])
        # s_pred = pd.Series(pred_area[i])
        # corr = s_gt.corr(s_pred)
        # print("相関係数({})：".format(color_list[i]),corr)
        res = pearsonr(gt_area[i], pred_area[i])
        corr_list.append([color_list[i], res[0], res[1]])
        print('相関係数：{},p値：{:f}'.format(res[0],res[1]))
    
    draw_all(gt_area, pred_area,data_name,color_list)
    res = pearsonr(gt_all, pred_all)
    corr_list.append(['all',res[0],res[1]])
    print('相関係数：{},p値：{:f}'.format(res[0],res[1]))

    with open(os.path.join(args.dest_dir,'Corr_{}.csv'.format(data_name)), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['plaque', 'corr','p'])
        for row in corr_list:
            writer.writerow(row)


main()


