import sys
import json

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #    raise ValueError("More or less than 2 arguments provided. Aborting")

    input_path = "../../data/external/spider/train_spider.json"  # sys.argv[0]
    esp_path = "../../data/interim/out_esp.txt"
    output_path = "./out_json.txt"  # sys.argv[1]
    output_csv_path = "./out_questions.txt"

    input_file = open(input_path)
    esp_file = open(esp_path, encoding="utf-8")
    esp_queries = esp_file.readlines()
    output_json_file = open(output_path, "w+", encoding="utf-8")
    output_csv_file = open(output_csv_path, "w+", encoding="utf-8")
    input_json = json.load(input_file)

    AGG_OPS = ("none", "max", "min", "count", "sum", "avg")

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

        second_token = obj["query_toks"][1]
        if second_token in AGG_OPS:
            continue

        obj["question"] = esp_queries[i]
        # Only questions csv
        output_csv_file.write(f"{obj['question']}")

        output_json_file.write(f"{json.dumps(obj, ensure_ascii=False)},\n")

    input_file.close()
    output_csv_file.close()
    output_json_file.close()
