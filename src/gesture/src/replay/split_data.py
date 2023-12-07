import rospkg
import os
import numpy as np
from dataset.dataset import PoseDataset
from torch.utils.data import DataLoader
import torch

def main():
    name = 'data'
    pack_path = rospkg.RosPack().get_path('dataset')
    dataset_path = os.path.join(pack_path, 'dataset_raw',  f'{name}.zarr')
    dataset = PoseDataset(dataset_path)

    # Split the dataset into train and test
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

    # Save the datasets
    train_path = os.path.join(pack_path, 'dataset_split',  f'{name}_train.zarr')
    test_path = os.path.join(pack_path, 'dataset_split',  f'{name}_test.zarr')
    train_dataset.save(train_path)

    
            
    

if __name__ == '__main__':
    main()
