import pandas as pd
import settings as st
import tqdm
import datetime
from syndic import syn_dic
import unicodedata

date_now = datetime.datetime.now().strftime("%Y%m%d")
date = 20250122

cause_common_columns = []
incident_common_columns = []


def marge_status_and_cause(states: pd.DataFrame, cause: pd.DataFrame) -> pd.DataFrame:
    """
    2つのデータフレームをマージ

    Args:
        status (pd.DataFrame): 製品の性質のデータフレーム
        cause (pd.DataFrame): 事故原因のデータフレーム
    """
    # statesの方がcauseよりも行数が少ない場合、statesの行数をcauseに合わせる
    if len(states) < len(cause):
        repeats = len(cause) // len(states) + 1
        states = pd.concat([states] * repeats, ignore_index=True)
    cols = cause.columns.intersection(states.columns)

    for column in cols:
        if column in cause_common_columns:
            continue
        cause_common_columns.append(column)

    return pd.merge(
        states,
        cause,
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["", "_cause"],
    )


def marge_with_incident(data: pd.DataFrame, incident: pd.DataFrame) -> pd.DataFrame:
    """
    2つのデータフレームをマージ

    Args:
        data (pd.DataFrame): マージ先のデータフレーム
        incident (pd.DataFrame): 事故内容のデータフレーム
    """
    # dataの方がincidentよりも行数が少ない場合、dataの行数をincidentに合わせる
    if len(data) < len(incident):
        repeats = len(incident) // len(data) + 1
        data = pd.concat([data] * repeats, ignore_index=True)
    cols = incident.columns.intersection(data.columns)

    for column in cols:
        if column in incident_common_columns:
            continue
        incident_common_columns.append(column)

    return pd.merge(
        data,
        incident,
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["", "_incident"],
    )


def make_blacklist():
    all_states = (
        pd.read_csv("data/src/250115_products_states.csv", encoding="utf-8-sig")
        .drop(columns="product")
        .columns
    )
    # print(all_states)

    all_causes = []
    for product in tqdm.tqdm(st.products_250115):
        new_column = list(
            set(
                pd.read_csv(
                    f"data/output/gemini/binary/{product}_{date}_cause_bin.csv",
                    encoding="utf-8-sig",
                ).columns
            )
            - set(all_causes)
        )

        for col in new_column:
            if col == "2人乗り":
                col = "二人乗り"
            if col in cause_common_columns:
                col = f"{col}_cause"
                if col not in all_causes:
                    all_causes.append(col)
            else:
                all_causes.append(col)

    for cause in all_causes:
        for key in syn_dic.keys():
            for value in syn_dic[key]:
                if value in all_causes:
                    all_causes.remove(value)

    # print(all_causes)

    all_incidents = []
    for product in tqdm.tqdm(st.products_250115):
        new_column = list(
            set(
                pd.read_csv(
                    f"data/output/gemini/binary/{product}_{date}_incident_bin.csv",
                    encoding="utf-8-sig",
                ).columns
            )
            - set(all_incidents)
        )

        for col in new_column:
            if col in incident_common_columns:
                col = f"{col}_incident"
                if col not in all_incidents:
                    all_incidents.append(col)
            else:
                all_incidents.append(col)

    # print(all_incidents)

    all_states = pd.Series(all_states, name="states")
    all_states.to_csv(
        f"data/output/gemini/marged/data_all_states_{date_now}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    all_causes = pd.Series(all_causes, name="causes")
    all_causes.to_csv(
        f"data/output/gemini/marged/data_all_causes_{date_now}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    all_incidents = pd.Series(all_incidents, name="incidents")
    all_incidents.to_csv(
        f"data/output/gemini/marged/data_all_incidents_{date_now}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(
        f"states: {len(all_states)}, causes: {len(all_causes)}, incidents: {len(all_incidents)}"
    )


def main():
    for product in tqdm.tqdm(st.products_250115):
        states = pd.read_csv(
            "data/src/250115_products_states.csv", encoding="utf-8-sig"
        )
        states = states[states["product"] == product].drop(columns=["product"])
        marged = marge_status_and_cause(
            states,
            pd.read_csv(
                f"data/output/gemini/binary/{product}_{date}_cause_bin.csv",
                encoding="utf-8-sig",
            ),
        )
        marged = marge_with_incident(
            marged,
            pd.read_csv(
                f"data/output/gemini/binary/{product}_{date}_incident_bin.csv",
                encoding="utf-8-sig",
            ),
        )
        marged.fillna(0, inplace=True)
        marged = marged.astype(int)
        # 類似表現の結合
        cols = marged.columns
        for key in syn_dic.keys():
            for value in syn_dic[key]:
                if value in cols:
                    marged[key] = marged[key] | marged[value]
                    marged = marged.drop(value, axis=1)

        marged.to_csv(
            f"data/output/gemini/marged/{product}_{date_now}.csv",
            index=False,
            encoding="utf-8-sig",
        )

    marged_all_data = pd.DataFrame()
    for product in tqdm.tqdm(st.products_250115):
        data = pd.read_csv(
            f"data/output/gemini/marged/{product}_{date}.csv", encoding="utf-8-sig"
        )
        if marged_all_data.empty:
            marged_all_data = data
            continue
        marged_all_data = pd.concat([marged_all_data, data], ignore_index=True)

    marged_all_data.fillna(0, inplace=True)
    marged_all_data.rename(columns={"2人乗り": "二人乗り"}, inplace=True)
    marged_all_data.to_csv(
        f"data/output/gemini/marged/data_products_{date_now}.csv",
        index=False,
        encoding="utf-8-sig",
    )


if __name__ == "__main__":
    main()
    make_blacklist()
    print("Done!")
