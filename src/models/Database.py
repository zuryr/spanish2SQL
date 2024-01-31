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
