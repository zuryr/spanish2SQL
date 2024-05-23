from GroupStrategy import GroupStrategy
from Database import Database
from Section import Section


class MaxAttributesInTableStrategy(GroupStrategy):
    """
    Group strategy based in the maximization of attributes in a table
    """

    def __init__(self, database: Database):
        """
        Group strategy based on a greedy maximization of attributes in a table

        Args:
            database: current database
        """
        super().__init__()
        self.database = database

    def group_attributes(self, attributes: list[Section]) -> list[list[Section]]:
        """
        Groups a list of attributes following a strategy that maximizes the number of attributes in a table.

        Args:
            attributes: list of sections with classification ATTRIBUTE
        Returns:
            A list with groups of attributes following this strategy
        """
        attribute_groups = []
        table_names = self.database.get_all_table_names()
        for table_name in table_names:
            current_table = self.database.get_table_by_name(table_name)
            current_group = set()
            for attribute in attributes:
                exists_in_table = (
                    current_table.get_column_by_name(attribute.text) != None
                )
                if exists_in_table:
                    current_group.add(attribute)

            attribute_groups.append(current_group)

        return attribute_groups
