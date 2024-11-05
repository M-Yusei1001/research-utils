import MeCab

wordClass = ["名詞", "動詞", "形容詞"]


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

        if pos in wordClass:
            terms.append(term)

        node = node.next

    return terms


def main():
    text = "エアコン室内機から爆発音がして発煙し、前面パネル内で出火した。"
    result = extractWords(text)
    print(result)


if __name__ == "__main__":
    main()
