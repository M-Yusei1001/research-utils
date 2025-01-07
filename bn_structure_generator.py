import pandas as pd
import settings as st
import tqdm

status = [
    "高温",
    "とがっている",
    "電気",
    "機械的力",
    "火",
    "回転",
]

incident = [
    "火傷",
    "発煙",
    "異臭",
    "焼損",
    "過熱",
    "異音",
    "通電",
    "断線",
    "引火",
    "漏洩",
    "裂傷",
    "混入",
    "出火",
    "死亡",
    "爆発",
]

usage = [
    "製品に問題がある",
    "応力をかける",
    "落下させる",
    "触れる",
    "可燃物がある",
    "着火する",
    "放置する",
    "過熱する",
    "誤装着する",
    "汚す",
    "誤操作する",
    "誤使用する",
]


def make_structure() -> str:
    structure = ""
    evd_status = evidence(status)
    evd_usage = evidence(usage)

    for string in status:
        structure += "[" + string + "]"

    for string in incident:
        structure += "[" + string + "|" + evd_status + ":" + evd_usage + "]"

    for string in usage:
        structure += "[" + string + "|" + evd_status + "]"

    return structure


def evidence(evd: list[str]) -> str:
    e = ""
    for i in range(0, len(evd)):
        if i == len(evd) - 1:
            e += evd[i]
            continue
        e += evd[i] + ":"
    return e


def main():
    with open("data/output/bn_structure.txt", mode="w", encoding=st.encoding) as file:
        file.write(make_structure())


if __name__ == "__main__":
    main()
    print("DONE!")
