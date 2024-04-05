from Database import Database
from Query import Query
from Table import Table
from Exceptions.TableNotFoundError import TableNotFoundError
from Exceptions.ColumnNotFoundError import ColumnNotFoundError
from WordProcessingSemanticEvaluator import WordProcessingSemanticEvaluator
from FixedSemanticEvaluator import FixedSemanticEvaluator
from EmbeddingSemanticEvaluator import EmbeddingSemanticEvaluator


class SemanticEvaluator:
    """Utilities for evaluating if a SQL query (or any of its parts) is semantically correct respecting to a database."""

    def __init__(self, database: Database, evaluator_type: str = 'fixed'):
        """
        Initializes a SemanticEvaluator instance respecting to a database.

        Args:
            database: schema to evaluate respect with
        """
        self.database = database
        self.tableNotFound = TableNotFoundError(database, '')
        self.columnNotFound = ColumnNotFoundError(database, '')
        self.evaluator_type = evaluator_type
        
        if self.evaluator_type == 'fixed':
            self.evaluator = FixedSemanticEvaluator(self.database)
        elif self.evaluator_type == 'word_processing':
            self.evaluator = WordProcessingSemanticEvaluator(self.database)
        elif self.evaluator_type == 'embeddings':
            self.evaluator = EmbeddingSemanticEvaluator(self.database)
        else:
            raise ValueError("Invalid evaluator type")


    def query_is_correct(self, query: Query) -> bool:
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
        table_name = query.table.name
        if not self.table_exists(table_name):
            raise self.tableNotFound(self.database,table_name)

        table = self.database.get_table(table_name)
        for column in query.columns:
            if not self.column_exists(table, column.name):
                raise self.columnNotFound(table_name, column.name)

        # TODO: Add more checks for operators, data types, etc.
        return True