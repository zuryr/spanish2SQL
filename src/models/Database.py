from typing import Dict, List
from Column import Column
from Table import Table


class Database:
    """
    Information about the structure of a relational database
    """

    def __init__(self, name: str):
        """
        Initializes an instance with information about the database.

        Args:
            name: name of the database
        """
        self.name = name
        self.tables: Dict[str, Table] = {}

    def table_exists(self, table_name: str) -> bool:
        """Check if the table exists in the database."""
        return table_name in list(self.tables.keys())

    def get_table_by_name(self, table_name: str) -> Table:
        """
        Returns a table by name.

        Args:
            table_name: name of the table
        Returns:
            The table with the given name
        Raises:
            ValueError: If the table is not found in the database
        """
        if self.table_exists(table_name):
            return self.tables[table_name]
        else:
            raise ValueError(f"Table '{table_name}' not found in the database")

    def add_table(self, table_name: str, columns: List[Column]):
        """
        Adds a new table to the database.

        Args:
            table_name: name of the table to be added
            column_names: list of column names for the new table
        """
        if not self.table_exists(table_name):
            new_table = Table(name=table_name, columns=columns)
            self.tables[table_name] = new_table
        else:
            print(f"Table '{table_name}' already exists in the database.")

    def get_all_table_names(self) -> List[str]:
        """
        Returns a list of all table names in the database.

        Returns:
            A list of table names
        """
        return list(self.tables.keys())

    def get_all_attributes_from_table(self, table_name: str):
        """
        Return all colums from a specific table.

        Args:
            table_name: name of the table
        """
        table = self.get_table_by_name(table_name)
        return table.get_all_colums_from_table()

    def get_all_attributes(self) -> List[Column]:
        """
        Return all attributes from the database
        """
        all_attributes = []
        for table in self.tables.values():
            columns_in_table = table.columns.values()
            for col in columns_in_table:
                all_attributes.append(col)

        return all_attributes

    def get_all_attribute_table_pairs(self) -> List[tuple[Column, Table]]:
        """
        Returns all attribute-table pairs from the database
        """
        all_pairs = []
        for table in self.tables.values():
            columns_in_table = table.columns.values()
            for col in columns_in_table:
                all_pairs.append((col, table))

        return all_pairs

    def column_exists(self, column_name: str) -> bool:
        all_columns = self.get_all_attributes()
        cols_names = list(map(lambda col: col.name, all_columns))

        return column_name in cols_names

    def database_to_string(self):
        all_tables = self.get_all_table_names()
        print("Nombre de la base de datos: ",self.name)
        for i, table in enumerate(all_tables):
            print(f"Nombre de la tabla {i+1}: {table}")
            all_columns_from_table = self.get_all_attributes_from_table(table)

            for j, column in enumerate(all_columns_from_table):
                print(f"Columna {j+1}: {column.name}")