from abc import ABC, abstractmethod

from Condition import Condition
from Section import Section
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator


class TextPipeline(ABC):
    """Manages the behavior to perform a transformation to a text."""

    def __init__(self, evaluator: SemanticEvaluator):
        """
        Instantiates the pipeline.
        evaluator: SemanticEvaluator
        """
        self.evaluator = evaluator

    @abstractmethod
    def transform_sections(
        self, section_list: list[Section]
    ) -> list[Section, Condition]:
        """
        Performs a transformation dirty sections to a cleaned sections.

        Args:
            section_list: text to perform the transformation to
        Returns:
            A list of the transformed sections
        """
        pass

    @abstractmethod
    def transform_section(self, section: Section) -> list[Section] | list[Condition]:
        """
        Performs a transformation of a section to cleaned section or condition.

        Args:
            section: text to perform the transformation to
        Returns:
            A cleaned section or a cleaned condition
        """
        pass

    @abstractmethod
    def extract_table(self, section: Section) -> Section:
        """Extracts the TABLE in a section."""
        pass

    @abstractmethod
    def extract_attributes(self, section: Section) -> list[Section]:
        """Extracts the attributes in a section."""
        pass

    @abstractmethod
    def extract_condition(self, section: Section) -> list[Condition] | None:
        """Extracts the condition in a section."""
        pass
