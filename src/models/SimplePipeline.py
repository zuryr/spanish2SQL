from Section import Section
from src.models import SemanticEvaluator
from src.models.SectionExtractor import SectionExtractor
from src.models.TextPipeline import TextPipeline
from src.models.Enums.Classifications import Classifications


class SimplePipeline(TextPipeline):
    """Semantic evaluator based on fixed rules."""

    def __init__(self, evaluator: SemanticEvaluator, extractor: SectionExtractor):
        super().__init__(evaluator, extractor)

    def transform_sections(self, text: list[Section]) -> list[Section]:
        cleaned_sections = []
        for section in text:
            cleaned_sections.append(self.transform_section(section))
        return cleaned_sections

    def transform_section(self, section: Section) -> Section:
        if section.classification == Classifications.TABLA.value:
            return self.evaluate_table(section)
        if section.classification == Classifications.ATRIBUTO.value:
            return self.evaluate_attribute(section)
        if section.classification == Classifications.CONDICION.value:
            return self.evaluate_condition(section)

    def evaluate_table(self, section: Section) -> Section:
        """Evaluate the TABLE section."""
        table = section
        if self.evaluator.database.table_exists(table.text):
            return table

    def evaluate_attribute(self, section: Section) -> Section:
        """Evaluate the ATTRIBUTE section."""
        attribute = section
        if self.evaluator.database.column_exists(attribute.text):
            return attribute

    def evaluate_condition(self, section: Section) -> Section:
        """Evaluate the CONDITION section."""
        condition = section
        # TODO: Implement logic to evluate condition
        return condition
