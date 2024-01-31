class ColumnNotFoundError(Exception):
    """
    Referenced column doesn't exist in the table.

    Attributes:
        table_name: name of the table where the search was performed
        column_name: name of the column that wasn't found in the database
    """

    def __init__(self, table_name: str, column_name: str):
        """
        Initializes the exception with information about the column that wasn't found in the table.

        Args:
            table_name: name of the table where the search was performed
            column_name: name of the column that wasn't found in the database
        """
        message = f"{column_name} was not found in {table_name} database."
        super().__init__(message)
