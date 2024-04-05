import spacy
from Section import Section
from Database import Database

nlp = spacy.load("es_core_news_md") 

class EmbeddingSemanticEvaluator:
    """Semantic evaluator based on word embeddings."""

    def __init__(self, database: Database):
        self.database = database  # Database instance containing schema information

    def evaluate_table(self, section: Section) -> str:
        """Evaluate the TABLE section."""
        section_words = section.text.split()
        max_similarity = ('', 0)
        
        for word in section_words:
            doc1 = nlp(word)
            for table in self.database.get_all_table_names():
                doc2 = nlp(table)
                similarity = doc2.similarity(doc1)
                if similarity > max_similarity[1]:
                    max_similarity = (str(doc2), similarity)
                
        return max_similarity[0]

    def evaluate_attribute(self, section: Section, table_name: str) -> str:
        """Evaluate the ATTRIBUTE section."""
        section_words = section.text.split()
        max_similarity = ('', 0)

        for word in section_words:
            doc1 = nlp(word)
            for column in self.database.get_all_attributes_from_table(table_name):
                doc2 = nlp(column.name)
                similarity = doc2.similarity(doc1)
                if similarity > max_similarity[1]:
                    max_similarity = [str(doc2), similarity]
                    
        return max_similarity[0]

    def evaluate_condition(self, section: Section, table_name: str) -> str:
        """Evaluate the CONDITION section."""
        condition_text = section.text
        # Aquí puedes implementar la lógica para validar la condición
        return condition_text if condition_text else None

    def evaluate_sections(self, triplet: tuple[Section]) -> tuple[str]:
        """Evaluate all sections in the triplet."""
        table_section, attribute_section, condition_section = triplet
        table_name = self.evaluate_table(table_section)
        attribute_name = self.evaluate_attribute(attribute_section, table_name)
        condition_text = self.evaluate_condition(condition_section, table_name)
        return table_name, attribute_name, condition_text
