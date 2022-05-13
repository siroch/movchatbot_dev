import csv
import pandas as pd
# f = open('./model.csv','r')
# rdr = csv.reader(f)

# print(rdr[1,1])

csv_input = pd.read_csv("./model.csv")
print(csv_input.loc[1508,f'{2818}'])