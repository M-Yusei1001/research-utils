import csv
import tqdm
import unicodedata
import re
import time
import settings as st


# データ整形
def toRegExp(data: str) -> str:
    data = data.replace("\u3000", "")
    data = data.replace("\ufeff", "")
    return data


def removeBrackets(data: str) -> str:
    return re.sub(r"\(.*?\)", "", data)


def removeBigBrackets(data: str) -> str:
    return re.sub(r"\【.*?\】", "", data)


def main():
    print("データ前処理中...")
    # 生データcsv読み込み
    with open(
        f"data/src/{st.data_path[st.category][0]}", "r", encoding="utf_8_sig"
    ) as file:
        reader = csv.reader(file)

        # 読み込んだデータを2次元配列に変換、整形
        l = [
            [unicodedata.normalize("NFKC", toRegExp(elem)) for elem in row]
            for row in reader
        ]

    for row in tqdm.tqdm(l):
        row[2] = removeBrackets(row[2])
        row[2] = removeBigBrackets(row[2])

    # 整形データ書き出し
    with open(
        f"data/output/{st.data_path[st.category][1]}", "w", encoding="utf_8_sig"
    ) as file:
        writer = csv.writer(file, lineterminator="\n")
        for row in tqdm.tqdm(l):
            writer.writerow(row)

    print("前処理完了")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"DONE in {time.time() - start_time} sec")
