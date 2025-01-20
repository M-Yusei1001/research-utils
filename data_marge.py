import pandas as pd
import settings as st
import tqdm


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
    common_columns = states.columns.intersection(cause.columns)
    # statesとcauseの共通カラムを削除。statesを優先する。
    cause = cause.drop(columns=common_columns)
    return pd.merge(states, cause, how="left", left_index=True, right_index=True)


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
    common_columns = data.columns.intersection(incident.columns)
    # dataとincidentの共通カラムを削除。dataを優先する。
    incident = incident.drop(columns=common_columns)
    return pd.merge(data, incident, how="left", left_index=True, right_index=True)


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
                    f"data/output/gemini/binary/{product}_cause_bin.csv",
                    encoding="utf-8-sig",
                ).columns
            )
            - set(all_causes)
        )
        all_causes.extend(new_column)
    # print(all_causes)
    all_incidents = []
    for product in tqdm.tqdm(st.products_250115):
        new_column = list(
            set(
                pd.read_csv(
                    f"data/output/gemini/binary/{product}_incident_bin.csv",
                    encoding="utf-8-sig",
                ).columns
            )
            - set(all_incidents)
        )
        all_incidents.extend(new_column)
    # print(all_incidents)
    blacklist = pd.DataFrame(columns=["from", "to"])
    index = 0
    for incident in tqdm.tqdm(all_incidents):
        for cause in all_causes:
            blacklist.loc[index] = [incident, cause]
            index += 1
    for cause in tqdm.tqdm(all_causes):
        for state in all_states:
            blacklist.loc[index] = [cause, state]
            index += 1
    for state in tqdm.tqdm(all_states):
        for incident in all_incidents:
            blacklist.loc[index] = [state, incident]
            index += 1
    for incident in tqdm.tqdm(all_incidents):
        for state in all_states:
            blacklist.loc[index] = [incident, state]
            index += 1
    blacklist.to_csv(
        "data/output/gemini/marged/blacklist.csv", index=False, encoding="utf-8-sig"
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
                f"data/output/gemini/binary/{product}_cause_bin.csv",
                encoding="utf-8-sig",
            ),
        )
        marged = marge_with_incident(
            marged,
            pd.read_csv(
                f"data/output/gemini/binary/{product}_incident_bin.csv",
                encoding="utf-8-sig",
            ),
        )
        marged.fillna(0, inplace=True)
        marged.to_csv(
            f"data/output/gemini/marged/{product}.csv",
            index=False,
            encoding="utf-8-sig",
        )

    marged_all_data = pd.DataFrame()
    for product in tqdm.tqdm(st.products_250115):
        data = pd.read_csv(
            f"data/output/gemini/marged/{product}.csv", encoding="utf-8-sig"
        )
        if marged_all_data.empty:
            marged_all_data = data
            continue
        marged_all_data = pd.concat([marged_all_data, data], ignore_index=True)

    marged_all_data.fillna(0, inplace=True)
    marged_all_data.to_csv(
        "data/output/gemini/marged/data_products_250115.csv",
        index=False,
        encoding="utf-8-sig",
    )


if __name__ == "__main__":
    make_blacklist()
    print("Done!")
