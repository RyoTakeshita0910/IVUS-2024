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
from sklearn.metrics import roc_auc_score

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--eval_csv", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--gt_csv", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--thrs", type=float, default=0.55, help='path to the folder containing origial pngs')
args = parser.parse_args()

def draw(x,y,name):
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(1,1,1)

    #ax.scatter(x,y, c='orange',marker='o',s=5)
    # ax.plot(x,y,"-", linewidth=1)
    # ax.plot(x,y,"-", c='red', linewidth=2)
    ax.plot(x,y,"-", c='#ed551b', linewidth=2)


    ax.set_title("ROC曲線", fontname="MS Gothic")
    ax.set_xlabel('False Positive Rate[%]', fontname="MS Gothic")
    ax.set_ylabel('True Positive Rate[%]', fontname="MS Gothic")
    ax.axline((0,0),(1,1),color='Black', lw=1, linestyle='dashed')

    fig.savefig(os.path.join(args.dest_dir, name))

def calc_roc(pred,label,thrs,true_thrs):
    true_cnt = 0
    fp_cnt = 0
    bad_cnt = 0
    data_num = len(pred)
    for i in range(data_num):
        if pred[i] >= thrs and label[i] >= true_thrs: #recall
            true_cnt += 1
            bad_cnt += 1
        elif pred[i] >= thrs and label[i] < true_thrs: # false positve
            fp_cnt += 1
        elif pred[i] < thrs and label[i] >= true_thrs: # count number of bad
            bad_cnt += 1
    
    tpr = float(true_cnt / bad_cnt)
    fpr = float(fp_cnt / (data_num - bad_cnt))
    #print(tpr)
    #print(fpr)

    return tpr, fpr

def calc_auc(label,pred,true_thrs):
    data_num = len(pred)
    true_list = np.zeros(data_num)
    for i in range(data_num):
        if label[i] >= true_thrs:
            true_list[i] = 1
    
    #print(pred)
    #print(true_list)
    auc = roc_auc_score(np.array(true_list),np.array(pred))

    return auc


def main():
    true_thrs = args.thrs

    data_name = os.path.basename(args.eval_csv).split('.')[0]

    tpr_list = []
    fpr_list = []

    pred_ratio = []
    with open(args.eval_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            pred_ratio.append(float(row[1]))

    gt_ratio = []
    with open(args.gt_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            gt_ratio.append(float(row[1]))

    #print("pred",pred_ratio)
    #print("gt",gt_ratio)

    assert len(pred_ratio) ==  len(gt_ratio)

    out_list = []
    for i in range(0,101,5):
        thrs = float(i / 100)
        print(thrs)
        tpr, fpr = calc_roc(pred_ratio, gt_ratio, thrs, true_thrs)
        tpr_list.append(tpr)
        fpr_list.append(fpr)
        print('感度:',tpr)
        print('特異度:',(1-fpr))
        out_list.append([thrs,tpr,fpr])

    draw(fpr_list, tpr_list, data_name)
    #print(fpr_list)
    #print(tpr_list)

    auc = calc_auc(gt_ratio,pred_ratio,true_thrs)
    print("AUC:",auc)

    with open(os.path.join(args.dest_dir,'{}.csv'.format(data_name)), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['threshold','sensitivity','specificity'])
        for row in out_list:
            writer.writerow(row)
        writer.writerow([''])
        writer.writerow(['AUC',auc])

main()