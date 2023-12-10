import torch

class GestureClassifierNN(torch.nn.Module):
    def __init__(self, num_classes = 255):
        super().__init__()
        self.input_dim = 33 * 5 # 33 landmarks, 5 dimensions per landmark
        self.num_classes = num_classes
        dims = (self.input_dim, 256, 128, 64, self.num_classes)
        self.model = torch.nn.Sequential(
            torch.nn.Linear(dims[0], dims[1]),
            torch.nn.ReLU(),
            torch.nn.Linear(dims[1], dims[2]),
            torch.nn.ReLU(),
            torch.nn.Linear(dims[2], dims[3]),
            torch.nn.ReLU(),
            torch.nn.Linear(dims[3], dims[4]),
        )

    def forward(self, x, mask):
        x = x[:, 0]
        x = self.model(x)
        return x

    