import urllib.request as req
import requests
import json
import pandas as pd
import re

from datetime import datetime as dt
from bs4 import BeautifulSoup as bs

from utils.kakao_map import KakaoMap

class Theater_Info:
    def __init__(self):
        # 현재날짜
        self.date = dt.today().strftime("%Y%m%d")
        # 영화코드들 목록
        self.path = "../staticfiles/theater_code"
        self.Cgv_list = json.load(f"{self.path}/cgv.json")
        self.MegaBox_list = json.load(f"{self.path}/megabox.json")
        self.LotteCinema_list = json.load(f"{self.path}/megabox.json")

    """
    리턴 예제
    'CGV동수원': {'cinema': None,
                'date': '20220306',
                'event': 'http://www.cgv.co.kr/culture-event/event/defaultNew.aspx#1',
                'name': 'CGV동수원',
                'nav': 'https://map.kakao.com/?sName=경기수원시팔달구인계동&eName=CGV동수원',
                'pos': {'pos1': '경기 수원시 팔달구 권광로 181',
                        'pos2': '경기 수원시 팔달구 인계동 1113-11'},
                'ticket': 'http://www.cgv.co.kr/theaters/?areacode=02&theatercode=0041&date=20220306'}
    """ # cgv 상영관 정보 제공
    def CGV(self, theatercode, areacode, regioncode, name, pos1, pos2, startpos):
        event = 'http://www.cgv.co.kr/culture-event/event/defaultNew.aspx#1'
        if areacode == 'None':
            ticket = f'http://www.cgv.co.kr/theaters/special/show-times.aspx?regioncode={regioncode}&theatercode={theatercode}'
        if regioncode == 'None':
            ticket = f'http://www.cgv.co.kr/theaters/?areacode={areacode}&theatercode={theatercode}&date={self.date}'

        pos = dict(
            pos1=pos1,
            pos2=pos2
        )
        startpos = re.sub(' |\n|\r|\t', '', startpos.strip())
        nav_name = re.sub(' |\n|\r|\t', '', name.strip())
        nav = f'https://map.kakao.com/?sName={startpos}&eName={nav_name}'

        theater_list = dict(
            name=name,
            cinema=None,
            date=self.date,
            event=event,
            ticket=ticket,
            pos=pos,
            nav=nav
        ) # 상영관 이름, 현재날짜, 이벤트 링크, 예매링크, 주소지, 입력받은 주소에서 해당 상영관까지 가는길 지도 링크 제공
        return theater_list
    """
    리턴 예제
    '메가박스마곡': {'cinema': None,
            'date': '20220306',
            'event': 'https://www.megabox.co.kr/event',
            'name': '메가박스마곡',
            'nav': 'https://map.kakao.com/?sName=서울강서구&eName=메가박스마곡',
            'pos': {'pos1': '서울 강서구 공항대로 247', 'pos2': '서울 강서구 마곡동 797-1'}
    """ # 메가박스 상영관 정보 제공
    def MegaBox(self, theatercode, name, pos1, pos2, startpos):
        event = 'https://www.megabox.co.kr/event'
        ticket = f'https://www.megabox.co.kr/theater?brchNo={theatercode}'
        
        pos = dict(
            pos1=pos1,
            pos2=pos2
        )
        startpos = re.sub(' |\n|\r|\t', '', startpos.strip())
        nav_name = re.sub(' |\n|\r|\t', '', name.strip())
        nav = f'https://map.kakao.com/?sName={startpos}&eName={nav_name}'

        theater_list = dict(
            name=name,
            cinema=None,
            date=self.date,
            event=event,
            ticket=ticket,
            pos=pos,
            nav=nav
        )
        return theater_list

    """
    리턴 예제
    '롯데시네마김포공항': {'cinema': None,
               'date': '20220306',
               'event': 'https://event.lottecinema.co.kr/NLCHS/Event',
               'name': '롯데시네마김포공항',
               'nav': 'https://map.kakao.com/?sName=서울강서구&eName=롯데시네마김포공항',
               'pos': {'pos1': '서울 강서구 하늘길 지하 77', 'pos2': '서울 강서구 방화동 886'},
               'ticket': 'https://www.lottecinema.co.kr/NLCHS/Cinema/Detail?divisionCode=1&detailDivisionCode=1&cinemaID=1009'}
    """ # 롯데시네마 상영관 정보 제공
    def LotteCinema(self, divcode, detaildiv_code, cinema_code, name, pos1, pos2, startpos):
        event = 'https://event.lottecinema.co.kr/NLCHS/Event'
        ticket = f'https://www.lottecinema.co.kr/NLCHS/Cinema/Detail?divisionCode={divcode}&detailDivisionCode={detaildiv_code}&cinemaID={cinema_code}'
        
        pos = dict(
            pos1=pos1,
            pos2=pos2
        )
        startpos = re.sub(' |\n|\r|\t', '', startpos.strip())
        nav_name = re.sub(' |\n|\r|\t', '', name.strip())
        nav = f'https://map.kakao.com/?sName={startpos}&eName={nav_name}'

        theater_list = dict(
            name=name,
            cinema=None,
            date=self.date,
            event=event,
            ticket=ticket,
            pos=pos,
            nav=nav
        )
        return theater_list

    """
    리턴 예제
    {'CGV동수원': {'cinema': None,
                'date': '20220306',
                'event': 'http://www.cgv.co.kr/culture-event/event/defaultNew.aspx#1',
                'name': 'CGV동수원',
                'nav': 'https://map.kakao.com/?sName=경기수원시팔달구인계동&eName=CGV동수원',
                'pos': {'pos1': '경기 수원시 팔달구 권광로 181',
                        'pos2': '경기 수원시 팔달구 인계동 1113-11'},
                'ticket': 'http://www.cgv.co.kr/theaters/?areacode=02&theatercode=0041&date=20220306'},
     'CGV수원': {'cinema': None,
               'date': '20220306',
               'event': 'http://www.cgv.co.kr/culture-event/event/defaultNew.aspx#1',
               'name': 'CGV수원',
               'nav': 'https://map.kakao.com/?sName=경기수원시팔달구인계동&eName=CGV수원',
               'pos': {'pos1': '경기 수원시 팔달구 덕영대로 924',
                       'pos2': '경기 수원시 팔달구 매산로1가 18'},
               'ticket': 'http://www.cgv.co.kr/theaters/?areacode=02&theatercode=0012&date=20220306'}}
    """ # 영화관 정보 제공
    def theater(self, startaddr, name):
        map_data = KakaoMap()
        theater_list = {}

        # 입력받은 주소지의 정보를 가져옴, 주소를 가져올수 없는 경우의 예외처리가 진행됨
        pos = map_data.addr_conv_pos(startaddr)
        if pos == None:
            return '잘못된 주소입니다.'
        if len(pos['documents']) == 0:
            return '잘못된 주소입니다.'

        # 주소값을 받아옴, '인계동 수원시'의 경우 '경기 수원시 팔달구 인계동'이 정확한 명칭이므로 바꿔줌
        x = pos['documents'][0]['x']
        y = pos['documents'][0]['y']
        startaddr = pos['documents'][0]['address_name']

        # name, 영화관의 종류이자 키워드를 뜻함, 해당 값 기준으로 영화관을 찾아줌
        # 상영관의 정보가 2개이상 들어오거나 반경이 10km를 넘어가면 탐색 종료
        radius = 3000
        t_list = map_data.pos_conv_addr(name, x, y, radius)
        while len(t_list['documents']) < 2 and radius < 10000:
            radius += 1000
            t_list = map_data.pos_conv_addr(name, x, y, radius)
        if len(t_list['documents']) == 0:
            return '근처에 상영관이 존재하지 않습니다.'
        
        # 정보가 제대로 들어올 경우 해당 상영관들의 주소지를 통해 cgv,megabox,lottecinema에 맞게 데이터를 가공하여 작동함
        for theater in t_list['documents']:
            x = theater['x']
            y = theater['y']
            pos1 = theater['road_address_name']
            pos2 = theater['address_name']
            
            if name == 'cgv':
                if theater['place_name'].find('씨네드쉐프') != -1:
                    cgv_theater = "CINE de CHEF " + theater['place_name'].split()[-1]
                    theater_code = self.Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = 'None'
                    regioncode = self.Cgv_list[f'{cgv_theater}']['regioncode']
                elif theater['place_name'].find('DRIVE') != -1:
                    cgv_theater = theater['place_name']
                    theater_code = self.Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = self.Cgv_list[f'{cgv_theater}']['areacode']
                    regioncode = 'None'
                else:
                    cgv_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    theater_code = self.Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = self.Cgv_list[f'{cgv_theater}']['areacode']
                    regioncode = 'None'
                theater_list[f'{cgv_theater}'] = self.CGV(theater_code, f'{areacode}', f'{regioncode}', cgv_theater, pos1, pos2, startaddr)
            elif name == '메가박스':
                if theater['place_name'].find('(') != -1:
                    continue
                else:
                    mega_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    theater_code = self.MegaBox_list[f'{mega_theater[4:]}']['brchNo']
                theater_list[f'{mega_theater}'] = self.MegaBox(theater_code, mega_theater, pos1, pos2, startaddr)
            elif name == '롯데시네마':
                if theater['place_name'].find('(') != -1:
                    continue
                else:
                    lotte_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    div_code = self.LotteCinema_list[f'{lotte_theater[5:]}']['divisionCode']
                    detaildiv_code = self.LotteCinema_list[f'{lotte_theater[5:]}']['detailDivisionCode']
                    cinema_code = self.LotteCinema_list[f'{lotte_theater[5:]}']['cinemaID']
                theater_list[f'{lotte_theater}'] = self.LotteCinema(div_code, detaildiv_code, cinema_code, lotte_theater, pos1, pos2, startaddr)   

        return theater_list