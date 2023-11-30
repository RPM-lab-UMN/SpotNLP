import zarr
from torch.utils.data import Dataset

class PoseDataset(Dataset):
    def __init__(self, path):
        self.path = path
        self.store = zarr.DirectoryStore(self.path)
        self.root = zarr.group(store=self.store, overwrite=False)
        self.local_landmarks = self.root['local_landmarks']
        self.world_landmarks = self.root['world_landmarks']
        self.len_landmarks = self.root['len_landmarks']
        self.label = self.root['label']
        self.timestamp = self.root['timestamp']
        self.num_samples = len(self.label)

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        return {  'local_landmarks': self.local_landmarks[idx],
                  'world_landmarks': self.world_landmarks[idx],
                  'len_landmarks': self.len_landmarks[idx],
                  'label': self.label[idx],
                  'timestamp': self.timestamp[idx] }