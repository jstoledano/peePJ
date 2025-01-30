import os


def tipo_seccion(filename):
    try:
        tipo = filename[:4]
        return tipo
    except:
        return None


def extract_section(filename):
    try:
        section = filename[13:16]  # Dígitos en la posición 14 a 16
        return section
    except IndexError:
        return None

def list_sections_in_directory(directory):
    sections = set()
    tipos = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                section = extract_section(file)
                tipo = tipo_seccion(file)
                if section:
                    tipos.add(tipo)
                    sections.add(section)

    return sections, tipos


def main():
    input_directory = r"c:\\Users\\javier.sanchezt\\Projects\\psi"
    
    sections, tipos = list_sections_in_directory(input_directory)

    print(f"Número total de secciones encontradas: {len(sections)}")
    print(f'Tipos de sección: ', tipos)

if __name__ == "__main__":
    main()
