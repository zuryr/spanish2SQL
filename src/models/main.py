from Column import Column
from Database import Database
from QueryGenerator import QueryGenerator
from Rule import Rule
from SectionExtractor import SectionExtractor
from SemanticEvaluator import SemanticEvaluator

# from EmbeddingPipeline import EmbeddingPipeline
from SimplePipeline import SimplePipeline

# Definir la estructura básica de la base de datos
database = Database("Escuela")
columns_1 = [
    Column("identificador", "int"),
    Column("nombre", "varchar"),
    Column("pais", "varchar"),
]
database.add_table("Estudiantes", columns_1)
columns_2 = [
    Column("identificador", "int"),
    Column("nombre", "varchar"),
    Column("profesor", "varchar"),
]
database.add_table("Cursos", columns_2)

# rules_file_path = "src\data\ctx_general.csv"
# rules = CsvHandler.load_rules_from_csv(rules_file_path)
rules = [
    Rule(left_context="los", right_context="que", classification="ATRIBUTO"),
    Rule(left_context="que", right_context="en", classification="TABLA"),
    Rule(left_context="en", right_context="<END>", classification="CONDICION"),
]

operator_rules = [
    Rule(left_context="", right_context="", exact_match="igual", classification="="),
    Rule(left_context="", right_context="", exact_match="mayor", classification=">"),
]

value_rules = [
    Rule(left_context="que", right_context="<END>", classification="VALOR"),
    Rule(
        left_context="aquellos", right_context="que", classification="ATR_CONDICIONAL"
    ),
]

section_extractor = SectionExtractor(rules=rules)
operator_extractor = SectionExtractor(rules=operator_rules)
value_extractor = SectionExtractor(rules=value_rules)

# Definimos el evaluador
evaluator = SemanticEvaluator(database)

# Definimos el threshold para la similaridad
threshold = 0.5

# Definimos las pipelines
# pipelines = [SimplePipeline(evaluator, section_extractor), EmbeddingPipeline(evaluator, section_extractor, threshold)]
pipelines = [SimplePipeline(evaluator, operator_extractor, value_extractor)]

for pipeline in pipelines:
    # Inicializar el generador de consultas
    query_generator = QueryGenerator(database, evaluator, section_extractor, pipeline)

    # Consulta en lenguaje natural
    natural_language_query = (
        "<START>Muestra todos los nombres e identificadores que estudian en Mexico<END>"
    )

    # Generar consultas SQL a partir de la consulta en lenguaje natural
    generated_queries = query_generator.generate_queries(natural_language_query)

    # Imprimir las consultas generadas
    for query in generated_queries:
        print(query.to_SQL_string())
