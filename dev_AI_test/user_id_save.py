import pickle
import pandas as pd
import json

test = [["6a4300e36a0f6498bd0da951924304208eaee4387c99a1a2f1324d671933a38911", "1100", "1,2,3,4,5"]]

x = ['UserRequestID', 'UserID', 'MovieID']

list_df = pd.DataFrame(test, columns=x)

with open("users.pickle","wb") as f:
    pickle.dump(list_df, f)