import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import RecommendationDataset

class Filtering_Data:
    def __init__(self):
        self.data = RecommendationDataset()
        self.pd_file = self.data.csv_load()
        self.pd_file = self.pd_file.fillna('')

    def dataset(self):
        return self.pd_file

    def single_genre(self, genre):
        return self.pd_file[self.pd_file['장르'].str.contains(genre, na=False)]

    def many_or_genres(self, genre):
        genre = '|'.join(genre)
        return self.pd_file.query(f'장르.str.contains("{genre}")', engine='python')

    def many_and_genres(self, genre):
        return self.pd_file[self.pd_file['장르'].map(lambda x: all(string in x for string in genre))]

    def director(self, name):
        return self.pd_file[self.pd_file['감독'].str.contains(name, na=False)]

    def single_actor(self, name):
        return self.pd_file[self.pd_file['배우'].str.contains(name, na=False)]

    def many_actor(self, name):
        return self.pd_file[self.pd_file['배우'].map(lambda x: all(string in x for string in name))]

    def nation(self, name):
        return self.pd_file[self.pd_file['제작국가'].str.contains(name, na=False)]

    def filter_order(self, query, filter_data):
        if query == '단일 장르':
            output = self.single_genre(filter_data)
        elif query == '모든 장르':
            output = self.many_and_genres(filter_data)
        elif query == '장르':
            output = self.many_or_genres(filter_data)
        elif query == '감독':
            output = self.director(filter_data)
        elif query == '단일 배우':
            output = self.single_actor(filter_data)
        elif query == '배우':
            output = self.many_actor()
        elif query == '국가':
            output = self.nation(filter_data)
        return output

def find_sim_movie(df, sorted_ind, title_name, top_n=10):
    title_movie = df[df['영화명']==title_name]

    title_index = title_movie.index.values
    similar_indexes = sorted_ind[title_index, :(top_n)]

    similar_indexes = similar_indexes.reshape(-1)

    return df.iloc[similar_indexes]

def recommendsystem(data, query, filter_data, cinema_name):
    fil_data = data.filter_order(query, filter_data).reset_index()

    count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
    genre_mat = count_vect.fit_transform(fil_data['줄거리'])

    genre_sim = cosine_similarity(genre_mat, genre_mat)

    genre_sim_sorted_ind = genre_sim.argsort()[:, ::-1]

    similar_movies = find_sim_movie(fil_data, genre_sim_sorted_ind, cinema_name, len(fil_data))
    return similar_movies[['영화명', '평점']]


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    test = Filtering_Data()
    query = '단일 장르'
    filter_tag = '판타지'
    cinema_name = '해리포터와 마법사의 돌'
    # filter_data는 함수 호출 이전에 리스트 or 단일 문자열로 처리
    # 단일 장르, 감독, 단일 배우, 국가는 문자열, 모든 장르와 장르와 배우는 리스트(인자 2개 이상임)
    print(recommendsystem(test, query, filter_tag, cinema_name))