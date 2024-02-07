from src.models.Table import Table


class Database:
    """
    Information about the structure of a relational database
    """

    def __init__(self, name: str, tables: list[Table]):
        """
        Initializes an instance with information about the database.

        Args:
            name: name of the database
            tables: list of tables in the database
        """
        self.name = name
        self.tables = tables

    def get_table_by_name(self, table_name: str) -> Table:
        """
        Returns a table by name.

        Args:
            table_name: name of the table
        """
        for table in self.tables:
            if table.name == table_name:
                return table
        raise ValueError(f"Table '{table_name}' not found in the database")