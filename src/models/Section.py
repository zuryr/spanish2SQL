class Section:
    """
    Section of a text and its classification.
    """

    def __init__(
        self,
        text: str,
        classification: str,
        right_context: str,
        left_context: str,
        tracker: int = 0,
    ):
        """
        Initializes an instance with a text and its classification.

        Args:
            text: sectioned text
            classification: class assigned to the text
        """
        self.text = text
        self.classification = classification
        self.left_context = left_context
        self.right_context = right_context
        self.tracker = tracker

    def __hash__(self):
        return hash(
            f"{self.text}-{self.classification}-{self.left_context}-{self.right_context}"
        )
