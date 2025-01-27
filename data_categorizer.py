import pandas as pd
import settings as st


def identify_category(data: pd.DataFrame) -> list[str]:
    """
    読み込んだ製品事故のデータから「被害の種類」を抽出して、カテゴリ作成
    """
    result = []
    for value in data.loc[:, "被害の種類"]:
        if value not in result:
            result.append(value)
    # print(result)

    another = []
    for res in result:
        value = res.split(":")
        if value is not str:
            for val in value:
                temp = val.split(".")
                if temp[1] not in another:
                    another.append(temp[1])
        else:
            temp = value.split(".")
            if temp[1] not in another:
                another.append(temp[1])
    # print(another)

    return another


def count_category(data: pd.DataFrame, categories: list[str]) -> None:
    """
    引数で指定されたデータフレームについて、カテゴリの数をカウント
    """
    result = {}
    for value in data.loc[:, "被害の種類"]:
        for category in categories:
            if category in value:
                if category not in result.keys():
                    result[category] = 0
                result[category] += 1
    print(result)


def export_cat_bin(data: pd.DataFrame, categories: list[str]) -> pd.DataFrame:
    new = pd.DataFrame(columns=categories)
    for i in range(0, data.loc[:, "被害の種類"].__len__()):
        for cat in categories:
            if cat in data.loc[i, "被害の種類"]:
                new.loc[i, cat] = 1
            else:
                new.loc[i, cat] = 0
    return new


if __name__ == "__main__":
    for product in st.products_250115:
        data = pd.read_csv(
            f"data/output/extracted_data/{st.category}_{product}_extracted.csv",
            encoding="utf-8-sig",
        )
        cat = identify_category(data=data)
        print(f"{product}")
        count_category(data=data, categories=cat)
        new = export_cat_bin(data=data, categories=cat)
        new.to_csv(
            f"data/output/inc_categorized/{product}_inc_cat.csv",
            encoding="utf-8-sig",
            index=False,
        )
    print("Done!")
