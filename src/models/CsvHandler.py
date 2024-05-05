import csv
from typing import List
from Rule import Rule
from Section import Section

class CsvHandler:
    """
    Class to handle operations related to CSV files.
    """

    @staticmethod
    def load_general_rules_from_csv(file_path: str) -> List[Rule]:
        """
        Loads rules from a CSV file.

        Args:
            file_path: path to the CSV file containing rules
        Returns:
            List of Rule objects
        """
        rules = []
        with open(file_path, 'r', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if len(row) == 3:
                    rule = Rule(left_context=row[0], right_context=row[1], classification=row[2])
                    rules.append(rule)
                else:
                    print("Invalid rule format in CSV:", row)
        return rules

    @staticmethod
    def load_operators_rules_from_csv(file_path: str) -> List[Rule]:
        """
        Loads rules from a CSV file.

        Args:
            file_path: path to the CSV file containing rules
        Returns:
            List of Rule objects
        """
        rules = []
        with open(file_path, 'r', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if len(row) == 2:
                    rule = Rule(left_context='', right_context='', exact_match=row[1], classification=row[0])
                    rules.append(rule)
                else:
                    print("Invalid rule format in CSV:", row)
        return rules

    @staticmethod
    def load_values_rules_from_csv(file_path: str) -> List[Rule]:
        """
        Loads rules from a CSV file.

        Args:
            file_path: path to the CSV file containing rules
        Returns:
            List of Rule objects
        """
        rules = []
        with open(file_path, 'r', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if len(row) == 3:
                    rule = Rule(left_context=row[0], right_context=row[1], classification=row[2])
                    rules.append(rule)
                else:
                    print("Invalid rule format in CSV:", row)
        return rules

    @staticmethod
    def save_results_to_csv(output_file_path: str, input_text: str, extracted_sections: List[Section]):
        """
        Saves extraction results to a CSV file.

        Args:
            output_file_path: path to the CSV file for storing extraction results
            input_text: original input text
            extracted_sections: list of Section objects
        """
        with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
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