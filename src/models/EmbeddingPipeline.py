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

    def __init__(self, evaluator: SemanticEvaluator, extractor: SectionExtractor, threshold: float,
                 operator_extractor: SectionExtractor, value_extractor: SectionExtractor):
        """
        threshold: Threshold to define how similar words should be between the real names and the predicted names on
        the embedding pipeline
        """
        super().__init__(evaluator)
        self.threshold = threshold
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
                if similarity >= self.threshold:
                    best_words_list.append(str(doc2))

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
        conditional_atribute = [
            section for section in extracted_values if section.classification == atribute
        ]

        # Generate condition
        if not operators:
            return Condition()

        first_operator = operators[0]
        best_conditional_attribute = None
        first_conditional_value = None

        if conditional_atribute:
            first_conditional_atribute = conditional_atribute[0]

            conditional_atribute_split = first_conditional_atribute.text.split()
            best_words_list = []
            for word in conditional_atribute_split:
                doc1 = nlp(word)
                for column in self.evaluator.database.get_all_attributes():
                    doc2 = nlp(column.name)
                    similarity = doc2.similarity(doc1)
                    if similarity >= 0.3:
                        best_words_list.append(str(doc2))

            best_conditional_attribute = ", ".join(set(best_words_list))

        if not conditional_atribute and conditional_value:
            first_conditional_value = conditional_value[0]

            conditional_value_split = first_conditional_value.text.split()
            best_words_list = []
            for word in conditional_value_split:
                doc1 = nlp(word)
                for column in self.evaluator.database.get_all_attributes():
                    doc2 = nlp(column.name)
                    similarity = doc2.similarity(doc1)
                    if similarity >= 0.3:
                        best_words_list.append(str(doc2))

            best_conditional_attribute = ", ".join(set(best_words_list))

        # Generate condition
        if not operators or not best_conditional_attribute or not first_conditional_value:
            return Condition()

        condition = Condition(
            best_conditional_attribute, first_conditional_value.text, first_operator
        )

        return condition

