import csv
import os
import sys
import django
from datetime import datetime

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Configure the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peePJ.settings')
django.setup()

from gis.models import Entidad, Seccion, Padron

def cargar_datos_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entidad = Entidad.objects.get(entidad=int(row['entidad']))
            try:
                seccion = Seccion.objects.get(entidad=entidad, seccion=int(row['seccion']))
            except Seccion.DoesNotExist:
                print(f"Seccion with entidad {entidad} and seccion {row['seccion']} does not exist. Skipping row.")
                continue

            pe = int(row['pe'])
            ln = int(row['ln'])

            Padron.objects.create(
                entidad=entidad,
                seccion=seccion,
                pe=pe,
                ln=ln
            )

if __name__ == "__main__":
    file_paths = ['./data/20250115-pe_ln.csv']
    for file_path in file_paths:
        cargar_datos_csv(file_path)