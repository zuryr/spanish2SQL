class TableNotFoundError(Exception):
    """
    Referenced table doesn't exist in the database.

    Attributes:
        database_name: name of the database where the search was performed
        table_name: name of the table not found in the database
    """

    def __init__(self, database_name: str, table_name: str):
        """
        Initializes the exception with information about the table that wasn't found in the database.

        Args:
            database_name: name of the database where the search was performed
            table_name: name of the table not found in the database
        """
        message = f"{table_name} was not found in {database_name} database."
        super().__init__(message)
