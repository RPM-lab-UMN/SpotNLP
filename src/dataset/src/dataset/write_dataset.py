import zarr
import numpy as np

class WriteDataset:
    def __init__(self, path, max_history=300):
        self.path = path
        self.store = zarr.DirectoryStore(self.path)
        self.max_size = max_history
        self.compress = None # zarr.Blosc(cname='zstd', clevel=3, shuffle=2)
        self.root = zarr.group(store=self.store, overwrite=True)
        self.zarr_local = self.root.create_dataset('local_landmarks', 
                                 shape=(0, self.max_size, 33, 5), 
                                 chunks=(10, self.max_size, 33, 5), 
                                 dtype='float32', 
                                 maxshape=(None, self.max_size, 33, 5),
                                 compressor=self.compress)
        self.zarr_global = self.root.create_dataset('world_landmarks', 
                                 shape=(0, self.max_size, 33, 5), 
                                 chunks=(10, self.max_size, 33, 5), 
                                 dtype='float32', 
                                 maxshape=(None, self.max_size, 33, 5),
                                 compressor=self.compress)
        self.zarr_len = self.root.create_dataset('mask_landmarks', 
                                 shape=(0,self.max_size), 
                                 chunks=(1000,self.max_size), 
                                 dtype='bool', 
                                 maxshape=(None,self.max_size),)
        self.zarr_label = self.root.create_dataset('label', 
                                 shape=(0,1), 
                                 chunks=(1000,), 
                                 dtype='int32', 
                                 maxshape=(None,))
        self.zarr_time = self.root.create_dataset('timestamp', 
                                 shape=(0,1), 
                                 chunks=(1000,), 
                                 dtype='int32', 
                                 maxshape=(None,))
        self.local_landmarks = []
        self.world_landmarks = []
        self.mask_landmarks = []
        self.label = []
        self.timestamp = []

    def add_sample(self, local_landmarks, world_landmarks, label, timestamp):
        local = np.zeros((self.max_size, 33, 5), dtype=np.float32)
        local[:len(local_landmarks)] = local_landmarks
        world = np.zeros((self.max_size, 33, 5), dtype=np.float32)
        world[:len(world_landmarks)] = world_landmarks
        # Boolean mask of valid landmarks
        mask_landmarks = np.pad(np.ones(len(local_landmarks), dtype=bool), 
                        (0, self.max_size - len(local_landmarks)), 
                        'constant', 
                        constant_values=False)

        label = np.array(label)
        timestamp = np.array(timestamp)

        self.local_landmarks.append(local)
        self.world_landmarks.append(world)
        self.mask_landmarks.append(mask_landmarks)
        self.label.append(label)
        self.timestamp.append(timestamp)
    
    def add_samples(self, local_landmarks, world_landmarks, label, timestamp):
        local = np.zeros((len(local_landmarks), self.max_size, 33, 5), dtype=np.float32) 
        for i in range(len(local_landmarks)):
            local[i, :len(local_landmarks[i])] = np.expand_dims(local_landmarks[i], axis=0)
        world = np.zeros((len(world_landmarks), self.max_size, 33, 5), dtype=np.float32)
        for i in range(len(world_landmarks)):
            world[i, :len(world_landmarks[i])] = np.expand_dims(world_landmarks[i], axis=0)
        mask_landmarks = np.array([len(local_landmarks[i]) for i in range(len(local_landmarks))])
        label = np.array(label)
        timestamp = np.array(timestamp)

        self.local_landmarks.append(local)
        self.world_landmarks.append(world)
        self.mask_landmarks.append(mask_landmarks)
        self.label.append(label)
        self.timestamp.append(timestamp)

    def remove_sample(self):
        self.local_landmarks.pop()
        self.world_landmarks.pop()
        self.mask_landmarks.pop()
        self.label.pop()
        self.timestamp.pop()

    def __len__(self):
        return len(self.label)
    
    def write(self):
        assert self.store is not None, 'Dataset not initialized'
        self.zarr_local.append(np.array(self.local_landmarks, dtype=np.float32))
        self.zarr_global.append(np.array(self.world_landmarks, dtype=np.float32))
        self.zarr_len.append(np.array(self.mask_landmarks, dtype=np.int32))
        self.zarr_label.append(np.array(self.label, dtype=np.int32))
        self.zarr_time.append(np.array(self.timestamp, dtype=np.int32))
        self.local_landmarks = []
        self.world_landmarks = []
        self.mask_landmarks = [] 
        self.label = []
        self.timestamp = []


    def close(self):
        assert self.store is not None, 'Dataset not initialized'
        self.write()
        self.store.close()

    def print_shapes(self):
        assert self.store is not None, 'Dataset not initialized'
        print(f'local_landmarks: {self.zarr_local.shape}')
        print(f'world_landmarks: {self.zarr_global.shape}')
        print(f'mask_landmarks: {self.zarr_len.shape}')
        print(f'label: {self.zarr_label.shape}')
        print(f'timestamp: {self.zarr_time.shape}')


        
