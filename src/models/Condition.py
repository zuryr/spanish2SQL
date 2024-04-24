from Column import Column


class Condition:
    """Condition in a SQL query."""

    def __init__(
        self, column_name: str = "", value_name: str = "", logic_operator: str = "="
    ):
        """
        Initializes a condition for a SQL query.

        Args:
            column_name: column that needs to meet the condition
            value_name: value that needs to be meeted by the column
            logic_operator: conditional operator. Needs to be compatible with the column's datatype
        Raises:
            InvalidOperator: the operator isn't compatible with the column's datatype.
        """
        self.column_name = column_name
        self.value_name = value_name
        self.logic_operator = logic_operator

    def condition_to_string(self) -> str:
        """Returns the equivalent string of the current string"""
        return f"{self.column_name}{self.logic_operator}{self.value_name}"

    def is_empty(self) -> bool:
        """Returns true if the current condition is empty"""
        return self.column_name == "" or self.value_name == ""
