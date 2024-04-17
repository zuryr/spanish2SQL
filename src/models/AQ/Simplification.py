from sympy.logic.boolalg import Or, And
from sympy.logic.boolalg import simplify_logic
from sympy.abc import symbols as sym_symbols

from Hypothesis import Hypothesis


def simplify_boolean_expression(expression):
    disjunctions = []
    for conjunction in expression:
        terms = []
        for i, var in enumerate(conjunction):
            if var[0] == "*":
                continue
            symbol = sym_symbols(f"{i}={var[0]}")
            terms.append(symbol)
        disjunctions.append(And(*terms))

    result = Or(*disjunctions)
    simplified_result = simplify_logic(result, force=True)

    return simplified_result


def simplify_cover(cover):
    complex_set = cover.complex_set
    all_hyp_values = []
    for h in complex_set:
        all_hyp_values.append(h.values)
    res = simplify_boolean_expression(all_hyp_values)

    return res
