from typing import List

from Rule import Rule
from Section import Section


class SectionExtractor:
    """
    Extracts potentially relevant sections following a given set of rules.

    Attributes:
        rules: list of rules that will be used to section respect with
    """

    def __init__(self, rules: List[Rule]):
        """
        Initialize an instance with a list of rules.

        Args:
            rules: list of rules that will be used to section respect with
        """
        self.rules = rules

    def extract(self, text: str) -> List[Section]:
        """
        Extracts all the possible relevant sections that match with the rules provided.

        Args:
            text: string to perform the extraction respect with

        Returns:
            A list containing the sections that matches the rules in the extractor.
        """
        extracted_sections = []
        for rule in self.rules:
            try:
                extracted_section = rule.extract(text)
                if extracted_section is not None:
                    extracted_sections.append(extracted_section)
            except ValueError as e:
                # Handle exception (e.g., rule delimiters not found)
                print(e)

        return extracted_sections
    
    def extract_exact_match(self) -> List[str]:
        classified_rules = []
        for rule in self.rules:
            if self.doesMatch(rule) == True:
                classified_rules.append(rule)
        return classified_rules
    

# Example of how to use SectionExtractor and save results to CSV
# # rules = [
# #     Rule(left_context="los", right_context="que", classification="TABLA")
# # ]
# rules_file_path = "src\data\ctx_general.csv" 
# rules = CsvHandler.load_rules_from_csv(rules_file_path)

# section_extractor = SectionExtractor(rules=rules)
# # section_extractor = SectionExtractor(rules=rules, output_file_path=output_file_path) # with fixed rules

# # Test sentences with SQL queries in natural language
# sentences = [
#     "Selecciona los jugadores que juega en el america.",
#     "Muestra todos los estudiantes que estudian en la escuela.",
#     "Encuentra los animales que viven en Africa."
# ]

# timestamp = datetime.now().strftime("%Y_%m_%d%H_%M_%S")
# file_output_name = f"results_rule_extraction_{timestamp}.csv"
# output_file_path = f"src/data/results/{file_output_name}"

# # Extract sections from each sentence
# for sentence in sentences:
#     extracted_sections = section_extractor.extract(sentence)

#     # Save extraction results to CSV only if sections are found
#     if extracted_sections:
#         CsvHandler.save_results_to_csv(output_file_path, sentence, extracted_sections)
