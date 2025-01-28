# 「事故の内容」を「被害の種類」から集計したバイナリデータを出力する

import pandas as pd
import settings as st
import tqdm
import datetime
from syndic import syn_dic
import unicodedata
import logging
import time

logger = logging.getLogger(__name__)

# 生成するファイル名に含まれる今日の日付
date_now = datetime.datetime.now().strftime("%Y%m%d")


# ログファイル名に含まれる今日の日付
def localtime_to_str():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


logging.basicConfig(
    filename=f"data/output/inc_categorized/log/{localtime_to_str()}.log",
    encoding="utf-8",
    level=logging.DEBUG,
)

# 読み込むファイル名に含まれる日付
date = 20250123

# 読み込むファイルが存在するディレクトリの日付
# マージ前データ、ブラックリスト作成用データのディレクトリ
dir_index = "20250123_001"

output_dir = st.create_dir(base_dir="data/output/inc_categorized/marged")


states_and_causes_cmn_cols = []
states_and_incidents_cmn_cols = []
causes_and_incidents_cmn_cols = []


def marge_status_and_cause(states: pd.DataFrame, causes: pd.DataFrame) -> pd.DataFrame:
    """
    2つのデータフレームをマージ

    Args:
        status (pd.DataFrame): 製品の性質のデータフレーム
        cause (pd.DataFrame): 事故原因のデータフレーム
    """
    # statesの行数をcausesに合わせる
    if len(states) < len(causes):
        repeats = len(causes) // len(states) + 1
        states = pd.concat([states] * repeats, ignore_index=True)

    return pd.merge(
        states,
        causes,
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["", "_C"],
    )


def marge_with_incident(data: pd.DataFrame, incidents: pd.DataFrame) -> pd.DataFrame:
    """
    2つのデータフレームをマージ

    Args:
        data (pd.DataFrame): マージ先のデータフレーム
        incident (pd.DataFrame): 事故内容のデータフレーム
    """

    return pd.merge(
        data,
        incidents,
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["", "_I"],
    )


def check_syn(df: pd.DataFrame) -> pd.DataFrame:
    """
    類義語辞書に登録した類似表現を統一する。
    """
    # Unicode統一処理
    cols = df.columns
    for col in cols:
        renamed_col = unicodedata.normalize("NFKC", col)
        df.rename(columns={col: renamed_col}, inplace=True)

    # 類似表現の結合
    cols = df.columns

    for col in cols:
        for key in syn_dic.keys():
            key = unicodedata.normalize("NFKC", key)
            if type(syn_dic[key]) is str and col == syn_dic[key]:
                if key not in df.columns:
                    df[key] = 0
                df[key] = df[key] | df[col]
                df.drop(col, axis=1, inplace=True)
                # print(f"key: {key}, col: {col}")
            elif type(syn_dic[key]) is not str:
                for value in syn_dic[key]:
                    # print(f"value: {value}, col: {col}")
                    if col == value:
                        if key not in df.columns:
                            df[key] = 0
                        df[key] = df[key] | df[col]
                        df.drop(col, axis=1, inplace=True)
                        # print(f"key: {key}, col: {col}")

    return df


def check_duplicated(
    df1: pd.DataFrame, df2: pd.DataFrame, checkList: list[str]
) -> None:
    """
    df1とdf2の同じカラム名をcheckListに記録する。
    """
    for column in df1.columns.intersection(df2.columns):
        if column in checkList:
            continue
        checkList.append(column)


def main():
    """
    DataFrameを結合する。
    結合する際に類似表現を統一し、ブラックリスト用にカラム名を記録する。
    """
    # 結合するproductのDataFrameを格納する配列
    marged_df = []
    # DataFrameの一時保存用
    temp_states_df = {}
    temp_causes_df = {}
    temp_incidents_df = {}
    # ブラックリスト用のカラム名を格納する配列
    states_cols = []
    causes_cols = []
    incidents_cols = []

    # 前処理
    # 類似表現の統一
    for product in tqdm.tqdm(st.products_250115):
        states_df = pd.read_csv(
            "data/src/250115_products_states.csv", encoding="utf-8-sig"
        )
        causes_df = pd.read_csv(
            f"data/output/gemini/binary/{dir_index}/{product}_{date}_cause_bin.csv",
            encoding="utf-8-sig",
        )
        incidents_df = pd.read_csv(
            f"data/output/inc_categorized/{product}_inc_cat.csv",
            encoding="utf-8-sig",
        )

        states_df = states_df[states_df.loc[:, "product"] == product]
        states_df = states_df.drop(columns=["product"])
        causes_df = check_syn(df=causes_df)
        incidents_df = check_syn(df=incidents_df)

        temp_states_df[product] = states_df
        temp_causes_df[product] = causes_df
        temp_incidents_df[product] = incidents_df

    # 完全一致表現のカウント
    for product_1 in tqdm.tqdm(st.products_250115):
        for product_2 in tqdm.tqdm(st.products_250115):
            check_duplicated(
                df1=temp_states_df[product_1],
                df2=temp_causes_df[product_2],
                checkList=states_and_causes_cmn_cols,
            )
            check_duplicated(
                df1=temp_states_df[product_1],
                df2=temp_incidents_df[product_2],
                checkList=states_and_incidents_cmn_cols,
            )
            check_duplicated(
                df1=temp_causes_df[product_1],
                df2=temp_incidents_df[product_2],
                checkList=causes_and_incidents_cmn_cols,
            )

    # 全カラム名にサフィックス付け
    for product in tqdm.tqdm(st.products_250115):
        states_df = temp_states_df[product]
        causes_df = temp_causes_df[product]
        incidents_df = temp_incidents_df[product]

        for col in states_df.columns:
            states_df = states_df.rename(columns={col: f"{col}_S"})
        for col in causes_df.columns:
            causes_df = causes_df.rename(columns={col: f"{col}_C"})
        for col in incidents_df.columns:
            incidents_df = incidents_df.rename(columns={col: f"{col}_I"})

        temp_states_df[product] = states_df
        temp_causes_df[product] = causes_df
        temp_incidents_df[product] = incidents_df

    # 結合処理とブラックリストの作成
    for product in tqdm.tqdm(st.products_250115):
        states_df = temp_states_df[product]
        causes_df = temp_causes_df[product]
        incidents_df = temp_incidents_df[product]

        # 「製品の特性」を記録
        states_new_cols = list(set(states_df.columns) - set(states_cols))
        for col in states_new_cols:
            if col not in states_cols:
                states_cols.append(col)
        # print(states_cols)

        # 「事故の原因」を記録
        causes_new_cols = list(set(causes_df.columns) - set(causes_cols))
        # 特殊表現の置換
        for col in causes_new_cols:
            if col == "2人乗り":
                col = "二人乗り"
            # causes_colsに既に含まれていないことを確認して、追加する
            if col not in causes_cols:
                causes_cols.append(col)
        # print(causes_cols)

        # 「事故の内容」を記録
        incidents_new_columns = list(set(incidents_df.columns) - set(incidents_cols))
        # 特殊表現の置換
        for col in incidents_new_columns:
            # all_incidentsに既に含まれていないことを確認して、追加する
            if col not in incidents_cols:
                incidents_cols.append(col)
        # print(incidents_cols)

        # productごとの結合処理
        marged = marge_status_and_cause(states=states_df, causes=causes_df)
        marged = marge_with_incident(data=marged, incidents=incidents_df)
        marged.fillna(0, inplace=True)
        marged = marged.astype(int)
        marged_df.append(marged)

    marged_all_data = pd.DataFrame()
    for df in marged_df:
        if marged_all_data.empty:
            marged_all_data = df
            continue
        marged_all_data = pd.concat([marged_all_data, df])

    marged_all_data.fillna(0, inplace=True)
    marged_all_data = marged_all_data.astype(int)
    marged_all_data.rename(columns={"2人乗り": "二人乗り"}, inplace=True)
    marged_all_data = marged_all_data.reset_index(drop=True)

    # 出現回数が指定した回数より少ない列は削除する
    cols = marged_all_data.columns
    deleted = []
    for col in cols:
        if marged_all_data[col].sum() <= 3:
            marged_all_data = marged_all_data.drop(columns=[col])
            deleted.append(col)
            for states_col in states_cols:
                if col == states_col:
                    states_cols.remove(col)
            for causes_col in causes_cols:
                if col == causes_col:
                    causes_cols.remove(col)
            for incidents_col in incidents_cols:
                if col == incidents_col:
                    incidents_cols.remove(col)
    print(f"Deleted: {deleted}")
    logger.info(f"Deleted columns: {deleted}")

    # 指定した列の合計が0の行は削除する
    target_row = []
    for i in range(0, len(marged_all_data)):
        if not (marged_all_data.iloc[i, :][causes_cols].sum().all()):
            target_row.append(i)
            continue
        if not (marged_all_data.iloc[i, :][incidents_cols].sum().all()):
            target_row.append(i)
    print(target_row)
    logger.info(f"Deleted row: {target_row}")
    for row in target_row:
        marged_all_data = marged_all_data.drop(axis=0, index=row)

    # 完全一致表現の二重チェック
    same_exp = []
    count = 0
    for cause in causes_cols:
        for incident in incidents_cols:
            if cause == incident:
                count += 1
                same_exp.append(cause)
    if count > 0:
        print(f"There are (is) {count} same expressions between cause and incident")
        logger.info(
            f"There are (is) {count} same expressions between cause and incident"
        )

    count = 0
    for state in states_cols:
        for incident in incidents_cols:
            if state == incident:
                count += 1
                same_exp.append(incident)
    if count > 0:
        print(f"There are (is) {count} same expressions between state and incident")
        logger.info(
            f"There are (is) {count} same expressions between state and incident"
        )

    count = 0
    for state in states_cols:
        for cause in causes_cols:
            if cause == state:
                count += 1
                same_exp.append(state)
    if count > 0:
        print(f"There are (is) {count} same expressions between state and cause")
        logger.info(f"There are (is) {count} same expressions between state and cause")
    if same_exp:
        print(f"Same exp: {same_exp}")
        logger.info(f"Same exp: {same_exp}")

    # アークの向き設定用のデータを作成
    arcs_from = []
    arcs_to = []
    for state in states_cols:
        for cause in causes_cols:
            arcs_from.append(state)
            arcs_to.append(cause)
    arcs_s2c = pd.DataFrame({"from": arcs_from, "to": arcs_to})
    arcs_from = []
    arcs_to = []
    for cause in causes_cols:
        for incident in incidents_cols:
            arcs_from.append(cause)
            arcs_to.append(incident)
    arcs_c2i = pd.DataFrame({"from": arcs_from, "to": arcs_to})

    # 書き出し
    arcs_s2c.to_csv(
        f"{output_dir}/data_arcs_s2c_{date_now}_cat.csv",
        index=False,
        encoding="utf-8-sig",
    )

    arcs_c2i.to_csv(
        f"{output_dir}/data_arcs_c2i_{date_now}_cat.csv",
        index=False,
        encoding="utf-8-sig",
    )

    marged_all_data.to_csv(
        f"{output_dir}/data_products_{date_now}_cat.csv",
        index=False,
        encoding="utf-8-sig",
    )

    states_cols = pd.Series(states_cols, name="states")
    states_cols.to_csv(
        f"{output_dir}/data_states_{date_now}_cat.csv",
        index=False,
        encoding="utf-8-sig",
    )

    causes_cols = pd.Series(causes_cols, name="causes")
    causes_cols.to_csv(
        f"{output_dir}/data_causes_{date_now}_cat.csv",
        index=False,
        encoding="utf-8-sig",
    )

    incidents_cols = pd.Series(incidents_cols, name="incidents")
    incidents_cols.to_csv(
        f"{output_dir}/data_incidents_{date_now}_cat.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(
        f"states: {len(states_cols)}, causes: {len(causes_cols)}, incidents: {len(incidents_cols)}, arcs: {len(arcs_s2c) + len(arcs_c2i)}"
    )
    logger.info(
        f"states: {len(states_cols)}, causes: {len(causes_cols)}, incidents: {len(incidents_cols)}, arcs: {len(arcs_s2c) + len(arcs_c2i)}"
    )
    print(f"All data: {len(marged_all_data)}")
    logger.info(f"All data: {len(marged_all_data)}")


if __name__ == "__main__":
    main()
    print("Done!")
