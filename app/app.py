# Importa as bibliotecas necessárias para execução do projeto
import os
import sys
import random
import warnings
import gradio as gr
import torch
from diffusers import DiffusionPipeline

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

if device == "cpu":
    pipe.enable_attention_slicing()  

print("Modelo SDXL carregado com as dimensões corretas!")

# ============================================================================
# 3. ACOPLAMENTO DO LORA (Adaptado para o ambiente de Deploy)
# ============================================================================
# Os pesos ficam na raiz da pasta app para evitar caminhos relativos quebrados
lora_weights_path = "pytorch_lora_weights.safetensors"

if not os.path.exists(lora_weights_path):
    # Fallback caso ainda esteja testando localmente com a estrutura antiga
    lora_weights_path = "../treinamento/pytorch_lora_weights.safetensors"

if os.path.exists(lora_weights_path):
    print(f"Injetando os pesos refinados do seu LoRA a partir de: {lora_weights_path}")
    # Divide o caminho para carregar usando a função nativa do Diffusers
    folder, filename = os.path.split(lora_weights_path)
    pipe.load_lora_weights(folder if folder else ".", weight_name=filename)
    print("SUCESSO: Estilo 'estilo_azulejaria' acoplado e pronto para uso!")
else:
    print("ATENÇÃO: Arquivo de pesos LoRA não encontrado. O modelo rodará sem o estilo customizado.")

# ============================================================================
# 4. FUNÇÃO CORE DE INFERÊNCIA
# ============================================================================
def processar_e_gerar(user_input, tipo_composicao, progress=gr.Progress(track_tqdm=True)):
    if not user_input.strip():
        raise gr.Error("O objeto não pode ficar em branco!")

    # Limpeza sutil do input
    objeto_limpo = user_input.strip().lower()

    # Sorteio de paletas históricas (Exatamente sua lista)
    paletas_historicas = [
        "cobalt blue and white",
        "copper green and white",
        "yellow ochre and white",
        "terracotta and white"
    ]
    cor_sorteada = random.choice(paletas_historicas)

    # Componentes compactos do seu prompt original
    trigger = "estilo_azulejaria"
    materialidade = "flat ceramic tiles, suttle grout lines, smooth glazed surface" 
    ornamentacao = "decorative corner motifs on each tile, traditional cantoneiras" 
    qualidade = "masterpiece, authentic antique look"

    # --- OPÇÃO: PADRÃO REPETITIVO (Sua Opção 2) ---
    if tipo_composicao == "Padrão Repetitivo":
        prompt = (
            f"patchwork azulejo panel depicting a sharp detailed {objeto_limpo} alternating with plain white tiles, "
            f"{trigger}, {materialidade}, {cor_sorteada}, {qualidade}"
        )
        negative_prompt = (
            "deformed objects, fused tiles, broken grid, wavy lines, continuous landscape, photo, blurry, low quality"
        )
    
    # --- OPÇÃO: PAINEL HISTÓRICO (Sua Opção 1 com Sorteio de Sistema) ---
    else:
        estilo_sorteado = random.choice(["continuo", "historico"])

        if estilo_sorteado == "continuo":
            prompt = (
                f"A large {objeto_limpo} hand-painted on a continuous artwork painted across a ceramic tile mural, "
                f"subtle tile grout lines, elegant azulejo grid background, glossy glazed ceramic surface, "
                f"{trigger}, intricate blue and white patterns, {qualidade}"
            )
            negative_prompt = "modern photo, abstract mess, blurry, low quality"
        else:
            prompt = (
                f"historical azulejo panel depicting {objeto_limpo}, "
                f"{trigger}, {ornamentacao}, {materialidade}, {cor_sorteada}, {qualidade}"
            )
            negative_prompt = "modern photo, abstract mess, blurry, low quality"

    # Execução da Inferência com os parâmetros definidos
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=30,
        guidance_scale=7.5
    ).images[0]

    return image, f"Paleta Aplicada: {cor_sorteada} | Prompt enviado ao CLIP: {prompt}"

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
#mural-banner h1 { font-weight: bold; margin-bottom: 0.5rem; }
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
        gr.Markdown("Aplicação de Inteligência Artificial para criação de painéis cerâmicos tradicionais.")

    with gr.Row():
        # Coluna de Configurações (Inputs)
        with gr.Column(scale=4):
            gr.Markdown("### Configuração da Pintura")
            
            input_texto = gr.Textbox(
                label="Objeto Desejado (Digite em inglês)",
                placeholder="Ex: classic vintage car, majestic dragon, ceramic teapot...",
                max_lines=1
            )
            
            input_estilo = gr.Radio(
                choices=["Painel Histórico", "Padrão Repetitivo"],
                value="Painel Histórico",
                label="Estilo de Montagem da Cerâmica",
                info="Painel Histórico: Escolha randômica do sistema entre Objeto Monumental Contínuo ou Estilo Cenográfico Dinâmico.\n\nPadrão Repetitivo: Painel do tipo Figura Avulsa estruturado em grade rígida e intercalado com azulejos brancos."
            )
            
            botao_gerar = gr.Button("Iniciar Renderização Cerâmica", variant="primary", elem_classes="btn-mural")
            
            # Exemplos rápidos guiados (Apresenta a lista de exemplos)
            gr.Examples(
                examples=[["ceramic teapot"], ["classic vintage car"], ["majestic dragon"]],
                inputs=[input_texto],
                label="Exemplos de Entrada"
            )

        # Coluna de Exibição (Output)
        with gr.Column(scale=5):
            gr.Markdown("### Cerâmica Finalizada")
            output_img = gr.Image(label="Azulejo Renderizado", type="pil", interactive=False)
            output_status = gr.Markdown("*Aguardando definições do usuário...*")

    # Gatilho de execução vinculado ao clique do botão
    botao_gerar.click(
        fn=processar_e_gerar,
        inputs=[input_texto, input_estilo],
        outputs=[output_img, output_status]
    )

if __name__ == "__main__":
    demo.launch()