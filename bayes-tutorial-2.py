import japanize_matplotlib.japanize_matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import pymc as pm
import pytensor as pt
import arviz as az

pt.config.cxx = ""

df = sns.load_dataset("iris")
df1 = df.query('species == "setosa"')


def main():
    # 観測値Xを定義
    # Xはsetosaのsepal_lengthになる
    s1 = df1["sepal_length"]
    X = s1.values

    # Xの確率分布モデルを定義
    model1 = pm.Model()
    with model1:
        mu = pm.Normal("mu", mu=0.0, sigma=10.0)
        sigma = pm.HalfNormal("sigma", sigma=10.0)

        # Xが平均mu, 標準偏差sigmaの正規分布に従うとする
        X_obs = pm.Normal("X_obs", mu=mu, sigma=sigma, observed=X)

        # 確率モデルの定義を描画
        g = pm.model_to_graphviz(model1)
        g.render(outfile="./data/output/bayes_t2_model1.png")

        # サンプリング
        # 事前分布を大量に生成する
        idata1 = pm.sample(random_seed=42)
        az.plot_trace(idata1, compact=False)
        az.plot_posterior(idata1)

        # サンプリング結果の統計分析
        summary1 = az.summary(idata1)
        print(summary1)

        # 推論結果を抽出
        mu_mean1 = summary1.loc["mu", "mean"]
        sigma_mean1 = summary1.loc["sigma", "mean"]

        # 結果とモデルを比較
        x_min = X.min()
        x_max = X.max()
        x_list = np.arange(x_min, x_max, 0.01)
        y_list = norm(x_list, mu_mean1, sigma_mean1)

        delta = 0.2
        bins = np.arange(4.0, 6.0, delta)
        fig, ax = plt.subplots()
        sns.histplot(
            df1, ax=ax, x="sepal_length", bins=bins, kde=True, stat="probability"
        )
        ax.get_lines()[0].set_label("KDE曲線")
        ax.plot(x_list, y_list * delta, c="b", label="ベイズ推論結果")
        ax.set_title("ベイズ推論結果とKDE曲線の比較")

        plt.tight_layout()
        japanize_matplotlib.japanize()
        plt.show()


def preCheck():
    print(df.head())
    print(df["species"].value_counts())

    bins = np.arange(4.0, 6.2, 0.2)

    japanize_matplotlib.japanize()
    sns.histplot(df1, x="sepal_length", bins=bins, kde=True)
    plt.grid()
    plt.xticks(bins)
    plt.show()


def norm(x, mu, sigma):
    y = (x - mu) / sigma
    a = np.exp(-(y**2) / 2)
    b = np.sqrt(2 * np.pi) * sigma
    return a / b


if __name__ == "__main__":
    main()
