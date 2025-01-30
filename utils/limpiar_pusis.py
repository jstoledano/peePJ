import os
from PyPDF2 import PdfMerger

def extract_section_and_page(filename):
    try:
        section = filename[13:16]
        page = int(filename[22:26])
        return section, page
    except ValueError:
        return None, None

def log_message(message, log_file):
    print(message)
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(message + "\n")

def collect_pdfs_by_section(directory, log_file):
    pdf_files = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                section, page = extract_section_and_page(file)
                if section and page:
                    if section not in pdf_files:
                        pdf_files[section] = []
                    pdf_files[section].append((page, os.path.join(root, file)))

    for section in pdf_files:
        pdf_files[section].sort(key=lambda x: x[0])
        log_message(f"Sección {section}: {len(pdf_files[section])} archivos encontrados.", log_file)

    return pdf_files

def merge_pdfs_by_section(pdf_files, output_directory, log_file):
    os.makedirs(output_directory, exist_ok=True)

    for section, files in pdf_files.items():
        if not files:
            log_message(f"Sección {section} está vacía. No se creó un archivo.", log_file)
            continue

        log_message(f"Procesando sección {section} con {len(files)} archivos...", log_file)
        log_message(f"  Archivos encontrados para la sección {section}: {[f[1] for f in files]}", log_file)

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

def main():
    input_directory = r"c:\Users\javier.sanchezt\Projects\psi"
    output_directory = r"c:\Users\javier.sanchezt\Projects\pusis"
    log_file = os.path.join(output_directory, "log.txt")

    if os.path.exists(log_file):
        os.remove(log_file)  # Eliminar el archivo de log anterior

    pdf_files = collect_pdfs_by_section(input_directory, log_file)
    merge_pdfs_by_section(pdf_files, output_directory, log_file)

if __name__ == "__main__":
    main()
