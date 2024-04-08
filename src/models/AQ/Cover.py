from Hypothesis import Hypothesis


class Cover:
    def __init__(self, complex_set: list[Hypothesis], class_evaluated: str):
        self.complex_set = complex_set
        self.class_evaluated = class_evaluated

    def belongs_to_cover(self, x):
        for hypothesis in self.complex_set:
            if hypothesis.follows_hypothesis(x):
                return True

        return False

    def array_belongs_to_cover(self, X):
        predictions = []
        for x in X:
            pred = self.belongs_to_cover(x)
            predictions.append(pred)

        return predictions

    def __str__(self):
        string = f"Model for class '{self.class_evaluated}': \n"
        string += f"\tComplex: {{{' v '.join([str(h) for h in self.complex_set])}}}\n"

        return string
