import csv
import json

# Define the input and output file paths
csv_file_path = '../data/qry_seccion.csv'
json_file_path = '../data/seccion.json'

# Read the CSV file with latin-1 encoding
with open(csv_file_path, newline='', encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile)
    secciones = []

    for row in reader:
        seccion = {
            "model": "gis.seccion",
            "pk": int(row["id"]),
            "fields": {
                "entidad": int(row["entidad"]),
                "distrito_federal": int(row["distrito_federal"]),
                "distrito_local": int(row["distrito_local"]),
                "municipio": int(row["municipio"]),
                "are": int(row["are"]) if row["are"] else None,
                "seccion": int(row["seccion"]),
                "tipo": int(row["tipo"]),
                "activa": row["activa"].lower() == 'true'
            }
        }
        secciones.append(seccion)

# Write the JSON file
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(secciones, jsonfile, ensure_ascii=False, indent=4)