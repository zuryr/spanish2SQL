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

    def __init__(self, database: Database, section_extractor: SectionExtractor):
        """
        Creates an instance of a query generator for a specific database.

        Args:
            database: schema to generate the queries respect with
            evaluator: previously initialized semantic evaluator with the same database
            section_extractor: instance of SectionExtractor for extracting relevant sections
        """
        self.database = database
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
        
        # Initialize the semantic evaluator and section extractor
        semantic_evaluators = ['fixed', 'word_processing', 'embeddings']
        
        generated_queries = []
        
        for evaluator_type in semantic_evaluators:
            evaluator = SemanticEvaluator(self.database, evaluator_type)

            # Iterate through possible triplets and generate queries
            for triplet in possible_triplets:
                query = self.generate_query_from_triplet(triplet, evaluator)
                if query:
                    generated_queries.append(query)

        return generated_queries

    def generate_query_from_triplet(self, triplet: tuple[Section], evaluator_type: SemanticEvaluator) -> Query:
        """
        Generates a semantically valid query from a triplet of sections.

        Args:
            triplet: tuple containing three sections (TABLA, ATRIBUTO, CONDICION)
            evaluator: Type of semantic evaluator
        Returns:
            A Query object representing the generated query.
        """
        
        # Evaluate sections using the selected evaluator
        table_name, attribute_name, condition_text = evaluator_type.evaluator.evaluate_sections(triplet)

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
        if condition_text:
            condition = Condition(condition_text)

        # Return Query object
        return Query(table=table, columns=[column], condition=condition)
                
            
        