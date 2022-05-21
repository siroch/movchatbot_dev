import pickle
import pandas as pd
import numpy as np
import random
import json

class DataSave:
    def __init__(self, req):
        self.User_req = req
        self.user_req_id = self.User_req['userRequest']['user']['id']
        self.user_input_data = self.User_req['userRequest']['utterance']

        with open("datas.pickle","rb") as f:
            self.Review_Datas_df = pickle.load(f)

        with open("users.pickle","rb") as f:
            self.User_Datas_df = pickle.load(f)

        self.isUser = True
        self.user_data = self.User_Datas_df[self.User_Datas_df['UserRequestID'] == self.user_req_id]
        try:
            self.user_data.iloc[0]
        except:
            self.isUser = False

    def new_user(self, movie_id):
        new_user_id = str(self.Review_Datas_df.iloc[len(self.Review_Datas_df.index)-1]['UserID'] + 1)
        new_user_data = {'UserRequestID':self.user_req_id, 'UserID':new_user_id, 'MovieID':movie_id}
        self.User_Datas_df.loc[len(self.User_Datas_df.index)] = new_user_data

        self.review_data(list(map(int, movie_id.split(','))).sort(), new_user_id)

    def old_user(self, movie_id):
        old_user_id = self.user_data.iloc[0]['UserID']
        old_user_movie = self.user_data.iloc[0]['MovieID']
        head = list(map(int, old_user_movie.split(',')))
        tail = list(map(int, movie_id.split(',')))
        new_item = []
        print(head,tail)
        for i in tail:
            if i not in head:
                head.append(i)
                new_item.append(i)

        head.sort()
        new_item.sort()
        movie = ','.join(list(map(str,head)))

        old_user_data = {'UserRequestID':self.user_req_id, 'UserID':old_user_id, 'MovieID':movie}
        self.User_Datas_df = self.User_Datas_df.drop(index=self.User_Datas_df.loc[self.User_Datas_df['UserRequestID'] == self.user_req_id].index)
        self.User_Datas_df.loc[len(self.User_Datas_df.index)] = old_user_data
        print(new_item)
        self.review_data(new_item, old_user_id)

    def review_data(self, movie_id, user_id): # movieid userid int rating str
        columns = ['MovieName', 'MovieID', 'Genre', 'Rating', 'UserID', 'Review']
        review = '리뷰 없음'
        data = []
        for i in movie_id:
            movie = self.Review_Datas_df[self.Review_Datas_df['MovieID'] == i].iloc[0]
            name = movie['MovieName']
            genre = movie['Genre']
            rating = random.randrange(7,11)
            data.append([name, i, genre, rating, int(user_id), review])

        df = pd.DataFrame(data, columns=columns)

        self.Review_Datas_df = self.Review_Datas_df.append(df, ignore_index=True)

    def save_data(self):
        ''' 유저 쿼리 전문이 오는 방식에 따라 수정할 예정
        movie_names = self.user_input_data.split(',')
        idx = []
        for i in movie_names:
            try:
                movie = self.Review_Datas_df[self.Review_Datas_df['MovieName'] == i].iloc[0]
            except:
                continue
            idx.append(movie['MovieID'])
        m_list = list(map(int, idx))
        m_list.sort()
        movie_id = ','.join(list(map(str,m_list)))
        '''
        movie_id = '9,10,11,12,13,14'
        if self.isUser:
            self.old_user(movie_id)
        else:
            self.new_user(movie_id)
        return self.User_Datas_df, self.Review_Datas_df


if __name__ == '__main__':
    with open(f"./test.json", "r") as file:
        User_req = json.load(file)

    test = DataSave(User_req)
    new_data = test.save_data()
    new_user_dataset = new_data[0]
    new_movie_dataset = new_data[1]
    print(new_user_dataset)
    print(new_movie_dataset[new_movie_dataset['UserID'] == 1100]) # 지금 임시 등록한 유저id

    # 아래 코드는 실행하면 데이터를 덮어씌움
    # with open("users.pickle","wb") as f:
    #     pickle.dump(new_user_dataset, f)

    # with open("datas.pickle","wb") as f:
    #     pickle.dump(new_movie_dataset, f)


