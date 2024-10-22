import pymc as pm
import arviz as az
import pandas as pd
import pytensor as pt
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

pt.config.cxx = ""


def main():
    # 事前分布の準備
    X_pre = np.array([1, 0, 0, 1, 0])

    model1 = pm.Model()

    with model1:
        # 一様分布の生成
        p = pm.Uniform("p", lower=0.0, upper=1.0)

        # ベルヌーイ分布による観測値の生成
        X_obs = pm.Bernoulli("X_obs", p=p, observed=X_pre)

        idata1 = pm.sample(random_seed=42)

    g = pm.model_to_graphviz(model1)
    g.render(outfile="model1.png")

    az.plot_trace(idata1, compact=False)

    ax = az.plot_posterior(idata1)
    ax.set_xlim(0, 1)
    ax.set_title("ベイズ推論結果")

    plt.tight_layout()
    japanize_matplotlib.japanize()
    plt.show()


if __name__ == "__main__":
    print(f"Running on PyMC v{pm.__version__}")
    print(f"Running on ArviZ v{az.__version__}")
    print("Processing...")
    main()
    print("DONE")
