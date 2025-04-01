import csv
import zipfile
import pdfplumber
import os

# Função para extrair dados da tabela no PDF
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_table = []
        # Iterando por todas as páginas
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                full_table.extend(table)
        return full_table

# Função para salvar os dados extraídos em formato CSV
def save_to_csv(data, csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Dados salvos em {csv_path} com sucesso!")

# Função para compactar o CSV em formato ZIP
def zip_csv(csv_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))
    print(f"{csv_path} compactado em {zip_name} com sucesso!")

# Função para substituir abreviações das colunas
def replace_abbreviations(csv_path):
    # Substituir as abreviações por suas descrições completas
    replacement_dict = {
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial",
        "HCO": "Seg. Hospitalar Com Obstetrícia",
        "HSO": "Seg. Hospitalar Sem Obstetrícia",
        "REF": "Plano Referência",
        "PAC": "Procedimento de Alta Complexidade",
        "DUT": "Diretriz de Utilização"
    }

    # Lê o conteúdo do CSV
    with open(csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    # Substitui as abreviações nas colunas
    for i, row in enumerate(rows):
        if i == 0:  # Cabeçalho
            row = [replacement_dict.get(cell, cell) for cell in row]
        else:  # Dados
            row = [replacement_dict.get(cell, cell) for cell in row]

    # Salva o arquivo CSV com as substituições
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print(f"Abreviações substituídas em {csv_path}")

# Caminho do PDF (Anexo I) e caminho de saída do CSV
pdf_path = "Anexo_I.pdf"  # Altere conforme o nome do arquivo
csv_path = "Tabela_Rol_Procedimentos.csv"
zip_name = "Teste_Luiz.zip"  # Substitua pelo seu nome

# Passos: 1. Extrair os dados, 2. Salvar como CSV, 3. Substituir abreviações, 4. Compactar em ZIP
table_data = extract_table_from_pdf(pdf_path)
save_to_csv(table_data, csv_path)
replace_abbreviations(csv_path)
zip_csv(csv_path, zip_name)
