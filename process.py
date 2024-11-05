import pandas as pd
import csv
from reader import output_filename, toRegExp
import time
import tqdm

encoding = "utf_8_sig"
objs = [
    "パソコン",
    "電気ストーブ",
    "自転車",
    "カラーテレビ",
    "照明器具",
    "電気温風機",
    "電気衣類乾燥機",
    "冷蔵庫",
    "扇風機",
    "ノートパソコン",
    "掃除機",
    "ヘアドライヤー",
    "電気洗濯機",
    "電気こんろ",
    "電気スタンド",
    "スチームアイロン",
    "電気オーブントースター",
    "電気オーブンレンジ",
    "電気やかん",
    "加湿器",
    "電気玩具",
    "電子レンジ",
    "エアコン",
    "電気ファンヒーター",
    "電気床暖房機",
    "電動工具",
    "電気ジャー炊飯器",
    "電気ポット",
    "電磁調理器",
    "電気たこ焼き器",
    "ミキサー",
    "電気文具",
    "ホットプレート",
    "ふとん乾燥機",
]

cols = ["事故原因区分", "被害の種類", "品名", "品目"]


def main():
    for obj in tqdm.tqdm(objs):
        extractData(objName=obj)
    for col in tqdm.tqdm(cols):
        freqAnalysis(col=col)


def freqAnalysis(col: str) -> None:
    """
    指定した列（col）の項目について、ユニークな項目の出現回数をカウントする。

    Params
    ------
    col: str
    列名を指定する。

    Returns
    -------
    None
    """
    # 整形データcsv読み込み
    with open(f"data/output/{output_filename}", "r", encoding=encoding) as file:
        reader = csv.reader(file)

        # 読み込んだデータを2次元配列に変換、整形
        l = [[toRegExp(elem) for elem in row] for row in reader]

    # データをpandasで扱える配列に変換
    cols = l.pop(0)
    df = pd.DataFrame(l, columns=cols)

    # 出現頻度
    frequency = df[col].value_counts()
    frequency.to_csv(
        f"data/output/frequency_data/frequency_{col}.csv", encoding=encoding
    )


def extractData(objName: str) -> None:
    """
    品名（objName）を含む行について、以下の項目を抽出する。
    - 被害の種類
    - 事故通知内容
    - 事故原因
    - 事故原因区分
    - 再発防止措置
    - 品目

    Params
    ------
    objName: str
    品名を入力する。

    Returns
    -------
    None
    """
    with open(f"data/output/{output_filename}", "r", encoding=encoding) as file:
        reader = csv.reader(file)
        l = [[toRegExp(elem) for elem in row] for row in reader]

    cols = l.pop(0)
    df = pd.DataFrame(l, columns=cols)

    # 特定の品名のデータを抽出
    targetCol = "品名"
    data = df[df[targetCol] == objName].loc[
        :,
        [
            "被害の種類",
            "事故通知内容",
            "事故原因",
            "事故原因区分",
            "再発防止措置",
            "品目",
        ],
    ]
    data.to_csv(
        f"data/output/extracted_data/{objName}_extracted.csv", encoding=encoding
    )


if __name__ == "__main__":
    start_time = time.time()
    main()
    finish_time = time.time()
    print(f"DONE in {finish_time - start_time} sec")
