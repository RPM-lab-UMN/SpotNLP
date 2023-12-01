import rospkg
import os
import numpy as np
from dataset.dataset import PoseDataset
from torch.utils.data import DataLoader

def main():
    name = 'data'
    pack_path = rospkg.RosPack().get_path('dataset')
    dataset_path = os.path.join(pack_path, 'dataset_raw',  f'{name}.zarr')
    dataset = PoseDataset(dataset_path)
    loader = DataLoader(dataset, batch_size=7, shuffle=False, num_workers=0)

    for batch in loader:
        for world, mask in zip(batch['world_landmarks'], batch['mask_landmarks']):
            for w, m in zip(world, mask):
                if m > 0:
                    print(w[0,0], end='|')
            print()
            input()
            
    

if __name__ == '__main__':
    main()
