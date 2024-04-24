from Section import Section
from spanish2SQL.src.models.Condition import Condition
from src.models import SemanticEvaluator
from src.models.SectionExtractor import SectionExtractor
from src.models.TextPipeline import TextPipeline
from src.models.Enums.Classifications import Classifications


class SimplePipeline(TextPipeline):
    """Semantic evaluator based on fixed rules."""

    def __init__(self, evaluator: SemanticEvaluator, operator_extractor: SectionExtractor, value_extractor: SectionExtractor):
        super().__init__(evaluator)
        self.operator_extractor = operator_extractor
        self.value_extractor = value_extractor

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
    
    def evaluate_condition(self, section: Section, ATR_CONDITION: str, VAL_CONDITION: str) -> Condition:
        """Extract operator, conditional_value and conditional_atribute """
        
        # TODO: extract operators
        operators = self.operator_extractor.extract_exact_match(section.text)
        
        # Assume that the value extractor contains rules with
        # classification ATR_CONDICION y VALOR
        extracted_values = self.value_extractor.extract(section.text)

        atribute = "ATR_CONDIcION"
        value = "VALOR"
        #TODO: filter by conditional value and conditional attribute
        conditional_value = [section for section in extracted_values if section.clasification == atribute] 
        conditional_atribute = [section for section in extracted_values if section.clasification == value] 

        # TODO: generate condition
        condition = Condition()
     
        if operators:
            first_operator = operators[0]
        if conditional_value:
            first_conditional_value = conditional_value[0]
        if conditional_atribute:
            first_conditional_atribute = conditional_atribute[0]

        condition.operator = first_operator
        condition.conditional_value = first_conditional_value
        condition.conditional_attribute = first_conditional_atribute

        condition = Condition(first_operator, first_conditional_value, first_conditional_atribute)

        return condition
   
