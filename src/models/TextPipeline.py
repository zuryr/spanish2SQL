from abc import ABC, abstractmethod

from src.models.Condition import Condition
from src.models.Section import Section
from src.models.SectionExtractor import SectionExtractor
from src.models.SemanticEvaluator import SemanticEvaluator


class TextPipeline(ABC):
    """Manages the behavior to perform a transformation to a text."""

    def __init__(self, evaluator: SemanticEvaluator):
        """
        Instantiates the pipeline.
        evaluator: SemanticEvaluator
        """
        self.evaluator = evaluator

    @abstractmethod
    def transform_sections(self, section_list: list[Section]) -> list[Section | Condition]:
        """
        Performs a transformation dirty sections to a cleaned sections.

        Args:
            section_list: text to perform the transformation to
        Returns:
            A list of the transformed sections
        """
        pass

    @abstractmethod
    def transform_section(self, section: Section) -> Section | Condition:
        """
        Performs a transformation of a section to cleaned section or condition.

        Args:
            section: text to perform the transformation to
        Returns:
            A cleaned section or a cleaned condition
        """
        pass

    @abstractmethod
    def evaluate_table(self, section: Section) -> Section:
        """Evaluate the TABLE in a section."""
        pass

    @abstractmethod
    def evaluate_attribute(self, section: Section) -> Section:
        """Evaluate the attribute in a section."""
        pass

    @abstractmethod
    def evaluate_condition(self, section: Section) -> Condition:
        """Evaluate the condition in a section."""
        pass