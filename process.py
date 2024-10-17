import pandas as pd
import csv
from reader import output_filename, toRegExp



def main():
    #整形データcsv読み込み
    with open(f"data/output/{output_filename}", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        
        #読み込んだデータを2次元配列に変換、整形
        l = [[toRegExp(elem) for elem in row] for row in reader]

    #データをpandasで扱える配列に変換
    cols = l.pop(0)
    df = pd.DataFrame(l, columns=cols)

    #品目の出現頻度
    col = "品名"
    print(df[col].value_counts())
    frequency = df[col].value_counts()
    frequency.to_csv(f"data/output/frequency_{col}.csv", encoding="shift-jis")

if __name__=="__main__":
    main()