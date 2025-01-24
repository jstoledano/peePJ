import csv
import os
import sys
import django
from datetime import datetime

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Print the Python path for debugging
print("Python Path:", sys.path)

# Configure the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peePJ.settings')

# Print the DJANGO_SETTINGS_MODULE for debugging
print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))

django.setup()

from gis.models import EstadisticoSeccion, HistoricoPE, Seccion, Entidad

def cargar_datos_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fecha_str = os.path.basename(file_path).split('-')[0]
        fecha = datetime.strptime(fecha_str, '%Y%m%d').date()

        historico, created = HistoricoPE.objects.get_or_create(fecha=fecha, defaults={'observaciones': '', 'pe': None, 'ln': None})

        for row in reader:
            entidad = Entidad.objects.get(entidad=int(row['entidad']))
            try:
                seccion = Seccion.objects.get(entidad=entidad, seccion=int(row['seccion']))
            except Seccion.DoesNotExist:
                print(f"Seccion with entidad {entidad} and seccion {row['seccion']} does not exist. Skipping row.")
                continue

            pe = int(row['pe'])
            ln = int(row['ln'])

            EstadisticoSeccion.objects.create(
                historico=historico,
                entidad=entidad,
                seccion=seccion,
                pe=pe,
                ln=ln
            )

if __name__ == "__main__":
    file_paths = ['./data/20241231-pe_ln.csv', './data/20250115-pe_ln.csv']
    for file_path in file_paths:
        cargar_datos_csv(file_path)