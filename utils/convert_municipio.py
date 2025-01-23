import csv
import json

# Define the input and output file paths
csv_file_path = '../data/municipios_temp1.csv'
json_file_path = '../data/municipio.json'

# Read the CSV file with latin-1 encoding
with open(csv_file_path, newline='', encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile)
    municipios = []

    for row in reader:
        municipio = {
            "model": "gis.municipio",
            "pk": int(row["id"]),
            "fields": {
                "entidad": int(row["entidad"]),
                "municipio": int(row["municipio"]),
                "nombre": row["nombre"],
                "djp": int(row["djp"]),
                "djc": int(row["djc"])
            }
        }
        municipios.append(municipio)

# Write the JSON file
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(municipios, jsonfile, ensure_ascii=False, indent=4)