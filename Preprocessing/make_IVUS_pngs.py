import argparse
import os
import os.path
from shutil import rmtree, move, copy
import random

import pydicom
from PIL import Image
import numpy as np

import shutil
import datetime
import csv
from pathlib import Path

# For parsing commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("--src_dir", type=str, required=True, help='path to the folder containing dicoms')
parser.add_argument("--dest_dir", type=str, required=True, help='path to the output dataset folder')
parser.add_argument("--csv_name", type=str, default='', help='file name for outputing csv')
args = parser.parse_args()

def set_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def extract_DICOM(ds):
    fps = 0
    if "CineRate" in ds:
        fps = ds[0x0018, 0x0040].value
    
    numFrames = 0
    if "NumberOfFrames" in ds:
        numFrames = ds[0x0028,0x0008].value

    return fps,numFrames

def main():
    
    # setting output folder
    set_dir(args.dest_dir)

    dcm_dir = os.path.join(args.dest_dir,'dicom')
    # gt_dir = os.path.join(args.dest_dir,'gt')
    anno_dir = os.path.join(args.dest_dir,'gt_anno')
    ib_dir = os.path.join(args.dest_dir,'gt_ib')
    pngs_dir = os.path.join(args.dest_dir,'pngs')
    input_dir = os.path.join(args.dest_dir,'input')

    set_dir(dcm_dir)
    # set_dir(gt_dir)
    set_dir(anno_dir)
    set_dir(ib_dir)
    set_dir(pngs_dir)
    set_dir(input_dir)

    # inittialize csv file
    csv_rows = []
    if args.csv_name == '':
        # csv_name = str(datetime.datetime.today()).split('.')[0].replace(':','-').replace(' ','_') + '.csv'
        paths = Path(args.src_dir).parts
        print(paths)
        csv_name = '{}_{}.csv'.format(paths[-2],paths[-1])
    else:
        csv_name = args.csv_name + '.csv'

    # initialize output pngs folder
    for dir in os.listdir(args.src_dir):
        comment = ''
        gt_list = []
        csv_row = []
        dir_path = os.path.join(args.src_dir, dir)
        print(dir)
        csv_row.append(dir)
        if ' ' in dir:
            id  = dir.split(' ')[1]
        else:
            id = dir
        csv_row.append(id)
        pngs_path = os.path.join(pngs_dir,dir)
        set_dir(pngs_path)

        for data in os.listdir(dir_path):
            data_path = os.path.join(dir_path, data)

            if os.path.isdir(data_path):
                dcm_path = data_path
                dcm_list = os.listdir(dcm_path)
            elif os.path.isfile(data_path) and data.split('.')[-1] == 'png':
                gt_list.append(data_path)

        # extract DICOM file
        out_flag = False
        dcm_plist = []
        while not out_flag:
            for dcm in dcm_list:
                if os.path.isdir(os.path.join(dcm_path, dcm)):
                    dcm_path = os.path.join(dcm_path, dcm)
                    dcm_list = os.listdir(dcm_path)
                    if len(dcm_list) == 0:
                        out_flag = True
                        print('Not_file',dcm_path)
                elif os.path.isfile(os.path.join(dcm_path, dcm)):
                    dcm_plist.append(os.path.join(dcm_path, dcm))
                    out_flag = True
                    print('DICOM',dcm_path)

        # print("plist",dcm_plist)
        if len(dcm_plist) == 0:
            for i in range(3):
                csv_row.append('')
            csv_row.append('Dicom is Notihing')
            csv_rows.append(csv_row)
            continue
        else:
            if len(dcm_plist) == 1:
                dcm_path = dcm_plist[0]
                dicomName = os.path.basename(dcm_path)
                csv_row.append(dicomName)
                copy(dcm_path, dcm_dir)

                ds = pydicom.dcmread(dcm_path)
                fps, numFrames = extract_DICOM(ds)
                csv_row.append(str(fps))
                csv_row.append(str(numFrames))

                print(numFrames)
                imgMono = ds.pixel_array
                dup_flag = False
                if numFrames == 0:
                    img = Image.fromarray(imgMono)
                    img.save(os.path.join(pngs_path,'000000.png'))
                else:
                    for i in range(imgMono.shape[0]):
                        img = Image.fromarray(imgMono[i])

                        if not os.path.isfile(os.path.join(pngs_path,'{:06}.png'.format(i+1))):
                            img.save(os.path.join(pngs_path,'{:06}.png'.format(i+1)))
                        else:
                            dup_flag = True
                    
                    if dup_flag:
                        dup_flag = False
                        comment += 'Duplication pngs '
            
            elif len(dcm_plist) > 1:
                dicomName_list = []
                fps_list = []
                numFrames_list = []
                for dcm_path in dcm_plist:
                    dicomName = os.path.basename(dcm_path)
                    dicomName_list.append(dicomName)
                    copy(dcm_path, dcm_dir)

                    ds = pydicom.dcmread(dcm_path)
                    fps, numFrames = extract_DICOM(ds)
                    fps_list.append(fps)
                    numFrames_list.append(numFrames)

                    imgMono = ds.pixel_array
                    dup_flag = False
                    for i in range(imgMono.shape[0]):
                        img = Image.fromarray(imgMono[i])
                        set_dir(os.path.join(pngs_path,dicomName))
                        if not os.path.isfile(os.path.join(pngs_path,dicomName,'{:06}.png'.format(i+1))):
                            img.save(os.path.join(pngs_path,dicomName,'{:06}.png'.format(i+1)))
                        else:
                            dup_flag = True
                    
                    if dup_flag:
                        dup_flag = False
                        comment += 'Duplication pngs '
                
                csv_row.append(dicomName_list)
                csv_row.append(fps_list)
                csv_row.append(numFrames_list)

            if len(gt_list) > 0:
                for gt in gt_list:
                    gt_name = os.path.basename(gt)
                    gt_num = int(gt_name.split('Frame')[-1].split('.')[0])
                    imgname = '{}_{:06}.png'.format(id,gt_num)
                    # copy(gt, os.path.join(gt_dir,'{}_{:06}.png'.format(id,gt_num)))
                    gt_img = Image.open(gt)
                    gt_anno = gt_img.crop((0,0,512,512))
                    if not os.path.isfile(os.path.join(anno_dir,imgname)):
                        gt_anno.save(os.path.join(anno_dir,imgname))
                    else:
                        if not 'anno' in comment:
                            comment += 'Duplication anno '

                    gt_ib = gt_img.crop((512,0,1024,512))
                    if not os.path.isfile(os.path.join(ib_dir,imgname)):
                        gt_ib.save(os.path.join(ib_dir,imgname))
                    else:
                        if not 'IB' in comment:
                            comment += 'Duplication IB '

                    if len(dcm_plist) == 1:
                        if numFrames == 0:
                            input_img = Image.fromarray(imgMono)
                        else:
                            input_img = Image.fromarray(imgMono[gt_num])
                        if not os.path.isfile(os.path.join(input_dir,imgname)):
                            input_img.save(os.path.join(input_dir,imgname))
                        else:
                            if not 'input' in comment:
                                comment += 'Duplication input '
                    elif len(dcm_plist) > 1:
                        for dcm_path in dcm_plist:
                            dicomName = os.path.basename(dcm_path)
                            ds = pydicom.dcmread(dcm_path)
                            imgMono = ds.pixel_array
                            input_img = Image.fromarray(imgMono[gt_num])
                            set_dir(os.path.join(input_dir,dicomName))
                            if not os.path.isfile(os.path.join(input_dir,dicomName,imgname)):
                                input_img.save(os.path.join(input_dir,dicomName,imgname))
                            else:
                                if not 'input' in comment:
                                    comment += 'Duplication input '

            else:
                comment += 'GT Image is Nothing '
            
            csv_row.append(comment)
            csv_rows.append(csv_row)

        
    with open(os.path.join(args.dest_dir,csv_name), 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['Data','ID','Dicom','fps','Num Frame','Comment'])
        for row in csv_rows:
            writer.writerow(row)


main()
    
   

