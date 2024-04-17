from Column import Column
from typing import Dict


# TODO: handle relations between tables
class Table:
    """
    Information about a table in a Database
    """

    def __init__(self, name: str, columns: list[Column] = None):
        """
        Initializes an instance with information about the table.

        Args:
            name: name of the table
            columns: list of columns in the table
        """
        self.name = name
        self.columns: Dict[str, Column] = {}
        for col in columns:
            if col.name not in self.columns:
                self.columns[col.name] = col
                
        self.rows = []  # Assuming each table has a list of rows for data storage
        
    def get_all_colums_from_table(self):
        """ Return all columns from a table """
        return self.columns.values()
    
    def get_column_by_name(self, attribute_name: str):
        """ 
        Return column with its name
        
        Args:
            attribute_name: name of the column
        """
        if attribute_name in self.columns.keys():
            return self.columns[attribute_name]
        
        return None
    
    # def column_exists(self, database: Database, column_name: str) -> bool:
    #     """Check if the column exists in the given table."""
    #     if database.table_exists(self.name):
    #         return column_name in self.columns
    #     return False
    
