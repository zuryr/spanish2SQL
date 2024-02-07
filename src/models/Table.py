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
        
        def create_row(self, values: list):
        """
        Creates a new row in the table.

        Args:
            values: list of values for each column in the row
        """
        if len(values) == len(self.columns):
            self.rows.append(dict(zip([column.name for column in self.columns], values)))
        else:
            raise ValueError("Number of values must match the number of columns")

    def read_rows(self):
        """
        Returns all rows in the table.
        """
        return self.rows

    def update_row(self, index: int, values: list):
        """
        Updates a row in the table.

        Args:
            index: index of the row to be updated
            values: list of new values for each column in the row
        """
        if 0 <= index < len(self.rows) and len(values) == len(self.columns):
            self.rows[index] = dict(zip([column.name for column in self.columns], values))
        else:
            raise ValueError("Invalid index or number of values")

    def delete_row(self, index: int):
        """
        Deletes a row from the table.

        Args:
            index: index of the row to be deleted
        """
        if 0 <= index < len(self.rows):
            del self.rows[index]
        else:
            raise ValueError("Invalid index")
