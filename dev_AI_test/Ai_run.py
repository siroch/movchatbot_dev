import pickle
from temp import Feature

feat = Feature()

with open("model.pickle","rb") as f:
    list_ex_load = pickle.load(f)

# 로드 방식
# user 1의 movie 2를 보고 싶은경우 list_ex_load[0][1]
# list 형식으로 저장되어 index 참조해야하므로 1씩 빼서 보면 됨

feat.view_print('1,1: ',list_ex_load[0][0])