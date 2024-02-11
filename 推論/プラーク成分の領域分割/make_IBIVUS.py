import argparse
import os
import os.path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, required=True, help='path to the folder containing prediction IB-IVUS all masks pngs')
parser.add_argument("--lumen_dir", type=str, required=True, help='path to the folder containing prdiction Lumen mask pngs')
parser.add_argument("--media_dir", type=str, required=True, help='path to the folder containing prediction Media mask pngs')
parser.add_argument("--wire_dir", type=str, required=True, help='path to the folder containing prediction Wire mask pngs')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
args = parser.parse_args()


h = 512
w = 512

# 各プラークのクラス番号と画素値(確信度)の統合
def set_info(img,info,class_num):
    for y in range(h):
        for x in range(w):
            img_c = img[y][x]
            if info[y][x][1] <= img_c:
                info[y][x][0] = class_num
                info[y][x][1] = img_c
    
    return info

# LumenとMediaの輪郭を抽出するメソッド
def make_8mask(img):
    new_img = np.zeros((h,w))
    for y in range(1,h-1):
        for x in range(1,w-1):
            y_min = y-1
            x_min = x-1
            if y_min < 0:
                y_min = 0
            if x_min < 0:
                x_min = 0
            
            y_max = y+2
            x_max = x+2
            if y_max > 512:
                y_max = 512
            if x_max > 512:
                x_max = 512

            flag = False
            if img[y][x] <= 0:
                for yy in range(y_min, y_max):
                    for xx in range(x_min, x_max):
                        if img[yy][xx] > 0:
                            flag = True
                            break
                    if flag:
                        break
            else:
                new_img[y][x] = 0

            if flag:
                new_img[y][x] = 255
    
    return new_img.astype('uint8')

# 血管壁内で色がついていないピクセルに対して、周囲から色を特定するメソッド
def pick8color(x,y,img):
    c_dict = {}
    for i in range(5):
        c_dict[i+1] = 0
    
    y_min = y-1
    x_min = x-1
    if y_min < 0:
        y_min = 0
    if x_min < 0:
        x_min = 0
    
    y_max = y+2
    x_max = x+2
    if y_max > 512:
        y_max = 512
    if x_max > 512:
        x_max = 512

    for yy in range(y_min,y_max):
        for xx in range(x_min,x_max):
            info_c = img[yy][xx][0]
            if info_c != 0:
                c_dict[info_c] += 1
    
    out_c = 0
    c_max = 0
    for i in range(5):
        if c_max < c_dict[i+1]:
            out_c = i+1
            c_max = c_dict[i+1]
    
    return out_c


# IB-IVUSの生成メソッド
def set_seg(info,img_name):
    seg_img = np.zeros((h,w,3))

    lumen_list = sorted(os.listdir(args.lumen_dir))
    media_list = sorted(os.listdir(args.media_dir))
    wire_list = sorted(os.listdir(args.wire_dir))

    for l in lumen_list:
        if l == img_name:
            l_img = cv2.imread(os.path.join(args.lumen_dir, l), cv2.IMREAD_GRAYSCALE)
    for m in media_list:
        if m == img_name:
            m_img = cv2.imread(os.path.join(args.media_dir, m), cv2.IMREAD_GRAYSCALE)
    for wire in wire_list:
        if wire == img_name:
            w_img = cv2.imread(os.path.join(args.wire_dir, wire), cv2.IMREAD_GRAYSCALE)
    
    # IB-IVUSにおける白い線を抽出 
    trace_img = m_img.astype(float) - l_img.astype(float)
    white_mask = make_8mask(trace_img)

    # set_infoにおける色の情報を統合する
    for y in range(h):
        for x in range(w):
            # 白い線の描画
            if white_mask[y][x] == 255:
                seg_img[y][x] = [255,255,255]
                continue
            # 背景の描画
            elif w_img[y][x] == 255 or trace_img[y][x] != 255:
                seg_img[y][x] = [0,0,0]
                continue
            
            # 各プラーク成分の描画
            info_c = info[y][x][0]
            if info_c == 0 and trace_img[y][x] == 255:
                info_c = pick8color(x,y,info)

            if info_c == 1:
                seg_img[y][x] = [255,0,0]
            elif info_c == 2:
                seg_img[y][x] = [0,255,0]
            elif info_c == 3:
                seg_img[y][x] = [170,0,85]
            elif info_c == 4:
                seg_img[y][x] = [0,0,255]
            elif info_c == 5:
                seg_img[y][x] = [0,255,255]
            

    return seg_img.astype('uint8')


def main():

    if not os.path.isdir(args.dest_dir):
        os.mkdir(args.dest_dir)

    # 画像のファイル名を取得
    bla_path = os.path.join(args.input_dir,'0')
    img_list = sorted(os.listdir(bla_path))

    for img in img_list:
        # 深層学習から出力された各プラーク成分のマスク画像の情報を統合するリスト
        seg_info = np.zeros((512,512,2)) # (y,x,[色のクラス,画素値])
        print(img)
        for c in range(0,6):
            src_img = cv2.imread(os.path.join(args.input_dir, str(c), img), cv2.IMREAD_GRAYSCALE)
            seg_info = set_info(src_img, seg_info, c)

        seg_img = set_seg(seg_info, img)
        cv2.imwrite(os.path.join(args.dest_dir, img), seg_img)
        
main()


