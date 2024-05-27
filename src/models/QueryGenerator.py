from itertools import combinations

from Condition import Condition
from Database import Database
from GroupStrategy import GroupStrategy
from Query import Query
from Section import Section
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator
from TextPipeline import TextPipeline
from Enums.Classifications import Classifications


class QueryGenerator:
    """
    Generates semantically correct queries using information about a specific database.
    """

    def __init__(
        self,
        database: Database,
        evaluator: SemanticEvaluator,
        section_extractor: SectionExtractor,
        pipeline: TextPipeline,
        group_strategy: GroupStrategy,
    ):
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
        self.group_strategy = group_strategy

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

        # Clean the sections with the pipeline
        cleaned_sections = self.pipeline.transform_sections(extracted_sections)

        # Generate combinations of query elements
        possible_triplets = self.generate_triplets(cleaned_sections)

        generated_queries = []

        for triplet in possible_triplets:
            query = self.generate_query_from_triplet(triplet)

            # evaluate queries and conserve those that are semantically correct
            if self.evaluator.query_is_correct(query):
                generated_queries.append(query)
            # generated_queries.append(query)

        unique_queries = self.remove_duplicates(generated_queries)

        return unique_queries

    def remove_duplicates(self, queries):
        """Remove duplicates from a list of Query objects."""
        seen = set()
        unique_queries = []
        for query in queries:
            if query not in seen:
                unique_queries.append(query)
                seen.add(query)
        return unique_queries

    def generate_triplets(
        self, cleaned_sections: list[Section, Condition]
    ) -> list[list[Section, Condition] | list[Section, Condition, None]]:
        """
        Generates all possible valid triplets of sections.

        Args:
            cleaned_sections: list of extracted sections

        Returns:
            A list of tuples, where each tuple represents a valid triplet of sections.
        """

        possible_triplets = []

        found_tables = []
        found_attributes = []
        found_condition = []

        all_columns = [Section("*",Classifications.ATRIBUTO.value,"","")]

        for section in cleaned_sections:
            if type(section) is Section:
                if section.classification in Classifications.TABLA.value:
                    found_tables.append(section)
                if section.classification in Classifications.ATRIBUTO.value:
                    found_attributes.append(section)
            elif section:
                found_condition.append(section)

        found_condition = list(set(found_condition))
        attribute_groups = self.group_strategy.group_attributes(found_attributes)

        for table in found_tables:
            for attribute_group in attribute_groups:
                for condition in found_condition:
                    possible_triplets.append([table, attribute_group, condition])
                possible_triplets.append([table, attribute_group, None])
            possible_triplets.append([table, all_columns, None])

        return possible_triplets

    def generate_query_from_triplet(self, triplet: tuple[Section, Condition]) -> Query:
        """
        Generates a semantically valid query from a triplet of sections.

        Args:
            triplet: tuple containing three sections (TABLA, ATRIBUTO, CONDICION)
        Returns:
            A Query object representing the generated query.
        """
        # TODO: condition instead of condition_str
        table_section, column_section, condition_section = triplet

        table_name = ""
        columns = []
        condition = Condition("", "", "")

        if table_section:
            table_name = table_section.text if table_section.text else ""

        if column_section:
            columns = [column.text for column in column_section]
            columns = list(set(columns))

        if condition_section:
            condition = condition_section

        return Query(table_name, columns, condition)
