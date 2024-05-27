from GroupStrategy import GroupStrategy
from Database import Database
from Section import Section


class ContextStrategy(GroupStrategy):
    """
    Group strategy based in the maximization of attributes in a table
    """

    def __init__(self):
        """
        Group strategy based on a greedy maximization of attributes in a table

        Args:
            database: current database
        """
        super().__init__()

    def group_attributes(self, attributes: list[Section]) -> list[list[Section]]:
        """
        Groups a list of attributes following a strategy that maximizes the number of attributes in a table.

        Args:
            attributes: list of sections with classification ATTRIBUTE
        Returns:
            A list with groups of attributes following this strategy
        """
        attribute_groups = {}
        final_attributes = []

        for attribute in attributes:
            group_id = f"{attribute.left_context}-{attribute.right_context}"
            if group_id not in attribute_groups:
                attribute_groups[group_id] = []
            attribute_groups[group_id].append(attribute)

        for group_id, attributes in attribute_groups.items():
            final_attributes.append(attributes)

        return final_attributes
