import numpy as np
import pandas as pd


def develop_dataset(X, y):
    domains = [X.iloc[:, i].unique().tolist() for i in range(len(X.columns))]
    domains = [[s_d for s_d in d if s_d != "*"] for d in domains]
    X_developed = []
    y_developed = []
    for i, x in X.iterrows():
        all_x_dev = develop_sample(x, domains)
        for x_dev in all_x_dev:
            X_developed.append(x_dev.tolist())
            y_developed.append(y[i])

    return pd.DataFrame(X_developed), pd.Series(y_developed)


def develop_sample(x, X_domains):
    developed_sample = [x]
    not_fully_developed = True

    while not_fully_developed:
        should_break = True
        tmp_developed_sample = []
        for s_x in developed_sample:
            for i, x_i in enumerate(s_x):
                if x_i != "*":
                    continue

                for el in X_domains[i]:
                    x_tmp = s_x.copy()
                    x_tmp[i + 1] = el
                    tmp_developed_sample.append(x_tmp)
                should_break = False

                break

        if should_break:
            break
        developed_sample = tmp_developed_sample

    return developed_sample
