import MeCab
import pandas as pd
import tqdm
from process import products
import time

word_class = ["名詞", "形容詞"]
encoding = "utf_8_sig"


def extractDescription(product: str) -> list[str]:
    """
    すべての事故通知内容から、word_class で指定した品詞の単語をリストとして取り出す

    Params
    ------
    product: str
    品名

    Returns
    -------
    extracted_words: list[str]
    指定した品詞の単語からなるリスト
    """

    target_col = "事故通知内容"

    with open(
        f"data/output/extracted_data/{product}_extracted.csv",
        "r",
        encoding=encoding,
    ) as file:
        df = pd.read_csv(file)
        descriptions = [extractWords(description) for description in df[target_col]]
        extracted_words = [word for description in descriptions for word in description]

        return extracted_words


def extractWords(text: str) -> list[str]:
    """
    形態素解析をする

    Params
    ------
    text: str

    Returns
    -------
    terms: list[str]
    """
    mecab = MeCab.Tagger("")
    mecab.parse("")
    node = mecab.parseToNode(text)
    terms = []

    while node:
        # 単語を抽出
        term = node.surface
        # 品詞を抽出
        pos = node.feature.split(",")[0]

        if pos in word_class:
            terms.append(term)

        node = node.next

    return terms


def main(product: str):
    df = pd.DataFrame(extractDescription(product))
    freq = df.value_counts()
    freq.to_csv(
        f"data/output/words_freq_data/words_freq_{product}.csv", encoding=encoding
    )


if __name__ == "__main__":
    start_time = time.time()
    for product in tqdm.tqdm(products):
        main(product)
    print(f"Done in {time.time() - start_time} sec")
