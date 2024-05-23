from abc import ABC

from Database import Database
from Section import Section


class GroupStrategy(ABC):
    """Defines the strategy to group attributes"""

    def __init__(self):
        """
        Creates an instance of the strategy
        """
        pass

    def group_attributes(self, attributes: list[Section]) -> list[list[Section]]:
        """
        Groups a list of attributes following a strategy.

        Args:
            attributes: list of sections with classification ATTRIBUTE
        Returns:
            A list with groups of attributes following a strategy
        """
        pass
