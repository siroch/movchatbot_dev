import argparse

import matplotlib.pyplot as plt
import torch
from torch import nn


from torch.utils.data import DataLoader

from model import ModelClass
from utils import RecommendationDataset


def train_and_valid(epoch, batchsize, learning_rate, rank, valid_size, early_stop):
	parser = argparse.ArgumentParser(description='2021 AI Final Project')
	parser.add_argument('--save-model', default='model.pt', help="Model's state_dict")
	parser.add_argument('--dataset', default='../data/csv', help='dataset directory')

	args = parser.parse_args()
	mf_model = ModelClass(610, 193609, rank = rank)
	train_size = 90752-valid_size
	train_data = RecommendationDataset(f'{args.dataset}/ratings.csv', train=True) # 90752개의 데이터
	train_set, valid_set = torch.utils.data.random_split(train_data, [train_size, valid_size])
	train_loader = DataLoader(train_set, batch_size=batchsize, shuffle=True)
	valid_loader = DataLoader(valid_set, batch_size=batchsize, shuffle=True)

	optimizer = torch.optim.Adam(mf_model.parameters(), lr=learning_rate)#weight_decay=weight
	criterion = nn.MSELoss()
	
	valid_list = [0.0, 0.0, 0.0]
	count = 0
	Epoch_list = []
	Train_list = []
	Valid_list = []
	for e in range(epoch):
		cost = 0
		for users, items, ratings in train_loader:
			optimizer.zero_grad()
			rating_pred = mf_model(users, items)
			loss = criterion(rating_pred, ratings)
			loss.backward()
			optimizer.step()
			cost += loss.item() * len(ratings)

		cost /= train_size
		
		cost_valid = 0
		for users, items, ratings in valid_loader:
			rating_pred = mf_model(users, items)
			loss = criterion(rating_pred, ratings)
			cost_valid += loss.item() * len(ratings)

		cost_valid /= valid_size

		if e < 3:
			valid_list[e] = cost_valid
		else:
			valid_list[0] = valid_list[1]
			valid_list[1] = valid_list[2]
			valid_list[2] = cost_valid

		if valid_list[0] < valid_list[1] and valid_list[0] < valid_list[2]:
			count += 1

		Epoch_list.append(e)
		Train_list.append(cost)
		Valid_list.append(cost_valid)
		print(f"Epoch : {e}")
		print("train cost : {:.6f}".format(cost))
		print("valid cost : {:.6f}".format(cost_valid))

		if count == early_stop:
			break

	torch.save(mf_model.state_dict(), args.save_model)
	return Epoch_list, Train_list, Valid_list
	

if __name__ == '__main__':
	ep = 40
	lr = 0.005
	r = 10
	batch = 32
	v_size = 20000
	e_stop = 3
	
	E, T, V = train_and_valid(epoch=ep,batchsize=batch,learning_rate=lr,rank=r,valid_size=v_size,early_stop=e_stop)
	
	plt.ylabel("MSE, cost")
	plt.xlabel(f"Epoch\nbatch_size={batch}, learning_rate={lr}, rank={r}, valid_size={v_size}, early_stop={e_stop}")
	plt.plot(E, T, c='black', label='Train cost for MSE')
	plt.plot(E, V, c='red', label='Valid cost for MSE')
	plt.legend()
	plt.show()
	# df = train_data.data_pd
	# df_table = df.set_index(['userId', 'itemId']).unstack().fillna(0)
	# print(df_table)
