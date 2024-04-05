from Database import Database
from Section import Section
from Table import Table
from Column import Column
from Condition import Condition

class FixedSemanticEvaluator:
    """Semantic evaluator based on fixed rules."""

    def __init__(self, database: Database):
        self.database = database  # Database instance containing schema information

    def evaluate_table(self, section: Section) -> str:
        """Evaluate the TABLE section."""
        table_name = section.text
        if self.database.table_exists(table_name):
            return table_name
        else:
            return None

    def evaluate_attribute(self, section: Section, table_name: str) -> str:
        """Evaluate the ATTRIBUTE section."""
        attribute_name = section.text
        if table_name and self.database.column_exists(table_name, attribute_name):
            return attribute_name
        else:
            return None

    def evaluate_condition(self, section: Section, table_name: str) -> str:
        """Evaluate the CONDITION section."""
        condition_text = section.text
        # TODO: Implement logic to evluate condition
        return condition_text if condition_text else None

    def evaluate_sections(self, triplet: tuple[Section]) -> tuple[str]:
        """Evaluate all sections in the triplet."""
        table_section, attribute_section, condition_section = triplet
        table_name = self.evaluate_table(table_section)
        attribute_name = self.evaluate_attribute(attribute_section, table_name)
        condition_text = self.evaluate_condition(condition_section, table_name)
        return table_name, attribute_name, condition_text
