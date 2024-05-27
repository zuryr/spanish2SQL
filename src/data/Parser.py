import re

from Query import Query
from Condition import Condition
from Tokenizer import Tokenizer

class Parser:
    @staticmethod
    def str_to_query(query_str: str) -> Query:
        """
        Turns a string containing a condition into a query object
        """
        query_str = re.sub(r"\s{2,}", " ", query_str)
        regex = re.compile(
            r"^SELECT\s+([\w ,*]+?)\s+FROM\s+(\w+?)(?:\s+WHERE\s+(.+))?;?$",
            re.MULTILINE,
        )
        match = re.search(regex, query_str)

        column_names = match.group(1).replace(" ", "").split(",")
        table_name = match.group(2)
        condition = Condition("","","")
        if match.group(3) is not None:
            condition_elements = Tokenizer.tokenize_condition(match.group(3))
            condition = Condition(condition_elements[0],condition_elements[2],condition_elements[1])

        return Query(table_name, column_names, condition)
