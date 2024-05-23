import json
import pickle

import pandas as pd

from CsvHandler import CsvHandler
from EmbeddingPipeline import EmbeddingPipeline
from MaxAttributesInTableStrategy import MaxAttributesInTableStrategy
from Query import Query
from QueryGenerator import QueryGenerator
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator
from TopNAccuracy import TopNAccuracyValidator
from Tokenizer import Tokenizer
from GreedyStrategy import GreedyStrategy
from ContextStrategy import ContextStrategy


def load_real_databases():
    databases_file_path = "../../data/processed/databases.pickle"
    databases = pd.read_pickle(databases_file_path)
    db_dict = {}
    for database in databases:
        db_dict[database.name] = database

    return db_dict


def load_rules():
    general_rules_file_path = "../../data/processed/ctx_general_reduced.csv"
    rules = CsvHandler.load_general_rules_from_csv(general_rules_file_path)

    general_rules_file_path = "../../data/processed/detailed_labels_reduced.csv"
    operator_rules = CsvHandler.load_operators_rules_from_csv(general_rules_file_path)

    general_rules_file_path = "../../data/processed/ctx_detallado_reduced.csv"
    value_rules = CsvHandler.load_values_rules_from_csv(general_rules_file_path)

    return rules, operator_rules, value_rules


def load_objects_querys() -> list[Query]:
    querys_file_path = "../../data/processed/equivalent_queries.pkl"

    querys = pd.read_pickle(querys_file_path)

    return querys


def load_natural_language_querys() -> tuple:
    natural_language_query_file_path = "../../data/processed/out_json.json"
    list_natural_language_querys = []
    file = open(natural_language_query_file_path, "r", encoding="utf-8")
    js = json.load(file)
    file.close()
    dbs = []
    for line in js:
        natural_language_query = line["question"]
        # TODO: what is this for?
        # natural_language_query = re.sub(
        #    r"""[^\w<>!=áéíóúñ"\s,'.¿?]""", "", natural_language_query
        # )
        natural_language_query = "start " + natural_language_query.strip() + " end"
        list_natural_language_querys.append(natural_language_query)
        dbs.append(line["db_id"])

    return list_natural_language_querys, dbs


def execute_real_data(m=0, n=None, threshold=0.8):
    real_databases = load_real_databases()
    rules, operator_rules, value_rules = load_rules()
    section_extractor = SectionExtractor(rules=rules)
    operator_extractor = SectionExtractor(rules=operator_rules)
    value_extractor = SectionExtractor(rules=value_rules)
    querys_objects = load_objects_querys()
    list_natural_language_query, dbs = load_natural_language_querys()
    final_generated_queries = []

    strategy = ContextStrategy()

    if n is None:
        n = len(list_natural_language_query)

    i = 0
    for natural_language_query, db_id in zip(
        list_natural_language_query[m:n], dbs[m:n]
    ):
        database = real_databases[db_id]
        natural_language_query = " ".join(Tokenizer.tokenize_question(natural_language_query))

        # strategy = MaxAttributesInTableStrategy(database)
        # Definimos el evaluador
        evaluator = SemanticEvaluator(database)

        # Definimos el threshold para la similaridad

        # Definimos las pipelines
        # pipelines = [SimplePipeline(evaluator, operator_extractor, value_extractor)]
        pipelines = [
            EmbeddingPipeline(evaluator, threshold, operator_extractor, value_extractor)
        ]

        for pipeline in pipelines:
            print(natural_language_query)
            # Inicializar el generador de consultas
            query_generator = QueryGenerator(
                database, evaluator, section_extractor, pipeline, strategy
            )

            list_querys_strings = []

            # Generar consultas SQL a partir de la consulta en lenguaje natural
            generated_queries = query_generator.generate_queries(natural_language_query)
            final_generated_queries.append(generated_queries)

            for query in generated_queries:
                list_querys_strings.append(query.SQL_to_string())

            list_querys_strings = set(list_querys_strings)
            for query in list_querys_strings:
                print(query)

        # print(natural_language_query)
        i += 1
        print(i)
        if i % 50 == 0:
            with open("./predicted_queries.pkl", "wb+") as f:
                pickle.dump(final_generated_queries, f)

    for query in querys_objects[m:n]:
        print(query.SQL_to_string())

    if len(final_generated_queries) > 0:
        validator = TopNAccuracyValidator()
        top_n_accuracy = validator.calculate_accuracy(
            final_generated_queries, querys_objects[m:n]
        )
        print("Top-N Accuracy:", top_n_accuracy)
        print(
            f"Respuestas correctas: {int(len(final_generated_queries)*top_n_accuracy)} / {len(final_generated_queries)}"
        )


if __name__ == "__main__":
    execute_real_data(9, 10)
    # executeExample()
