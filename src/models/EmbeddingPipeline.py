import spacy

from Section import Section
from src.models.Condition import Condition
from src.models.Enums.Classifications import Classifications
from src.models.SectionExtractor import SectionExtractor
from src.models.SemanticEvaluator import SemanticEvaluator
from src.models.TextPipeline import TextPipeline

nlp = spacy.load("es_core_news_md")


class EmbeddingPipeline(TextPipeline):
    """Semantic evaluator based on word embeddings."""

    def __init__(self, evaluator: SemanticEvaluator, thresholdForAtrribute: float, operator_extractor: SectionExtractor, value_extractor: SectionExtractor):
        """
        threshold: Threshold to define how similar words should be between the real names and the predicted names on
        the embedding pipeline
        """
        super().__init__(evaluator)
        self.thresholdForAtrribute = thresholdForAtrribute
        self.operator_extractor = operator_extractor
        self.value_extractor = value_extractor

    def transform_sections(self, text: list[Section]) -> list[Section | Condition]:
        cleaned_sections = []
        for section in text:
            cleaned_sections.append(self.transform_section(section))
        return cleaned_sections

    def transform_section(self, section: Section) -> Section | Condition:
        if section.classification == Classifications.TABLA.value:
            return self.extract_table(section)
        if section.classification == Classifications.ATRIBUTO.value:
            return self.extract_attribute(section)
        if section.classification == Classifications.CONDICION.value:
            return self.extract_condition(section)

    def extract_table(self, section: Section) -> Section:
        """Evaluate the TABLE section."""
        section_words = section.text.split()
        max_similarity = ('', 0)

        for word in section_words:
            doc1 = nlp(word)
            for table in self.evaluator.database.get_all_table_names():
                doc2 = nlp(table)
                similarity = doc2.similarity(doc1)
                if similarity > max_similarity[1]:
                    max_similarity = (str(doc2), similarity)

        return Section(max_similarity[0], section.classification, section.right_context, section.left_context)

    def extract_attribute(self, section: Section) -> Section:
        """Evaluate the ATTRIBUTE section."""
        section_words = section.text.split()
        best_words_list = []
        for word in section_words:
            doc1 = nlp(word)
            for column in self.evaluator.database.get_all_attributes():
                doc2 = nlp(column.name)
                similarity = doc2.similarity(doc1)
                if similarity >= self.thresholdForAtrribute:
                    best_words_list.append(str(doc2))

        best_words = None
        if len(best_words_list) > 0:
            best_words = ", ".join(set(best_words_list))

        return Section(best_words, section.classification, section.right_context, section.left_context)

    def extract_condition(self, section: Section) -> Condition:
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
            section for section in extracted_values if section.classification == value
        ]
        conditional_attribute = [
            section for section in extracted_values if section.classification == atribute
        ]

        # Generate condition
        if not operators:
            return Condition()

        first_operator = operators[0]
        best_conditional_attribute = None
        best_conditional_value = None

        if conditional_attribute:
            best_conditional_attribute, _ = self.getBestConditionalAttributeAndValue(conditional_attribute)

        if not conditional_attribute and conditional_value:
            best_conditional_attribute, best_conditional_value = self.getBestConditionalAttributeAndValue(conditional_value)

        # Generate condition
        if not operators or not best_conditional_attribute:
            return Condition()

        condition = Condition(
            best_conditional_attribute, best_conditional_value, first_operator
        )

        return condition

    def getBestConditionalAttributeAndValue(self, conditional_attribute_or_value: list[Section]) -> str or None:

        max_similarity = ('', 0, '')
        for conditionals in conditional_attribute_or_value:
            possible_conditional_attributes_or_values = conditionals.text.split()

            for attr_or_val in possible_conditional_attributes_or_values:
                doc1 = nlp(attr_or_val)
                for attribute in self.evaluator.database.get_all_attributes():
                    doc2 = nlp(attribute.name)
                    similarity = doc2.similarity(doc1)
                    if similarity > max_similarity[1]:
                        max_similarity = (str(doc2), similarity, attr_or_val)

        return max_similarity[0], max_similarity[2]

