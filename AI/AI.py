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

    def find_sim_movie(self, df, sorted_ind, title_name, top_n=10):
        title_movie = df[df['title']==title_name]

        title_index = title_movie.index.values
        similar_indexes = sorted_ind[title_index, :(top_n)]

        print(similar_indexes)
        similar_indexes = similar_indexes.reshape(-1)

        return df.iloc[similar_indexes]

def find_sim_movie_item(df, title_name, top_n=10):
    title_movie_sim = df[[title_name]].drop(title_name, axis=0)

    return title_movie_sim.sort_values(title_name, ascending=False)[:top_n]

if __name__ == '__main__':
    # 오류(SettingWithCopyError 발생)
    pd.set_option('mode.chained_assignment', 'raise') # SettingWithCopyError

    # 경고(SettingWithCopyWarning 발생, 기본 값입니다)
    pd.set_option('mode.chained_assignment', 'warn') # SettingWithCopyWarning

    # 무시
    pd.set_option('mode.chained_assignment',  None) # <==== 경고를 끈다

    ai = AI()
    temp = ai.aitest()[0]
    movie_data = temp.genres.str.replace('|',',')
    result2 = pd.concat([temp.title,movie_data],axis=1)
    print(result2)
    
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

    movies_df.insert(8,"genres_literal",genres_list,True)

    print(movies_df)

    count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
    genre_mat = count_vect.fit_transform(movies_df['genres_literal'])

    genre_sim = cosine_similarity(genre_mat, genre_mat)
    print(genre_sim[:2])

    genre_sim_sorted_ind = genre_sim.argsort()[:, ::-1]
    print(genre_sim_sorted_ind[:1])

    similar_movies = ai.find_sim_movie(movies_df, genre_sim_sorted_ind, "The Godfather", 10)
    print(similar_movies[['title', 'vote_average']])


    movies = ai.aitest()[0]
    ratings = ai.aitest()[1]

    rating_movies = pd.merge(ratings, movies, on='movieId')
    ratings_matrix = rating_movies.pivot_table('rating', index='userId', columns='title')
    ratings_matrix.fillna(0, inplace=True)
    ratings_matrix_T = ratings_matrix.transpose()
    item_sim = cosine_similarity(ratings_matrix_T, ratings_matrix_T)
    item_sim_df = pd.DataFrame(data=item_sim, index=ratings_matrix.columns, columns=ratings_matrix.columns)

    print(item_sim_df.shape)
    print(item_sim_df.head(2))

    print(find_sim_movie_item(item_sim_df, 'Godfather, The (1972)'))