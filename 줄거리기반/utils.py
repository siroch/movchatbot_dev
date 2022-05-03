import pandas as pd

class RecommendationDataset:
    def __init__(self):
        self.json_path = "../data/json"
        self.csv_path = "../data/csv"
        self.data_path = "../data"
        self.movies_list = f"{self.data_path}/movie_list.csv"

    def csv_load(self):
        movie_list = pd.read_csv(self.movies_list)

        return movie_list