import zarr

def test():
    print('Hello World!')

class Dataset:
    def __init__(self, path):
        self.path = path
        self.store = zarr.DirectoryStore(path)
        self.root = zarr.group(store=self.store, overwrite=True)
        self.root.create_dataset('local_landmarks', shape=(0, 32, 5), chunks=(100, 32, 5), dtype='float32', maxshape=(None, 32, 5))
        self.root.create_dataset('world_landmarks', shape=(0, 32, 5), chunks=(100, 32, 5), dtype='float32', maxshape=(None, 32, 5))
        self.root.create_dataset('label', shape=(0,), chunks=(1000,), dtype='int32', maxshape=(None,))
        self.root.create_dataset('timestamp', shape=(0,), chunks=(1000,), dtype='int32', maxshape=(None,))
        self.local_landmarks = self.root['local_landmarks']
        self.world_landmarks = self.root['world_landmarks']
        self.label = self.root['label']
        self.timestamp = self.root['timestamp']
        self.num_samples = 0

    def add_sample(self, local_landmarks, world_landmarks, label, timestamp):
        self.local_landmarks.resize(self.num_samples+1, axis=0)
        self.world_landmarks.resize(self.num_samples+1, axis=0)
        self.label.resize(self.num_samples+1, axis=0)
        self.timestamp.resize(self.num_samples+1, axis=0)
        self.local_landmarks[self.num_samples] = local_landmarks
        self.world_landmarks[self.num_samples] = world_landmarks
        self.label[self.num_samples] = label
        self.timestamp[self.num_samples] = timestamp
        self.num_samples += 1

    def remove_sample(self, index=-1):
        self.local_landmarks.resize(self.num_samples-1, axis=0)
        self.world_landmarks.resize(self.num_samples-1, axis=0)
        self.label.resize(self.num_samples-1, axis=0)
        self.timestamp.resize(self.num_samples-1, axis=0)
        self.num_samples -= 1

    def get_sample(self, index=-1):
        return self.local_landmarks[index], self.world_landmarks[index], self.label[index], self.timestamp[index]
    
    def get_samples(self, start=0, end=-1):
        return self.local_landmarks[start:end], self.world_landmarks[start:end], self.label[start:end], self.timestamp[start:end]
    
    def get_num_samples(self):
        return self.num_samples

    def close(self):
        self.store.close()

