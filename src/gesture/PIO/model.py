import torch
import torch.nn as nn
import torch.nn.functional as F
from perceiver_pytorch import PerceiverIO
# $ pip install rotary-embedding-torch
from rotary_embedding_torch import RotaryEmbedding



class GestureClassifier(torch.nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.model = PerceiverIO(
            dim = 32,                    # dimension of sequence to be encoded
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
        self.position_emb = RotaryEmbedding(32, 32)

    def forward(self, x):
        x = self.position_emb(x)
        return self.model(x)
    
    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        self.model.load_state_dict(torch.load(path))
        


    

