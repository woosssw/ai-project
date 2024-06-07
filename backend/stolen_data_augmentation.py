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

def crop_data(alpha_list, img_dir, save_folder):
    for alpha in tqdm(alpha_list):
        data_path = alpha
        image = cv2.imread(data_path, cv2.IMREAD_COLOR)
        img_x, img_y = image.shape[1], image.shape[0]
        img_x_move, img_y_move = img_x//2, img_y//2
        x_crop_list = [[img_x_move//2, img_x-img_x_move//2]]
        y_crop_list = [[0, img_y-img_y_move], [img_y_move//2, img_y-img_y_move//2], [img_y_move, img_y]]

        count = 1
        for w in range(len(x_crop_list)):
            for h in range(len(y_crop_list)):
                trans = A.Compose([
                            A.Crop(x_min=x_crop_list[w][0], y_min=y_crop_list[h][0], x_max=x_crop_list[w][1], y_max=y_crop_list[h][1], p=1),
                        ])
                label = '_'+str(count)
                image_seq = trans(image=image)['image']
                ori_name = os.path.splitext(data_path)[0].split('/')[-1]
                if not os.path.exists(save_folder+'/'+ori_name):
                    os.makedirs(save_folder+'/'+ori_name)
                cv2.imwrite(save_folder+'/'+ori_name+'/'+ori_name+label+'.jpg', image_seq)
                count += 1

def prepare_data():
    processed_dir = "data/our_processed"
    val_data_dir = "data/our_processed/original_data/val"
    save_stolen = "data/our_processed/stolen"

    os.makedirs(save_stolen)
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    val_alpha = [x for x in glob(val_data_dir + '/*')]
    val_alpha.sort()

    crop_data(val_alpha, val_data_dir, save_stolen)

if __name__ == '__main__':
    Fire({"prepare_data": prepare_data})