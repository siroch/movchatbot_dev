import argparse

import matplotlib.pyplot as plt
import torch
import pandas as pd
from torch import nn

from torch.utils.data import DataLoader

from utils import RecommendationDataset


if __name__ == '__main__':
    x = RecommendationDataset()
    pd_file = x.csv_load()

    filtering_genre = '애니메이션'
    print("단일 장르 필터링, 해당 장르가 포함된 영화의 장르")
    print("--------------------------------------------------------")
    print(pd_file[pd_file['장르'].str.contains(filtering_genre)]['장르'])

    print("\n\n\n\n")
    print("or 연산, 주어진 장르들 중 하나라도 포함된 영화의 장르")
    print("--------------------------------------------------------")
    print(pd_file.query(f'장르.str.contains("{filtering_genre}|판타지")', engine='python')['장르'])


    print("\n\n\n\n")
    print("and 연산, 주어진 장르들 모두 포함된 영화의 장르")
    print("--------------------------------------------------------")
    filtering_genre_list = ['애니메이션', '판타지']
    print(pd_file[pd_file['장르'].map(lambda x: all(string in x for string in filtering_genre_list))]['장르'])
