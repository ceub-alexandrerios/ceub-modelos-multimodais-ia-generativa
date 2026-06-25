import csv
import os

# Define o diretório onde o script atual está salvo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define o caminho da pasta que contém os arquivos de texto (.txt) com as legendas
CAPTIONS_DIR = os.path.join(BASE_DIR, "dados", "captions")

# Define o caminho completo onde o arquivo CSV de saída será criado
csv_saida = os.path.join(BASE_DIR, "dados", "captions_revisao.csv")

# Abre (ou cria) o arquivo CSV para escrita ("w"), garantindo a codificação UTF-8
with open(csv_saida, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # Escreve o cabeçalho do arquivo CSV
    writer.writerow(["arquivo", "caption_original", "caption_final"])

    # Lista e ordena em ordem alfabética apenas os arquivos que terminam com ".txt" no diretório
    arquivos = sorted([f for f in os.listdir(CAPTIONS_DIR) if f.endswith(".txt")])

    # Itera sobre cada arquivo de texto encontrado
    for arquivo in arquivos:
        # Monta o caminho completo do arquivo .txt atual
        caminho = os.path.join(CAPTIONS_DIR, arquivo)

        # Abre o arquivo .txt para leitura ("r")
        with open(caminho, "r", encoding="utf-8") as f:
            # Lê o conteúdo do arquivo e remove espaços em branco ou quebras de linha
            caption = f.read().strip()

        # Escreve uma nova linha no CSV:
        # 1. Substitui a extensão do arquivo de .txt para .png
        # 2. Insere a legenda original lida do arquivo
        # 3. Deixa a coluna "caption_final" em branco para futuras revisões manuais
        writer.writerow([arquivo.replace(".txt", ".png"), caption, ""])

print("Arquivo captions_revisao.csv criado com sucesso em dados/")