import urllib.request as req
import requests

from decouple import config

class KakaoMap:
    def __init__(self):
        # 카카오 맵 api key
        self.KAKAO_MAP_API_KEY = config("KAKAO_MAP_API_KEY")

    # 주소지 입력받으면 해당 주소지에 맞는 정보를 리턴
    """
    리턴 형태 예시
    {'documents': [{'address': {'address_name': '경기 수원시 팔달구 인계동',
                                'b_code': '4111514100',
                                'h_code': '4111573000',
                                'main_address_no': '',
                                'mountain_yn': 'N',
                                'region_1depth_name': '경기',
                                'region_2depth_name': '수원시 팔달구',
                                'region_3depth_h_name': '인계동',
                                'region_3depth_name': '인계동',
                                'sub_address_no': '',
                                'x': '127.021317877448',
                                'y': '37.2703764922259'},
                    'address_name': '경기 수원시 팔달구 인계동',
                    'address_type': 'REGION',
                    'road_address': None,
                    'x': '127.021317877448',
                    'y': '37.2703764922259'}],
     'meta': {'is_end': True, 'pageable_count': 1, 'total_count': 1}}    
    """
    def addr_conv_pos(self, addr):
        _kakao_url = f'https://dapi.kakao.com/v2/local/search/address.json?analyze_type=similar&page=1&size=1&query={addr}'
        _kakao_header = {
            'Authorization': self.KAKAO_MAP_API_KEY
        }
        res = requests.get(_kakao_url, headers=_kakao_header)

        if res.status_code == 200:
            if len(res.json()['documents']) == 0:
                return self.pos_conv_addr(addr, None, None, None, None)
            else:
                return res.json()
        else:
            print('Error : {}'.format(res.status_code))
            return '에러가 발생하였습니다.'

    # 좌표값 x,y 기준으로 반경 radius 내에 존재하는 query에 맞는 위치 정보 제공
    """
    리턴 형태 예시
    {'documents': [{'address_name': '경기 수원시 팔달구 인계동 1113-11',
                    'category_group_code': 'CT1',
                    'category_group_name': '문화시설',
                    'category_name': '문화,예술 > 영화,영상 > 영화관 > CJCGV',
                    'distance': '1210',
                    'id': '8552500',
                    'phone': '1544-1122',
                    'place_name': 'CGV 동수원',
                    'place_url': 'http://place.map.kakao.com/8552500',
                    'road_address_name': '경기 수원시 팔달구 권광로 181',
                    'x': '127.03231003231717',
                    'y': '37.26390632559984'},
                   {'address_name': '경기 수원시 팔달구 매산로1가 18',
                    'category_group_code': 'CT1',
                    'category_group_name': '문화시설',
                    'category_name': '문화,예술 > 영화,영상 > 영화관 > CJCGV',
                    'distance': '1923',
                    'id': '8590676',
                    'phone': '1544-1122',
                    'place_name': 'CGV 수원',
                    'place_url': 'http://place.map.kakao.com/8590676',
                    'road_address_name': '경기 수원시 팔달구 덕영대로 924',
                    'x': '127.00016910936856',
                    'y': '37.26655258928165'}],
     'meta': {'is_end': True,
              'pageable_count': 2,
              'same_name': {'keyword': 'cgv', 'region': [], 'selected_region': ''},
              'total_count': 2}}
    """
    def pos_conv_addr(self, query, x, y, radius, error=0):
        if error == None:
            _kakao_url = f'https://dapi.kakao.com/v2/local/search/keyword.json?page=1&sort=accuracy&query={query}'
        else:
            _kakao_url = f'https://dapi.kakao.com/v2/local/search/keyword.json?page=1&sort=accuracy&query={query}&size=15&x={x}&y={y}&radius={radius}&category_group_code=CT1'
        _kakao_header = {
            'Authorization': self.KAKAO_MAP_API_KEY
        }
        res = requests.get(_kakao_url, headers=_kakao_header)

        if res.status_code == 200:
            return res.json()
        else:
            print('Error : {}'.format(res.status_code))
            return '에러가 발생하였습니다.'