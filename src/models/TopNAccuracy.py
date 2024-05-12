from Query import Query

class TopNAccuracyValidator:

    def calculate_accuracy(self, y_pred: list[list[Query]], y_true: list[Query]) -> float:
        """
        Calculates the Top-N accuracy given predicted queries and true queries.

        Args:
            y_pred: A list of lists where each inner list contains predicted Query instances.
            y_true: A list of true Query instances.

        Returns:
            The Top-N accuracy as a float between 0 and 1.
        """
        total_queries = len(y_true)
        correct_predictions = 0

        for i in range(total_queries):
            true_query = y_true[i]
            top_n_predictions = y_pred[i]  # Get the top N predictions

            # Check if true query is in top N predictions
            for prediction in top_n_predictions:
                if true_query == prediction:
                    correct_predictions += 1

        # Calculate accuracy
        accuracy = correct_predictions / total_queries if total_queries > 0 else 0.0

        return accuracy

if __name__ == '__main__':

    # Crear instancias de Query para probar
    query1 = Query("Table1", ["Column1", "Column2", "column10"], "Condition1")
    query2 = Query("Table2", ["Column3", "Column4"], "Condition2")
    query3 = Query("Table3", ["Column5", "Column6"], "Condition3")
    query4 = Query("Table4", ["Column7", "Column8"], "Condition4")
    query1_1 = Query("Table1", ["Column2", "column10", "Column1", "column4"], "Condition1")

    # Crear una lista de predicciones y verdaderos Query para probar el validador
    y_pred = [
        [query3, query1, query2],  # Predicciones para la primera consulta verdadera
        [query3, query2, query1],  # Predicciones para la segunda consulta verdadera
        [query1, query2, query4]   # Predicciones para la tercera consulta verdadera
    ]

    y_true = [query1_1, query1_1, query4]  # Consultas verdaderas

    # Crear una instancia del validador
    validator = TopNAccuracyValidator()

    # Calcular la precisión para las predicciones y_true
    top_n_accuracy = validator.calculate_accuracy(y_pred, y_true)
    print("Top-N Accuracy:", top_n_accuracy)
