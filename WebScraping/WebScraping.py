import os
import zipfile
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # Para resolver links relativos

# URL do site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Função para fazer download do PDF
def download_pdf(pdf_url, pdf_name):
    response = requests.get(pdf_url)
    with open(pdf_name, 'wb') as f:
        f.write(response.content)
    print(f"{pdf_name} baixado com sucesso!")

# Função para compactar os PDFs em um arquivo ZIP
def zip_pdfs(pdfs, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for pdf in pdfs:
            zipf.write(pdf, os.path.basename(pdf))
            print(f"{pdf} adicionado ao arquivo ZIP.")
    print(f"Arquivos compactados em {zip_name}.")

# Acessa a página e encontra os links dos PDFs
def main():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra os links para os PDFs (obtendo os links completos se forem relativos)
    pdf_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if '.pdf' in a['href']]

    # Exibe os links encontrados para depuração
    print(f"Links encontrados: {pdf_links}")

    # Inicializa variáveis para os links dos anexos
    anexo_i_pdf_url = None
    anexo_ii_pdf_url = None

    # Filtra os links para encontrar o Anexo I e Anexo II com maior precisão
    for link in pdf_links:
        if "Anexo_I_Rol_2021" in link and ".pdf" in link:  # Busca mais precisa para o Anexo I
            anexo_i_pdf_url = link
        elif "Anexo_II_DUT" in link and ".pdf" in link:  # Busca mais precisa para o Anexo II
            anexo_ii_pdf_url = link

    # Verifica se os links para os anexos foram encontrados
    if anexo_i_pdf_url and anexo_ii_pdf_url:
        # Nomes dos arquivos para salvar localmente
        file_urls = [anexo_i_pdf_url, anexo_ii_pdf_url]
        file_names = ["Anexo_I.pdf", "Anexo_II.pdf"]

        # Baixar os arquivos
        for file_url, name in zip(file_urls, file_names):
            download_pdf(file_url, name)

        # Compacta os PDFs em um arquivo ZIP
        zip_pdfs(file_names, "Anexos.zip")
    else:
        print("Erro: Não foi possível encontrar todos os anexos corretamente.")
        print(f"Links encontrados: {pdf_links}")  # Para depuração

# Executa a função principal
if __name__ == "__main__":
    main()
