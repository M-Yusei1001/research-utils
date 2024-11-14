import pandas as pd
import bayes as by


def main():
    with open("data/src/badmail.csv", "r", encoding="utf_8_sig") as file:
        df = pd.read_csv(file)

        prob = [0.6]

        for row in df.itertuples():
            # ベイズ更新
            bayes = by.Bayes(row[1] * prob[0] + row[2] * (1 - prob[0]))
            prob.append(bayes.posterior_probability(row[1], prob[0]))
            prob.pop(0)

        print(round(prob[0], 5))


if __name__ == "__main__":
    main()
