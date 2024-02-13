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
import cv2
import csv

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--eval_csv", type=str, required=True, help='path to the prediction lipid rate csv')
parser.add_argument("--gt_csv", type=str, required=True, help='path to the ground-truth lipid rate csv')
parser.add_argument("--out_csv", type=str, required=True, help='path to the output csv')
parser.add_argument("--thrs", type=float, default=0.55, help='path to the thrershold of lipid rate')
args = parser.parse_args()


def judge_bg(bp):
    thrs = args.thrs

    if bp >= thrs:
        return 'Bad'
    elif bp < thrs:
        return 'Good'

def main():
    
    eval_list = []
    with open(args.eval_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            eval_list.append(row)

    gt_list = []
    with open(args.gt_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            gt_list.append(row)

    bb_cnt = 0
    bg_cnt = 0
    gb_cnt = 0
    gg_cnt = 0

    data_list = []
    for i in range(np.shape(eval_list)[0]):
        eval_file = eval_list[i][0]
        eval_bp = float(eval_list[i][1])

        for j in range(np.shape(gt_list)[0]):
            gt_file = gt_list[j][0]
            if gt_file == eval_file:
                gt_bp = float(gt_list[j][1])

                eval_dia = judge_bg(eval_bp)
                gt_dia = judge_bg(gt_bp)

                if eval_dia == 'Bad' and gt_dia == 'Bad':
                    bb_cnt += 1
                elif eval_dia == 'Bad' and gt_dia == 'Good':
                    bg_cnt += 1
                elif eval_dia == 'Good' and gt_dia == 'Bad':
                    gb_cnt += 1
                elif eval_dia == 'Good' and gt_dia == 'Good':
                    gg_cnt += 1

                data_list.append([eval_file,gt_bp,gt_dia,eval_bp,eval_dia])
                break

    sens = float(bb_cnt/(bb_cnt+gb_cnt))
    spec = float(gg_cnt/(bg_cnt+gg_cnt))


    # 症例 index 0:bad  1:good
    pb_cnt = [0,0] #bad patient
    pg_cnt = [0,0] #good patient

    out_list = []
    p_list = []
    
    gt_bad = False
    pred_bad = False

    gt_cnt = [0,0] # 1:bad_cnt 2:bad_連続_cnt
    pred_cnt = [0,0]

    bad_thrs = 3
    im_cnt = 0

    for i,row in enumerate(data_list):
        img_id = '{}_{}'.format(row[0].split('_')[0], row[0].split('_')[1])
        if not img_id in p_list:
            if i != 0:
                if gt_bad or gt_cnt[0] >= im_cnt/2:
                    if pred_bad or pred_cnt[0] >= im_cnt/2:
                        pb_cnt[0] += 1
                        out_list.append([p_list[-1],'Bad','Bad', gt_cnt[0], pred_cnt[0]])
                    else:
                        pb_cnt[1] += 1
                        out_list.append([p_list[-1],'Bad','Good', gt_cnt[0], pred_cnt[0]])
                else:
                    if pred_bad or pred_cnt[0] >= im_cnt/2:
                        pg_cnt[0] += 1
                        out_list.append([p_list[-1],'Good','Bad', gt_cnt[0], pred_cnt[0]])
                    else:
                        pg_cnt[1] += 1
                        out_list.append([p_list[-1],'Good','Good', gt_cnt[0], pred_cnt[0]])

   
            p_list.append(img_id)
            gt_bad = False
            pred_bad = False
            gt_cnt = [0,0]
            pred_cnt = [0,0]
            im_cnt = 0

        if row[2] == 'Bad':
            gt_cnt[0] += 1
            gt_cnt[1] += 1

            if gt_cnt[1] >= bad_thrs:
                gt_bad = True
        else:
            gt_cnt[1] = 0
            
        if row[4] == 'Bad':
            pred_cnt[0] += 1
            pred_cnt[1] += 1
            if pred_cnt[1] >= bad_thrs:
                pred_bad = True
        else:
            pred_cnt[1] = 0

        im_cnt += 1
        
        if i == len(data_list)-1:
            if gt_bad or gt_cnt[0] >= im_cnt/2:
                if pred_bad or pred_cnt[0] >= im_cnt/2:
                    pb_cnt[0] += 1
                    out_list.append([img_id,'Bad','Bad', gt_cnt[0], pred_cnt[0]])
                else:
                    pb_cnt[1] += 1
                    out_list.append([img_id,'Bad','Good', gt_cnt[0], pred_cnt[0]])
            else:
                if pred_bad or pred_cnt[0] >= im_cnt/2:
                    pg_cnt[0] += 1
                    out_list.append([img_id,'Good','Bad', gt_cnt[0], pred_cnt[0]])
                else:
                    pg_cnt[1] += 1
                    out_list.append([img_id,'Good','Good', gt_cnt[0], pred_cnt[0]])
    
    psens = float(pb_cnt[0]/sum(pb_cnt))
    pspec = float(pg_cnt[1]/sum(pg_cnt))

    print(p_list)
    print(out_list)

    with open(args.out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['断面'])
        writer.writerow(['img_name','true blue & purple ratio', 'true result', 'eval blue & purple ratio', 'eval result'])
        for data in data_list:
            writer.writerow(data)
        writer.writerow([''])

        writer.writerow(['断面','不安定(正解)','安定(正解)'])
        writer.writerow(['不安定(予測)',bb_cnt,bg_cnt])
        writer.writerow(['安定(予測)',gb_cnt, gg_cnt])

        writer.writerow([''])
        writer.writerow(['感度',sens])
        writer.writerow(['特異度',spec])

        writer.writerow([''])
        writer.writerow(['症例'])
        writer.writerow(['patient_name',  'gt result', 'eval result', 'gt_bad','pred_bad'])
        for row in out_list:
            writer.writerow(row)
        writer.writerow([''])

        writer.writerow(['症例','不安定(正解)','安定(正解)'])
        writer.writerow(['不安定(予測)',pb_cnt[0],pg_cnt[0]])
        writer.writerow(['安定(予測)',pb_cnt[1], pg_cnt[1]])

        writer.writerow([''])
        writer.writerow(['感度',psens])
        writer.writerow(['特異度',pspec])

main()


