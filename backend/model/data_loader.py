import os
import random
from random import Random

import numpy as np
import torch
import cv2
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets as dset
from albumentations.pytorch import ToTensorV2
import albumentations as A


def get_train_validation_loader(data_dir, batch_size, num_train, augment, way, trials, shuffle, seed, num_workers,
                                pin_memory):
    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')

    train_dataset = dset.ImageFolder(train_dir)
    train_dataset = OmniglotTrain(train_dataset, num_train, augment)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers,
                              pin_memory=pin_memory)

    val_dataset = dset.ImageFolder(val_dir)
    val_dataset = OmniglotTest(val_dataset, trials, way, seed)
    val_loader = DataLoader(val_dataset, batch_size=way, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)

    return train_loader, val_loader


def get_test_loader(data_dir, way, trials, seed, num_workers, pin_memory):
    test_dir = os.path.join(data_dir, 'val')
    test_dataset = dset.ImageFolder(test_dir)
    test_dataset = OmniglotTest(test_dataset, trials=trials, way=way, seed=seed)
    test_loader = DataLoader(test_dataset, batch_size=way, shuffle=False, num_workers=num_workers,
                             pin_memory=pin_memory)

    return test_loader

def get_infer_loader(data_dir, way, trials, seed, num_workers, pin_memory, image):
    infer_dir = os.path.join(data_dir, 'original')
    infer_dataset = dset.ImageFolder(infer_dir)
    infer_dataset = OmniglotInfer(infer_dataset, trials=trials, way=way, seed=seed, image=image)
    infer_loader = DataLoader(infer_dataset, batch_size=way, shuffle=False, num_workers=num_workers,
                             pin_memory=pin_memory)

    return infer_loader


# adapted from https://github.com/fangpin/siamese-network
class OmniglotTrain(Dataset):
    def __init__(self, dataset, num_train, augment=False):
        self.dataset = dataset
        self.num_train = num_train
        self.augment = augment
        self.mean = 0.8444
        self.std = 0.5329

    def __len__(self):
        return self.num_train

    def __getitem__(self, index):
        idx = random.randint(0, len(self.dataset.classes) - 1)
        image_list = [x for x in self.dataset.imgs if x[1] == idx]
        image1 = image_list[0]

        # get image from same class
        if index % 2 == 1:
            label = 1.0
            image2 = random.choice(image_list)
            while image1[0] == image2[0]:
                image2 = random.choice(image_list)
        # get image from different class
        else:
            label = 0.0
            image2 = random.choice(self.dataset.imgs)
            while image1[1] == image2[1]:
                image2 = random.choice(self.dataset.imgs)

        # apply transformation
        if self.augment:
            trans1 = A.Compose([
                A.Rotate((-15, 15), p=1),
                A.Normalize(mean=self.mean, std=self.std),
                ToTensorV2(),
            ])
        else:
            trans = A.Compose([
                A.Resize(28, 28),
                A.Normalize(mean=self.mean, std=self.std),
                ToTensorV2(),
            ])

        image1 = cv2.imread(image1[0], cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread(image2[0], cv2.IMREAD_GRAYSCALE)
        image1 = trans1(image=image1)['image']
        image2 = trans1(image=image2)['image']
        label = torch.from_numpy(np.array(label, dtype=np.float32))

        return image1, image2, label


class OmniglotTest:
    def __init__(self, dataset, trials, way, seed=0):
        self.dataset = dataset
        self.trials = trials
        self.way = way
        self.seed = seed
        self.image1 = None
        self.mean = 0.8444
        self.std = 0.5329

    def __len__(self):
        return self.trials * self.way

    def __getitem__(self, index):
        rand = Random(self.seed + index)
        # get image pair from same class
        if index % self.way == 0:
            label = 1.0
            idx = index//self.way
            image_list = [x for x in self.dataset.imgs if x[1] == idx]
            self.image1 = image_list[0]
            image2 = rand.choice(image_list)
            while self.image1[0] == image2[0]:
                image2 = rand.choice(image_list)
        # get image pair from different class
        else:
            label = 0.0
            image2 = random.choice(self.dataset.imgs)
            while self.image1[1] == image2[1]:
                image2 = random.choice(self.dataset.imgs)

        trans = A.Compose([
            A.Normalize(mean=self.mean, std=self.std),
            ToTensorV2(),
        ])

        image1_name = self.image1
        image2_name = image2
        image1 = cv2.imread(self.image1[0], cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread(image2[0], cv2.IMREAD_GRAYSCALE)
        image1 = trans(image=image1)['image']
        image2 = trans(image=image2)['image']

        return image1, image2, label, image1_name, image2_name
    
class OmniglotInfer:
    def __init__(self, dataset, trials, way, image, seed=0):
        self.dataset = dataset
        self.trials = trials
        self.way = way
        self.seed = seed
        self.image1 = image
        self.mean = 0.8444
        self.std = 0.5329

        self.image1_ori_name = os.path.splitext(image)[0].split('/')[-1][:-2]

    def __len__(self):
        return self.trials * self.way

    def __getitem__(self, index):
        rand = Random(self.seed + index)
        image2 = self.dataset.imgs[index]
        # get image pair from same class
        # if index == 0:
        #     image2 = [f'./data/our_processed/val/{self.image1_ori_name}/{self.image1_ori_name}_0.jpg', -1]
        # get image pair from different class
        # else:
        #     image2 = self.dataset.imgs[index]
            # image2 = random.choice(self.dataset.imgs)
            # while self.image1_ori_name == os.path.splitext(image2[0])[0].split('/')[-1]:
            #     image2 = random.choice(self.dataset.imgs)

        trans = A.Compose([
            A.Resize(125, 105),
            A.Normalize(mean=self.mean, std=self.std),
            ToTensorV2(),
        ])

        image2_ori_name = image2[0].split('/')[-1]

        image1 = cv2.imread(self.image1, cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread(image2[0], cv2.IMREAD_GRAYSCALE)
        image1 = trans(image=image1)['image']
        image2 = trans(image=image2)['image']

        return image1, image2, image2_ori_name