# Constants
UNIVERSE = "*"
VOID = "@"


class Hypothesis:
    def __init__(self, hypothesis_values: list[list[str]] = []):
        # Positional values that an example must have to be positive
        self.values: list[list[str]] = hypothesis_values

    def follows_hypothesis(self, x: list):
        """Evaluates an example with the current hypothesis"""
        if len(x) != len(self.values):
            raise ValueError("The sample must be the same size as the hypothesis")

        evaluation = True

        for i in range(len(x)):
            sample_value = x[i]
            hypothesis_value = self.values[i]

            if not Hypothesis.follows_rule(sample_value, hypothesis_value):
                evaluation = False
                break

        return evaluation

    def array_follows_hypothesis(self, X):
        labels = []
        for x in X:
            labels.append(self.follows_hypothesis(x))
        return labels

    def any_array_element_follows_hypothesis(self, X):
        for x in X:
            if self.follows_hypothesis(x):
                return True
        return False

    def follows_rule(x_attr: str, set_of_rules: list[str]):
        """Evaluates a set of rules for an attribute of x"""
        evaluation = False

        for rule in set_of_rules:
            # After cleaning process, a rule can't be true and false at the same time
            if rule == VOID or rule[0] == "-":
                continue
            if x_attr == rule or rule == UNIVERSE:
                evaluation = True
                break
        return evaluation

    def __str__(self):
        string = "<"
        for arr in self.values[:-1]:
            string += " v ".join(arr)
            string += f","
        string += " v ".join(self.values[-1]) + ">"
        return string
