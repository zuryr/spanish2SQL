from Database import Database
from GroupStrategy import GroupStrategy
from Section import Section


class GreedyStrategy(GroupStrategy):
    """
    Group strategy based on a greedy approach
    """

    def __init__(self):
        """
        Group strategy based on a greedy approach
        """
        super().__init__()

    def group_attributes(self, attributes: list[Section]) -> list[list[Section]]:
        """
        Groups a list of attributes following a greedy strategy.

        Args:
            attributes: list of sections with classification ATTRIBUTE
        Returns:
            A list with a group containing all the attributes
        """
        return [attributes]
