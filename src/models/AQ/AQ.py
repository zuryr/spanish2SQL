import numpy as np
from Cover import Cover
from Hypothesis import Hypothesis

# Constants
UNIVERSE = "*"
VOID = "@"


class AQ:
    def __init__(self):
        self.covers: list[Cover] = []

    def fit(self, X, y):
        # Create a model for each class
        classes = y.value_counts(ascending=False)
        classes = classes.index.tolist()
        domains = [X.iloc[:, i].unique().tolist() for i in range(len(X.columns))]
        domains = [[s_d for s_d in d if s_d != "*"] for d in domains]
        self.domains = domains

        for c in classes:
            cover = self._fit_for_specific_class(X, y, c)
            self.covers.append(cover)
            # X = X.loc[y != c]

    def _fit_for_specific_class(self, X, y, c):
        X_positives = X.loc[y == c]
        X_negatives = X.loc[y != c]
        cover: list[Hypothesis] = []
        attr_combinations = []
        n = len(X_positives.iloc[0])
        n = n if n < 5 else 5

        # Get the possible combinations of attributes to form an hypothesis
        for k in range(1, n + 1):
            k_combinations = self._get_combinations(n, k, 0, [], [])
            for comb in k_combinations:
                attr_combinations.append(comb)

        while len(X_positives) > 0:
            seed = X_positives.iloc[0]
            best_complex: Hypothesis = self._get_best_complex(
                X_positives, X_negatives, seed, attr_combinations
            )
            X_positives = self._remove_hypothesis_compliant(X_positives, best_complex)
            cover.append(best_complex)

        return Cover(cover, c)

    def predict(self, X):
        if len(self.covers) == 0:
            raise NameError(
                "The covers hasn't been initialized. Please fit the algorithm before making predictions."
            )

        y_pred = ["-1"] * len(X)
        for cover in self.covers:
            cover_labels = cover.array_belongs_to_cover(X.to_numpy())
            for i in range(len(cover_labels)):
                belongs_to_cover = cover_labels[i]
                if belongs_to_cover:
                    y_pred[i] = cover.class_evaluated

        return y_pred

    def _remove_hypothesis_compliant(self, X_positives, hypothesis: Hypothesis):
        is_hypothesis_compliant = hypothesis.array_follows_hypothesis(
            X_positives.to_numpy()
        )
        mask = np.array(is_hypothesis_compliant)
        mask = np.bitwise_not(mask).tolist()
        return X_positives.loc[mask]

    def _get_best_complex(self, X_positives, X_negatives, seed, attr_combinations):
        hypothesis_len = len(seed)
        best_complex = Hypothesis()
        best_n_selectors = hypothesis_len + 1
        best_n_covered_examples = 0

        for combination in attr_combinations:
            mid_hypothesis = Hypothesis([[UNIVERSE] for _ in range(hypothesis_len)])
            for domain_idx in combination:
                mid_hypothesis.values[domain_idx] = [seed.iloc[domain_idx]]
            if mid_hypothesis.any_array_element_follows_hypothesis(
                X_negatives.to_numpy()
            ):
                continue

            is_covered: list[bool] = mid_hypothesis.array_follows_hypothesis(
                X_positives.to_numpy()
            )

            current_n_covered_examples = self._count_true_in_array(is_covered)
            rule_covers_more_elements = (
                current_n_covered_examples > best_n_covered_examples
            )
            if rule_covers_more_elements:
                best_complex = mid_hypothesis
                best_n_selectors = len(combination)
                best_n_covered_examples = current_n_covered_examples
                continue

            rule_has_less_elements = len(combination) < best_n_selectors
            rule_covers_same_n_elements = (
                current_n_covered_examples == best_n_covered_examples
            )
            if rule_has_less_elements and rule_covers_same_n_elements:
                best_complex = mid_hypothesis
                best_n_selectors = len(combination)

        if len(best_complex.values) == 0:
            best_complex = Hypothesis([[UNIVERSE] for _ in range(hypothesis_len)])
            for i, seed_attr in enumerate(seed):
                best_complex.values[i] = [seed_attr]

        return best_complex

    def _count_true_in_array(self, arr):
        count = 0
        for el in arr:
            if el:
                count += 1
        return count

    def _get_combinations(self, n, k, idx=0, partial_combinations=[], memo=[]):
        if k <= 0:
            memo.append(partial_combinations)
            return

        for i in range(idx, n):
            current_combination = partial_combinations.copy()
            current_combination.append(i)
            self._get_combinations(n, k - 1, i + 1, current_combination, memo)

        return memo
