import rospkg
import os
from dataset.dataset import PoseDataset
from torch.utils.data import DataLoader

def main():
    name = 'data'
    pack_path = rospkg.RosPack().get_path('dataset')
    dataset_path = os.path.join(pack_path, 'dataset_raw',  f'{name}.zarr')
    dataset = PoseDataset(dataset_path)
    # data = dataset[0:5]['world_landmarks']
    # for d in data:
    #     print(d.shape)
    loader = DataLoader(dataset, batch_size=7, shuffle=False, num_workers=0)

    for batch in loader:
        local = []
        world = []
        raw = zip(batch['local_landmarks'], batch['world_landmarks'], batch['len_landmarks'])      
        for local_element, world_element, data_len in raw:
            local.append(local_element[:int(data_len)])
            world.append(world_element[:int(data_len)])

        for data in zip(local, world):
            print(data[0].shape, data[1].shape)
        print(batch['label'])
        print('---')
    

if __name__ == '__main__':
    main()
