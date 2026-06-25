# Dataset - Azulejaria Luso-Brasileira

## Objetivo
Construir um conjunto de dados especializado e curado para o treinamento de um modelo acoplado via LoRA (Low-Rank Adaptation), capaz de aprender, preservar e reproduzir com alta fidelidade as características estéticas, cromáticas e texturais da azulejaria luso-brasileira tradicional, moderna e contemporânea.

## Volumetria e Especificações Técnicas
- **Quantidade de imagens:** 40 imagens selecionadas manualmente.
- **Dimensões e Resolução:** 512x512 pixels (otimizado para o aspect ratio nativo de modelos base).
- **Formato Visual:** Imagens em formato `.png` de alta qualidade, livres de artefatos digitais agressivos.

## Origem e Governança de Dados
- **Fontes:** Wikimedia Commons, Unsplash e acervos históricos catalogados.
- **Rastreabilidade:** Mapeamento completo de URLs, autores e licenças documentado no arquivo `dados/fontes.csv`.
- **Licenciamento:** Imagens restritas a licenças de Domínio Público ou Creative Commons (CC BY / CC BY-SA), totalmente compatíveis com uso acadêmico, científico e de pesquisa.

## Critérios de Seleção e Variabilidade do Dataset
O dataset foi balanceado estrategicamente para cobrir diferentes vertentes históricas e artísticas:
- **Painéis Históricos & Narrativos:** Cenas complexas e composições detalhadas.
- **Motivos Religiosos (Hagiográficos):** Representações sacras tradicionais.
- **Ornamentações Florais & Arabescos:** Elementos orgânicos barrocos e coloniais.
- **Padrões Geométricos:** Composições modulares clássicas (estilo Pombalino) e ilusões de ótica (*trompe l'oeil*).
- **Heráldica:** Brasões e escudos de armas detalhados.
- **Composições em Patchwork:** Mosaicos e colagens de azulejos variados.
- **Azulejaria Modernista Brasileira:** Padrões abstratos e minimalistas inspirados na escola geométrica de Athos Bulcão.

## Estratégia de Anotação e Prompting (Captioning)
- **Trigger Word (Token de Ativação):** `estilo_azulejaria`
- **Abordagem de Engenharia de Dados:**
  1. **Fase Inicial:** Geração de descrições automáticas via modelo multimodal BLIP.
  2. **Fase de Consolidação:** Criação de interface de revisão (`captions_revisao.csv`).
  3. **Fase de Curadoria Manual:** Ajuste fino linguístico e técnico, substituindo termos literais por descrições especializadas de azulejaria (ex: *sepia glazed azulejos*, *cobalt blue*, *symmetrical tessellation*).
- **Formatos Disponibilizados:**
  - **Arquivo Mestre:** `dados/metadata.csv` contendo o mapeamento `arquivo,caption` (padrão Hugging Face / Diffusers).
  - **Arquivos Individuais:** 40 arquivos `.txt` sincronizados dentro da pasta `dados/captions/` (padrão de compatibilidade para frameworks como Kohya_ss).