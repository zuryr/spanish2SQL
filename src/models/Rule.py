from Section import Section

class Rule:
    """
    Rule to perform section extraction.
    """

    def __init__(self, left_context: str, right_context: str, classification: str):
        """
        Initializes an instance with the delimiters and classification to perform section extraction.

        Args:
            left_context: keyword where the relevant section starts (exclusive)
            right_context: keyword where the relevant section ends (exclusive)
                           use "end" to indicate no delimiter
            classification: classification assigned to sections following this rule
        """
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
            end_index = len(text)
        else:
            end_index = text.find(self.right_context, start_index + len(self.left_context))

        if end_index == -1:
            return None  # No right delimiter found, return None

        extracted_text = text[start_index + len(self.left_context) + 1:end_index].strip()
        return Section(classification=self.classification, text=extracted_text, left_context=self.left_context, right_context=self.right_context)

# # Example of how to use the Rule class
# rule_example = Rule(left_context="los", right_context="en", classification="TABLA")
# text_example = "Selecciona los jugadores que juegan en el america."
# extracted_section = rule_example.extract(text_example)

# if extracted_section is not None:
#     print(f"Classification: {extracted_section.classification}")
#     print(f"Extracted content: {extracted_section.text}")
# else:
#     print("Left or right delimiter not found, nothing extracted.")
