import pandas as pd


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


if __name__ == "__main__":
    patterns()
