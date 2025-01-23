import pandas as pd
import settings as st
import tqdm
import datetime

date_now = datetime.datetime.now().strftime("%Y%m%d")
output_dir = st.create_dir("data/output/gemini/binary")
dir_index = "20250115"


def data_counter(data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    データフレームからcsvバイナリデータを作成

    Args:
        data (pd.DataFrame): 読み込んだcsvのデータフレーム
        column_name (str): カウントするデータ（事故通知内容 or 事故原因）

    """
    # カラムを作成
    new_columns = []
    for i in range(0, data.__len__()):
        data_columns = data[column_name][i].split()
        # print(f"data_column: {data_columns}")
        extend = list(set(data_columns) - set(new_columns))
        new_columns.extend(extend)

    new_data = pd.DataFrame(columns=new_columns)

    # カウント
    for i in range(0, data.__len__()):
        data_columns = data[column_name][i].split()
        for column in new_data.columns:
            if column in data_columns:
                new_data.loc[i, column] = 1
            else:
                new_data.loc[i, column] = 0

    # print(new_data.head())
    return new_data


def main():
    # 事故通知内容のバイナリデータを作成
    for product in tqdm.tqdm(st.products_250115):
        data = pd.read_csv(
            f"data/output/gemini/responses/{dir_index}/{product}_res.csv",
            encoding="utf-8-sig",
        )
        data_counter(
            data=data,
            column_name="事故通知内容",
        ).to_csv(
            f"{output_dir}/{product}_{date_now}_incident_bin.csv",
            encoding="utf-8-sig",
            index=False,
        )

    # 事故原因のバイナリデータを作成
    for product in tqdm.tqdm(st.products_250115):
        data = pd.read_csv(
            f"data/output/gemini/responses/{dir_index}/{product}_res.csv",
            encoding="utf-8-sig",
        )
        data_counter(
            data=data,
            column_name="事故原因",
        ).to_csv(
            f"{output_dir}/{product}_{date_now}_cause_bin.csv",
            encoding="utf-8-sig",
            index=False,
        )


if __name__ == "__main__":
    main()
    print("Done!")
