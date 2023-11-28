import sys
import json

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #    raise ValueError("More or less than 2 arguments provided. Aborting")

    input_path = "../../data/external/spider/train_others.json"  # sys.argv[0]
    output_path = "./clean.txt"  # sys.argv[1]

    input_file = open(input_path)
    output_file = open(output_path, "w+")
    input_json = json.load(input_file)
    for obj in input_json:
        question = obj["question"]
        question_dont_have_terminal_char = question[-1] != "." and question[-1] != "?"
        if question_dont_have_terminal_char:
            question += "?"
        output_file.write(f"{question}\n")

    input_file.close()
    output_file.close()
