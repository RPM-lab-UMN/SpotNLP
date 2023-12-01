import rospkg
import os
import torch
from dataset.dataset import PoseDataset
from torch.utils.data import DataLoader
from model.model import GestureClassifier

def main():
    name = 'data'

    pack_path = rospkg.RosPack().get_path('dataset')
    dataset_path = os.path.join(pack_path, 'dataset_raw',  f'{name}.zarr')
    dataset = PoseDataset(dataset_path)
    loader = DataLoader(dataset, batch_size=20, shuffle=True, num_workers=0)

    num_classes = 256
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')
    model = GestureClassifier(num_classes=num_classes).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.CrossEntropyLoss()

    # Move the model and criterion to the GPU if available
    model = model.to(device)
    criterion = criterion.to(device)

    for epoch in range(100):
        for batch in loader:
            world_landmarks = batch['world_landmarks'] 
            # Collapse sub-batch dimension: [20, 64, 33, 5] -> [20, 64, 165]
            world_landmarks = world_landmarks.reshape(world_landmarks.shape[0], world_landmarks.shape[1], -1).to(device)
            mask_landmarks = batch['mask_landmarks'].to(device)
            label = batch['label'].long()  # Convert to index tensor
            label = torch.nn.functional.one_hot(label, num_classes=num_classes).float().to(device)

            optimizer.zero_grad()
            output = model(world_landmarks, mask_landmarks)
            print(output.shape)
            print(label.shape)
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()
            print(loss.item())

    torch.save(model.state_dict(), 'model.pth')


    

            
    

if __name__ == '__main__':
    main()
