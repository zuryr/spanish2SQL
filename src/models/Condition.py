from Column import Column


class Condition:
    """Condition in a SQL query."""

    def __init__(
        self, column_name: str | None, value_name: str | None, logic_operator: str = "="
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
        # TODO: format according to the datatype
        return f'{self.column_name} {self.logic_operator} "{self.value_name}"'

    def is_empty(self) -> bool:
        """Returns true if the current condition is empty"""
        return self.column_name == "" or self.value_name == ""

    def __eq__(self, other) -> bool:
        """
        Compares whether two Conditions objects are equal.

        Args:
            other: Another Condition object to compare.

        Returns:
            True if the objects are equal, False otherwise.
        """
        # Check if both columns are None
        return (
            self.column_name == other.column_name
            # and self.value_name == other.value_name # value its omitted because can't be compared with translation
            and self.logic_operator == other.logic_operator
        )

    def __hash__(self):
        """Override hash function."""
        return hash((self.column_name, self.value_name, self.logic_operator))
