from sentence_transformers import SentenceTransformer, util

# Cargar el modelo DistilBERT
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Función para calcular la similitud del coseno
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Frases de ejemplo
phrase1 = "ID de los estudiantes"
phrase2 = "Identificación de los estudiantes"

# Obtener embeddings para las frases
embeddings = model.encode([phrase1, phrase2])

# Calcular la similitud del coseno entre las frases
similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

print(f"Similitud entre las frases: {similarity}")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Frases de ejemplo
phrases = ["ID de los estudiantes", "Identificación de los estudiantes"]

# Crear el vectorizador TF-IDF
vectorizer = TfidfVectorizer()

# Convertir las frases a matrices TF-IDF
tfidf_matrix = vectorizer.fit_transform(phrases)

# Calcular la similitud del coseno
similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

similarity = similarity_matrix[0][0]

print(f"Similitud entre las frases: {similarity}")
