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

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--lumen_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--media_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--wire_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--img_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()

w = 512
h = 512

# 出力先のフォルダにLumen, Media, Wireの保存先を作成
def make_dir(path):
    if not os.path.isdir(os.path.join(path,"Lumen")):
        os.mkdir(os.path.join(path,"Lumen"))

    if not os.path.isdir(os.path.join(path,"Media")):
        os.mkdir(os.path.join(path,"Media"))
    
    if not os.path.isdir(os.path.join(path,"Wire")):
        os.mkdir(os.path.join(path,"Wire"))

# LumenとMediaに関するラベル削除メソッド
def pick_label(retval, labels, stats):
    # 画像の中心におけるラベル番号を取得
    label_num = labels[255][255]

    # 画像の中心におけるラベル番号が背景である場合 
    # -> 面積が背景の次に大きいラベルのラベル番号を取得
    if label_num == 0:
        label_list = []
        for i in range(retval):
            area = stats[i][-1]
            label_list.append(area)

        max_area = max(label_list)
        max_idx = label_list.index(max_area)

        label_list[max_idx] = 0

        sec_area = max(label_list)
        label_num = label_list.index(sec_area)

    # 取得したラベル番号以外のラベルを削除する
    for y in range(h):
        for x in range(w):
            if labels[y][x] == label_num:
                labels[y][x] = 255
            else:
                labels[y][x] = 0

    return labels.astype('uint8')

# Wireのラベル削除に関するメソッド
def pick_label_wire(retval, labels, stats):
    label_list = []
    # 面積が2000[pixel]以上150000[pixel]以下のラベルのラベル番号を全て取得
    for i in range(retval):
        area = stats[i][-1]
        if area >= 2000 and area < 150000:
            label_list.append(i)

    # 取得したラベル番号以外のラベルを削除
    for y in range(h):
        for x in range(w):
            if labels[y][x] in label_list:
                labels[y][x] = 255
            else:
                labels[y][x] = 0

    return labels.astype('uint8')

# マスク画像の調整：画素値が0未満 -> 画素値を0にする
def set_trace(img):
    for y in range(h):
        for x in range(w):
            if img[y][x] < 0:
                img[y][x] = 0

# IVUS画像にマスク画像を適用する
def set_input(img,bi):
    for y in range(h):
        for x in range(w):
            bi_c = bi[y][x]
            # 背景の色をシアンにする
            if bi_c == 0:
                img[y][x] = [255,255,0]

    return img


def main():
    # Lumen, Media, Wireの予測領域のリストアップ
    lumen_list = sorted(os.listdir(args.lumen_dir))
    media_list = sorted(os.listdir(args.media_dir))
    wire_list = sorted(os.listdir(args.wire_dir))


    otsu_path = os.path.join(args.dest_dir,"otsu")
    if not os.path.isdir(otsu_path):
            os.mkdir(otsu_path)
            make_dir(otsu_path)

    cut_path = os.path.join(args.dest_dir,"cut")
    if not os.path.isdir(cut_path):
            os.mkdir(cut_path)
            make_dir(cut_path)

    print("Lumen Otsu & Cut")
    for l in lumen_list:
        l_img = cv2.imread(os.path.join(args.lumen_dir,l),cv2.IMREAD_GRAYSCALE)

        # 大津の二値化
        _, l_otsu = cv2.threshold(l_img, 0, 255, cv2.THRESH_OTSU)
        cv2.imwrite(os.path.join(otsu_path,"Lumen",l), l_otsu)

        # ラベル削除
        l_ret, l_labels, l_stats, _ = cv2.connectedComponentsWithStats(l_otsu)
        l_cut = pick_label(l_ret, l_labels, l_stats)
        l_contours, _ = cv2.findContours(l_cut, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(l_contours)):
            l_out = cv2.drawContours(l_cut, [l_contours[i]], 0, 255, -1)
        cv2.imwrite(os.path.join(cut_path,"Lumen",l), l_out)

    print("Media Otsu & Cut")
    for m in media_list:
        m_img = cv2.imread(os.path.join(args.media_dir,m),cv2.IMREAD_GRAYSCALE)

        # 大津の二値化
        _, m_otsu = cv2.threshold(m_img, 0, 255, cv2.THRESH_OTSU)
        cv2.imwrite(os.path.join(otsu_path,"Media",m), m_otsu)

        # ラベル削除
        m_ret, m_labels, m_stats, _ = cv2.connectedComponentsWithStats(m_otsu)
        m_cut = pick_label(m_ret, m_labels, m_stats)
        m_contours, _ = cv2.findContours(m_cut, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(m_contours)):
            m_out = cv2.drawContours(m_cut, [m_contours[i]], 0, 255, -1)
        cv2.imwrite(os.path.join(cut_path,"Media",m), m_out)
    

    print("Wire Otsu & Cut")
    for w in wire_list:
        w_img = cv2.imread(os.path.join(args.wire_dir,w),cv2.IMREAD_GRAYSCALE)

        # 大津の二値化
        _, w_otsu = cv2.threshold(w_img, 0, 255, cv2.THRESH_OTSU)
        cv2.imwrite(os.path.join(otsu_path,"Wire",w), w_otsu)

        # ラベル削除
        w_ret, w_labels, w_stats, _ = cv2.connectedComponentsWithStats(w_otsu)
        w_cut = pick_label(w_ret, w_labels, w_stats)
        w_contours, _ = cv2.findContours(w_cut, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(w_contours)):
            w_out = cv2.drawContours(w_cut, [w_contours[i]], 0, 255, -1)
        cv2.imwrite(os.path.join(cut_path,"Wire",w), w_out)

    # add lumen & media
    lumen_list = sorted(os.listdir(os.path.join(cut_path,'Lumen')))
    media_list = sorted(os.listdir(os.path.join(cut_path,'Media')))
    wire_list = sorted(os.listdir(os.path.join(cut_path,'Wire')))
    img_list = sorted(os.listdir(args.img_dir))

    out_path = os.path.join(args.dest_dir,"ib_input")
    if not os.path.isdir(out_path):
            os.mkdir(out_path)

    print("create IB-IVUS input Image")
    for l in lumen_list:
        for m in media_list:
            if l == m:
                for w in wire_list:
                    if l == w:
                        l_img = cv2.imread(os.path.join(cut_path,'Lumen',l), cv2.IMREAD_GRAYSCALE)
                        m_img = cv2.imread(os.path.join(cut_path,'Media',m), cv2.IMREAD_GRAYSCALE)
                        w_img = cv2.imread(os.path.join(cut_path,'Wire',w), cv2.IMREAD_GRAYSCALE)

                        # 血管壁のマスク画像を作成
                        trace_gray = m_img.astype(float) - l_img.astype(float) - w_img.astype(float)
                        set_trace(trace_gray)
                    

                        for img in img_list:
                            if img == l:
                                ivus_img = cv2.imread(os.path.join(args.img_dir, img))
                                # IVUS画像にマスク画像を適用
                                seg_input = set_input(ivus_img, trace_gray)
                                cv2.imwrite(os.path.join(out_path, img), seg_input)
                                print(img)  
                                break
                        break
                break

main()


