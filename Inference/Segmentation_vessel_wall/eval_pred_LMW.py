import argparse
import os
import os.path
from shutil import rmtree, move
import numpy as np
import cv2
from monai.metrics import compute_iou, compute_hausdorff_distance
import torch
import csv

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--eval_dir", type=str, required=True, help='path to the folder containing prediction mask pngs')
parser.add_argument("--gt_dir", type=str, required=True, help='path to the folder containing ground-truth mask pngs')
parser.add_argument("--out_csv", type=str, required=True, help='path to the output csv')
args = parser.parse_args()


def main():
    # 評価するマスク画像と正解のマスク画像をリストアップ
    eval_list = sorted(os.listdir(args.eval_dir))
    gt_list = sorted(os.listdir(args.gt_dir))

    device = torch.device('cpu')
    file_list = []
    iou_list = []
    hd_list = []

    print('eval_list',eval_list)
    print('\n')
    print('gt_list',gt_list)

    # 評価したいマスク画像のJacard係数とHausdorff距離の計算
    for eval in eval_list:
        eval_name = eval.split('.')[0]
        # 評価したいマスク画像の読込
        eval_img = cv2.imread(os.path.join(args.eval_dir, eval), cv2.IMREAD_GRAYSCALE)
        for gt in gt_list:
            if gt == eval:
                print(eval_name)
                # 正解のマスク画像の読込
                gt_img = cv2.imread(os.path.join(args.gt_dir, gt), cv2.IMREAD_GRAYSCALE)

                # それぞれのマスク画像をTensor型に変換
                eval_np = np.expand_dims(np.expand_dims(np.array(eval_img), 0).astype(np.float32) / 255 , 0)
                gt_np = np.expand_dims(np.expand_dims(np.array(gt_img), 0).astype(np.float32) / 255 , 0)
                eval_tensor = torch.tensor(eval_np, dtype=torch.uint8)
                gt_tensor = torch.tensor(gt_np, dtype=torch.uint8)

                # Jaccard係数とHausdorff距離の計算
                iou = compute_iou(eval_tensor, gt_tensor)
                hd = compute_hausdorff_distance(eval_tensor, gt_tensor)

                print(float(iou))
                print(float(hd))
                print('\n')
                file_list.append(eval_name)
                iou_list.append(float(iou))
                hd_list.append(float(hd))
                break
    
    # Jaccard係数とHausdorff距離の平均値の算出
    ave_iou = np.mean(iou_list)
    ave_hd = np.mean(hd_list)

    # 計算結果をcsvで出力
    with open(args.out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['img_name', 'IoU', 'Hausdorff_distance'])
        for i in range(len(file_list)):
            writer.writerow([file_list[i], iou_list[i], hd_list[i]])
        writer.writerow([''])
        writer.writerow(['ave', ave_iou, ave_hd])

main()


