import re


class Tokenizer:
    @staticmethod
    def tokenize_question(question: str) -> list[str]:
        """Tokenizes a question on whitespaces and special characters (accents and Ñ characters excluded)"""
        return re.findall(r"[\wáéíóúñ]+|[^\wáéíóúñ\s]", question)

    @staticmethod
    def tokenize_condition(condition: str) -> list[str]:
        """Tokenizes a simple condition into its parts"""
        m = re.findall(r"""[\wáéíóúñ"\s,'.]+|[=!><]+""", condition)
        tokens = [sub_condition.strip() for sub_condition in m]
        if len(tokens) != 3:
            return ["", "", ""]
        return tokens

    @staticmethod
    def tokenize_attributes(attributes: str) -> list[str]:
        """Tokenizes a text potentially containing attributes on commas and whitespaces"""
        m = re.findall(r"[a-zA-Záéíóúñ]+(?=[\s,]|$)", attributes)
        # y its a common nexus when mentioning attributes
        return [attr for attr in m]
