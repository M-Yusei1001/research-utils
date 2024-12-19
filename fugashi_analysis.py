from fugashi import Tagger
import jdepp
import settings


def text_analysis(text: str, output_filename: str) -> None:
    """
    入力された文章を形態素解析、係り受け解析する。

    params
    ------
    text: string
    output_filename: string

    出力ファイルは.dot形式。
    data/output/dot直下に保存される。
    """

    jdepp_model_path = "model/knbc"

    tagger = Tagger("-Owakati")
    # result = tagger.parse(text)

    parser = jdepp.Jdepp()
    parser.load_model(jdepp_model_path)

    # fugashiの出力をMeCabと同じ形式に整える
    tagged_text = []
    for word in tagger(text):
        # print(word, word.feature.lemma, word.pos, sep="\t")
        f = word.feature
        formatted = "{}\t{},{},{},{},{},{},{}".format(
            word.surface,
            f.pos1,
            f.pos2,
            f.cType,
            f.cForm,
            f.lemma,
            f.kana,
            f.pron,
        )
        tagged_text.append(formatted)
    tagged_text.append("EOS\n")

    sent = parser.parse_from_postagged("\n".join(tagged_text))
    print(jdepp.to_tree(str(sent)))

    with open(
        f"data/output/dot/{output_filename}.dot", mode="w", encoding=settings.encoding
    ) as f:
        f.write(str(jdepp.to_dot(str(sent))))


if __name__ == "__main__":
    text = "カセットこんろの五徳付プレートを洗っていたところ、指が切れ、第一関節裏側を2針縫った。"
    output_filename = "graph"
    text_analysis(text=text, output_filename=output_filename)
