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
    syn_dic = {"A": ["B", "C"]}

    data = pd.read_csv("data/test/test_dataset.csv", encoding="utf-8-sig")

    data_cols = data.columns
    for key in syn_dic.keys():
        for value in syn_dic[key]:
            if value in data_cols:
                data[key] = data[key] | data[value]
                data = data.drop(value, axis=1)

    data.to_csv("data/test/test_dataset_marged.csv", encoding="utf-8-sig", index=False)


if __name__ == "__main__":
    print(st.syn_dic["割れ"])
