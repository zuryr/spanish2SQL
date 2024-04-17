import json
import os
from typing import List
from Column import Column
from Table import Table
from Database import Database


class DatabaseBuilder:
    def __init__(self, json_path: str):
        self.json_path = json_path

    def load_json(self) -> List[dict]:
        with open(self.json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data

    def build_databases(self) -> List[Database]:
        json_data = self.load_json()
        databases = []
        for db_info in json_data:
            db_id = db_info.get("db_id")
            table_names = db_info.get("table_names")
            column_names = db_info.get("column_names")[1:]
            column_types = db_info.get("column_types")

            tables = {}
            for table_name in table_names:
                table = Table(table_name)
                tables[table_name] = table

            for (column_info, column_type) in zip(column_names, column_types):
                table_index, column_name = column_info
                table_name = table_names[table_index]
                table = tables[table_name]
                column = Column(column_name, column_type, [])
                table.columns[column_name] = column

            database = Database(db_id)
            database.tables = tables
            databases.append(database)

        return databases


script_dir = os.path.dirname(__file__)

json_path = os.path.abspath(os.path.join(script_dir, '../../data/processed/tables_columns_spanish.json'))

builder = DatabaseBuilder(json_path)
databases = builder.build_databases()


# Iterar sobre cada base de datos
for db in databases:
    print("Nombre de la base de datos:", db.name)
    # Acceder a cada tabla en la base de datos
    for table_name, table in db.tables.items():
        print("Tabla:", table_name)
        # Acceder a cada columna en la tabla
        for column_name, column in table.columns.items():
            print("  Columna:", column_name)
            print("    Tipo de dato:", column.datatype)