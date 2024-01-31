from src.models.Database import Database
from src.models.Query import Query


class SemanticEvaluator:
    """Utilities for evaluating if a SQL query (or any of its parts) is semantically correct respecting to a database."""

    def __init__(self, database: Database):
        """
        Initializes a SemanticEvaluator instance respecting to a database.

        Args:
            database: schema to evaluate respect with
        """
        self.database = database

    def query_is_correct(self, query: Query):
        """
        Determines if a query is semantically correct respecting to a database.

        A query is semantically correct if:
        - The table exists in the database
        - The column exists in the table
        - The operators used are valid with the column's data type
        - The aggregators used are valid with the column's data type

        Args:
            query: query to evaluate
        Returns:
            True if the query is correct
        Raises:
            TableNotFoundError: The table doesn't exist in the database
            ColumnNotFoundError: The column doesn't exist in the table
        """
        # TODO: implement individual methods to detect each error.
