import MeCab
import pandas as pd
import tqdm
import time
import settings as st


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
        f"data/output/extracted_data/{st.category}_{product}_extracted.csv",
        "r",
        encoding=st.encoding,
    ) as file:
        df = pd.read_csv(file)

        # 1つの事故通知内容から抽出した単語のリストを作成
        descriptions = [extractWords(description) for description in df[target_col]]

        # すべてのリストを1つにまとめる
        extracted_words = [word for description in descriptions for word in description]

        return extracted_words


def extractWords(text: str) -> list[str]:
    """
    形態素解析をする。
    settings.py で指定した word_class の品詞に該当する単語を抽出する。

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

        if pos in st.word_class:
            terms.append(term)

        node = node.next

    return terms


def main():
    for product in tqdm.tqdm(st.products_test):
        df = pd.DataFrame(extractDescription(product))
        freq = df.value_counts()
        freq[freq >= 3].to_csv(
            f"data/output/words_freq_data/{st.category}_{product}_words_freq.csv",
            encoding=st.encoding,
            index_label="単語",
        )


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"DONE in {time.time() - start_time} sec")
