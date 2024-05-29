import random
from typing import List

import spacy

from Section import Section
from Condition import Condition
from Enums.Classifications import Classifications
from Enums.ClassNames import ClassNames
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator
from TextPipeline import TextPipeline
from Tokenizer import Tokenizer
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("es_core_news_md")


class BertPipeline(TextPipeline):
    """Semantic evaluator based on word embeddings."""

    def __init__(
        self,
        evaluator: SemanticEvaluator,
        thresholdForAtrribute: float,
        operator_extractor: SectionExtractor,
        value_extractor: SectionExtractor
    ):
        """
        threshold: Threshold to define how similar words should be between the real names and the predicted names on
        the embedding pipeline
        """
        super().__init__(evaluator)
        self.attribute_threshold = thresholdForAtrribute
        self.operator_extractor = operator_extractor
        self.value_extractor = value_extractor
        self.model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

    def transform_sections(
        self, text: list[Section]
    ) -> list[Section | list[Condition]]:
        cleaned_sections = []
        for section in text:
            if section.classification != Classifications.TABLA.value:
                clean_section = self.transform_section(section)
                cleaned_sections.extend(clean_section)
        return cleaned_sections

    def transform_section(self, section: Section) -> list[Section] | list[Condition]:
        if section.classification == Classifications.ATRIBUTO.value:
            return self.extract_attributes(section)
        if section.classification == Classifications.CONDICION.value:
            return self.extract_condition(section)

    def extract_table(self, section: Section) -> Section:
        """Evaluate the TABLE section."""
        # TODO: use a threshold
        section_words = Tokenizer.tokenize_question(section.text)
        max_similarity = ("", 0)

        for phrase1 in section_words:
            for table in self.evaluator.database.get_all_table_names():
                phrase2 = table
                embeddings = self.model.encode([phrase1, phrase2])
                similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
                if similarity > max_similarity[1]:
                    max_similarity = (phrase2, similarity)

        return [
            Section(
                max_similarity[0],
                section.classification,
                section.right_context,
                section.left_context,
            )
        ]

    def extract_attributes(self, section: Section) -> list[Section]:
        """Evaluate the ATTRIBUTE section."""
        section_words = Tokenizer.tokenize_attributes(section.text)
        attributes_found = []
        tables_found = []
        for phrase1 in section_words:
            for (column, table) in self.evaluator.database.get_all_attribute_table_pairs():
                phrase2 = column.name
                embeddings = self.model.encode([phrase1, phrase2])
                similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

                if similarity >= self.attribute_threshold:
                    attributes_found.append(column.name)
                    tables_found.append(table.name)

        attributes_found = set(attributes_found)
        if len(attributes_found) == 0:
            return []

        output = [
            Section(
                attribute,
                section.classification,
                section.right_context,
                section.left_context,
            )
            for attribute in attributes_found
        ]
        tables = [
            Section(t, Classifications.TABLA.value, "", "") for t in set(tables_found)
        ]
        output.extend(tables)

        return output

    def extract_condition(self, section: Section) -> list[Condition]:
        """Extracts a condition from a section"""

        # Extract operators
        operators = self.operator_extractor.extract_exact_match(section.text)

        # Assume that the value extractor contains rules with
        # classification ATR_CONDICION y VALOR
        extracted_values = self.value_extractor.extract(section.text)

        # Filter by conditional value and conditional attribute
        possible_conditional_values = [
            section
            for section in extracted_values
            if section.classification == ClassNames.CONDITIONAL_VALUE.value
        ]
        possible_conditional_attributes = [
            section
            for section in extracted_values
            if section.classification == ClassNames.CONDITIONAL_ATTRIBUTE.value
        ]

        no_conditional_values = len(possible_conditional_values) == 0
        no_conditional_attributes = len(possible_conditional_attributes) == 0
        if no_conditional_attributes and no_conditional_values:
            return []

        # Generate condition
        if len(operators) == 0:
            # Default behavior
            operators = ["="]

        obtained_conditions = []
        obtained_conditional_attributes = []
        obtained_conditional_values = []
        operators = set(operators)

        # NOTE: this is a combinatory problem, it isn't necessary to go through a for loop when the results will be the same
        # NOTE: There is no best conditional attr/value, only valid ones
        for operator in operators:
            best_conditional_attribute = []

            if possible_conditional_attributes:
                best_conditional_attribute = (
                    self.get_most_probable_conditional_attribute(
                        possible_conditional_attributes
                    )
                )
                if possible_conditional_values:
                    for attribute in best_conditional_attribute:
                        for val in possible_conditional_values:
                            value = val.text
                            # best_conditional_value = best_conditional_value.replace(
                            #    " ", "_"
                            # )
                            obtained_conditions.append(
                                Condition(
                                    attribute,
                                    value,
                                    operator,
                                )
                            )

            # Generate condition
            if not best_conditional_attribute:
                return []

            obtained_conditions = self.remove_condition_duplicates(obtained_conditions)

        return obtained_conditions

    def get_most_probable_conditional_attribute(
        self, conditional_attribute_or_value: list[Section]
    ) -> str:

        attributes = []
        for conditionals in conditional_attribute_or_value:
            possible_conditional_attributes_or_values = Tokenizer.tokenize_question(
                conditionals.text
            )

            for attr_or_val in possible_conditional_attributes_or_values:
                phrase1 = attr_or_val
                for attribute in self.evaluator.database.get_all_attributes():
                    phrase2 = attribute.name
                    embeddings = self.model.encode([phrase1, phrase2])
                    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
                    if similarity > self.attribute_threshold:
                        attributes.append(phrase2) # .replace(" ", "_")
        probable_attr = []
        if attributes:
            probable_attr = attributes

        return probable_attr

    def remove_condition_duplicates(self, conditions):
        """Remove duplicates from a list of Condition objects."""
        seen = set()
        unique_conditions = []
        for cond in conditions:
            if cond not in seen:
                unique_conditions.append(cond)
                seen.add(cond)
        return unique_conditions
