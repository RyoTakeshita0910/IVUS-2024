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
parser.add_argument("--gt_dir", type=str, required=True, help='path to the folder containing origial pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--fill", action='store_true', help='path to the output folder')
args = parser.parse_args()

w = 512
h = 512

def set_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def pick_label(retval, labels, stats):
    dup_cnt = 0
    label_num = []
    for i in range(retval):
        area = stats[i][-1]
        # 面積が小さいラベルを除外
        if area >= 100 and area <= 5000:
            label_num.append(i)
            if area >= 1000:
                dup_cnt += 1

    for y in range(h):
        for x in range(w):
            if labels[y][x] in label_num:
                labels[y][x] = 255
            else:
                labels[y][x] = 0

    return len(label_num)+dup_cnt, labels

# Wireと交錯するLumenやMediaのピクセルの周辺を探索するメソッド
def bool_connect(y,x,img,thrs):
    con_flag = False
    y_min = y-1
    y_max = y+1
    x_min = x-1
    x_max = x+1
    if y_min < 0:
        y_min = y
    elif y_max > h-1:
        y_max = y
    
    if x_min < 0:
        x_min = x
    elif x_max > w-1:
        x_max = x

    for i in range(y_min,y_max+1):
        for j in range(x_min,x_max+1):
            if x == j and y == i:
                continue
            
            if np.sum(np.abs(img[i][j]-thrs)) < 60:
            #if np.mean(np.abs(con_c-thrs)) < 60:
                con_flag = True
                break
        if con_flag == True:
            break
    return con_flag


def main():

    # parameter
    top = 0
    left = 0

    gt_list = sorted(os.listdir(args.gt_dir))

    for gt in gt_list:
        gt_path = os.path.join(args.gt_dir,gt)
        if args.fill:
            gt_img = cv2.imread(gt_path, cv2.IMREAD_GRAYSCALE)
            contours, _ = cv2.findContours(gt_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            print(gt)
            print(contours)

            # 閉じた領域を塗りつぶす          
            for i in range(len(contours)):
                drawarea = cv2.contourArea(contours[i])
                print(i, " drawarea:",drawarea)
                gt_anno = cv2.drawContours(gt_img, [contours[i]], 0, (255,255,255), -1)

            if len(contours) == 0:
                cv2.imwrite(os.path.join(args.dest_dir, gt), gt_img)
            else:
                cv2.imwrite(os.path.join(args.dest_dir, gt), gt_anno)

        else:
            # output
            dest_path = os.path.join(args.dest_dir,'label')
            set_dir(dest_path)

            error_path = os.path.join(args.dest_dir,'error')
            set_dir(error_path)

            # label output
            media_path = os.path.join(dest_path,'Media')
            set_dir(media_path)
            lumen_path = os.path.join(dest_path,'Lumen')
            set_dir(lumen_path)
            wire_path = os.path.join(dest_path,'Wire')
            set_dir(wire_path)

            # 失敗した画像の保存先
            e_media_path = os.path.join(error_path,'Media')
            set_dir(e_media_path)
            e_lumen_path = os.path.join(error_path,'Lumen')
            set_dir(e_lumen_path)
            e_wire_path = os.path.join(error_path,'Wire')
            set_dir(e_wire_path)


            gt_img = cv2.imread(gt_path)
            gt_crop = gt_img[top:top+h,left:left+w]
            
            np_gt = gt_crop.astype(int)

            np_m = np.zeros((h, w))
            np_l = np.zeros((h, w))
            np_w = np.zeros((h, w))

            # LumenとMediaをトレースする線を抽出
            for y in range(h):
                for x in range(w):
                    im_c = np_gt[y][x]

                    # media
                    if all(im_c == [0, 165, 255]):
                    # if all(im_c == [0, 165, 255]) or all(im_c == [16, 155, 239]):
                        np_m[y][x] = 255
                        if y >= 430 and x >= 430:
                            if bool_connect(y,x,np_gt,[255, 255, 0]) or bool_connect(y,x,np_gt,[0, 0, 255]):
                                np_w[y][x] = 255

                    # lumen
                    elif all(im_c == [0, 255, 0]):
                    # elif all(im_c == [0, 255, 0]) or all(im_c == [16, 239, 0]):
                        np_l[y][x] = 255
                        if y >= 430 and x >= 430:
                            if bool_connect(y,x,np_gt,[255, 255, 0]) or bool_connect(y,x,np_gt,[0, 0, 255]):
                                np_w[y][x] = 255

                    # wire
                    elif all(im_c == [255, 255, 0]) or all(im_c == [0, 0, 255]):
                        np_w[y][x] = 255
                        # wireと交錯するMediaやLumenを抽出
                        if bool_connect(y,x,np_gt,[0, 165, 255]):
                            np_m[y][x] = 255
                        if bool_connect(y,x,np_gt,[0, 255, 0]):
                            np_l[y][x] = 255
                    # elif all(im_c == [0, 0, 255]):
                    #     np_w[y][x] = 255
                    #     # wireと交錯するMediaやLumenを抽出
                    #     if bool_connect(y,x,np_gt,[0, 165, 255]):
                    #         np_m[y][x] = 255
                    #     if bool_connect(y,x,np_gt,[0, 255, 0]):
                    #         np_l[y][x] = 255
                    
                    else:
                        if np.sum(np.abs(im_c-[0, 165, 255])) < 60:
                            np_m[y][x] = 255
                        if np.sum(np.abs(im_c-[0, 255, 0])) < 60:
                            np_l[y][x] = 255
                        
                        if y >= 430 and x >= 430:
                            if all(im_c == [102, 255, 0]) or all(im_c == [0, 102, 255]):
                                if bool_connect(y,x,np_gt,[255,255,0]):
                                    np_w[y][x] = 255

            im_m = np_m.astype(np.uint8)
            im_l = np_l.astype(np.uint8)

            ### 二値化画像から領域を抽出 ###
            # retval:ラベルの数, labels:ラベリング画像, 
            # stats:ラベルのステータス([左上のx座標,左上のy座標,領域の幅,領域の高さ,面積])　※今回は面積のみ使用
            # centroid:ラベルの重心
            m_retval, m_labels, m_stats, _ = cv2.connectedComponentsWithStats(im_m)
            l_retval, l_labels, l_stats, _ = cv2.connectedComponentsWithStats(im_l)

            # ラベルの選定
            _, m_label = pick_label(m_retval, m_labels, m_stats)
            _, l_label = pick_label(l_retval, l_labels, l_stats)

            m_anno = m_label.astype("uint8")
            l_anno = l_label.astype("uint8")

            # 閉じた領域を探す
            m_contours, _ = cv2.findContours(m_anno, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            l_contours, _ = cv2.findContours(l_anno, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # 閉じた領域を塗りつぶす
            for i in range(len(m_contours)):
                m_drawarea = cv2.contourArea(m_contours[i])
                print(i, " m_drawarea:", m_drawarea)
                if m_drawarea < 1000:
                    cv2.imwrite(os.path.join(e_media_path, gt), m_anno)
                    break
                else:
                    m_anno = cv2.drawContours(m_anno, [m_contours[i]], 0, (255,255,255), -1)
                    cv2.imwrite(os.path.join(media_path, gt), m_anno)
                    break
            
            for i in range(len(l_contours)):
                    l_drawarea = cv2.contourArea(l_contours[i])
                    print(i, " l_drawarea:",l_drawarea)
                    if l_drawarea < 1000:
                        cv2.imwrite(os.path.join(e_lumen_path, gt), l_anno)
                        break
                    else:
                        l_anno = cv2.drawContours(l_anno, [l_contours[i]], 0, (255,255,255), -1)
                        cv2.imwrite(os.path.join(lumen_path, gt), l_anno)
                        break

            
            we_flag = False
            w_cnt = 0
            im_w = np_w.astype(np.uint8)
            w_retval, w_labels, w_stats, _ = cv2.connectedComponentsWithStats(im_w)
            w_num, w_label = pick_label(w_retval, w_labels, w_stats)
            w_anno = w_label.astype("uint8")

            w_mid_path = os.path.join(args.dest_dir,"w_mid")
            set_dir(w_mid_path)
            cv2.imwrite(os.path.join(w_mid_path,gt),w_anno)

            for y in range(50,h-50):
                w_anno[y][0] = 255
                w_anno[y][w-1] = 255
            for x in range(50,w-50):
                w_anno[0][x] = 255
                w_anno[h-1][x] = 255
            
            w_contours, _ = cv2.findContours(w_anno, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            
            # print(np.squeeze(np.array(w_contours[0])))

            
            for i in range(len(w_contours)):
                w_drawarea = cv2.contourArea(w_contours[i])
                if w_drawarea < 100000:
                    print(i, ' w_drawarea:', w_drawarea)
                    w_anno = cv2.drawContours(w_anno, [w_contours[i]], 0, (255,255,255), -1)
                    if w_drawarea > 10000:
                        w_cnt += 1
            
            for y in range(h):
                if w_anno[y][1] == 0:
                    w_anno[y][0] = 0
                if w_anno[y][w-2] == 0:
                    w_anno[y][w-1] = 0
            for x in range(w):
                if w_anno[1][x] == 0:
                    w_anno[0][x] = 0
                if w_anno[h-2][x] == 0:
                    w_anno[h-1][x] = 0

            print("cont,label:{},{}".format(w_cnt,w_num))
            if len(w_contours) == 0 or w_cnt < w_num or w_num == 0:
                we_flag = True

            if we_flag:
                cv2.imwrite(os.path.join(e_wire_path, gt), w_anno)
                print("ERROR",gt)
            else:
                cv2.imwrite(os.path.join(wire_path, gt), w_anno)


main()

