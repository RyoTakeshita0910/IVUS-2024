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
import matplotlib.animation as animation

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--img_dir", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--video_name", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--pick_idx", type=int, required=True, help='path to the output dataset folder')
parser.add_argument("--dtype", type=str, required=True, help='path to the output dataset folder')
# parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
#parser.add_argument("--thrs", type=float, required=True, help='path to the folder containing origial pngs')
args = parser.parse_args()

h = 512
w = 512
x_list = [[],[]]
y_list = [[],[]]
z_list = [[],[]]
img_list = sorted(os.listdir(args.img_dir))


for index,img in enumerate(img_list):
    src_im = cv2.imread(os.path.join(args.img_dir,img),cv2.IMREAD_GRAYSCALE)

    contours, _ = cv2.findContours(src_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    z = 10 * (index+1)
    if index == args.pick_idx:
        for i in range(len(contours[0])):
            # print(l_contours[0][i][0][0],l_contours[0][i][0][1])
            x_list[1].append(contours[0][i][0][0])
            y_list[1].append(contours[0][i][0][1])
            z_list[1].append(z)
    else:
        for i in range(len(contours[0])):
            # print(l_contours[0][i][0][0],l_contours[0][i][0][1])
            x_list[0].append(contours[0][i][0][0])
            y_list[0].append(contours[0][i][0][1])
            z_list[0].append(z)

rotate_elev = np.concatenate((np.linspace(0,180,50,endpoint = False),np.linspace(-180,0,51)))

fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')

if args.dtype == 'Lumen':
    ol_color = 'green'
elif args.dtype == 'Media':
    ol_color = 'orange'
else:
    ol_color = 'blue'
ax.scatter(x_list[0],y_list[0],z_list[0], c=ol_color,s=0.5, alpha=0.5)
ax.scatter(x_list[1],y_list[1],z_list[1], c='red',s=0.5, alpha=0.5)

def animate(i):
    ax.view_init(elev=rotate_elev[i], azim=255)
    return fig,

ani = animation.FuncAnimation(fig, animate, frames=100, interval=100, blit=True)
ani.save('{}.gif'.format(args.video_name),writer="pillow")


