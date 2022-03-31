import pandas as pd


class RecommendationDataset:
    def __init__(self):
        self.data_pd = pd.read_csv("../data/movie_list.csv")