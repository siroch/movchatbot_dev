import urllib.request as req
import requests
import json

from datetime import datetime as dt
from bs4 import BeautifulSoup as bs

class UserRating_Recommend:
    def __init__(self):
        # 현재 날짜
        self.date = dt.today().strftime("%Y%m%d")
        # genre list인 json 경로 지정, 형식 ex) genre_list = {'판타지':'1'}
        self.path = "../staticfiles/genre"
        self.Genre_list = json.load(f"{self.path}/genre.json")

    def recommend(self, genre):
        # 존재하지 않는 장르일경우, 올바르지 못한 입력일경우
        if self.Genre_list.get(genre) == None:
            return '잘못된 장르입니다.'

        # 현재 날짜에 맞는 입력된 장르의 유저 평점순 정렬된 웹 페이지 크롤링
        url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date={self.date}&tg={self.Genre_list[genre]}'
        url_res = requests.get(url)
        soup = bs(url_res.text,'html.parser')
        cinema = soup.select("#old_content > table > tbody > tr > td > div.tit5 > a")
        cinema_list = []
        for i in cinema:
            cinema_list.append(i.get_text())
        return {'cinema' : cinema_list}
        """
        리턴 타입
        {'cinema' : ['영화1',
                    '영화2',
                    '영화3',
                    ...
                    ]}
        """