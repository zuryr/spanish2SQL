import random
from typing import List

import spacy

from Section import Section
from Condition import Condition
from Enums.Classifications import Classifications
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator
from TextPipeline import TextPipeline

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

    def transform_sections(self, text: list[Section]) -> list[Section | list[Condition]]:
        cleaned_sections = []
        for section in text:
            # if section.classification == 'ATRIBUTO' and section.text == 'creación, nombre y presupuesto':
            #     print("")
            clean_section = self.transform_section(section)
            # if clean_section is None:
            #     continue
            # if type(clean_section) is Section and clean_section.text is None:
            #     continue
            cleaned_sections.append(clean_section)
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
                for column_part in column.name.split():
                    column_part = column_part.strip()
                    doc2 = nlp(column_part)
                    similarity = doc2.similarity(doc1)
                    if similarity >= self.thresholdForAtrribute:
                        best_words_list.append(column.name)

        best_words = None
        if len(best_words_list) > 0:
            best_words = ", ".join(set(best_words_list))

        return Section(best_words, section.classification, section.right_context, section.left_context)

    def extract_condition(self, section: Section) -> Condition | list[Condition] | None:
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
            return None

        obtained_conditions = []
        operators = set(operators)

        for operator in operators:
            best_conditional_attribute = None
            best_conditional_value = None

            if conditional_attribute:
                best_conditional_attribute, _ = self.getBestConditionalAttributeAndValue(conditional_attribute)
                if conditional_value:
                    for val in conditional_value:
                        best_conditional_value = val.text
                        best_conditional_value = best_conditional_value.replace(" ", "_")
                        obtained_conditions.append(Condition(best_conditional_attribute, best_conditional_value, operator))

            if not conditional_attribute and conditional_value:
                best_conditional_attribute, best_conditional_value = self.getBestConditionalAttributeAndValue(conditional_value)

            # Generate condition
            if not best_conditional_attribute or not best_conditional_value:
                return None

            condition = Condition(
                best_conditional_attribute, best_conditional_value, operator
            )

            obtained_conditions.append(condition)

            obtained_conditions = self.remove_conditon_duplicates(obtained_conditions)

        return obtained_conditions

    def getBestConditionalAttributeAndValue(self, conditional_attribute_or_value: list[Section]) -> str or None:

        max_similarity = (None, 0, None)
        for conditionals in conditional_attribute_or_value:
            possible_conditional_attributes_or_values = conditionals.text.split()

            for attr_or_val in possible_conditional_attributes_or_values:
                doc1 = nlp(attr_or_val)
                for attribute in self.evaluator.database.get_all_attributes():
                    doc2 = nlp(attribute.name)
                    similarity = doc2.similarity(doc1)
                    if similarity > max_similarity[1]:
                        max_similarity = (str(doc2), similarity, attr_or_val)
        attr, val = None, None
        if max_similarity[0]:
            attr = max_similarity[0].replace(" ", "_")
        if max_similarity[2]:
            val = max_similarity[2].replace(" ", "_")

        return attr, val


    def remove_conditon_duplicates(self, conditions):
        """Remove duplicates from a list of Condition objects."""
        seen = set()
        unique_conditions = []
        for cond in conditions:
            if cond not in seen:
                unique_conditions.append(cond)
                seen.add(cond)
        return unique_conditions