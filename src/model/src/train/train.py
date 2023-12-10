import rospkg
import os
import torch
import numpy as np
from dataset.dataset import PoseDataset
from torch.utils.data import DataLoader, WeightedRandomSampler
from model.model import GestureClassifier
from model.model_nn import GestureClassifierNN

def main():
    # name = 'alpha'
    name = 'modalpha'
    pack_path = rospkg.RosPack().get_path('dataset')
    dataset_path = os.path.join(pack_path, 'dataset_raw',  f'{name}.zarr')
    dataset = PoseDataset(dataset_path)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')
    num_classes = 256
    mod_version = "PIO"
    if mod_version == "PIO":
        model = GestureClassifier(num_classes=num_classes).to(device)
        batch_size = 64
    else:
        model = GestureClassifierNN(num_classes=num_classes).to(device)
        batch_size = 256

    all_labels = dataset.label[:].reshape(-1).tolist()
    class_counts = np.bincount(all_labels)
    class_weights = 1. / class_counts
    weights = class_weights[all_labels]
    sampler = WeightedRandomSampler(weights, len(weights))
    loader = DataLoader(dataset, batch_size=batch_size, sampler=sampler, num_workers=0)

    distrobution = {}
    labels = dataset.label[:].reshape(-1).tolist()
    labels = [int(label) for label in labels]
    for label in set(labels):
        print(f'Label {label}: {labels.count(label)}')
        distrobution[label] = labels.count(label)


    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.CrossEntropyLoss()

    # Move the model and criterion to the GPU if available
    model = model.to(device)
    # Load the pretrained model
    # model.load_state_dict(torch.load('model.pth'))
    criterion = criterion.to(device)

    for epoch in range(300):
        for batch in loader:
            world_landmarks = batch['world_landmarks'] 
            # Collapse sub-batch dimension: [20, 64, 33, 5] -> [20, 64, 165]
            world_landmarks = world_landmarks.reshape(world_landmarks.shape[0], world_landmarks.shape[1], -1).to(device)
            mask_landmarks = batch['mask_landmarks'].to(device)
            label = batch['label'].squeeze(1).long().to(device)

            optimizer.zero_grad()
            output = model(world_landmarks, mask_landmarks).squeeze(1)
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch} Loss: {loss.item()}')

    torch.save(model.state_dict(), 'model.pth')


    

            
    

if __name__ == '__main__':
    main()
