import os
import random
from glob import glob

import numpy as np
from tqdm import tqdm
from zipfile import ZipFile
import wget

from fire import Fire
import shutil

import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2

def resize_data(alpha_list, img_dir):
    for alpha in tqdm(alpha_list):
        data_path = alpha+'/'+alpha.split('/')[-1]
        os.rename(data_path+'.jpg', data_path+'_0.jpg')
        data_path = alpha+'/'+alpha.split('/')[-1]+'_0.jpg'

        image = cv2.imread(data_path, cv2.IMREAD_COLOR)
        trans = A.Compose([
                    A.Resize(125, 105),
                ])
        image_seq = trans(image=image)['image']
        cv2.imwrite(data_path, image_seq)

def move_image_to_processed_dir(alpha_list, copy_dir):
    for alpha in tqdm(alpha_list):
        folder_path = copy_dir+'/'+os.path.splitext(alpha)[0].split('/')[-1]
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        shutil.copy(alpha, folder_path)

def prepare_data():
    processed_dir = "data/our_processed"
    ori_data_dir = "data/our_processed/original_data/val"
    copy_data_dir = "data/our_processed/original"

    os.makedirs(copy_data_dir)
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    train_alpha = [x for x in glob(ori_data_dir + '/*')]
    train_alpha.sort()

    move_image_to_processed_dir(train_alpha, copy_data_dir)

    train_alpha = [x for x in glob(copy_data_dir + '/*')]
    train_alpha.sort()

    resize_data(train_alpha, copy_data_dir)

if __name__ == '__main__':
    Fire({"prepare_data": prepare_data})