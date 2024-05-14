import re
from Database import Database
from Table import Table
from Exceptions.ColumnNotFoundError import ColumnNotFoundError
from Exceptions.TableNotFoundError import TableNotFoundError
from Query import Query
from Enums.DataTypes import DataTypes


class SemanticEvaluator:
    """Utilities for evaluating if a SQL query (or any of its parts) is semantically correct respecting to a database."""

    def __init__(self, database: Database):
        """
        Initializes a SemanticEvaluator instance respecting to a database.

        Args:
            database: schema to evaluate respect with
        """
        self.database = database
        self.tableNotFound = TableNotFoundError
        self.columnNotFound = ColumnNotFoundError

    def has_numbers(self, string_to_evaluate: str) -> bool:

        string_to_evaluate = string_to_evaluate.replace('"', '')

        pattern = r"^[-+]?\d*\.?\d+$"
        
        return re.match(pattern, string_to_evaluate) is not None
    
    def is_time(self, string_to_evaluate: str):

        pattern_time = r'^\d{2}:\d{2}:\d{2}(\.\d{1,3})?$'

        pattern_date = r'^\d{4}-\d{2}-\d{2}$'

        return ((re.match(pattern_time, string_to_evaluate) is not None) or (re.match(pattern_date, string_to_evaluate) is not None))

    def query_is_correct(self, query: Query) -> bool:
        """
        Determines if a query is semantically correct respecting to a database.
        
        A query is semantically correct if:
        - The table exists in the database
        - The column exists in the table
        - The operators used are valid with the column's data type

        Args:
            query: query to evaluate
        Returns:
            True if the query is correct
        Raises:
            TableNotFoundError: The table doesn't exist in the database
            ColumnNotFoundError: The column doesn't exist in the table
        """


        table_name = query.table

        if table_name is None:
            return False
        


        if not self.database.table_exists(table_name):
            return False

        table = self.database.get_table_by_name(table_name)

        if query.columns is not None:
            for column in query.columns:
                column = column.strip()
                if not table.column_exists(column):
                    return False
                    
        
        if query.condition is not None and query.condition != "":
            condition = query.condition
            conditional_attribute, conditional_operator, conditional_value = condition.split()

            if not table.column_exists(conditional_attribute):
                return False
            
            conditional_column = table.get_column_by_name(conditional_attribute)

            valid_varchar_operators = ['=', '!=']
            valid_numeric_operators = ['<', '>', '=', '<=', '>=', '!=']
            
            if conditional_column.datatype == DataTypes.TEXT.value and ((conditional_operator not in valid_varchar_operators)):
                return False
            
            if conditional_column.datatype == DataTypes.NUMBER.value and ((conditional_operator not in valid_numeric_operators) or (not self.has_numbers(conditional_value))):
                return False
            
            if conditional_column.datatype == DataTypes.TIME.value and ((conditional_operator not in valid_numeric_operators) or (not self.is_time(conditional_value))):
                return False
            
        return True