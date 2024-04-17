from Column import Column


class Condition:
    """Condition in a SQL query."""

    def __init__(self, column: Column, value: str, operator: str):
        """
        Initializes a condition for a SQL query.

        Args:
            column: column that needs to meet the condition
            value: value that needs to be meeted by the column
            operator: conditional operator. Needs to be compatible with the column's datatype
        Raises:
            InvalidOperator: the operator isn't compatible with the column's datatype.
        """
        self.column = column
        self.value = value
        self.operator = operator

    def to_SQL_string(self):
        return f"{self.column.name} {self.value} {self.operator}"
