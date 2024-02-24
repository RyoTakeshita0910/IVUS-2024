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
import statsmodels.api as sm

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--eval_csv", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--gt_csv", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
#parser.add_argument("--thrs", type=float, required=True, help='path to the folder containing origial pngs')
args = parser.parse_args()

error_all = []

def draw(x,y,name):
    x = np.asarray(x)
    y = np.asarray(y)
    mean = np.mean([x,y],axis=0)
    diff = x - y
    md = np.mean(diff)
    sd = np.std(diff, axis=0)

    loa_p = md + 1.96*sd
    loa_m = md - 1.96*sd

    fig = plt.figure(figsize=(7,6))
    ax = fig.add_subplot(1,1,1)

    m_max = np.max(mean)
    print(m_max)

    ax.set_xlabel('MMEAN')
    ax.set_ylabel('DIFF')

    # ax.axhline(md, c='gray', linestyle='--',alpha=0.5)
    # ax.axhline(loa_p, c='gray', linestyle='--',alpha=0.5)
    # ax.axhline(loa_m, c='gray', linestyle='--',alpha=0.5)

    ax.axhline(md, c='Black', linestyle='--', linewidth=3)
    ax.axhline(loa_p, c='Black', linestyle='--',linewidth=3)
    ax.axhline(loa_m, c='Black', linestyle='--',linewidth=3)
    ax.scatter(mean,diff,alpha=0.5)

    # ax.text(m_max*0.8,md,"mean[{:2.02f}]".format(md),fontsize=10)
    # ax.text(m_max*0.8,loa_p,"+1.96SD[{:2.02f}]".format(loa_p),fontsize=10)
    # ax.text(m_max*0.8,loa_m,"-1.96SD[{:2.02f}]".format(loa_m),fontsize=10)

    fig.savefig(os.path.join(args.dest_dir,'Lipid_rate_{}.png'.format(name)))
    plt.close()


def set_num(dlist):
    num_list = []
    for dname in dlist:
        num = dname.split('_')[0]
        if not num in num_list:
            num_list.append(num)
    
    return num_list


def bland_altman_plot(x,y,dlist,name):
    x = np.asarray(x)
    y = np.asarray(y)
    mean = np.mean([x,y],axis=0)
    diff = x - y
    md = np.mean(diff)
    sd = np.std(diff, axis=0)

    num_list = set_num(dlist)

    loa_p = md + 1.96*sd
    loa_m = md - 1.96*sd

    plt.axhline(md, c='gray', linestyle='--')
    plt.axhline(loa_p, c='gray', linestyle='--')
    plt.axhline(loa_m, c='gray', linestyle='--')

    for num in num_list:
        tmp_mean = []
        tmp_diff = []
        # e_flag = False
        ecnt = 0
        for i in range(len(dlist)):
            dnum = dlist[i].split('_')[0]
            if num == dnum:
                if diff[i] > loa_p or diff[i] < loa_m:
                    # e_flag  = True
                    ecnt += 1
                    tmp_mean.append(mean[i])
                    tmp_diff.append(diff[i])
                    error_all.append(dlist[i])
        
        # if e_flag:
        if ecnt >= 3:
            plt.plot(tmp_mean,tmp_diff,c=np.random.rand(3,),label=num,marker='o')
            # print(num)
        # else:
        #     # plt.plot(tmp_mean,tmp_diff,c='orange',label='in_LOA')
        #     plt.plot(tmp_mean,tmp_diff,c='orange',marker='o')
        
    plt.legend()
    plt.savefig(os.path.join(args.dest_dir,'ERROR_Lipid_rate_{}.png'.format(name)))
    plt.close()



def main():

    data_name = os.path.basename(args.eval_csv).split('.')[0]

    data_list = []
    pred_ratio = []
    with open(args.eval_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            data_list.append(row[0])
            pred_ratio.append(float(row[1])*100)

    gt_ratio = []
    with open(args.gt_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            gt_ratio.append(float(row[1])*100)

    
    draw(gt_ratio,pred_ratio,data_name)
    bland_altman_plot(gt_ratio,pred_ratio,data_list,data_name)

    with open(os.path.join(args.dest_dir, 'ERROR_{}.csv'.format(data_name)), 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(error_all)):
            writer.writerow([error_all[i]])

main()


