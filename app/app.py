# Importa as bibliotecas necessárias para execução do projeto
import os
import sys
import random
import warnings
import gc
import gradio as gr
import torch
from diffusers import DiffusionPipeline
from deep_translator import GoogleTranslator
from gtts import gTTS

# Silencia avisos do Transformers
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# ============================================================================
# 1. DETECÇÃO DE HARDWARE
# ============================================================================
if torch.cuda.is_available():
    device = "cuda"
    dtype = torch.float16
    variant = "fp16"
    print("Detectada GPU local/nuvem!")
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    device = "mps"
    dtype = torch.float32
    variant = None
    print("Detectado Apple Silicon!")
else:
    device = "cpu"
    dtype = torch.float32
    variant = None
    print("Modo CPU Otimizado para SDXL.")

# ============================================================================
# 2. CARREGAMENTO DO MODELO BASE SDXL
# ============================================================================
print("Carregando Stable Diffusion XL Base 1.0...")
pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=dtype,
    variant=variant if variant else None,
    low_cpu_mem_usage=True,           
    use_safetensors=True
).to(device)

# Otimizações de Engenharia de Memória Mandatórias para rodar na CPU do Spaces
pipe.enable_attention_slicing(slice_size="auto")  
pipe.enable_vae_slicing()

print("Modelo SDXL carregado com as dimensões corretas!")

# ============================================================================
# 3. ACOPLAMENTO DO LORA (Adaptado para o ambiente de Deploy)
# ============================================================================
lora_weights_path = "pytorch_lora_weights.safetensors"

if not os.path.exists(lora_weights_path):
    lora_weights_path = "../treinamento/pytorch_lora_weights.safetensors"

if os.path.exists(lora_weights_path):
    print(f"Injetando os pesos refinados do seu LoRA a partir de: {lora_weights_path}")
    folder, filename = os.path.split(lora_weights_path)
    pipe.load_lora_weights(folder if folder else ".", weight_name=filename)
    print("SUCESSO: Estilo 'estilo_azulejaria' acoplado e pronto para uso!")
else:
    print("ATENÇÃO: Arquivo de pesos LoRA não encontrado. O modelo rodará sem o estilo customizado.")

# Dicionário de tradução para manter a consistência do gTTS em português brasileiro
tradutor_cores = {
    "cobalt blue and white": "azul cobalto com branco",
    "copper green and white": "verde cobre com branco",
    "yellow ochre and white": "ocre amarelo com branco",
    "terracotta and white": "terracota com branco"
}

# ============================================================================
# 4. FUNÇÃO CORE DE INFERÊNCIA MULTIMODAL (Orquestração Sequencial)
# ============================================================================
def processar_e_gerar(user_input_pt, tipo_composicao, progress=gr.Progress(track_tqdm=True)):
    if not user_input_pt.strip():
        raise gr.Error("O objeto não pode ficar em branco!")

    # Ativação do Garbage Collector para limpar resíduos da RAM antes da difusão
    gc.collect()

    # Tradução Automática Bridge: Usuário digita em PT-BR -> Sistema envia em EN-US ao CLIP
    user_input_en = GoogleTranslator(source='pt', target='en').translate(user_input_pt.strip().lower())

    # Sorteio de paletas históricas
    paletas_historicas = [
        "cobalt blue and white",
        "copper green and white",
        "yellow ochre and white",
        "terracotta and white"
    ]
    cor_sorteada = random.choice(paletas_historicas)
    cor_pt = tradutor_cores.get(cor_sorteada, cor_sorteada)

    # Componentes estruturais do prompt ideal
    trigger = "estilo_azulejaria"
    materialidade = "flat ceramic tiles, suttle grout lines, smooth glazed surface" 
    ornamentacao = "decorative corner motifs on each tile, traditional cantoneiras" 
    qualidade = "masterpiece, authentic antique look"

    # --- OPÇÃO: PADRÃO REPETITIVO ---
    if tipo_composicao == "Padrão Repetitivo":
        prompt = (
            f"patchwork azulejo panel depicting a sharp detailed {user_input_en} alternating with plain white tiles, "
            f"{trigger}, {materialidade}, {cor_sorteada}, {qualidade}"
        )
        negative_prompt = (
            "deformed objects, fused tiles, broken grid, wavy lines, continuous landscape, photo, blurry, low quality"
        )
        texto_narracao = f"Painel de azulejo no estilo luso brasileiro com aspectos modernos, retratando {user_input_pt}, utilizando a paleta {cor_pt}."
    
    # --- OPÇÃO: PAINEL HISTÓRICO ---
    else:
        estilo_sorteado = random.choice(["continuo", "historico"])

        if estilo_sorteado == "continuo":
            prompt = (
                f"A large {user_input_en} hand-painted on a continuous artwork painted across a ceramic tile mural, "
                f"subtle tile grout lines, elegant azulejo grid background, glossy glazed ceramic surface, "
                f"{trigger}, intricate blue and white patterns, {qualidade}"
            )
            negative_prompt = "modern photo, abstract mess, blurry, low quality"
            texto_narracao = f"Painel de azulejo no estilo luso brasileiro, retratando {user_input_pt}, utilizando o estilo clássico com padrão contínuo."
        else:
            prompt = (
                f"historical azulejo panel depicting {user_input_en}, "
                f"{trigger}, {ornamentacao}, {materialidade}, {cor_sorteada}, {qualidade}"
            )
            negative_prompt = "modern photo, abstract mess, blurry, low quality"
            texto_narracao = f"Painel de azulejo no estilo luso brasileiro, retratando {user_input_pt}, utilizando o estilo clássico com cantoneiras na paleta {cor_pt}."

    # Execução da Inferência de Imagem (SDXL)
    print(f"Executando difusão para o prompt: {prompt}")
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=30,
        guidance_scale=7.5
    ).images[0]

    # Na sequência: Execução da Síntese de Voz (gTTS)
    audio_path = "narracao_output.mp3"
    tts = gTTS(text=texto_narracao, lang='pt', tld='com.br')
    tts.save(audio_path)

    # Coleta de lixo final para manter o servidor do Spaces estável
    gc.collect()

    status_log = (
        f"**LOG DE AUDITORIA DA TRADUÇÃO**\n"
        f"• Entrada (PT-BR): {user_input_pt}\n"
        f"• Enviado ao CLIP (EN-US): {user_input_en}\n"
        f"• Paleta Sorteada: {cor_sorteada}\n"
        f"• Prompt Final: `{prompt}`"
    )

    return image, audio_path, status_log

# ============================================================================
# 5. ESTILIZAÇÃO INTERFACE GRADIO (Mural Luso-Brasileiro)
# ============================================================================
css = """
.gradio-container {
    background-color: #f4f7f6 !important;
}
#mural-banner {
    background: linear-gradient(135deg, #0d3b66 0%, #001f3d 100%);
    color: #faf0ca;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    border-bottom: 5px solid #f4d35e;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 2rem;
}
#mural-banner h1 { font-weight: bold; margin-bottom: 0.5rem; color: #faf0ca !important; }
.btn-mural {
    background-color: #0d3b66 !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 6px !important;
}
.btn-mural:hover { background-color: #001f3d !important; }
"""

with gr.Blocks(css=css, title="Gerador de Azulejaria Luso-Brasileira") as demo:
    
    # Banner de abertura temático
    with gr.Group(elem_id="mural-banner"):
        gr.Markdown("# Gerador Avançado - Estilo Azulejaria Luso-Brasileira")
        gr.Markdown("Interface Multimodal em Nuvem para a criação e descrição de painéis cerâmicos tradicionais.")

    with gr.Row():
        # Coluna de Configurações (Inputs)
        with gr.Column(scale=4):
            gr.Markdown("### Configuração da Pintura")
            
            input_texto = gr.Textbox(
                label="Objeto Desejado (Digite em Português)",
                placeholder="Ex: uma fênix majestosa, um navio caravela, um dragão...",
                max_lines=1
            )
            
            input_estilo = gr.Radio(
                choices=["Painel Histórico", "Padrão Repetitivo"],
                value="Painel Histórico",
                label="Estilo de Montagem da Cerâmica",
                info="Painel Histórico: Geração monumental contínua ou cenográfica com sorteio cromático colonial.\n\nPadrão Repetitivo: Estrutura em grade rígida (patchwork) intercalada com azulejos brancos."
            )
            
            botao_gerar = gr.Button("Iniciar Pipeline Multimodal", variant="primary", elem_classes="btn-mural")
            
            gr.Examples(
                examples=[["uma fênix majestosa"], ["um navio caravela antigo"], ["um vaso de flores colonial"]],
                inputs=[input_texto],
                label="Exemplos de Entrada Adaptados"
            )

        # Coluna de Exibição Sequencial Integrada (Outputs)
        with gr.Column(scale=5):
            gr.Markdown("### Entrega Multimodal Integrada")
            output_img = gr.Image(label="Azulejo Renderizado (SDXL + LoRA)", type="pil", interactive=False)
            output_audio = gr.Audio(label="Descrição Conceitual (gTTS)", type="filepath", interactive=False)
            output_status = gr.Markdown("*Aguardando comandos da esteira...*")

    # Vinculação dos gatilhos à função unificada
    botao_gerar.click(
        fn=processar_e_gerar,
        inputs=[input_texto, input_estilo],
        outputs=[output_img, output_audio, output_status]
    )

if __name__ == "__main__":
    demo.launch()