# Especificação Formal do Estilo – Dataset Azulejaria

## 1. Identificação do Estilo
* **Nome do Gatilho (Trigger Word):** `estilo_azulejaria`

## 2. Descrição Geral
O escopo deste projeto compreende a representação visual da Azulejaria Luso-Brasileira, contemplando a evolução histórica, técnica e artística da tradição cerâmica portuguesa e suas ramificações, adaptações e reinterpretações no contexto arquitetônico e cultural brasileiro. 

O estilo proposto busca capturar não apenas a estética clássica da azulejaria histórica, mas também a diversidade visual presente ao longo de sua evolução, incluindo composições ornamentais, painéis figurativos e mosaicos decorativos amplamente encontrados em edifícios, igrejas, monumentos e fachadas urbanas.

O conjunto visual é composto por:

* **Painéis Figurativos:** Representações de figuras humanas, alegorias, cenas cotidianas, elementos heráldicos e composições narrativas.
* **Cenas Históricas:** Narrativas visuais retratando acontecimentos históricos, batalhas, atividades econômicas, paisagens urbanas e registros da vida social de diferentes épocas.
* **Motivos Religiosos:** Painéis sacros contendo santos, anjos, passagens bíblicas, símbolos cristãos e demais elementos da tradição católica ibérica.
* **Padrões Geométricos:** Estruturas modulares repetitivas baseadas em simetria, tesselações, encaixes geométricos e composições matematicamente organizadas.
* **Mosaicos e Colagens de Azulejos:** Composições do tipo *patchwork* ("colcha de retalhos"), comuns em fachadas históricas, reformas arquitetônicas e aplicações decorativas que combinam diferentes padrões cerâmicos em uma mesma superfície.
* **Ornamentação Cerâmica:** Elementos decorativos utilizados como cercaduras, molduras, frisos, barras ornamentais e composições de acabamento para delimitação visual de painéis e superfícies.

## 3. Características Visuais de Controle (Features)
Para garantir a coerência estética do modelo treinado e a convergência do processo de fine-tuning, as imagens geradas devem manifestar, total ou parcialmente, as seguintes características visuais:

* **Textura e Materialidade:**
  * Aparência inequívoca de cerâmica esmaltada e vitrificada.
  * Reflexos característicos sobre superfícies polidas.
  * Presença de juntas entre azulejos.
  * Possíveis marcas naturais do envelhecimento, como desgaste, craquelados e pequenas irregularidades.
* **Paleta de Cores Predominante:**
  * Predominância da combinação tradicional de Azul Cobalto e Branco, característica da azulejaria portuguesa clássica.
  * São admitidas composições policromáticas historicamente presentes na tradição azulejar portuguesa e brasileira, incluindo: Amarelo/Ocre, Verde-cobre, Manganês/Castanho, Terracota e tons acinzentados provenientes do envelhecimento natural da cerâmica.
* **Estrutura Modular:**
  * Capacidade de representação tanto em padrões contínuos e repetitivos (*seamless tile patterns*), painéis fechados com molduras decorativas, composições mosaicais ou superfícies arquitetônicas revestidas por azulejos.
* **Ornamentação:**
  * Presença frequente de arabescos, elementos florais, folhagens, motivos heráldicos, cercaduras decorativas, simetria visual e estruturas repetitivas.
* **Composição Visual:**
  * O estilo deve preservar características associadas à tradição azulejar luso-brasileira, tais como: equilíbrio visual, simetria, repetição de padrões, organização modular, forte caráter ornamental e integração entre arte e arquitetura.

## 4. Exclusões Deliberadas
Para preservar a identidade visual do estilo e evitar contaminação do processo de treinamento, foram deliberadamente excluídos do dataset:

* Revestimentos cerâmicos industriais sem caráter ornamental.
* Pisos contemporâneos sem relação estética ou histórica com a tradição azulejar.
* Artes vetoriais digitais que não representem azulejos reais.
* Imagens sintéticas geradas por Inteligência Artificial.
* Fotografias com excesso de elementos externos que ocultem ou descaracterizem os azulejos.
* Objetos decorativos que utilizem apenas fragmentos isolados de azulejaria sem representar efetivamente o estilo proposto.

## 5. Justificativa da Curadoria
A curadoria deste dataset não se restringe exclusivamente à azulejaria monocromática azul e branca produzida entre os séculos XVII e XVIII. Optou-se por representar a diversidade estética da azulejaria luso-brasileira por meio de uma seleção equilibrada de imagens contemplando painéis históricos, motivos religiosos, padrões geométricos, ornamentações florais, composições policromáticas, mosaicos decorativos e colagens de azulejos do tipo *patchwork*.

Essa abordagem busca permitir que o modelo aprenda não apenas um conjunto restrito de formas e cores, mas também a riqueza artística, cultural e histórica associada à evolução da azulejaria em Portugal e no Brasil. A diversidade controlada do dataset favorece a capacidade de generalização do modelo, permitindo a geração de novas imagens que preservem a identidade visual da azulejaria mesmo quando aplicadas a temas inéditos durante a inferência.

## 6. Objetivo do Fine-Tuning
O objetivo deste projeto é realizar o fine-tuning de um modelo generativo de imagens utilizando a técnica LoRA (Low-Rank Adaptation), de modo que o token `estilo_azulejaria` seja capaz de representar visualmente os elementos característicos da tradição azulejar luso-brasileira.

Ao final do treinamento, espera-se que o modelo seja capaz de reinterpretar diferentes conceitos, objetos, cenários e personagens através da estética da azulejaria, preservando elementos como: textura cerâmica esmaltada, estrutura modular dos azulejos, ornamentação tradicional, paleta cromática característica e a identidade visual da azulejaria portuguesa e brasileira.

## 7. Aplicação no Projeto Multimodal
O estilo treinado será utilizado como componente central de um pipeline multimodal capaz de integrar:

1. Processamento de Linguagem Natural (NLP);
2. Modelos de Linguagem de Grande Escala (LLMs);
3. Geração de Imagens por Difusão via Fine-Tuning LoRA;
4. Síntese de Voz (TTS);
5. Interface Interativa para Demonstração (Gradio/Hugging Face Spaces).

O objetivo final consiste na geração automática de imagens e descrições narradas utilizando o estilo visual definido por meio do token `estilo_azulejaria`, permitindo a demonstração prática dos conceitos abordados na disciplina de Modelos Multimodais.