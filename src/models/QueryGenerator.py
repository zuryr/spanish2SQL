from SectionExtractor import SectionExtractor
from Database import Database
from Query import Query
from SemanticEvaluator import SemanticEvaluator
from Section import Section
from Table import Table
from Column import Column
from Condition import Condition
from TextPipeline import TextPipeline


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

        # TODO: filter sections by classification

        # TODO: generate combinations of query elements and save in queries
        possible_triplets = self.section_extractor.generate_triplets(cleaned_sections)

        generated_queries = []

        for triplet in possible_triplets:
            query = self.generate_query_from_triplet(triplet)
            generated_queries.append(query)

        # TODO: evaluate queries and conserve those that are semantically correct
        final = []
        for query in generated_queries:
            if self.evaluator.query_is_correct(query):
                final.append(query)

        return final

    def generate_query_from_triplet(self, triplet: tuple[Section]) -> Query:
        """
        Generates a semantically valid query from a triplet of sections.

        Args:
            triplet: tuple containing three sections (TABLA, ATRIBUTO, CONDICION)
            evaluator: Type of semantic evaluator
        Returns:
            A Query object representing the generated query.
        """
        
        # Evaluate sections using the selected evaluator
        table, attribute, condition = triplet
        table_name, attribute_name, condition_text = table.text, attribute.text, condition.text

        # Check if the table exists in the database
        if not table_name:
            return None

        # Get table and column objects
        table = self.database.get_table_by_name(table_name)
        column = None
        if attribute_name:
            column = table.get_column_by_name(attribute_name)

        # Convert condition text into Condition object
        condition = None
        # if condition_text:
        #     condition = Condition(condition_text)

        # Return Query object
        return Query(table=table, columns=[column], condition=condition)
                
            
        