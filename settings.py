# global settings
encoding = "utf_8_sig"

data_path = {
    "A-B": ["J20241017103313.csv", "cat_AB_data_processed.csv"],
    "E": ["J20241118145808.csv", "cat_E_data_processed.csv"],
    "ALL": ["J20241121151249.csv", "all_cat_processed.csv"],
    "ALL_250115": ["J20250115134912.csv", "250115_processed.csv"],
}

category = "ALL_250115"

products = [
    "電気スタンド",
    "扇風機",
    "電気ポット",
    "加湿器",
    "電気オーブントースター",
    "乾電池",
    "配線器具",
    "玩具",
    "脚立",
    "シュレッダー",
]

products_test = [
    "ミキサー",
    "カセットこんろ",
    "ヘアアイロン",
]

products_250115 = [
    "電気オーブントースター",
    "乾電池",
    "扇風機",
    "玩具",
    "脚立",
    "シュレッダー",
]


# process.py
cols = ["事故原因区分", "被害の種類", "品名", "品目"]

# mecab_analysis.py
word_class = ["名詞", "形容詞", "動詞"]

danger_states = [
    "溶融",
    "発煙",
    "焼損",
    "異音",
    "異臭",
    "破損",
    "発火",
    "火花",
    "破裂",
    "煙",
    "焦げ臭い",
    "出火",
    "破片",
    "火",
    "変色",
    "変形",
    "熱",
    "破裂音",
    "飛散",
    "炎",
    "点滅",
    "発熱",
    "充満",
    "感電",
    "損傷",
    "溶解",
    "汚損",
    "切断",
    "発光",
    "破断",
]

danger_actions = []

injures = ["傷", "裂傷", "軽傷", "火傷", "痛く"]
