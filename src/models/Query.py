from Condition import Condition
from Exceptions.TableNotFoundError import TableNotFoundError


class Query:
    """SQL query container."""

    def __init__(self, table_name: str, columns_names: list[str], condition: Condition):
        """
        Initializes an abstraction of an SQL query.

        Args:
            table_name: table where to perform the query
            columns_names: columns to extract from the query
            condition: conditional statement to filter the results in the query
        """
        self.table = table_name
        self.columns = columns_names
        self.condition = condition

    def __eq__(self, other):
        """
        Compares whether two Query objects are equal.

        Args:
            other: Another Query object to compare.

        Returns:
            True if the objects are equal, False otherwise.
        """

        condition_met = self.condition == other.condition

        # Check if both columns are None (shouldn't be empty)
        # if self.columns != [] and other.columns != []:
        #   return self.table == other.table and condition_met

        # If one column is None and the other is not, they are not equal
        # if self.columns is None or other.columns is None:
        #    return False

        # Both columns are not None, compare sets
        return (
            self.table == other.table
            and set(self.columns) == set(other.columns)
            and condition_met
        )

    def __hash__(self):
        """Override hash function."""
        return hash((self.table, tuple(self.columns), self.condition or ""))

    def SQL_to_string(self) -> str:
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
                # Workaround for queries containing None at columns
                select_clause += f"{col}," if col is not None or col == "" else "* "

            # Remove last comma
            select_clause = select_clause[:-1]

        if not self.condition.is_empty():
            # WHERE statement (if condition exists)
            where_clause = f" WHERE {self.condition.condition_to_string()}"

        # Combine clauses into a complete SQL query
        sql_query = f"{select_clause} {from_clause}{where_clause};"

        return sql_query
