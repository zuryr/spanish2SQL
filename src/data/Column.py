class Column:
    """
    Information about a column contained in a Table
    """

    def __init__(self, name: str, datatype: str):
        """
        Initializes an instance with information about the column.

        Args:
            name: name of the column
            datatype: SQL data type of the column (https://thedataschools.com/sql/data-types/)
                NOTE: possibly could be reduced to string, numeric and datetime
        """
        self.name = name
        self.datatype = datatype
