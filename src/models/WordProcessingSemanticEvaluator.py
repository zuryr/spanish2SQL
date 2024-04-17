from Section import Section
from Table import Table
from Column import Column
from Condition import Condition
import nltk
from nltk.corpus import stopwords
import spacy

nltk.download('punkt')
nltk.download('stopwords')

class WordProcessingSemanticEvaluator:
    """Semantic evaluator based on word processing."""

    def __init__(self, database):
        self.database = database  # Database instance containing schema information
        self.nlp = spacy.load('es_core_news_sm')
        self.stop_words = set(stopwords.words('spanish'))

    def preprocess_text(self, text: str) -> str:
        """Preprocess the text by removing stop words, punctuation, and lemmatizing."""
        doc = self.nlp(text.lower())  # Tokenize and convert to lowercase
        filtered_tokens = [token.lemma_ for token in doc if token.is_alpha and token.text not in self.stop_words]
        return " ".join(filtered_tokens)

    def evaluate_table(self, section: Section) -> str:
        """Evaluate the TABLE section."""
        table_name = section.text
        processed_table_name = self.preprocess_text(table_name)
        if self.database.table_exists(processed_table_name):
            return table_name
        else:
            return None

    def evaluate_attribute(self, section: Section, table_name: str) -> str:
        """Evaluate the ATTRIBUTE section."""
        attribute_name = section.text
        processed_attribute_name = self.preprocess_text(attribute_name)
        if table_name and self.database.column_exists(table_name, processed_attribute_name):
            return attribute_name
        else:
            return None

    def evaluate_condition(self, section: Section, table_name: str) -> str:
        """Evaluate the CONDITION section."""
        condition_text = section.text
        processed_condition_text = self.preprocess_text(condition_text)
        # Here you can implement logic to validate the condition based on word processing
        return condition_text if condition_text else None

    def evaluate_sections(self, triplet: tuple[Section]) -> tuple[str]:
        """Evaluate all sections in the triplet."""
        table_section, attribute_section, condition_section = triplet
        table_name = self.evaluate_table(table_section)
        attribute_name = self.evaluate_attribute(attribute_section, table_name)
        condition_text = self.evaluate_condition(condition_section, table_name)
        return table_name, attribute_name, condition_text
