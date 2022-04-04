import argparse

import matplotlib.pyplot as plt
import torch
import pandas as pd
from torch import nn

from torch.utils.data import DataLoader

from utils import RecommendationDataset

class Filtering_Data:
    def __init__(self):
        self.data = RecommendationDataset()
        self.pd_file = self.data.csv_load()

    def single_genre(self, genre):
        print(self.pd_file[self.pd_file['장르'].str.contains(genre, na=False)])

    def many_or_genres(self, genre):
        genre = '|'.join(genre)
        print(self.pd_file.query(f'장르.str.contains("{genre}")', engine='python'))

    def many_and_genres(self, genre):
        print(self.pd_file[self.pd_file['장르'].map(lambda x: all(string in x for string in genre))])

    def director(self, name):
        print(self.pd_file[self.pd_file['감독'].str.contains(name, na=False)])

    def actor(self, name):
        print(self.pd_file[self.pd_file['배우'].str.contains(name, na=False)])

    def nation(self, name):
        print(self.pd_file[self.pd_file['제작국가'].str.contains(name, na=False)])

    def filter_order(self, query, filter_data):
        if query == '단일 장르':
            self.single_genre(filter_data)
        elif query == '모든 장르':
            self.many_and_genres(filter_data)
        elif query == '장르':
            self.many_or_genres(filter_data)
        elif query == '감독':
            self.director(filter_data)
        elif query == '배우':
            self.actor(filter_data)
        elif query == '국가':
            self.nation(filter_data)


if __name__ == '__main__':
    test = Filtering_Data()

    filtering_genre = '애니메이션'
    print("단일 장르 필터링, 해당 장르가 포함된 영화")
    print("--------------------------------------------------------")
    test.filter_order('단일 장르',filtering_genre)

    filtering_genre_list = ['애니메이션', '판타지']
    print("\n\n\n\n")
    print("or 연산, 주어진 장르들 중 하나라도 포함된 영화")
    print("--------------------------------------------------------")
    test.filter_order('장르',filtering_genre_list)


    print("\n\n\n\n")
    print("and 연산, 주어진 장르들 모두 포함된 영화")
    print("--------------------------------------------------------")
    test.filter_order('모든 장르',filtering_genre_list)

    print("\n\n\n\n")
    print("특정 감독이 찍은 영화")
    print("--------------------------------------------------------")
    test.filter_order('감독','정용기')

    print("\n\n\n\n")
    print("특정 배우가 찍은 영화")
    print("--------------------------------------------------------")
    test.filter_order('배우','정준호')

    print("\n\n\n\n")
    print("특정 국가에서 찍은 영화")
    print("--------------------------------------------------------")
    test.filter_order('국가','한국')

