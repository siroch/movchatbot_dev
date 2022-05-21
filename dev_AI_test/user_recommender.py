import pickle
import pandas as pd
import json

class User_Recommender:
    def __init__(self, req):
        self.User_req = req
        with open("model.pickle","rb") as f:
            self.Reco_Model_df = pickle.load(f)

        with open("datas.pickle","rb") as f:
            self.Review_Datas_df = pickle.load(f)

        with open("users.pickle","rb") as f:
            self.User_Datas_df = pickle.load(f)
        # 유저 식별자 아이디
        self.user_req_id = self.User_req['userRequest']['user']['id']
        # 유저 데이터셋에서 식별자 아이디가 있는 row를 가져옴
        self.user_data = self.User_Datas_df[self.User_Datas_df['UserRequestID'] == self.user_req_id]
        # UserRequestID | UserID | MovieID의 DataFrame에서 학습용 아이디와 유저가 학습한 영화번호들을 가져옴
        self.user_id = self.user_data['UserID']
        self.user_movie = self.user_data['MovieID']
        # 해당 유저의 영화별 평점 추정치 데이터를 가져옴
        self.user_reco_data = self.Reco_Model_df[int(self.user_id)]

    def user_estimate(self, item): # 상위 N(item)개의 영화를 (추정 평점, 영화 아이디) 형식으로 리턴해줌
        movie_datas = []
        for i in range(len(self.user_reco_data)):
            movie_datas.append((self.user_reco_data[i], i+1))
        movie_datas.sort(key=lambda x:x[0], reverse=True)
        return movie_datas[:item]

    def genre_extract(self): # 해당유저의 추정값 기준으로 가장 많이 나오는 순서대로 장르를 리턴, [[장르1,n],[장르2,m],...], 장르는 str n은 int
        movie_list = self.user_estimate(20)

        genre_list = []
        genre_check = []
        for i in movie_list:
            movie_id = i[1]
            genre_data = self.Review_Datas_df[self.Review_Datas_df['MovieID'] == movie_id]
            genre = genre_data.iloc[0]['Genre'].split(',')

            for j in genre:
                if j in genre_list:
                    genre_check[genre_list.index(j)] += 1
                else:
                    genre_list.append(j)
                    genre_check.append(1)

        genre_result = []
        for i in range(len(genre_check)):
            genre_result.append([genre_list[i],genre_check[i]])

        genre_result.sort(key=lambda x:x[1], reverse=True)
        return genre_result

    def recommender_movie(self,item): # 상위 N(item)개의 영화를 [영화1,영화2,영화3,...] 형식으로 리턴해줌, 인자값은 str형식
        movie_list = self.user_estimate(item)
        reco_movie_name = []
        for i in movie_list:
            movie_id = i[1]
            movie_name = self.Review_Datas_df[self.Review_Datas_df['MovieID'] == movie_id]
            reco_movie_name.append(movie_name.iloc[0]['MovieName'])
        return reco_movie_name




if __name__ == '__main__':
    with open(f"./test.json", "r") as file:
        User_req = json.load(file)

    test = User_Recommender(User_req)

    print(test.genre_extract())
    print(test.recommender_movie(5))


