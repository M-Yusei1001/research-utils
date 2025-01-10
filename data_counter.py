import pandas as pd
import settings as st


def data_counter(data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    データフレームからcsvバイナリデータを作成
    """
    new_data = pd.DataFrame()

    # 事故通知内容のカラムを作成
    for i in range(0, data.__len__()):
        data_columns = data[column_name][i].split()
        # print(f"data_column: {data_columns}")
        new_column = list(set(data_columns) - set(new_data.columns))
        for j in new_column:
            new_data[j] = 0

    # カウント
    for i in range(0, data.__len__()):
        data_columns = data[column_name][i].split()
        for column in new_data.columns:
            if column in data_columns:
                new_data.loc[i, column] = 1
            else:
                new_data.loc[i, column] = 0

    # print(f"new_column: {new_data.columns}")
    print(new_data.head())
    return new_data


if __name__ == "__main__":
    # 事故通知内容のバイナリデータを作成
    for product in st.products_test:
        data = pd.read_csv(
            f"data/output/gemini/responses/{product}_res.csv", encoding="utf-8-sig"
        )
        data_counter(
            data=data,
            column_name="事故通知内容",
        ).to_csv(
            f"data/output/gemini/binary/{product}_incident_bin.csv",
            encoding="utf-8-sig",
            index=False,
        )
        print("Done!")

    # 事故原因のバイナリデータを作成
    for product in st.products_test:
        data = pd.read_csv(
            f"data/output/gemini/responses/{product}_res.csv", encoding="utf-8-sig"
        )
        data_counter(
            data=data,
            column_name="事故原因",
        ).to_csv(
            f"data/output/gemini/binary/{product}_cause_bin.csv",
            encoding="utf-8-sig",
            index=False,
        )
        print("Done!")
