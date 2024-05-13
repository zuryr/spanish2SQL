import re

from Query import Query


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
        condition = ""
        if match.group(3) is not None:
            condition = match.group(3)

        return Query(table_name, column_names, condition)
