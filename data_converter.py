import pandas as pd
import settings as st
import tqdm


# プロンプト用にデータを加工
def main(product: str) -> None:
    data = pd.read_csv(
        f"data/output/extracted_data/{st.category}_{product}_extracted.csv",
        encoding="utf-8-sig",
    )
    data = data.drop(columns=["被害の種類", "事故原因区分", "再発防止措置", "品目"])
    data.to_csv(
        f"data/output/gemini/prompt_data/{product}.csv",
        index=False,
        encoding="utf-8-sig",
    )


def data_250130(product: str) -> None:
    data = pd.read_csv(
        f"data/output/extracted_data/{st.category}_{product}_extracted.csv",
        encoding="utf-8-sig",
    )
    data = data.drop(columns=["事故通知内容", "再発防止措置", "品目"])
    data.to_csv(
        f"data/output/gemini/prompt_data_250130/{product}_prompt.csv",
        index=False,
        encoding="utf-8-sig",
    )


if __name__ == "__main__":
    for product in tqdm.tqdm(st.products_250115):
        main(product)
        data_250130(product)
    print("Done!")
