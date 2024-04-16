import spacy

from Section import Section
from src.models.SectionExtractor import SectionExtractor
from src.models.SemanticEvaluator import SemanticEvaluator
from src.models.TextPipeline import TextPipeline
from src.models.enums.classifications import Classifications

nlp = spacy.load("es_core_news_md")


class EmbeddingSemanticEvaluator(TextPipeline):
    """Semantic evaluator based on word embeddings."""

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

    def evaluate_attribute(self, section: Section) -> Section:
        """Evaluate the ATTRIBUTE section."""
        section_words = section.text.split()
        max_similarity = ('', 0)

        for word in section_words:
            doc1 = nlp(word)
            for column in self.evaluator.database.get_all_attributes():
                doc2 = nlp(column.name)
                similarity = doc2.similarity(doc1)
                if similarity > max_similarity[1]:
                    max_similarity = [str(doc2), similarity]

        return Section(max_similarity[0], section.classification, section.right_context, section.left_context)

    def evaluate_condition(self, section: Section) -> Section:
        """Evaluate the CONDITION section."""
        condition = section
        # TODO: Implement logic to evluate condition
        return condition

