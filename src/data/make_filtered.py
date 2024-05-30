import os
import pickle
import sys
import json

import Parser
from Query import Query

from Condition import Condition

EMPTY_CONDITION = Condition("", "", "", "")
AGG_OPS = ("NONE", "MAX", "MIN", "COUNT", "SUM", "AVG")
FILTERED_TOKENS = (
    "SELECT",
    "JOIN",
    "BETWEEN",
    "AND",
    "OR",
    "DISTINCT",
    "UNIQUE",
    "NOT",
    "LIKE",
    "IN",
    "AS",
)


def filter_questions(esp_queries, output_json_file, output_csv_file, input_json):
    output_json_file.write("[\n")
    for i, obj in enumerate(input_json):
        sql_info = obj["sql"]
        has_groupby = len(sql_info["groupBy"]) > 0
        has_having = len(sql_info["having"]) > 0
        has_orderby = len(sql_info["orderBy"]) > 0
        has_limit = sql_info["limit"] != None
        has_intersect = sql_info["intersect"] != None
        has_union = sql_info["union"] != None
        has_except = sql_info["except"] != None
        properties_medium_difficulty_or_more = [
            has_groupby,
            has_having,
            has_orderby,
            has_limit,
            has_intersect,
            has_union,
            has_except,
        ]
        # print(properties_medium_difficulty_or_more)
        medium_difficulty_or_more = False
        for has_property in properties_medium_difficulty_or_more:
            if has_property:
                medium_difficulty_or_more = True
                break

        if medium_difficulty_or_more:
            continue

        # second_token = obj["query_toks"][1]
        # if second_token in AGG_OPS:
        #     continue

        flag = False
        for token in obj["query_toks"][1:]:
            token = token.upper()
            if token in FILTERED_TOKENS or token in AGG_OPS:
                flag = True
                break

        if flag:
            continue

        obj["question"] = esp_queries[i]
        # Only questions csv
        output_csv_file.write(f"{obj['question']}")

        output_json_file.write(f"{json.dumps(obj, ensure_ascii=False)},\n")
    output_json_file.write("]")


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #    raise ValueError("More or less than 2 arguments provided. Aborting")

    input_path = "../../data/external/spider/train_spider.json"  # sys.argv[0]
    esp_path = "../../data/interim/out_esp.txt"
    output_path = "./out_json.json"  # sys.argv[1]
    output_csv_path = "./out_questions.txt"

    input_file = open(input_path)
    esp_file = open(esp_path, encoding="utf-8")
    esp_queries = esp_file.readlines()
    # output_json_file = open(output_path, "w+", encoding="utf-8")
    # output_csv_file = open(output_csv_path, "w+", encoding="utf-8")
    input_json = json.load(input_file)

    # filter_questions(esp_queries, output_json_file, output_csv_file, input_json)

    # get the current dataset for the current question
    json_path = "../../data/processed/tables_columns_spanish.json"
    json_data = {}

    db_file = open(json_path, "r", encoding="utf-8")
    db_data = json.load(db_file)
    db_file.close()

    queries_file = open(output_path, "r", encoding="utf-8")
    queries_data = json.load(queries_file)
    queries_file.close()

    # load databases into a dictionary
    databases = {}
    for db in db_data:
        db_name = db["db_id"]
        databases[db_name] = db

    # equivalent queries generation
    equivalent_queries = []

    for query in queries_data:
        # get the column names in the query
        query_obj = Parser.Parser.str_to_query(query["query"])
        db_name = query["db_id"]
        original_attributes = query_obj.columns
        query_obj.table = query_obj.table.lower()
        original_attributes = [element.lower() for element in original_attributes]
        # original_conditional_elements = query_obj.condition.split(" ")
        original_conditional_attribute = query_obj.condition.column_name.lower()

        current_db = databases[db_name]
        original_columns = current_db["column_names_original"]
        translated_columns = current_db["column_names"]
        original_tables = current_db["table_names_original"]
        translated_tables = current_db["table_names"]

        equivalent_attributes = []
        equivalent_conditional_attribute = ""
        equivalent_table = ""

        # get the equivalent in the translated dataset
        for i, column_info in enumerate(original_columns):
            # early stop when all elements have been found
            if len(original_attributes) == len(equivalent_attributes):
                break
            table_index, column_name = column_info
            column_name = column_name.lower()

            if column_name not in original_attributes:
                continue
            # avoiding repeated elements
            if column_name in equivalent_attributes:
                continue
            equivalent_attribute = translated_columns[i][1]
            equivalent_attributes.append(equivalent_attribute)

        for i, table_name in enumerate(original_tables):
            if table_name.lower() == query_obj.table:
                equivalent_table = translated_tables[i]
                break

        # early return if no condition is fouund
        if original_conditional_attribute == "":
            equivalent_queries.append(
                Query(equivalent_table, equivalent_attributes, EMPTY_CONDITION)
            )
            continue

        for i, column_info in enumerate(original_columns):
            table_index, column_name = column_info
            column_name = column_name.lower()
            if column_name != original_conditional_attribute:
                continue
            equivalent_attribute = translated_columns[i][1]
            equivalent_conditional_attribute = equivalent_attribute
            break

        # equivalent_conditional_attribute
        query_obj.condition.column_name = equivalent_conditional_attribute
        equivalent_condition = query_obj.condition

        # TODO: early stop when all elements have been found
        # TODO: add _ to attributes separated by a whitespace
        equivalent_queries.append(
            Query(equivalent_table, equivalent_attributes, equivalent_condition)
        )

    with open("./equivalent_queries.pkl", "wb") as file:
        pickle.dump(equivalent_queries, file)

    input_file.close()
    # output_csv_file.close()
    # output_json_file.close()
