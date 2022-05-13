import os
import pandas as pd
import numpy as np
import csv
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

# base_src = './data'
# u_data_src = os.path.join(base_src,'u.data')
# r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
# ratings = pd.read_csv(u_data_src, sep='\t', names=r_cols, encoding='latin-1')

ratings = pd.read_csv('./review_datas.csv')

R_temp = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
ratings_train, ratings_test = train_test_split(ratings,
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


rating_matrix = ratings_train.pivot(index='user_id',columns='movie_id',values='rating')

rating_mean = rating_matrix.mean(axis=1)
rating_bias = (rating_matrix.T - rating_mean).T

matrix_dummy = rating_matrix.copy().fillna(0)
user_similarity = cosine_similarity(matrix_dummy,matrix_dummy)
user_similarity = pd.DataFrame(user_similarity,index=rating_matrix.index,columns=rating_matrix.index)

def CF_knn_bias(user_id, movie_id, neighbor_size=0):
	if movie_id in rating_bias.columns:
		sim_scores = user_similarity[user_id].copy()
		movie_ratings = rating_bias[movie_id].copy()
		none_rating_idx = movie_ratings[movie_ratings.isnull()].index

		movie_ratings = movie_ratings.drop(none_rating_idx)
		sim_scores = sim_scores.drop(none_rating_idx)

		if neighbor_size == 0:
			prediction = np.dot(sim_scores,movie_ratings) / sim_scores.sum()
			prediction = prediction + rating_mean[user_id]
		else:
			if len(sim_scores) > 1:
				neighbor_size = min(neighbor_size, len(sim_scores))
				sim_scores = np.array(sim_scores)
				movie_ratings = np.array(movie_ratings)
				user_idx = np.argsort(sim_scores)
				sim_scores = sim_scores[user_idx][-neighbor_size:]
				movie_ratings = movie_ratings[user_idx][-neighbor_size:]

				prediction = np.dot(sim_scores, movie_ratings) / (sim_scores.sum() if sim_scores.sum() > 0 else 1)
				prediction = prediction + rating_mean[user_id]
			else:
				prediction = rating_mean[user_id]
	else:
		prediction = rating_mean[user_id]
	return prediction


def RMSE2(y_true, y_pred):
	return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2))

def recommender_1(recom_list,mf):
	recommendations = np.array([
			mf.get_one_prediction(user,movie) for (user,movie) in recom_list
	])
	return recommendations

def recommender_2(recom_list,neighbor_size=0):
	recommendations = np.array([
			CF_knn_bias(user,movie,neighbor_size) for (user,movie) in recom_list
	])
	return recommendations

recom_list = np.array(ratings_test.iloc[:,[0,1]])

predictions_1 = recommender_1(recom_list,mf)
# predictions_2 = recommender_2(recom_list,37)

feat.view_print('reco 1 : ', RMSE2(ratings_test.iloc[:,2],predictions_1))
# feat.view_print('reco 2 : ', RMSE2(ratings_test.iloc[:,2],predictions_2))

weigth = [0.8,0.2]

# predictions = predictions_1*weigth[0] + predictions_2*weigth[1]

# feat.view_print('reco 1+2 : ',RMSE2(ratings_test.iloc[:,2],predictions))

feat.view_print('불사조: ',mf.get_one_prediction(1509,2819))
feat.view_print('불의잔: ',mf.get_one_prediction(1509,2993))
feat.view_print('죽성1: ',mf.get_one_prediction(1509,3003))
feat.view_print('신동사: ',mf.get_one_prediction(1509,549))
feat.view_print('그린델왈드: ',mf.get_one_prediction(1509,328))
feat.view_print('아이언맨: ',mf.get_one_prediction(1509,38))
feat.view_print('어벤져스 인피니티: ',mf.get_one_prediction(1509,184))
feat.view_print('1,1: ',mf.get_one_prediction(1,1))


print(mf.full_prediction())
print(type(mf.full_prediction()))
print(len(mf.full_prediction()[0]))
cols = []
for i in range(len(mf.full_prediction()[0])):
	cols.append(i)

df = pd.DataFrame(mf.full_prediction(), columns=cols)
df.to_csv("model.csv", mode='w')



