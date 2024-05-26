import re

from Section import Section


class Rule:
    """
    Rule to perform section extraction.
    """

    def __init__(
        self,
        left_context: str,
        right_context: str,
        classification: str,
        exact_match=None,
    ):
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
        final_section = Section("", "", "", "")
        escaped_left_context = re.escape(self.left_context)
        escaped_right_context = re.escape(self.right_context)
        # escaped_right_context = escaped_right_context.replace("\\", "")
        # escaped_right_context = escaped_right_context.replace(".", "")
        pattern = f"(?:\\s|^){escaped_left_context}(?:\\s)(.*?)(?:\\s){escaped_right_context}(?:\\s|$)"
        matches = re.search(pattern, text)
        if matches is None:
            return final_section
        extracted_text = matches.group(1)
        return Section(
            classification=self.classification,
            text=extracted_text,
            left_context=self.left_context,
            right_context=self.right_context,
        )

    def does_match(self, text: str) -> bool:

        text_without_end = text.replace("end", "")

        # coincidence_index = text_without_end.find(self.exact_match)
        coincidence = re.search(r"\b" + self.exact_match + r"\b", text_without_end)

        return coincidence != None


# # Example of how to use the Rule class
# rule_example = Rule(left_context="los", right_context="en", classification="TABLA")
# text_example = "Selecciona los jugadores que juegan en el america."
# extracted_section = rule_example.extract(text_example)

# if extracted_section is not None:
#     print(f"Classification: {extracted_section.classification}")
#     print(f"Extracted content: {extracted_section.text}")
# else:
#     print("Left or right delimiter not found, nothing extracted.")
