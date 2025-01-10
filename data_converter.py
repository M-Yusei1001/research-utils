import pandas as pd
import settings as st
import tqdm


def main(product: str) -> None:
    data = pd.read_csv(f"data/output/extracted_data/ALL_{product}_extracted.csv")
    data = data.drop(columns=["被害の種類", "事故原因区分", "再発防止措置", "品目"])
    data.to_csv(f"data/output/gemini/prompt_data/{product}.csv", index=False)


def convert(product: str) -> None:
    data = pd.read_csv(f"data/output/gemini/prompt_data/{product}.csv")
    print(data["事故原因"][0])
    print(data["事故原因"].__len__())


if __name__ == "__main__":
    for product in tqdm.tqdm(st.products_test):
        main(product)
    print("Done!")
    convert("ミキサー")
