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

def set_error():
    max_len = 0
    for e in error_all:
        e_len = len(e)
        if max_len < e_len:
            max_len = e_len
    
    for i,e in enumerate(error_all):
        dif_len = max_len -len(e)
        for j in range(dif_len):
            error_all[i].append('')
    
    new_elist =[]
    for i in range(max_len):
        tmp =[]
        for j in range(len(error_all)):
            tmp.append(error_all[j][i])
        new_elist.append(tmp)

    return new_elist

def draw(x,y,name,color):
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

    ax.axhline(md, c='Black', linestyle='--',linewidth=3)
    ax.axhline(loa_p, c='Black', linestyle='--',linewidth=3)
    ax.axhline(loa_m, c='Black', linestyle='--',linewidth=3)

    if color == 'yellow':
        ax.scatter(mean,diff,c='#fcc800',alpha=0.5)
    else:
        ax.scatter(mean,diff,c=color,alpha=0.5)

    # ax.text(m_max*0.8,md,"mean[{:6.01f}]".format(md),fontsize=10)
    # ax.text(m_max*0.8,loa_p,"+1.96SD[{:6.01f}]".format(loa_p),fontsize=10)
    # ax.text(m_max*0.8,loa_m,"-1.96SD[{:6.01f}]".format(loa_m),fontsize=10)

    fig.savefig(os.path.join(args.dest_dir,'{}_{}.png'.format(name,color)))
    plt.close()


def set_num(dlist):
    num_list = []
    for dname in dlist:
        num = dname.split('_')[0]
        if not num in num_list:
            num_list.append(num)
    
    return num_list


def bland_altman_plot(x,y,dlist,name,color):
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

    # print('\n')
    # print(color)

    error_data = []
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
                    # print(dlist[i])
                    tmp_mean.append(mean[i])
                    tmp_diff.append(diff[i])
                    error_data.append(dlist[i])
        
        # if e_flag:
        if ecnt >= 3:
            plt.plot(tmp_mean,tmp_diff,c=np.random.rand(3,),label=num,marker='o')
            # print(num)
        # else:
        #     # plt.plot(tmp_mean,tmp_diff,c='orange',label='in_LOA')
        #     plt.plot(tmp_mean,tmp_diff,c='orange',marker='o')
    
    error_all.append(error_data)

    plt.legend()
    plt.savefig(os.path.join(args.dest_dir,'ERROR_{}_{}.png'.format(name,color)))
    plt.close()



def main():

    data_name = os.path.basename(args.eval_csv).split('.')[0]

    color_list = ['purple','blue','green','yellow','red']

    if not os.path.isdir(args.dest_dir):
        os.mkdir(args.dest_dir)

    data_list = []
    pred_ratio = [[],[],[],[],[]]
    with open(args.eval_csv) as f:
        reader = csv.reader(f)
        row_cnt = 0
        for row in reader:
            if row_cnt == 0:
                row_cnt += 1
                continue
            else:
                data_list.append(row[0])
                for i in range(5):
                    pred_ratio[i].append(float(row[i+1]))
                row_cnt += 1

    gt_ratio = [[],[],[],[],[]]
    with open(args.gt_csv) as f:
        reader = csv.reader(f)
        row_cnt = 0
        for row in reader:
            if row_cnt == 0:
                row_cnt += 1
                continue
            else:
                for i in range(5):
                    gt_ratio[i].append(float(row[i+1]))
                row_cnt += 1

    for i in range(5):
        # draw(gt_ratio[i],pred_ratio[i],data_name,color_list[i])
        draw(gt_ratio[i],pred_ratio[i],data_name,color_list[i])
        bland_altman_plot(gt_ratio[i],pred_ratio[i],data_list,data_name,color_list[i])
    
    error_list = set_error()
    
    with open(os.path.join(args.dest_dir, 'ERROR_{}.csv'.format(data_name)), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(color_list)
        for row in error_list:
            writer.writerow(row)

main()


