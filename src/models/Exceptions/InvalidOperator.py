class InvalidOperator(Exception):
    """
    The operator isn't compatible with the column's datatype.

    Attributes:
        operator: operator that was tried to execute
        datatype: datatype of the column
    """

    def __init__(self, operator: str, datatype: str):
        """
        Initializes the exception with information about the incompatible operator.

        Args:
            operator: operator that was tried to execute
            datatype: datatype of the column
        """
        message = f"The operator {operator} is not compatible with {datatype} datatype."
        super().__init__(message)
