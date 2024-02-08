import csv
from datetime import datetime
from typing import List
from Rule import Rule
from Section import Section

class SectionExtractor:
    """
    Extracts potentially relevant sections following a given set of rules.

    Attributes:
        rules: list of rules that will be used to section respect with
    """

    def __init__(self, rules: List[Rule], output_file_path: str = None):
        """
        Initialize an instance with a list of rules.

        Args:
            rules: list of rules that will be used to section respect with
            output_file_path: optional path to the CSV file for storing extraction results
        """
        self.rules = rules
        self.output_file_path = output_file_path

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

        # Save extraction results to CSV only if sections are found and output_file_path is provided
        if self.output_file_path and extracted_sections:
            self.save_results_to_csv(text, extracted_sections)

        return extracted_sections

    def save_results_to_csv(self, input_text: str, extracted_sections: List[Section]):
        """
        Saves extraction results to a CSV file.

        Args:
            input_text: original input text
            extracted_sections: list of Section objects
        """ 
        with open(self.output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Input Text", "Left Context", "Right Context", "Extracted Text", "Classification"]
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only if the file is empty
            if csvfile.tell() == 0:
                csv_writer.writeheader()

            for section in extracted_sections:
                csv_writer.writerow({
                    "Input Text": input_text,
                    "Left Context": section.left_context,
                    "Right Context": section.right_context,
                    "Extracted Text": section.text,
                    "Classification": section.classification
                })
                
    def load_rules_from_csv(self, file_path: str) -> List[Rule]:
        """
        Loads rules from a CSV file.

        Args:
            file_path: path to the CSV file containing rules
        Returns:
            List of Rule objects
        """
        rules = []
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if len(row) == 3:
                    rule = Rule(left_context=row[0], right_context=row[1], classification=row[2])
                    rules.append(rule)
                else:
                    print("Invalid rule format in CSV:", row)
        return rules

# Example of how to use SectionExtractor and save results to CSV
rules = [
    Rule(left_context="los", right_context="que", classification="TABLA")
]

timestamp = datetime.now().strftime("%Y_%m_%d%H_%M_%S")

rules_file_path = "src\data\ctx_general.csv"

file_output_name = f"results_rule_extraction_{timestamp}.csv"
output_file_path = f"src/data/results/{file_output_name}"

section_extractor = SectionExtractor(rules=SectionExtractor(rules=None).load_rules_from_csv(rules_file_path), output_file_path=output_file_path) # with CSV rules
# section_extractor = SectionExtractor(rules=rules, output_file_path=output_file_path) # with fixed rules

# Test sentences with SQL queries in natural language
sentences = [
    "Selecciona los jugadores que juegan en el america.",
    "Muestra todos los estudiantes que estudian en la escuela.",
    "Encuentra los animales que viven en Africa."
]

# Extract sections from each sentence and save results to CSV
for sentence in sentences:
    extracted_sections = section_extractor.extract(sentence)
