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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pprint import pprint
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs
from ast import literal_eval

class AI:
    def __init__(self):
        self.json_path = "../data/json"
        self.csv_path = "../data/csv"

        self.movies_list = f"{self.csv_path}/movies.csv"
        self.ratings_list = f"{self.csv_path}/ratings.csv"
        self.data_list = f"{self.csv_path}/tmdb_5000_movies.csv"

    def aitest(self):
        ds_movies = pd.read_csv(self.movies_list, index_col=0)
        ds_ratings = pd.read_csv(self.ratings_list)
        ds_data = pd.read_csv(self.data_list)

        return ds_movies, ds_ratings, ds_data

if __name__ == '__main__':
    ai = AI()
    temp = ai.aitest()[0]
    movie_data = temp.genres.str.replace('|',',')
    result2 = pd.concat([temp.title,movie_data],axis=1)

    movies = ai.aitest()[2]
    movies_df = movies[['id', 'title', 'genres', 'vote_average', 'vote_count', 'popularity', 'keywords', 'overview']]
    genres_list = []
    for i in range(len(movies_df)):
        movies_df['genres'][i] = literal_eval(movies_df['genres'][i])
        movies_df['keywords'][i] = literal_eval(movies_df['keywords'][i])
        movies_df['genres'][i] = [y['name'] for y in movies_df['genres'][i]]
        movies_df['keywords'][i] = [y['name'] for y in movies_df['keywords'][i]]
        txt = " ".join(movies_df['genres'][i])
        genres_list.append(txt)

    movies_df['genres_literal'] = genres_list

    print(movies_df)

    count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
    genre_mat = count_vect.fit_transform(movies_df['genres_literal'])
    print(genre_mat.shape)

    genre_sim = cosine_similarity(genre_mat, genre_mat)
    print(genre_sim.shape)
    print(genre_sim[:2])

    genre_sim_sorted_ind = genre_sim.argsort()[:, ::-1]
    print(genre_sim_sorted_ind[:1])
