import torch
from torch import nn


class ModelClass(nn.Module):

    def __init__(self, num_users=610, num_items=193609, rank=10):
        """
        TODO: Write down your model
        """
        super().__init__()
        self.U = torch.nn.Parameter(torch.randn(num_users + 1, rank))
        self.V = torch.nn.Parameter(torch.randn(num_items + 1, rank))

    def forward(self, users, items):
        ratings = torch.sum(self.U[users] * self.V[items], dim=-1)
        return ratings

## 임시