import os
import csv
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# 1. Configurar caminhos das pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGENS_DIR = os.path.join(BASE_DIR, "dados", "imagens")
CAPTIONS_DIR = os.path.join(BASE_DIR, "dados", "captions")

# Criar a pasta de captions se ela não existir
os.makedirs(CAPTIONS_DIR, exist_ok=True)

print("Carregando o modelo Salesforce BLIP da nuvem:")
# 2. Carregar o processador e o modelo de legenda de imagens
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

print("Iniciando a leitura das imagens e geração automática das captions:")

# Listar todas as imagens ordenadas
imagens = sorted([f for f in os.listdir(IMAGENS_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))])

for idx, nome_arquivo in enumerate(imagens, 1):
    caminho_imagem = os.path.join(IMAGENS_DIR, nome_arquivo)
    
    try:
        # Abrir imagem usando o Pillow
        raw_image = Image.open(caminho_imagem).convert('RGB')
        
        # Processar a imagem para o formato que a IA entende
        inputs = processor(raw_image, return_tensors="pt")
        
        # Gerar os tokens de texto
        out = model.generate(**inputs)
        
        # Decodificar os tokens em uma frase em inglês
        caption_inicial = processor.decode(out[0], skip_special_tokens=True)
        
        # Definir nome do arquivo .txt correspondente
        nome_txt = os.path.splitext(nome_arquivo)[0] + ".txt"
        caminho_txt = os.path.join(CAPTIONS_DIR, nome_txt)
        
        # Salvar a caption bruta gerada pela IA na pasta de captions
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write(caption_inicial)
            
        print(f"[{idx}/{len(imagens)}] {nome_arquivo} -> {nome_txt}: '{caption_inicial}'")
        
    except Exception as e:
        print(f"Erro ao processar a imagem {nome_arquivo}: {str(e)}")

print("\nFase 2 concluída! Todas as captions iniciais foram geradas na pasta 'dados/captions/'.")