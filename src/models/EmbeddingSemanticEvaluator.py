import nltk
from nltk.corpus import wordnet as wn
from Section import Section

nltk.download('wordnet')

class EmbeddingSemanticEvaluator:
    """Semantic evaluator based on word embeddings."""

    def __init__(self, database):
        self.database = database  # Database instance containing schema information

    def evaluate_table(self, section: Section) -> str:
        """Evaluate the TABLE section."""
        table_name = section.text
        if wn.synsets(table_name, pos=wn.NOUN):
            return table_name
        else:
            return None

    def evaluate_attribute(self, section: Section, table_name: str) -> str:
        """Evaluate the ATTRIBUTE section."""
        attribute_name = section.text
        if table_name and wn.synsets(attribute_name, pos=wn.NOUN):
            return attribute_name
        else:
            return None

    def evaluate_condition(self, section: Section, table_name: str) -> str:
        """Evaluate the CONDITION section."""
        condition_text = section.text
        # Aquí puedes implementar la lógica para validar la condición
        return condition_text if condition_text else "Undefined"

    def evaluate_sections(self, triplet: tuple[Section]) -> tuple[str]:
        """Evaluate all sections in the triplet."""
        table_section, attribute_section, condition_section = triplet
        table_name = self.evaluate_table(table_section)
        attribute_name = self.evaluate_attribute(attribute_section, table_name)
        condition_text = self.evaluate_condition(condition_section, table_name)
        return table_name, attribute_name, condition_text
