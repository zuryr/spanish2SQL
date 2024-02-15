from Column import Column
from Condition import Condition
from Table import Table

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
        self.table = table
        self.columns = columns
        self.condition = condition

    def to_SQL_string(self) -> str:
        """
        Transforms the query into SQL code.
        Returns:
            A string with the SQL code equivalent to the query.
        """
        select_clause = ''
        from_clause = ''
        where_clause = ''
        
        if self.columns:
            # SELECT statement
            select_clause = f"SELECT {', '.join(column.name for column in self.columns)}"

            if self.table:
                # FROM statement
                from_clause = f"FROM {self.table.name}"
                
                if self.condition:
                    # WHERE statement (if condition exists)
                    where_clause = f"WHERE {self.condition.to_SQL_string()}" if self.condition else ""

            # Combine clauses into a complete SQL query
            sql_query = f"{select_clause} {from_clause} {where_clause};"

        return sql_query
