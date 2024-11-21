import pandas as pd
import csv
import time
import tqdm
import settings as st
from reader import toRegExp


def freqShow(output_filename: str):
    with open(f"data/output/{output_filename}", "r", encoding=st.encoding) as file:
        df = pd.read_csv(file)

        df.plot(kind="bar")
        plt.title(f"{output_filename}")
        plt.xlabel("組み合わせ")
        plt.ylabel("出現回数")
        plt.show()


def freqAnalysis(col: str, second_col: str = "") -> None:
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
    with open(
        f"data/output/{st.data_path[st.category][1]}", "r", encoding=st.encoding
    ) as file:
        reader = csv.reader(file)

        # 読み込んだデータを2次元配列に変換、整形
        l = [[toRegExp(elem) for elem in row] for row in reader]

    # データをpandasで扱える配列に変換
    cols = l.pop(0)
    df = pd.DataFrame(l, columns=cols)

    # 出現頻度
    if second_col != "":
        frequency = df.groupby([col, second_col]).size().sort_values(ascending=False)
        frequency.to_csv(
            f"data/output/frequency_data/{st.category}_frequency_{col}_and_{second_col}.csv",
            encoding=st.encoding,
            index_label="selected_col",
        )
    else:
        frequency = df[col].value_counts()
        frequency.to_csv(
            f"data/output/frequency_data/{st.category}_frequency_{col}.csv",
            encoding=st.encoding,
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
    with open(
        f"data/output/{st.data_path[st.category][1]}", "r", encoding=st.encoding
    ) as file:
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
        f"data/output/extracted_data/{st.category}_{product}_extracted.csv",
        encoding=st.encoding,
        index_label="No",
    )


def main():
    for product in tqdm.tqdm(st.products):
        extractData(product=product)
    for col in tqdm.tqdm(st.cols):
        freqAnalysis(col=col)
    freqAnalysis("品名", "品目")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"DONE in {time.time() - start_time} sec")
    # freqShow("frequency_data/A-B_frequency_品名_and_品目.csv")
