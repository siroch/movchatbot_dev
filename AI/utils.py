import pandas as pd
import torch
from torch.utils.data import Dataset


class RecommendationDataset(Dataset):
    def __init__(self, datapath, train=True):
        self.data_pd = pd.read_csv(datapath)
        self.items = torch.LongTensor(self.data_pd['itemId'])
        self.users = torch.LongTensor(self.data_pd['userId'])
        self.train = train
        if self.train == True:
            self.ratings = torch.FloatTensor(self.data_pd['rating'])

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        if self.train is False:
            return self.users[idx], self.items[idx]
        return self.users[idx], self.items[idx], self.ratings[idx]

    def get_datasize(self):
        if self.train is False:
            return self.users.max() + 1, self.items.max() + 1
        return self.users.max() + 1, self.items.max() + 1, len(self.ratings)