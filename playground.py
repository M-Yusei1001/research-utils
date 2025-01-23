import pandas as pd
import settings as st


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
    syn_dic = {"D": ["A", "B", "C"]}

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


if __name__ == "__main__":
    dropper()
