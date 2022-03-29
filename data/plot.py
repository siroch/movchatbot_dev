import os
import sys
import requests
import json
import openpyxl
from bs4 import BeautifulSoup
from openpyxl import Workbook
import pandas as pd
import urllib.request
import multiprocessing
from multiprocessing import Pool


headers = {
  'Host': 'openapi.naver.com',
  'User-Agent': 'curl/7.49..1',
  'Accept': '*/*',
  'X-Naver-Client-id': '0cRQYFHrJAQgcWi3njRi',
  'X-Naver-Client-Secret': 'vSOUBpiP02'
}

url = 'https://openapi.naver.com/v1/search/movie.json'

# 엑셀 파일 오픈
fileName = 'C:/Users/HEJ/Downloads/movie_list.xlsx'
myExcel = openpyxl.load_workbook(fileName,data_only=True)
# 시트 설정
mySheet = myExcel['korea']
get_cells = mySheet['A1001':'A8253'] # ending : 8253
idx = 1001

# 줄거리 크롤링
def getStory(plot_url):
    response = requests.get(plot_url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        story = soup.find('p','con_tx')
        if story is not None:
            story = str(story).replace('<p class="con_tx">','').replace('</p>','').replace('\n','').replace('\t','')
            story = story.replace('&lt;','<').replace('&gt;','>').replace('\r','').replace('\xa0','')
            story = story.replace('<b>','').replace('</b>','')
            story = story.replace('<br/>',' ')
            mySheet['I'+str(idx)] = story
        return False       
    else : 
        print(response.status_code)

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=6)
    for row in get_cells:
        for cell in row:
            movie = cell.value
            years = mySheet.cell(row=idx, column=3).value
            #years = int(mySheet(idx+1, 3)).value
            #print(movie)
            params ={
                'query': movie,
                'yearfrom' : years,
                'yearto' : years
            }
            res = requests.get(url, headers=headers, params=params)
            #print(res.text)

            jData = json.loads(res.text)
            itemCnt=jData['total']
            
            for item in jData['items']:
            # 동명영화가 2개 이상 존재하는 경우
                if itemCnt > 1 :
                    movName = item['title'].replace('<b>','')
                    movName= movName.replace('</b>','')
                    
                    if mySheet['A'+str(idx)] == movName and \
                    (item['director']==mySheet['F'+str(idx)] or (type(item['director'])=='list' and item['director'].split('|')[:-1].find(mySheet['F'+str(idx)])!=-1)) :

                    # 줄거리 link
                        plot_url = item['link']
                        getStory(plot_url)
                
            else:
                #actor
                posActor= 'G'+ str(idx)
                actors= item['actor'].split('|')[:-1]
                mySheet[posActor] = ','.join(actors)
                #score
                mySheet['H'+str(idx)] = item['userRating']
                # 줄거리 link
                plot_url = item['link']
                getStory(plot_url)
            print(res.text)
            
        idx=idx+1 
    myExcel.save('C:/Users/HEJ/Downloads/plotry.xlsx')