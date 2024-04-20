from abc import ABC, abstractmethod

from src.models.Condition import Condition
from src.models.Section import Section
from src.models.SectionExtractor import SectionExtractor
from src.models.SemanticEvaluator import SemanticEvaluator


class TextPipeline(ABC):
    """Manages the behavior to perform a transformation to a text."""

    def __init__(self, evaluator: SemanticEvaluator, extractor: SectionExtractor, threshold: float):
        """
        Instantiates the pipeline.
        evaluator: SemanticEvaluator
        extractor: SectionExtractor initialized with value rules
        threshold: Threshold to define how similar words should be between the real names and ther the predicted names
        """

        self.evaluator = evaluator
        self.extractor = extractor
        self.threshold = threshold

    @abstractmethod
    def transform_sections(self, section_list: list[Section]) -> list[Section | Condition]:
        """
        Performs a transformation to a text.

        Args:
            text: text to perform the transformation to
        Returns:
            The transformed text in a section without left/right context
        """
        pass

    @abstractmethod
    def transform_section(self, section: Section) -> Section | Condition:
        """
        Performs a transformation to a text.

        Args:
            text: text to perform the transformation to
        Returns:
            The transformed text in a section without left/right context
        """
        pass