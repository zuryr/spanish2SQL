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
        start_index = text.find(self.left_context)
        end_index = text.find(self.right_context, start_index + len(self.left_context))

        if start_index != -1 and end_index != -1:
            extracted_text = text[start_index + len(self.left_context):end_index].strip()
            return Section(classification=self.classification, text=extracted_text)
        else:
            raise ValueError("Rule delimiters not found in the text")
        
# Example of how to use the Rule class
rule_example = Rule(left_context="los", right_context="que", classification="TABLA")
text_example = "Lorem ipsum dolor sit amet, los consectetur adipiscing elit, que sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
extracted_section = rule_example.extract(text_example)
print(f"Classification: {extracted_section.classification}")
print(f"Extracted content: {extracted_section.text}")

