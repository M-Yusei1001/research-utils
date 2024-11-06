import pandas as pd
import csv
import time
import tqdm
from settings import encoding, products, cols
from reader import output_filename, toRegExp


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
        f"data/output/frequency_data/frequency_{col}.csv",
        encoding=encoding,
        index_label="selected_col",
    )


def extractData(product: str) -> None:
    """
    品名（product）を含む行について、以下の項目を抽出する。
    - 被害の種類
    - 事故通知内容
    - 事故原因
    - 事故原因区分
    - 再発防止措置
    - 品目

    Params
    ------
    product: str
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
    data = df[df[targetCol] == product].loc[
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
        f"data/output/extracted_data/{product}_extracted.csv",
        encoding=encoding,
        index_label="No",
    )


def main():
    for product in tqdm.tqdm(products):
        extractData(product=product)
    for col in tqdm.tqdm(cols):
        freqAnalysis(col=col)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"DONE in {time.time() - start_time} sec")
