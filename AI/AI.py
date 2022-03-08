import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import urllib.request as req

import requests
import scipy
import json
import re

import multiprocessing as mp
from multiprocessing import Pool

from pprint import pprint
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs

class AI:
    def __init__(self):
        self.json_path = "../data/json"
        self.csv_path = "../data/csv"

        self.movies_list = f"{self.csv_path}/movies.csv"
        self.ratings_list = f"{self.csv_path}/ratings.csv"

    def aitest(self):
        ds_movies = pd.read_csv(self.movies_list, index_col=0)
        ds_ratings = pd.read_csv(self.ratings_list)

        return ds_ratings, ds_movies

if __name__ == '__main__':
    ai = AI()
    print(ai.aitest()[0])
    print(ai.aitest()[1])
