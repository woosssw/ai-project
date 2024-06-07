import os
from glob import glob
from tqdm import tqdm
from fire import Fire
import shutil
from PIL import Image

import numpy as np
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2

def crop_data(alpha_list, img_dir):
    for alpha in tqdm(alpha_list):
        data_path = alpha+'/'+alpha.split('/')[-1]+'_0.jpg'

        image = cv2.imread(data_path, cv2.IMREAD_COLOR)
        img_x, img_y = image.shape[1], image.shape[0]
        # img_x_move, img_y_move = img_x//5, img_y//5
        img_x_move, img_y_move = img_x//2, img_y//2
        x_crop_list = [[0, img_x-img_x_move], [img_x_move//2, img_x-img_x_move//2], [img_x_move, img_x]]
        y_crop_list = [[0, img_y-img_y_move], [img_y_move//2, img_y-img_y_move//2], [img_y_move, img_y]]

        count = 1
        for w in range(len(x_crop_list)):
            for h in range(len(y_crop_list)):
                trans = A.Compose([
                            A.Crop(x_min=x_crop_list[w][0], y_min=y_crop_list[h][0], x_max=x_crop_list[w][1], y_max=y_crop_list[h][1], p=1),
                            A.Resize(img_y, img_x),
                        ])
                label = '_'+str(count)
                image_seq = trans(image=image)['image']
                cv2.imwrite(os.path.splitext(data_path)[0][:-2]+label+'.jpg', image_seq)
                count += 1

def prepare_data():
    processed_dir = "data/our_processed"
    train_data_dir = "data/our_processed/train"
    val_data_dir = "data/our_processed/val"

    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    train_alpha = [x for x in glob(train_data_dir + '/*')]
    train_alpha.sort()
    val_alpha = [x for x in glob(val_data_dir + '/*')]
    val_alpha.sort()

    crop_data(train_alpha, train_data_dir)
    crop_data(val_alpha, val_data_dir)

if __name__ == '__main__':
    Fire({"prepare_data": prepare_data})