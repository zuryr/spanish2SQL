from typing import List

from Section import Section
from Condition import Condition
from SemanticEvaluator import SemanticEvaluator
from SectionExtractor import SectionExtractor
from TextPipeline import TextPipeline
from Enums.Classifications import Classifications
from Condition import Condition


class SimplePipeline(TextPipeline):
    """Pipeline based on fixed rules."""

    def __init__(
        self,
        evaluator: SemanticEvaluator,
        operator_extractor: SectionExtractor,
        value_extractor: SectionExtractor,
    ):
        """
        Pipeline based on a naive strategy.

        It works by assuming that the incoming section contains the relevant element in its treated form and doesn't need any aditional treatment.

        Args:
            evaluator: previously initialized semantic evaluator
            operator_extractor: instance of SectionExtractor initialized with logic operator extraction rules
            value_extractor: instance of SectionExtractor initialized with value extraction rules (for conditional attribute and conditional value extraction)
        """
        super().__init__(evaluator)
        self.operator_extractor = operator_extractor
        self.value_extractor = value_extractor

    def transform_sections(self, text: list[Section]) -> list[Section]:
        cleaned_sections = []
        for section in text:
            cleaned_sections.append(self.transform_section(section))
        return cleaned_sections

    def transform_section(
        self, section: Section
    ) -> Section | Condition | list[Condition]:
        if section.classification == Classifications.TABLA.value:
            return self.extract_table(section)
        if section.classification == Classifications.ATRIBUTO.value:
            return self.extract_attributes(section)
        if section.classification == Classifications.CONDICION.value:
            return self.extract_condition(section)

    def extract_table(self, section: Section) -> Section:
        text = section.text
        text_split = text.split()

        return Section(
            "_".join(text_split),
            section.classification,
            section.right_context,
            section.left_context,
        )

    def extract_attributes(self, section: Section) -> list[Section]:
        text = section.text
        text_split = text.split()

        return Section(
            "_".join(text_split),
            section.classification,
            section.right_context,
            section.left_context,
        )

    def extract_condition(self, section: Section) -> list[Condition] | None:
        """Extracts a condition from a section"""

        # Extract operators
        operators = self.operator_extractor.extract_exact_match(section.text)

        # Assume that the value extractor contains rules with
        # classification ATR_CONDICION y VALOR
        extracted_values = self.value_extractor.extract(section.text)

        # Relevant class names
        atribute = "ATR_CONDICION"
        value = "VALOR"

        # Filter by conditional value and conditional attribute
        conditional_value = [
            section
            for section in extracted_values
            if section.classification == atribute
        ]
        conditional_atribute = [
            section for section in extracted_values if section.classification == value
        ]

        # Generate condition
        if not operators or not conditional_atribute or not conditional_value:
            return None

        first_operator = operators[0]
        first_conditional_value = conditional_value[0]
        first_conditional_atribute = conditional_atribute[0]

        condition = Condition(
            first_operator,
            first_conditional_value.text,
            first_conditional_atribute.text,
        )

        return [condition]
