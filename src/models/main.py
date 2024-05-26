import pickle
import re
import pandas as pd

from Column import Column
from CsvHandler import CsvHandler
from Database import Database
import json
from EmbeddingPipeline import EmbeddingPipeline
from GreedyStrategy import GreedyStrategy
from MaxAttributesInTableStrategy import MaxAttributesInTableStrategy
from QueryGenerator import QueryGenerator
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator

# from EmbeddingPipeline import EmbeddingPipeline
from SimplePipeline import SimplePipeline
from Query import Query
from Rule import Rule
from TopNAccuracy import TopNAccuracyValidator


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


def execute_real_data(m=0, n=None, threshold=0.75):
    real_databases = load_real_databases()
    rules, operator_rules, value_rules = load_rules()
    section_extractor = SectionExtractor(rules=rules)
    operator_extractor = SectionExtractor(rules=operator_rules)
    value_extractor = SectionExtractor(rules=value_rules)
    querys_objects = load_objects_querys()
    list_natural_language_query, dbs = load_natural_language_querys()
    final_generated_queries = []

    if n is None:
        n = len(list_natural_language_query)

    i = 0
    for natural_language_query, db_id in zip(
        list_natural_language_query[m:n], dbs[m:n]
    ):
        database = real_databases[db_id]

        strategy = MaxAttributesInTableStrategy(database)
        # Definimos el evaluador
        evaluator = SemanticEvaluator(database)

        # Definimos el threshold para la similaridad

        # Definimos las pipelines
        # pipelines = [SimplePipeline(evaluator, operator_extractor, value_extractor)]
        pipelines = [
            EmbeddingPipeline(evaluator, threshold, operator_extractor, value_extractor)
        ]

        for pipeline in pipelines:
            print()
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

    if len(final_generated_queries) > 0:
        validator = TopNAccuracyValidator()
        top_n_accuracy = validator.calculate_accuracy(
            final_generated_queries, querys_objects[m:n]
        )
        print("Top-N Accuracy:", top_n_accuracy)
        print(
            f"Respuestas correctas: {int(len(final_generated_queries)*top_n_accuracy)} / {len(final_generated_queries)}"
        )

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

def definitionPersonalDatabase() -> Database:
    print("A continuación se le solicitara los datos del esquema de su base de datos")

    tablesNotFinished = 's'
    i = 1
    database_name = input("Ingrese el nombre de su base datos: ")

    input_database = Database(database_name)

    while tablesNotFinished == 's' or tablesNotFinished == 'S':
        table_name = input(f"Ingrese el nombre su tabla {i}: ")
        columns = []

        columnsNotFinished = 's'

        j = 1
        while columnsNotFinished == 's' or columnsNotFinished == 'S':
            column_name = input(f"Ingrese el nombre de su columna: ")
            print(f"Escoja el tipo de dato de su columna {j}: \n"
                  "1. text \n"
                  "2. number")
            opc_column = int(input(f"Ingrese el tipo de dato: "))
            column_type = "number" if opc_column == 2 else "text"
            columns.append(Column(column_name, column_type))

            columnsNotFinished = input("\nDesea ingresar más columnas? [S/N] : ")
            j += 1

        input_database.add_table(table_name, columns)

        tablesNotFinished = input("\nDesea ingresar más tablas? [S/N] : ")
        i += 1

    return input_database


def executeInputExample():
    print("Bienvenido al sistema de ñ2SQL\n")
    opc_database = input("Desea ingresar su propio esquema de base datos? s/n: ")
    database = definitionDatabase() if opc_database != 's' else definitionPersonalDatabase()

    print("Se ingresó la base da datos personalizada") if (opc_database == 's' or opc_database == 'S') else\
        print("Se ingresó la base datos predeterminada")

    print("\nLa base de datos de entrada es:\n")
    database.database_to_string()

    opc_make_another_query = 's'
    while opc_make_another_query == 's' or opc_make_another_query == 'S':

        rules, operator_rules, value_rules = load_rules()
        section_extractor = SectionExtractor(rules=rules)
        operator_extractor = SectionExtractor(rules=operator_rules)
        value_extractor = SectionExtractor(rules=value_rules)
        strategy = MaxAttributesInTableStrategy(database)
        evaluator = SemanticEvaluator(database)

        generated_queries = []
        list_querys_strings = []
        natural_language_query = ''

        noQueriesResults = True
        while noQueriesResults:
            natural_language_query = input("\nIntroduzca su consulta en lenguaje natural: ")
            natural_language_query = "start " + natural_language_query + " end"
            threshold = float(input("\nIntroduzca el umbral de precisión: "))

            pipeline = EmbeddingPipeline(evaluator, threshold, operator_extractor, value_extractor)
            query_generator = QueryGenerator(database, evaluator, section_extractor, pipeline, strategy)

            generated_queries = query_generator.generate_queries(natural_language_query)
            noQueriesResults = len(generated_queries) == 0

            if len(generated_queries) == 0:
                print("ñ2SQL no ha encontrado resultados. Por favor, reformule su consulta o modifique su umbral e"
                      " intentelo de nuevo.\n")

        for query in generated_queries:
            list_querys_strings.append(query.SQL_to_string())
        list_querys_strings = set(list_querys_strings)

        print(f"\nSu consulta en lenguaje natural ingresada fue: {natural_language_query}")
        print("A continuación, los resultados: \n")

        for query in list_querys_strings:
            print(query)

        opc_make_another_query = input("\nDesea realizar otra consulta? [S/N] ")

    print("Hasta luego...")

if __name__ == "__main__":
    # execute_real_data(0, 2)
    # executeExample()

    executeInputExample()
