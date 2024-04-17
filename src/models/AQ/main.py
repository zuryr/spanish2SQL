from Decorators import repetition_decorator
import pandas as pd
from AQ import AQ
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


def print_metrics(y_test, y_pred, msg=""):
    print(msg)
    print(classification_report(y_test, y_pred, zero_division=0))
    print(confusion_matrix(y_test, y_pred))


@repetition_decorator
def main():
    df = pd.read_csv("./ctx_general.csv", dtype=str)
    # df = pd.read_csv("./agaricus-lepiota.data", dtype=str, header=None)
    # df = pd.read_csv("./data.txt")
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
    model = AQ()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_train)
    print_metrics(y_train, y_pred, "Metrics for learning set:")
    y_pred = model.predict(X_test)
    print_metrics(y_test, y_pred, "Metrics for test set:")
    for cover in model.covers:
        print(cover)


if __name__ == "__main__":
    main()
