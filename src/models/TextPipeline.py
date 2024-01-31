from abc import ABC, abstractmethod


class TextPipeline(ABC):
    """Manages the behavior to perform a transformation to a text."""

    def __init__(self):
        """
        Instantiates the pipeline.
        """
        pass

    @abstractmethod
    def transform(self, text: str) -> str:
        """
        Performs a transformation to a text.

        Args:
            text: text to perform the transformation to
        Returns:
            The transformed text
        """
        pass
