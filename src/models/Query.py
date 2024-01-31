from src.models.Column import Column
from src.models.Condition import Condition
from src.models.Table import Table


class Query:
    """SQL query container."""

    def __init__(self, table: Table, columns: list[Column], condition: Condition):
        """
        Initializes an abstraction of an SQL query.

        Args:
            table: table where to perform the query
            columns: columns to extract from the query
            condition: conditional statement to filter the results in the query
        """

    def to_SQL_string(self) -> str:
        """
        Transforms the query into SQL code.
        Returns:
            A string with the SQL code equivalent to the query.
        """
