from Condition import Condition
from Database import Database
from Query import Query
from Section import Section
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator
from TextPipeline import TextPipeline
from src.models.Enums.Classifications import Classifications


class QueryGenerator:
    """
    Generates semantically correct queries using information about a specific database.
    """

    def __init__(self, database: Database, evaluator: SemanticEvaluator, section_extractor: SectionExtractor, pipeline: TextPipeline):
        """
        Creates an instance of a query generator for a specific database.

        Args:
            database: schema to generate the queries respect with
            evaluator: previously initialized semantic evaluator with the same database
            section_extractor: instance of SectionExtractor for extracting relevant sections
            pipeline: instance of TextPipeline
        """
        self.database = database
        self.section_extractor = section_extractor
        self.evaluator = evaluator
        self.pipeline = pipeline

    def generate_queries(self, natural_language_query: str) -> list[Query]:
        """
        Generates all the semantically valid (but not necessarily correct) queries that match the NL query.

        Args:
            natural_language_query: query in natural language about data in the database
        Returns:
            A list of all the semantically valid (but not necessarily correct) queries that match the NL query.
        """
        # Extract relevant sections from the natural language query
        extracted_sections = self.section_extractor.extract(natural_language_query)

        #TODO: clean sections with pipelines
        cleaned_sections = self.pipeline.transform_sections(extracted_sections)

        print(cleaned_sections)

        # TODO: filter sections by classification

        # TODO: generate combinations of query elements and save in queries
        # TODO: evaluate queries and conserve those that are semantically correct
        possible_triplets = self.generate_triplets(cleaned_sections)

        generated_queries = []

        for triplet in possible_triplets:
            query = self.generate_query_from_triplet(triplet)
            # if self.evaluator.query_is_correct(query):
            #     generated_queries.append(query)
            if query is not None:
                generated_queries.append(query)

        return generated_queries

    def generate_triplets(self, cleaned_sections: list[Section | Condition]) -> list[list[Section | Condition] | list[Section | Condition | None]]:
        """
        Generates all possible valid triplets of sections.

        Args:
            extracted_sections: list of extracted sections

        Returns:
            A list of tuples, where each tuple represents a valid triplet of sections.
        """

        possible_triplets = []

        found_tables = []
        found_attributes = []
        found_condition = []

        for section in cleaned_sections:
            if type(section) is Section:
                if section.classification in Classifications.TABLA.value:
                    found_tables.append(section)
                if section.classification in Classifications.ATRIBUTO.value:
                    found_attributes.append(section)
            else:
                found_condition.append(section)

        for table in found_tables:
            for attribute in found_attributes:
                for condition in found_condition:
                    possible_triplets.append([table, attribute, condition])
                possible_triplets.append([table,attribute, None])
            possible_triplets.append([table, None, None])

        return possible_triplets

    def generate_query_from_triplet(self, triplet: tuple[Section | Condition]) -> Query:
        """
        Generates a semantically valid query from a triplet of sections.

        Args:
            triplet: tuple containing three sections (TABLA, ATRIBUTO, CONDICION)
            evaluator: Type of semantic evaluator
        Returns:
            A Query object representing the generated query.
        """

        table_section, column_section, condition_section = triplet

        table_name = None
        column_name = None
        condition_name = None

        if table_section:
            table_name = table_section.text

        if column_section:
            column_name = column_section.text

        if condition_section:
            condition_name = condition_section.condition_to_string()

        return Query(table_name, [column_name], condition_name)

            
        