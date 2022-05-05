import requests
import re
import csv

from bs4 import BeautifulSoup as bs
from pprint import pprint


cinema_review_data = []
fields = ['MovieName', 'Grade', 'Review', 'UserID']

for i in range(18054911,10000000,-1):
	# review data crawling
	review = f'https://movie.naver.com/movie/point/af/list.naver?st=nickname&sword={i}&target=after'
	url_res = requests.get(review)
	soup = bs(url_res.text,'html.parser')

	# delete user check
	check = 0
	for j in soup.select("script")[1]:
		check += 1
	# check == 1 -> delete user
	if check == 1:
		continue

	review_ = soup.select("#old_content > h5")
	review_list = divmod(int(review_[0].find_all("strong")[0].get_text()), 10)
	r_list = review_list[0] + 1 if review_list[1]>0 else 0
	if r_list < 3 or r_list > 30:
		continue

	review_all = soup.select("#old_content > table")[0]
	review_data = review_all.find_all("tr")[1:]

	for j in range(2, r_list+1):
		review = f'https://movie.naver.com/movie/point/af/list.naver?st=nickname&sword={i}&target=after&page={j}'
		url_res = requests.get(review)
		soup = bs(url_res.text,'html.parser')
		review_all = soup.select("#old_content > table")[0]
		for k in review_all.find_all("tr")[1:]:
			review_data.append(k)
	try:
		for j in review_data:
			review_text = j.get_text()
			indent_delete = re.sub('\n|\r|\t', ',', review_text)
			review_text_data = re.sub(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,|,,', '!@#$%^&*!@#$%^&*!@#$%^&*', indent_delete[1:])
			review_text_data = review_text_data.split('!@#$%^&*!@#$%^&*!@#$%^&*')
			sorted_review_data = review_text_data[1:4]
			if len(sorted_review_data[1]) == 14:
				sorted_review_data[1] = '10'
			else :
				sorted_review_data[1] = sorted_review_data[1][12:]

			sorted_review_data.append(f'{i}')
			cinema_review_data.append(sorted_review_data)
	except:
		continue

	if len(cinema_review_data) > 100000:
		break

# with open('review_data.csv', 'w', encoding='utf-8-sig',newline='') as f: 
# 	write = csv.writer(f) 
# 	write.writerow(fields) 
# 	write.writerows(cinema_review_data)

# f = open('review_data.csv','r')
# rdr = csv.reader(f)
# test = []
# for i in rdr:
# 	if i[3] == ',신고':
# 		test.append(i[0:3]+['리뷰 없음'])
# 	else:
# 		test.append(i)


# with open('review_datas.csv', 'w', encoding='utf-8-sig',newline='') as f: 
# 	write = csv.writer(f) 
# 	write.writerow(test[0]) 
# 	write.writerows(test[1:])