import pandas as pd
import settings as st

syn_dic = {"D": ["A", "B", "C"], "あ": ["かきくけこ", "うあ"]}


def patterns():
    causes = pd.read_csv(
        "data/output/gemini/marged/data_all_causes_250115.csv", encoding="utf-8-sig"
    )

    # print(causes.head())

    start = 420
    end = 423

    frm = []
    to = []
    for i in range(start, end):
        if i == causes["causes"].__len__() - 1:
            break
        for j in range(start, end):
            if j == causes["causes"].__len__() - 1:
                break
            if i == j:
                continue
            frm.append(causes["causes"][i])
            to.append(causes["causes"][j])

    output = pd.DataFrame({"from": frm, "to": to})

    print(output.head())
    output.to_csv(
        "data/output/gemini/marged/patterns.csv", encoding="utf-8-sig", index=False
    )


def checkdata():
    data = pd.read_csv(
        "data/output/gemini/marged/data_products_250115.csv", encoding="utf-8-sig"
    )
    data_cols = data.columns

    if "2人乗り" in data_cols:
        print("2人乗り is in data")


def syn_check():
    syn_dic = st.syn_dic
    for key in syn_dic.keys():
        if type(syn_dic[key]) is str:
            print(f"{syn_dic[key]} is in syn_dic")
        else:
            for value in syn_dic[key]:
                print(f"{value} is in syn_dic")


def syn_marger():
    data = pd.read_csv("data/test/test_dataset.csv", encoding="utf-8-sig")

    cols = data.columns

    try:
        for col in cols:
            for key in syn_dic.keys():
                if col in syn_dic[key]:
                    if key not in data.columns:
                        data[key] = 0
                    data[key] = data[key] | data[col]
                    data.drop(col, axis=1, inplace=True)
                    print(f"col: {col}, key: {key}")

    except Exception as e:
        print(f"Exception occured: {e}")

    data.to_csv("data/test/test_dataset_marged.csv", encoding="utf-8-sig", index=False)


def dropper():
    states_df = pd.read_csv("data/src/250115_products_states.csv", encoding="utf-8-sig")

    product = "シュレッダー"
    df = states_df[states_df.loc[:, "product"] == product]
    df = df.drop(columns=["product"])
    print(df)


def marger():
    df1 = pd.read_csv("data/test/test_marge_1.csv", encoding="utf-8-sig")
    df2 = pd.read_csv("data/test/test_marge_2.csv", encoding="utf-8-sig")
    df3 = pd.read_csv("data/test/test_marge_3.csv", encoding="utf-8-sig")
    df4 = pd.read_csv("data/test/test_marge_4.csv", encoding="utf-8-sig")

    duplicated_1 = df1.columns.intersection(df2.columns)
    duplicated_2 = df3.columns.intersection(df4.columns)

    for value in df2.columns:
        if value in duplicated_1:
            df2 = df2.rename(columns={value: f"{value}_2"})
    for value in df4.columns:
        if value in duplicated_2:
            df4 = df4.rename(columns={value: f"{value}_4"})

    df_1_and_2 = pd.merge(
        left=df1,
        right=df2,
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["", "_mg"],
    )

    df_3_and_4 = pd.merge(
        left=df3,
        right=df4,
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["", "_mg"],
    )

    df = pd.concat([df_1_and_2, df_3_and_4])
    df.fillna(0, inplace=True)
    print(df.head())
    df.to_csv("data/test/test_marge_marged.csv", encoding="utf-8-sig", index=False)


def isWordIn():
    print("ABC" in "OPPAPAABCAAAAA")


def lenOfSyndic():
    print(len(syn_dic["あ"]))


def dicTemp():
    df1 = pd.read_csv("data/test/test_marge_1.csv", encoding="utf-8-sig")
    df2 = pd.read_csv("data/test/test_marge_2.csv", encoding="utf-8-sig")
    df3 = pd.read_csv("data/test/test_marge_3.csv", encoding="utf-8-sig")
    df4 = pd.read_csv("data/test/test_marge_4.csv", encoding="utf-8-sig")

    temp = {}

    temp["df1"] = df1
    df1 = df1.drop(columns=["A"])
    temp["df1"] = df1

    print(len(temp))


def sumcols():
    df = pd.read_csv("data/test/test_marge_marged.csv", encoding="utf-8-sig")
    # print(df.iloc[1, :][["A", "B"]])
    # print(df.head())
    # df = df.drop(index=2)
    # print(df.head())
    # df.reset_index(drop=True, inplace=True)
    # print(df.head())

    count = 0
    for i in range(0, df.__len__()):
        count += 1
    print(f"count: {count}")

    count = 0
    for i in range(0, df.__len__()):
        if i % 2 == 0:
            df = df.drop(index=i)
        count += 1
        df.reset_index(drop=True, inplace=True)
        # if not i % 2 == 0:
        #     print(df.iloc[i, :][["A", "B"]])
    print(f"count: {count}")
    print(df.head())


def add_dataframe():
    data = pd.DataFrame(columns=["A", "B"])
    data.concat([0, 1])
    print(data)


if __name__ == "__main__":
    add_dataframe()
