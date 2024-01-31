from src.models.Database import Database
from src.models.Query import Query
from src.models.SemanticEvaluator import SemanticEvaluator


class QueryGenerator:
    """
    Generates semantically correct queries using information about a specific database.
    """

    def __init__(self, database: Database, evaluator: SemanticEvaluator):
        """
        Creates an instance of a query generator for a specific database.

        Args:
            database: schema to generate the queries respect with
            evaluator: previously initialized semantic evaluator with the same database
        """

    def generate_queries(self, natural_language_query: str) -> list[Query]:
        """
        Generates all the semantically valid (but not necessarily correct) queries that match the NL query.

        Args:
            natural_language_query: query in natural language about data in the database
        Returns:
            A list of all the semantically valid (but not necessarily correct) queries that match the NL query.
        """
