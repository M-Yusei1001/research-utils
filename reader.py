import csv
import pprint

def toRegExp(data:str) -> str:
    return data.replace("\u3000", "")

with open("data/src/J20241017103313.csv", encoding="utf-8") as f:
    #csv読み込み
    reader = csv.reader(f)
    
    #読み込んだデータを2次元配列に変換、整形
    l = [[toRegExp(elem) for elem in row] for row in reader]

pprint.pprint(l[1])