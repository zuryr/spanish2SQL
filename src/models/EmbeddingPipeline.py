import spacy

from Section import Section
from src.models.Column import Column
from src.models.Condition import Condition
from src.models.SectionExtractor import SectionExtractor
from src.models.SemanticEvaluator import SemanticEvaluator
from src.models.TextPipeline import TextPipeline
from src.models.Enums.Classifications import Classifications

nlp = spacy.load("es_core_news_md")


class EmbeddingPipeline(TextPipeline):
    """Semantic evaluator based on word embeddings."""

    def __init__(self, evaluator: SemanticEvaluator, extractor: SectionExtractor, threshold: float):
        super().__init__(evaluator, extractor, threshold)

    def transform_sections(self, text: list[Section]) -> list[Section | Condition]:
        cleaned_sections = []
        for section in text:
            cleaned_sections.extend(self.transform_section(section))
        return cleaned_sections

    def transform_section(self, section: Section) -> list[Section | Condition]:
        if section.classification == Classifications.TABLA.value:
            return self.evaluate_table(section)
        if section.classification == Classifications.ATRIBUTO.value:
            return self.evaluate_attribute(section)
        if section.classification == Classifications.CONDICION.value:
            return self.evaluate_condition(section)

    def evaluate_table(self, section: Section) -> list[Section]:
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

        return [Section(max_similarity[0], section.classification, section.right_context, section.left_context)]

    def evaluate_attribute(self, section: Section) -> list[Section]:
        """Evaluate the ATTRIBUTE section."""
        section_words = section.text.split()
        best_words = []
        for word in section_words:
            doc1 = nlp(word)
            for column in self.evaluator.database.get_all_attributes():
                doc2 = nlp(column.name)
                similarity = doc2.similarity(doc1)
                if similarity >= self.threshold:
                     best_words.append(Section(str(doc2), section.classification, section.right_context, section.left_context))

        return best_words

    def evaluate_condition(self, section: Section) -> list[Condition]:
        """Evaluate the CONDITION section."""
        # TODO: Implement logic to evaluate condition
        columnObserved = Column("pais", "varchar")
        condition = Condition(columnObserved, '500', '<')
        return [condition]

