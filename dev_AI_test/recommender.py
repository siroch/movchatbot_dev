import os
import pandas as pd
import numpy as np
import csv
import pickle
from temp import Feature
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

feat = Feature()

class NEW_MF():
	def __init__(self, ratings, hyper_params):
		# user_id movie_id rating이 있는 데이터셋
		self.R = np.array(ratings)
		# 사용자수와 아이템수를 받아옴
		self.num_users, self.num_items = np.shape(self.R)
		# K : 잠재요인(latent factor)수
		# alpha : 학습률, learning rate?
		# beta : 정규화 갯수
		# iterations : SGD 계산 반복횟수
		# verbose : 학습과정을 중간중간 출력 여부
		self.K = hyper_params['K']
		self.alpha = hyper_params['alpha']
		self.beta = hyper_params['beta']
		self.iterations = hyper_params['iterations']
		self.verbose = hyper_params['verbose']

		item_id_index = []
		index_item_id = []
		for i, one_id in enumerate(ratings):
			item_id_index.append([one_id, i])
			index_item_id.append([i, one_id])
		self.item_id_index = dict(item_id_index)
		self.index_item_id = dict(index_item_id)

		user_id_index = []
		index_user_id = []
		for i, one_id in enumerate(ratings.T):
			user_id_index.append([one_id, i])
			index_user_id.append([i, one_id])
		self.user_id_index = dict(user_id_index)
		self.index_user_id = dict(index_user_id)

	def rmse(self):
		# self.R에서 평점이 있는,0이아닌 요소의 인덱스 가져옴
		xp, yp = self.R.nonzero()
		# prediction과 error를 담을 리스트
		self.predictions = []
		self.errors = []
		# 평점이 있는 요소(사용자x 아이템y) 각각에 대해 아래에 코드 실행
		for x,y in zip(xp,yp):
			# 사용자 아이템에 대해 평점 예측치를 함수를 통해 계산
			prediction = self.get_prediction(x,y)
			# 예측값을 저장, 실값과 예측값 차이를 계산해 오차값 리스트에 저장
			self.predictions.append(prediction)
			self.errors.append(self.R[x,y] - prediction)

		self.predictions = np.array(self.predictions)
		self.errors = np.array(self.errors)
		return np.sqrt(np.mean(self.errors**2))

	def sgd(self):
		for i,j,r in self.samples:
			# 사용자에 대한 평점 예측치 계산
			prediction = self.get_prediction(i,j)
			# 실값과 비교한 오차 계산
			e = (r - prediction)

			# 사용자,아이템 평가 경향 계산 및 업뎃
			self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
			self.b_d[j] += self.alpha * (e - self.beta * self.b_d[j])
			# P Q 행렬 계산 및 업뎃
			self.P[i,:] += self.alpha * ((e * self.Q[j,:]) - (self.beta * self.P[i,:]))
			self.Q[j,:] += self.alpha * ((e * self.P[i,:]) - (self.beta * self.Q[j,:]))

	def get_prediction(self, i, j):
		prediction = self.b + self.b_u[i] + self.b_d[j] + self.P[i,:].dot(self.Q[j,:].T)
		return prediction

	def set_test(self, ratings_test):
		test_set = []
		for i in range(len(ratings_test)):
			x = self.user_id_index[ratings_test.iloc[i,0]]
			y = self.item_id_index[ratings_test.iloc[i,1]]
			z = ratings_test.iloc[i,2]
			test_set.append([x,y,z])
			self.R[x,y] = 0
		self.test_set = test_set
		return test_set

	def test_rmse(self):
		error = 0
		for one_set in self.test_set:
			predicted = self.get_prediction(one_set[0],one_set[1])
			error += pow(one_set[2] - predicted, 2)
		return np.sqrt(error/len(self.test_set))

	def test(self):
		self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
		self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))

		self.b_u = np.zeros(self.num_users)
		self.b_d = np.zeros(self.num_items)
		self.b = np.mean(self.R[self.R.nonzero()])

		rows, columns = self.R.nonzero()
		self.samples = [(i,j,self.R[i,j]) for i,j in zip(rows,columns)]

		training_process = []
		for i in range(self.iterations):
			np.random.shuffle(self.samples)
			self.sgd()
			rmse1 = self.rmse()
			rmse2 = self.test_rmse()
			training_process.append((i+1,rmse1,rmse2))
			if self.verbose:
				if (i+1) % 10 == 0:
					print('Iterations : %d, Train RMSE = %.4f, Test RMSE = %.4f'%(i+1,rmse1,rmse2))
		return training_process

	def get_one_prediction(self, user_id, item_id):
		return self.get_prediction(self.user_id_index[user_id], self.item_id_index[item_id])

	def full_prediction(self):
		return self.b + self.b_u[:,np.newaxis] + self.b_d[np.newaxis,:] + self.P.dot(self.Q.T)

with open("datas.pickle","rb") as f:
    df = pickle.load(f)

ratings = df[['UserID', 'MovieID', "Rating"]]

ratings.columns = ['user_id', 'movie_id', 'rating']

R_temp = ratings.astype(int).pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
ratings_train, ratings_test = train_test_split(ratings.astype(int),
												test_size=0.2,
												shuffle=True,
												random_state=2021)

hyper_params = {
	'K' : 30, # 이게 너무 크면 과적합
	'alpha' : 0.001,
	'beta' : 0.02,
	'iterations' : 30, # 이것도 과적합 가능성
	'verbose' : True
}

mf = NEW_MF(R_temp, hyper_params)
test_set = mf.set_test(ratings_test)
result = mf.test()

with open("model.pickle","wb") as f:
    pickle.dump(mf.full_prediction(), f)

