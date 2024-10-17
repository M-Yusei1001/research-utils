import csv
import pandas as pd
import tqdm

output_filename = "incident_data_processed.csv"

#データ整形
def toRegExp(data:str) -> str:
    data = data.replace("\u3000", "")
    data = data.replace("\ufeff", "")
    return data

#生データcsv読み込み
with open("data/src/J20241017103313.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    
    #読み込んだデータを2次元配列に変換、整形
    l = [[toRegExp(elem) for elem in row] for row in reader]

#整形データ書き出し
with open(f"data/output/{output_filename}", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    for row in tqdm.tqdm(l):
        writer.writerow(row)