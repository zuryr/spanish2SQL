import re


class Tokenizer:
    @staticmethod
    def tokenize_question(question: str) -> list[str]:
        """Tokenizes a question on whitespaces and special characters (accents and Ñ characters excluded)"""
        return re.findall(r"[\wáéíóúñ]+|[^\wáéíóúñ\s]", question)
