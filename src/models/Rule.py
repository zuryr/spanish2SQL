import re

from Section import Section

class Rule:
    """
    Rule to perform section extraction.
    """

    def __init__(self, left_context: str, right_context: str, classification: str, exact_match = None):
        """
        Initializes an instance with the delimiters and classification to perform section extraction.

        Args:
            left_context: keyword where the relevant section starts (exclusive)
            right_context: keyword where the relevant section ends (exclusive)
                           use "end" to indicate no delimiter
            classification: classification assigned to sections following this rule
        """
        if exact_match != None:
            self.exact_match = exact_match
        self.left_context = left_context
        self.right_context = right_context
        self.classification = classification

    def extract(self, text: str) -> Section:
        """
        Extracts the section of the text that matches the rule.

        Args:
            text: string to perform the extraction with
        Returns:
            Section of the text that follows the rule (excluding the delimiters)
        """
        start_index = text.find(f" {self.left_context} ")  # Include spaces before and after left_context
        if start_index == -1:
            return None  # No left delimiter found, return None

        if self.right_context == "?":
            end_index = text.find("?", start_index + len(self.left_context))
        elif self.right_context == "end":
            coincidence = re.search(r'\b' + "end", text)
            if coincidence:
                end_index = len(text) - 3
            else:
                end_index = len(text)
        else:
            searching_word = f" {self.right_context} "
            end_index = text.find(searching_word, start_index + len(self.left_context))

        if end_index == -1:
            return None  # No right delimiter found, return None

        extracted_text = text[start_index + len(self.left_context) + 1:end_index].strip()
        return Section(classification=self.classification, text=extracted_text, left_context=self.left_context, right_context=self.right_context)

    def does_match(self, text: str) -> bool:

        text_without_end = text.replace("end", "")

        # coincidence_index = text_without_end.find(self.exact_match)
        coincidence = re.search(r'\b' + self.exact_match + r'\b', text_without_end)

        if coincidence:
            return True
        return False

# # Example of how to use the Rule class
# rule_example = Rule(left_context="los", right_context="en", classification="TABLA")
# text_example = "Selecciona los jugadores que juegan en el america."
# extracted_section = rule_example.extract(text_example)

# if extracted_section is not None:
#     print(f"Classification: {extracted_section.classification}")
#     print(f"Extracted content: {extracted_section.text}")
# else:
#     print("Left or right delimiter not found, nothing extracted.")
