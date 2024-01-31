from src.models.Section import Section


class Rule:
    """
    Rule to perform section extraction.
    """

    def __init__(self, left_context: str, right_context: str, classification: str):
        """
        Initializes an instance with the delimiters and classification to perform section extraction.

        Args:
            left_context: keyword where the relevant section starts (exclusive)
            left_context: keyword where the relevant section ends (exclusive)
            classification: classification assigned to sections following this rule
        """
        self.left_context = left_context
        self.right_context = right_context
        self.classification = classification

    def extract(self, text: str) -> Section:
        """
        Extracts the section of the text that matches the rule.

        Args:
            text: string to perform the extraction respect with
        Returns:
            Section of the text that follows the rule (excluding the delimiters)
        """
