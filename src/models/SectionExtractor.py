from src.models.Rule import Rule
from src.models.Section import Section


class SectionExtractor:
    """
    Extracts potentially relevant sections following a given a set of rules.

    Attributes:
        rules: list of rules that will be used to section respect with
    """

    def __init__(self, rules: list[Rule]):
        """
        Initialize an instance with a list of rules.

        Args:
            rules: list of rules that will be used to section respect with
        """
        self.rules = rules

    def extract(self, text: str) -> list[Section]:
        """
        Extracts all the possible relevant sections that match with the rules provided.

        Args:
            text: string to perform the extraction respect with

        Returns:
            A list containing the sections that matches the rules in the extractor.
        """
        pass
