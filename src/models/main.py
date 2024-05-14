import pandas as pd

from Column import Column
from CsvHandler import CsvHandler
from Database import Database
import json
from EmbeddingPipeline import EmbeddingPipeline
from QueryGenerator import QueryGenerator
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator

# from EmbeddingPipeline import EmbeddingPipeline
from SimplePipeline import SimplePipeline
from Query import Query
from Rule import Rule
from TopNAccuracy import TopNAccuracyValidator


# TODO ñtosql
# TODO csv consultas sql y pregunta equivalente
# TODO Parsear stringsql a objeto Query


def definitionDatabase() -> Database:
    # Definir la estructura básica de la base de datos
    database = Database("Escuela")
    columns_1 = [
        Column("identificador", "number"),
        Column("nombre", "text"),
        Column("pais", "text"),
        Column("edad", "number"),
    ]
    database.add_table("Estudiantes", columns_1)
    columns_2 = [
        Column("identificador", "number"),
        Column("nombre", "text"),
        Column("profesor", "text"),
    ]
    database.add_table("Cursos", columns_2)

    return database


def loadRealDatabases():
    databases_file_path = "../../data/processed/databases.pickle"
    databases = pd.read_pickle(databases_file_path)
    db_dict = {}
    for database in databases:
        db_dict[database.name] = database

    return db_dict


def loadRules():
    general_rules_file_path = "../../data/processed/ctx_general_reduced.csv"
    rules = CsvHandler.load_general_rules_from_csv(general_rules_file_path)

    general_rules_file_path = "../../data/processed/detailed_labels_reduced.csv"
    operator_rules = CsvHandler.load_operators_rules_from_csv(general_rules_file_path)

    general_rules_file_path = "../../data/processed/ctx_detallado_reduced.csv"
    value_rules = CsvHandler.load_values_rules_from_csv(general_rules_file_path)

    # rules = [
    #     Rule(left_context="los", right_context="que", classification="ATRIBUTO"),
    #     Rule(left_context="que", right_context="en", classification="TABLA"),
    #     Rule(left_context="en", right_context="end", classification="CONDICION"),
    # ]
    # operator_rules = [
    #     Rule(left_context="", right_context="", exact_match="en", classification="="),
    #     Rule(left_context="", right_context="", exact_match="mayor", classification=">"),
    # ]
    # value_rules = [
    #     Rule(left_context="que", right_context="end", classification="VALOR"),
    #     Rule(
    #         left_context="aquellos", right_context="que", classification="ATR_CONDICIONAL"
    #     ),
    # ]

    # print(rules)
    # print(operator_rules)
    # print(value_rules)

    return rules, operator_rules, value_rules


def loadObjectsQuerys() -> list[Query]:
    querys_file_path = "../../data/processed/equivalent_queries.pkl"

    querys = pd.read_pickle(querys_file_path)

    return querys


def loadNaturalLanguageQuerys() -> tuple:
    natural_language_query_file_path = "../../data/processed/out_json.json"
    list_natural_language_querys = []
    file = open(natural_language_query_file_path, "r", encoding="utf-8")
    js = json.load(file)
    file.close()
    dbs = []
    for line in js:
        natural_language_query = line["question"]
        natural_language_query = "start " + natural_language_query.strip() + " end"
        list_natural_language_querys.append(natural_language_query)
        dbs.append(line["db_id"])

    return list_natural_language_querys, dbs


def executeExample():
    database = definitionDatabase()
    rules, operator_rules, value_rules = loadRules()

    section_extractor = SectionExtractor(rules=rules)
    operator_extractor = SectionExtractor(rules=operator_rules)
    value_extractor = SectionExtractor(rules=value_rules)

    # Definimos el evaluador
    evaluator = SemanticEvaluator(database)

    # Definimos el threshold para la similaridad
    thresholdForAttribute = 0.6

    # Definimos las pipelines
    # pipelines = [SimplePipeline(evaluator, operator_extractor, value_extractor),
    #              EmbeddingPipeline(evaluator, thresholdForAttribute, operator_extractor, value_extractor)]
    pipelines = [
        EmbeddingPipeline(
            evaluator, thresholdForAttribute, operator_extractor, value_extractor
        )
    ]
    # pipelines = [SimplePipeline(evaluator, operator_extractor, value_extractor)]

    for pipeline in pipelines:
        print()
        # Inicializar el generador de consultas
        query_generator = QueryGenerator(
            database, evaluator, section_extractor, pipeline
        )

        # Consulta en lenguaje natural
        natural_language_query = "start Muestra todos los nombres de los alumnos y sus identificadores que estudian en Mexico end"
        # natural_language_query = (
        #     "start Muestra todos los nombres de los alumnos menores de 20 end"
        # )

        querys_objects = [
            Query("Estudiantes", ["nombre", "identificador"], 'pais = "Mexico"')
        ]
        list_natural_language_query = [natural_language_query]
        final_generated_queries = []
        list_querys_strings = []

        for natural_language_query in list_natural_language_query:

            # Generar consultas SQL a partir de la consulta en lenguaje natural
            generated_queries = query_generator.generate_queries(natural_language_query)
            final_generated_queries.append(generated_queries)

            # Imprimir las consultas generadas
            for query in generated_queries:
                list_querys_strings.append(query.SQL_to_string())

            list_querys_strings = set(list_querys_strings)
            for query in list_querys_strings:
                print(query)

        if len(final_generated_queries) > 0:
            validator = TopNAccuracyValidator()
            top_n_accuracy = validator.calculate_accuracy(
                final_generated_queries, querys_objects
            )
            print("Top-N Accuracy:", top_n_accuracy)


def executeRealData():
    real_databases = loadRealDatabases()
    rules, operator_rules, value_rules = loadRules()
    section_extractor = SectionExtractor(rules=rules)
    operator_extractor = SectionExtractor(rules=operator_rules)
    value_extractor = SectionExtractor(rules=value_rules)
    querys_objects = loadObjectsQuerys()
    list_natural_language_query, dbs = loadNaturalLanguageQuerys()
    final_generated_queries = []
    for natural_language_query, db_id in zip(list_natural_language_query[:], dbs[:]):
        database = real_databases[db_id]
        # Definimos el evaluador
        evaluator = SemanticEvaluator(database)

        # Definimos el threshold para la similaridad
        thresholdForAttribute = 0.75

        # Definimos las pipelines
        # pipelines = [SimplePipeline(evaluator, operator_extractor, value_extractor)]
        pipelines = [
            EmbeddingPipeline(
                evaluator, thresholdForAttribute, operator_extractor, value_extractor
            )
        ]

        for pipeline in pipelines:
            print()
            # Inicializar el generador de consultas
            query_generator = QueryGenerator(
                database, evaluator, section_extractor, pipeline
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

        print(natural_language_query)

    if len(final_generated_queries) > 0:
        validator = TopNAccuracyValidator()
        top_n_accuracy = validator.calculate_accuracy(
            final_generated_queries, querys_objects[:]
        )
        print("Top-N Accuracy:", top_n_accuracy)


if __name__ == "__main__":
    executeRealData()
    # executeExample()
