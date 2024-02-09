from src.models.Column import Column


# TODO: handle relations between tables
class Table:
    """
    Information about a table in a Database
    """

    def __init__(self, name: str, columns: list[Column]):
        """
        Initializes an instance with information about the table.

        Args:
            name: name of the table
            columns: list of columns in the table
        """
        self.name = name
        self.columns = columns
        self.rows = []  # Assuming each table has a list of rows for data storage
