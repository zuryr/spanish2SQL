from SectionExtractor import SectionExtractor
from Database import Database
from Query import Query
from SemanticEvaluator import SemanticEvaluator
from Section import Section
from Table import Table
from Column import Column
from Condition import Condition


class QueryGenerator:
    """
    Generates semantically correct queries using information about a specific database.
    """

    def __init__(self, database: Database, evaluator: SemanticEvaluator, section_extractor: SectionExtractor):
        """
        Creates an instance of a query generator for a specific database.

        Args:
            database: schema to generate the queries respect with
            evaluator: previously initialized semantic evaluator with the same database
            section_extractor: instance of SectionExtractor for extracting relevant sections
        """
        self.database = database
        self.evaluator = evaluator
        self.section_extractor = section_extractor

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

        #TODO: evaluate condition and column sections

        # Generate possible valid triplets of sections
        possible_triplets = self.section_extractor.generate_triplets(extracted_sections)

        generated_queries = []

        # Iterate through possible triplets and generate queries
        for triplet in possible_triplets:
            # TODO: Implement the logic to generate queries based on the triplet
            query = self.generate_query_from_triplet(triplet)
            if query:
                generated_queries.append(query)

        return generated_queries

    def generate_query_from_triplet(self, triplet: tuple[Section]) -> Query:
        """
        Generates a semantically valid query from a triplet of sections.

        Args:
            triplet: tuple containing three sections (TABLA, ATRIBUTO, CONDICION)
        Returns:
            A Query object representing the generated query.
        """
        
        table_section, attribute_section, condition_section = triplet

        # Extract relevant information from sections
        table_name = table_section.text
        attribute_name = attribute_section.text
        condition_text = condition_section.text

        # Check if the table exists in the database
        # TODO: Implement logic to evaluate the existence of the table
        # if table_name and self.evaluator.table_exists(table_name):
        if not table_name:

            return None

        # table = self.database.get_table_by_name(table_name)
        table: Table = Table(table_name, columns=None)

        # Check if the attribute exists in the table
        # TODO: Given a table, implement logic to extract the existence of the column
        # if attribute_name and self.evaluator.column_exists(table, attribute_name):
        if not attribute_name:

            return Query(table=table, columns=[None], condition=None)

        # column = table.get_column_by_name(attribute_name)
        column: Column = Column(attribute_name, 'char')

        if not condition_text:

            # TODO: Implement logic to convert condition_text into a Condition object
            # condition = Condition(...)  # Replace with the actual Condition object

            return Query(table=table, columns=[column], condition=None)
        
        return Query(table=table, columns=[column], condition=None)
                
            
        