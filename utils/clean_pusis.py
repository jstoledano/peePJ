"""Módulo para limpiar los archivos PUSIS."""
import os
from PyPDF2 import PdfMerger


def tipo_seccion(filename):
    """Determina el tipo de sección."""
    try:
        tipo = filename[:4]
        return tipo
    except IndexError:
        return None
    

def log_message(message, log_file):
    """Imprime un mensaje y lo escribe en un archivo de log."""
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(message + "\n")


def extract_section(filename):
    """Extrae la sección del nombre del archivo."""
    try:
        section = int(filename[13:16])  # Dígitos en la posición 14 a 16
        page = int(filename[22:26])
        return section, page
    except IndexError:
        return None, page


def list_sections_in_directory(directory, log_file):
    """Lista las secciones en un directorio."""
    sections = set()
    tipos_encontrados = set()

    for _, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                section, _ = extract_section(file)
                tipo = tipo_seccion(file)
                if section and tipo:
                    tipos_encontrados.add(tipo)
                    sections.add(section)
    return sections, tipos_encontrados


def collect_pdfs_by_section(directory, log_file):
    """Recopila los archivos PDF por sección."""
    pdf_files = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                seccion, page = extract_section(file)
                section = int(seccion)
                if section:
                    if section not in pdf_files:
                        pdf_files[section] = []
                    pdf_files[section].append((page, os.path.join(root, file)))
    for section in pdf_files:
        pdf_files[section].sort(key=lambda x: x[0])
    return pdf_files


def merge_pdfs_by_section(pdf_files, output_directory, log_file):
    """Combina los archivos PDF por sección."""
    os.makedirs(output_directory, exist_ok=True)

    for section, files in pdf_files.items():
        merger = PdfMerger()
        for page_number, file_path in files:
            if os.path.exists(file_path):
                log_message(f"  Añadiendo página {page_number} desde {file_path}", log_file)
                merger.append(file_path)
            else:
                log_message(f"  Advertencia: Archivo no encontrado {file_path}", log_file)

        output_path = os.path.join(output_directory, f"{section}.pdf")
        merger.write(output_path)
        merger.close()
        log_message(f"Archivo creado: {output_path}", log_file)


if __name__ == "__main__":
    INPUT = r"c:\Users\javier.sanchezt\Projects\psi"
    OUTPUT = r"c:\Users\javier.sanchezt\Projects\pusis"
    log_file = os.path.join(OUTPUT, "log.txt")

    # secciones, tipos = list_sections_in_directory(INPUT, log_file)
    # print(f"Número total de secciones encontradas: {len(secciones)} y los tipos {tipos}")
    pdf_files = collect_pdfs_by_section(INPUT, log_file)
    merge_pdfs_by_section(pdf_files, OUTPUT, log_file)
