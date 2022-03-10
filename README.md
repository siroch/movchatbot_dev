# movchatbot_dev
movchatbot 기능 개발용 - 대학과제물

https://grouplens.org/datasets/movielens/

데이터셋 링크

recommended for new research - MovieLens Tag Genome Dataset 2021 사용해볼 예정

recommended for education and development - MovieLens Latest Datasets - ml-latest-small을 data/csv에 저장해둠

### 디렉토리 구조

	movchatbot_dev
		AI
			AI.py
			model.py
			run.py
			train.py
			utils.py
		data
			csv
				...
			json
				...
		utils
			...

AI 폴더
* * *
추천 시스템을 구현하기 위함.

1. **model.py** : 인공지능 모델을 구성
2. **run.py** : 학습된 모델을 기반으로 실 데이터를 넣어 값을 출력
3. **train.py** : 인공지능 학습을 위함
4. **utils.py** : 인공지능이 사용할 데이터를 처리하기 위함, 그 외적인 부가요소들을 구현
5. **AI.py** : 현재 테스트용도로 사용할 파일, 추후 삭제할수있음.



data 폴더
* * *
학습용 데이터셋 저장 및 기능 구현용 데이터셋



utils 폴더
* * *
추천 시스템 외 기능들을 구현한 자료들이 있는 폴더

