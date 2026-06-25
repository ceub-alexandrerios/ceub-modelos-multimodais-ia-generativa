import os
import sys
import pandas as pd

# Descobre a pasta raiz onde este script (atualizar_txt.py) está salvo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define o caminho exato do arquivo metadata.csv dentro da pasta dados
METADATA_PATH = os.path.join(BASE_DIR, "dados", "metadata.csv")

# Define o caminho da pasta onde os arquivos .txt individuais estão guardados
CAPTIONS_DIR = os.path.join(BASE_DIR, "dados", "captions")

# Verifica se o arquivo metadata.csv realmente existe no caminho especificado
if not os.path.exists(METADATA_PATH):
    print(f"Erro: O arquivo oficial de metadados não foi encontrado em: {METADATA_PATH}")
    print("Certifique-se de que o arquivo 'metadata.csv' foi salvo dentro da pasta 'dados/'.")
    sys.exit(1)

try:
    # Carrega o CSV para a memória como um DataFrame do Pandas
    df = pd.read_csv(METADATA_PATH)
    
    # Valida se as colunas obrigatórias ("arquivo" e "caption") existem no CSV
    if 'arquivo' not in df.columns or 'caption' not in df.columns:
        print("Erro: As colunas do seu 'metadata.csv' estão incorretas.")
        print("O cabeçalho representado pela primeira linha, deve conter: arquivo,caption")
        sys.exit(1)

    print("Sincronizando os arquivos .txt com as captions oficiais do metadata.csv...")
    
    # Garante que a pasta de destino dos .txt existe (se não existir, ele cria)
    os.makedirs(CAPTIONS_DIR, exist_ok=True)

    # Contador para acompanhar o progresso no terminal
    total_atualizado = 0

    # Percorre o arquivo CSV linha por linha
    for _, linha in df.iterrows():
        nome_imagem = linha['arquivo']  # Ex: "img_001.png"
        caption_final = list(linha)[1]  # Pega o texto da nova legenda tratada
        
        # Converte a extensão da imagem (.png, .jpg) para .txt (Ex: "img_001.txt")
        nome_txt = os.path.splitext(str(nome_imagem))[0] + ".txt"
        
        # Define o caminho completo onde o arquivo .txt será salvo/sobrescrito
        caminho_txt = os.path.join(CAPTIONS_DIR, nome_txt)
        
        # Abre o arquivo .txt em modo de escrita ("w") com codificação UTF-8
        # Isso vai apagar o texto antigo do BLIP e gravar a legenda perfeita com o token
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write(str(caption_final))
            
        total_atualizado += 1

    print(f"Sucesso! Todos os {total_atualizado} arquivos .txt foram atualizados com a Trigger Word 'estilo_azulejaria'.")

except Exception as e:
    # Captura qualquer outro erro inesperado (como falta de permissão de escrita no Windows)
    print(f"Ocorreu um erro inesperado durante o processamento: {str(e)}")