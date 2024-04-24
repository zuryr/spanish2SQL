from Column import Column
from Condition import Condition
from Table import Table
from Exceptions.TableNotFoundError import TableNotFoundError


class Query:
    """SQL query container."""

    def __init__(self, table_name: str, columns_names: list[str], condition_name: str):
        """
        Initializes an abstraction of an SQL query.

        Args:
            table_name: table where to perform the query
            columns_names: columns to extract from the query
            condition_name: conditional statement to filter the results in the query
        """
        self.table = table_name
        self.columns = columns_names
        self.condition = condition_name
        self.tableNotFound = TableNotFoundError

    def to_SQL_string(self) -> str:
        """
        Transforms the query into SQL code.
        Returns:
            A string with the SQL code equivalent to the query.
        """
        select_clause = "SELECT *"
        from_clause = ""
        where_clause = ""

        if not self.table:
            raise TableNotFoundError("", self.table)

        # FROM statement
        from_clause = f"FROM {self.table}"

        if self.columns is not None:
            # SELECT statement
            select_clause = "SELECT "
            for col in self.columns:
                if col:
                    select_clause += f"{col}"
                else:
                    select_clause += "*"

        if self.condition is not None:
            # WHERE statement (if condition exists)
            where_clause = f" WHERE {self.condition}"

        # Combine clauses into a complete SQL query
        sql_query = f"{select_clause} {from_clause}{where_clause};"

        return sql_query
