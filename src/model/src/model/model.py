import torch
import torch.nn as nn
from perceiver_pytorch import PerceiverIO
from torch import Tensor
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Arguments:
            x: Tensor, shape ``[seq_len, batch_size, embedding_dim]``
        """
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)


class GestureClassifier(torch.nn.Module):
    def __init__(self, num_classes = 255):
        super().__init__()
        self.input_dim = 33 * 5 # 33 landmarks, 5 dimensions per landmark
        self.num_classes = num_classes
        self.model = PerceiverIO(
            dim = 256,                    # dimension of sequence to be encoded
            queries_dim = 32,            # dimension of decoder queries
            logits_dim = 100,            # dimension of final logits
            depth = 6,                   # depth of net
            num_latents = 256,           # number of latents, or induced set points, or centroids. different papers giving it different names
            latent_dim = 512,            # latent dimension
            cross_heads = 1,             # number of heads for cross attention. paper said 1
            latent_heads = 8,            # number of heads for latent self attention, 8
            cross_dim_head = 64,         # number of dimensions per cross attention head
            latent_dim_head = 64,        # number of dimensions per latent self attention head
            weight_tie_layers = False,   # whether to weight tie layers (optional, as indicated in the diagram)
            seq_dropout_prob = 0.2       # fraction of the tokens from the input sequence to dropout (structured dropout, for saving compute and regularizing effects)
        )
        self.input_project = nn.Linear(33 * 5, 256)
        self.position_emb = PositionalEncoding(256)
        self.query = nn.Parameter(torch.randn(1, 1, 32))
        self.output_project = nn.Linear(100, num_classes)

    def forward(self, x, mask):
        x = self.input_project(x)
        x = self.position_emb(x)
        x = self.model(x, mask, self.query)
        x = self.output_project(x)
        return x

    