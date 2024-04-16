from Database import Database
from SemanticEvaluator import SemanticEvaluator
from SectionExtractor import SectionExtractor
from QueryGenerator import QueryGenerator
from CsvHandler import CsvHandler
from Rule import Rule
from Column import Column
from src.models.EmbeddingSemanticEvaluator import EmbeddingSemanticEvaluator
from src.models.FixedSemanticEvaluator import FixedSemanticEvaluator

# Definir la estructura básica de la base de datos
database = Database('Estudiantes')
columns_1 = [Column('id', 'varchar'), Column('nombre', 'varchar'), Column('pais','varchar')]
database.add_table("Estudiantes", columns_1)
columns_2 = [Column('id','varchar'), Column('nombre','varchar'), Column('profesor','varchar')]
database.add_table("Cursos", columns_2)

print(database.tables)

# rules_file_path = "src\data\ctx_general.csv" 
# rules = CsvHandler.load_rules_from_csv(rules_file_path)
rules = [
    Rule(left_context="los", right_context="que", classification="ATRIBUTO"),
    Rule(left_context="que", right_context="en", classification="TABLA"),
    Rule(left_context="en", right_context="end", classification="CONDICION")
]
section_extractor = SectionExtractor(rules=rules)

# Definimos el evaluador
evaluator = SemanticEvaluator(database)

# Definimos las pipelines
pipelines = [FixedSemanticEvaluator(evaluator, section_extractor), EmbeddingSemanticEvaluator(evaluator, section_extractor)]

for pipeline in pipelines:
    # Inicializar el generador de consultas
    query_generator = QueryGenerator(database, evaluator, section_extractor, pipeline)

    # Consulta en lenguaje natural
    natural_language_query = "Muestra todos los estudiantes que estudian en Mexico"

    # Generar consultas SQL a partir de la consulta en lenguaje natural
    generated_queries = query_generator.generate_queries(natural_language_query)

    # Imprimir las consultas generadas
    for query in generated_queries:
        print(query.to_SQL_string())
