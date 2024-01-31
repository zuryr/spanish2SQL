class Section:
    """
    Section of a text and its classification.
    """

    def __init__(self, text: str, classification: str):
        """
        Initializes an instance with a text and its classification.

        Args:
            text: sectioned text
            classification: class assigned to the text
        """
        self.text = text
        self.classification = classification
