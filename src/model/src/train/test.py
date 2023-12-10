import rospkg
import os
import torch
from dataset.dataset import PoseDataset
from torch.utils.data import DataLoader
from model.model import GestureClassifier
from model.model_nn import GestureClassifierNN
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

def main():
    # name = 'alpha'
    name = 'modalpha'
    pack_path = rospkg.RosPack().get_path('dataset')
    dataset_path = os.path.join(pack_path, 'dataset_raw',  f'{name}.zarr')
    dataset = PoseDataset(dataset_path)
    loader = DataLoader(dataset, batch_size=20, shuffle=True, num_workers=0)
    # Get distrobution of labels
    distrobution = {}
    labels = dataset.label[:].reshape(-1).tolist()
    labels = [int(label) for label in labels]
    for label in set(labels):
        print(f'Label {label}: {labels.count(label)}')
        distrobution[label] = labels.count(label)

    num_classes = 256
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')
    model = GestureClassifier(num_classes=num_classes).to(device)
    # model = GestureClassifierNN(num_classes=num_classes).to(device)
    model.eval()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0000001)

    # Load the pretrained model
    # model.load_state_dict(torch.load('model.pth'))
    model.load_state_dict(torch.load('model.pth', map_location=torch.device('cpu')))
    model = model.to(device)

    correct = 0
    all_labels = []
    all_predictions = []

    for batch in loader:
        world_landmarks = batch['world_landmarks'] 
        world_landmarks = world_landmarks.reshape(world_landmarks.shape[0], world_landmarks.shape[1], -1).to(device)
        mask_landmarks = batch['mask_landmarks'].to(device)
        label = batch['label'].squeeze(1).long().to(device)
        output = model(world_landmarks, mask_landmarks).squeeze(1)
        output_val = torch.argmax(output, dim=1)
        correct += torch.sum(output_val == label).item()

        # Append labels and predictions for confusion matrix
        all_labels.extend(label.cpu().numpy())
        all_predictions.extend(output_val.cpu().numpy())

    print(f'Accuracy: {correct / len(dataset)}')

    for label in set(all_predictions):
        print(f'Label {label}: {all_predictions.count(label)}')

    # Calculate the confusion matrix
    confusion_mat = confusion_matrix(all_labels, all_predictions)

    # Display the confusion matrix
    plt.figure(figsize=(num_classes, num_classes))
    plt.imshow(confusion_mat, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(num_classes)
    plt.xticks(tick_marks, range(num_classes))
    plt.yticks(tick_marks, range(num_classes))
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()


            
    

if __name__ == '__main__':
    main()
