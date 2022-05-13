import requests
import re
import csv

from bs4 import BeautifulSoup as bs
from pprint import pprint

f = open('../data/review_data.csv','r')
rdr = csv.reader(f)
test = []
list_l = []
cinema_name = []
user_name = []
movie_id = 0
user_id = 0
review = ''
count = 0
for i in rdr:
	if count==0:
		count = 1
		continue
	if i[0] in cinema_name:
		movie_id = cinema_name.index(i[0]) + 1
	else:
		cinema_name.append(i[0])
		movie_id = len(cinema_name)
	if i[2] in user_name:
		user_id = user_name.index(i[2]) + 1
	else:
		user_name.append(i[2])
		user_id = len(user_name)
	test.append([i[0], movie_id, i[1], user_id, i[3]])

fields = ['MovieName', 'MovieID', 'Rating', 'UserID', 'Review']

with open('review_datas_fix.csv', 'w', encoding='utf-8-sig',newline='') as f: 
	write = csv.writer(f) 
	write.writerow(fields) 
	write.writerows(test)