# CPCA A1 Methodological Note: Dataset, Benchmark and Explainable Semantic AI for BIM/IFC

Esta nota metodológica apresenta o enquadramento científico, a arquitetura de dados, o protocolo de validação e a estratégia experimental de inteligência artificial semântica para a modelação de informação da construção (BIM) utilizando o esquema normalizado Industry Foundation Classes (IFC, ISO 16739). O objetivo deste documento é fornecer uma base metodológica sólida para a candidatura informática CPCA A1.

---

## 1. Scientific question

A pergunta científica central que orienta esta investigação é:

> **Como podem modelos de IA interpretar pedidos BIM em linguagem natural, relacioná-los com conceitos IFC, produzir saídas técnicas estruturadas e justificar essas saídas com evidência rastreável?**

Esta questão liga conceitos fundamentais de engenharia civil e ciência da computação:
- **BIM como gestão de informação**: a informação alfanumérica é o núcleo funcional do modelo, e não apenas o seu aspeto visual ou geométrico.
- **IFC como estrutura semântica interoperável**: o mapeamento de classes e propriedades deve respeitar o esquema padrão neutro da indústria para garantir a portabilidade dos dados.
- **IA semântica**: traduz a intenção humana de engenharia expressa de forma vaga ou informal em esquemas técnicos estritos.
- **Explainable AI (XAI)**: garante que a interpretação da IA não seja uma "caixa preta", gerando uma justificação lógica e explícita baseada em termos textuais.
- **Candidatura CPCA A1**: fornece o suporte computacional robusto necessário para executar benchmarks de grande escala, treinar adaptadores leves de modelos e quantificar a qualidade e eficiência dos resultados.

---

## 2. Research gap

A literatura científica na interseção entre engenharia civil (AECO) e ciência computacional tem apresentado avanços isolados no uso de Large Language Models (LLMs) para tarefas genéricas de geração de código e parsing de prompts. Contudo, continua a ser necessário verificar de forma sistemática um protocolo integrado que combine:
- A tradução de pedidos BIM expressos em linguagem natural de engenharia civil;
- O grounding semântico direto no esquema regulamentar IFC;
- A validação estrutural contra contratos JSON rígidos;
- A rastreabilidade semântica (evidence trace);
- A avaliação reprodutível e automatizada (replay/harness);
- A adaptação experimental leve de modelos em ambientes restritos;
- A explicabilidade focada nas necessidades do engenheiro revisor.

Este trabalho aborda esta lacuna ao propor e testar um fluxo contínuo de inferência, validação de contratos e explicabilidade auditável para engenheiros civis.

---

## 3. Why this is CPCA A1 work

Esta candidatura não se foca no treino de modelos locais com computadores portáteis comuns. O projeto propõe uma infraestrutura computacional académica robusta para viabilizar:
- A curadoria e processamento de datasets semânticos volumosos;
- A execução sistemática de benchmarks em múltiplos LLMs abertos;
- A comparação de arquiteturas em termos de precisão e custo;
- A adaptação experimental fina via adaptadores de baixo rank (LoRA/QLoRA);
- A avaliação da estabilidade semântica do output gerado sob diferentes parâmetros;
- O estudo e validação do impacto de técnicas de quantização e Quantization-Aware Training (QAT) na qualidade e explicabilidade dos modelos.

Neste contexto, o recurso a computação de alto desempenho é o meio para gerar evidência científica sólida e reprodutível, e não o fim do projeto em si.

---

## 4. What has already been built as preliminary evidence

Como prova de maturidade e viabilidade da investigação, foi desenvolvida uma evidência preliminar pública e sanitizada, constituída por três elementos:
1. **Repositório público**: contém a especificação de dados, código de validação determinístico e scripts de replay.
2. **Harness público de replay**: validação offline do dataset sanitizado de 20 casos (`sample20_public_predictions.jsonl`).
3. **Demo guiada interativa**: interface gráfica web que permite experimentar o parsing de solicitações e visualizar em tempo real:
   - A classe IFC candidata sugerida;
   - A tabela dinâmica de atributos LOI (Level of Information);
   - A nota técnica explicativa sobre LOD (Level of Detail);
   - A visualização conceptual tridimensional (LOD) simplificada;
   - O payload JSON estruturado sob o contrato técnico;
   - O rastreio de evidência (*evidence trace*) e as limitações do modelo.

---

## 5. Dataset construction methodology

O dataset de teste foi concebido com base em cenários práticos da engenharia civil e gestão BIM. A curadoria de dados modela solicitações típicas sobre componentes fundamentais, incluindo pilares, paredes, vigas, lajes e janelas, bem como a definição de propriedades térmicas, acústicas, estruturais e de resistência ao fogo.

Cada registo semântico curado é estruturado como uma unidade contendo:
- **Pedido original**: a frase em linguagem natural enviada pelo utilizador.
- **Intenção de engenharia**: a categorização da tarefa requerida (ex: classificação, enriquecimento, validação).
- **Elemento BIM identificado**: o tipo físico do componente de construção.
- **Classe IFC candidata**: a entidade correspondente do esquema standard (ex: `IfcColumn`, `IfcWall`).
- **Requisitos de informação (LOI)**: campos regulamentares requeridos (tipo, material, função estrutural, validações).
- **Indicação de detalhe geométrico (LOD)**: notas de enquadramento sobre representação espacial.
- **JSON canónico**: a resposta esperada no formato do contrato.
- **Validação de esquema**: as restrições que validam a integridade do ficheiro.
- **Rastreio de evidência**: as pistas de texto que justificam a classificação.
- **Limitações de âmbito**: restrições específicas aplicadas à inferência.

### Exemplo conceptual de registo:
- **Input**: *“I need a reinforced concrete column with IFC classification and LOI information.”*
- **Grounding semântico**:
  - *"column"* &rarr; indica um elemento estrutural vertical.
  - *"reinforced concrete"* &rarr; define o material básico de composição.
  - *"IFC classification"* &rarr; indica a necessidade de mapeamento regulamentar para o esquema.
  - *"LOI information"* &rarr; especifica que são esperados atributos alfanuméricos normativos.
  - **Classe sugerida**: `IfcColumn`.
  - **LOD**: Representação tridimensional conceptual apenas (ilustrativa na demo).
  - **Status**: `PREVIEW`.

---

## 6. Why JSONL and structured contracts are used

O formato JSON Lines (JSONL) foi selecionado como padrão de armazenamento devido a várias vantagens metodológicas:
- Permite processar um caso de teste por linha de forma independente;
- Evita erros de parsing global ao analisar grandes volumes de dados;
- Simplifica a leitura, filtragem e escrita de partições de teste (splits);
- Facilita a validação individual contra o contrato técnico de dados.

O contrato estruturado exige que qualquer previsão de IA contenha, no mínimo, as seguintes chaves chave:
1. `status` &rarr; o estado de validação técnica do registo (ex: `PREVIEW`).
2. `canonical_output` &rarr; o mapeamento estruturado com a classe IFC candidata sugerida.
3. `validation` &rarr; a indicação de conformidade e completude.
4. `metadata` &rarr; dados sobre o modelo, split e métricas básicas de execução.
5. `evidence_trace` &rarr; as evidências extraídas para fundamentar a interpretação.
6. `limitations` &rarr; avisos sobre o alcance e precisão da informação.

Para a engenharia civil, este contrato em JSON atua como uma ponte determinística que reduz a ambiguidade inerente à linguagem natural, traduzindo ideias textuais em campos estruturados diretamente legíveis por bases de dados de software BIM.

---

## 7. Dataset validation methodology

A validação de integridade dos dados baseia-se em seis níveis técnicos sucessivos:

### 7.1 JSON parse validation
Garante que cada linha do ficheiro de dados corresponde a um objeto JSON sintaticamente válido. Qualquer falha de codificação ou caractere inválido invalida o registo no processo de leitura.

### 7.2 Schema validation
Verifica que todas as chaves obrigatórias descritas no contrato estruturado de dados estão presentes na raiz do objeto JSON e possuem os tipos corretos (dicionários, strings, listas).

### 7.3 IFC semantic validation
Confirma que a classe sugerida (ex: `IfcColumn`, `IfcSlab`) pertence ao esquema regulamentar autorizado do IFC e corresponde logicamente ao elemento de engenharia civil detetado no texto de entrada.

### 7.4 LOI/LOD consistency check
Garante a correta separação conceitual entre requisitos de dados. Os campos da chave `loi` devem referir-se a parâmetros alfanuméricos necessários para a gestão do modelo (material, fire rating, U-value). Os parâmetros de `lod` devem focar-se no nível de desenvolvimento e detalhe espacial, garantindo que representações conceituais (como previews OBJ tridimensionais) sejam marcadas como não certificadas.

### 7.5 Replay validation
O harness computacional lê todo o ficheiro do dataset, executa a validação de regras de ponta a ponta e reporta o rácio de conformidade e integridade estrutural.

### 7.6 Public sanitization
Todos os dados e artefactos públicos passam por um filtro de higienização rígido que assegura a ausência de chaves de API, segredos, caminhos de ficheiros locais, credenciais de desenvolvimento ou pesos de modelos proprietários.

---

## 8. Public sample20 and preliminary benchmark

O ficheiro `sample20_public_predictions.jsonl` constitui uma amostra de referência pública, contendo 20 casos de testes higienizados. A sua função não é servir para o treino final dos modelos, mas sim atuar como:
- Um modelo representativo da estrutura interna do dataset;
- Uma prova de conceito funcional para o protocolo de validação (replay);
- Um elemento de teste objetivo e auditável para avaliadores e investigadores.

O benchmark preliminar avalia o rácio de sucesso do replay e a conformidade do esquema das 20 previsões de teste. Nas fases subsequentes da candidatura CPCA A1, este mesmo ecossistema de validação será aplicado a conjuntos de dados alargados em diferentes arquiteturas de modelos.

---

## 9. Benchmark methodology for CPCA A1

Com o suporte computacional da candidatura CPCA A1, a metodologia de benchmarking será escalada para avaliar o desempenho comparativo de LLMs open-source de grande escala. O protocolo incluirá:
- **Modelos base abertos**: avaliação de desempenho em arquiteturas de diferentes tamanhos de parâmetros (ex: 8B, 70B).
- **Inferência comparativa**: testes comparativos entre modelos base puros sem afinação (zero-shot e few-shot).
- **Fine-tuning experimental**: aplicação de adaptadores leves LoRA/QLoRA com dados de engenharia civil/BIM.
- **Análise pós-adaptação**: comparação direta de desempenho antes e depois da afinação fina dos modelos.
- **Avaliação de compressão**: testes de perda de qualidade semântica sob técnicas de quantização.
- **Rastreabilidade semântica**: medição da qualidade das justificações lógicas geradas.

### Métricas de Avaliação:
- **JSON Validity Rate**: percentagem de respostas que são JSON sintaticamente válidos.
- **Schema Compliance Rate**: percentagem de objetos que cumprem todas as chaves obrigatórias.
- **IFC Class Accuracy**: taxa de acerto na classificação da entidade IFC correta.
- **LOI Field Completeness**: rácio de propriedades regulamentares obrigatórias identificadas.
- **LOD/LOI Consistency**: conformidade entre o detalhe de informação pedido e a resposta estruturada.
- **Evidence Trace Coverage**: precisão das referências textuais extraídas como justificação.
- **Hallucinated IFC Class Rate**: taxa de sugestão de classes inexistentes no padrão IFC.
- **Missing Information Detection**: capacidade do modelo em apontar quando um pedido carece de dados técnicos essenciais.
- **Replay Reproducibility**: estabilidade dos outputs sob sementes e ambientes idênticos.
- **Explanation Usefulness**: avaliação qualitativa do trace por engenheiros especialistas.

---

## 10. Explainability methodology: XAI before, during and after training

No contexto deste projeto, a explicabilidade (XAI) não é tratada como uma interface decorativa desenvolvida após a conclusão dos testes. A rastreabilidade semântica é integrada diretamente na conceção do dataset: o modelo aprende não apenas a classe final, mas o raciocínio que justifica essa escolha técnica.

A arquitetura de explicabilidade é governada por:
- **Evidence Trace**: mapeamento explícito do tipo `input fragment` &rarr; `engineering interpretation` &rarr; `output field`.
- **Justificação de Alternativas**: identificação de classes IFC secundárias que foram consideradas mas descartadas durante o processo de parsing.
- **Sinalização de Ambiguidade**: deteção de termos contraditórios ou incompletos no pedido original.
- **Counterfactual BIM prompts**: análise de variação sistemática de termos e o seu impacto na classificação (ex: analisar a transição de saída de `IfcColumn` para `IfcBeam` ao alterar apenas o termo espacial de vertical para horizontal no pedido).
- **Revisão técnica por humanos**: mecanismos de auditoria visual de atributos LOI para engenheiros.

---

## 11. Relationship between LoRA, QLoRA, quantization and QAT

Para atingir objetivos de viabilidade científica e eficiência operacional no CPCA A1, a relação entre métodos de adaptação, compressão e explicabilidade é definida como se segue:

### LoRA (Low-Rank Adaptation)
Método de afinação fina eficiente que introduz matrizes de baixo rank adicionais na rede sem alterar os pesos originais do modelo. Isto permite especializar os modelos nas regras de sintaxe BIM/IFC sem degradação do conhecimento geral e com baixo custo computacional.

### QLoRA (Quantized LoRA)
Aplica a adaptação LoRA sobre um modelo base cujos pesos foram quantizados em precisão de 4 bits. É o método principal proposto para a experimentação académica nesta candidatura, pois permite correr e especializar modelos de grande porte em recursos de hardware restritos.

### Post-training quantization
Redução sistemática de precisão de pesos (ex: de FP16 para INT8 ou INT4) após o processo de treino. O seu impacto deve ser avaliado medindo se a compactação dos pesos afeta a taxa de alucinação de classes IFC ou a precisão do trace.

### QAT (Quantization-Aware Training)
Simula os efeitos da quantização durante a fase de treino/fine-tuning. O QAT atua puramente como um mecanismo de eficiência computacional e robustez de precisão do modelo; não atua como explicação e não substitui a metodologia XAI.

> [!IMPORTANT]
> **Regra de Governança**:
> Neste projeto, a metodologia **XAI** governa a qualidade semântica e a rastreabilidade; **LoRA/QLoRA** governam a adaptação experimental dos modelos; a **quantização e o QAT** governam a eficiência computacional e devem ser sempre avaliadas sob a condição de não degradar a explicabilidade científica.

---

## 12. Proposed CPCA A1 computational workflow

O pipeline computacional experimental a ser executado na infraestrutura de processamento da candidatura é estruturado da seguinte forma:

1. **Curadoria de casos BIM/IFC**: recolha e estruturação de novos cenários regulamentares da construção.
2. **Normalização em JSONL**: transformação dos dados no formato unificado de registo em ficheiros de linhas.
3. **Validação de contrato**: controlo de conformidade estrutural inicial através do script harness.
4. **Benchmark comparativo**: avaliação inicial zero-shot de modelos open-source em modo puro.
5. **Adaptação LoRA/QLoRA**: treino dos pesos do adaptador leve com dados especializados.
6. **Avaliação pós-adaptação**: execução de novos testes de replay para medir o ganho de precisão de mapeamento.
7. **Quantização/QAT**: aplicação de técnicas de compressão numérica para otimização de execução.
8. **Reavaliação XAI**: validação final de robustez da precisão de classificação e da qualidade dos traces.
9. **Relatório científico**: consolidação e discussão científica dos resultados obtidos.

```mermaid
flowchart LR
    A[Casos BIM/IFC curados] --> B[Registros semânticos JSONL]
    B --> C[Validação de contrato]
    C --> D[Benchmark com modelos open-source]
    D --> E[Adaptação LoRA/QLoRA]
    E --> F[Avaliação com harness]
    F --> G[Quantização ou QAT quando aplicável]
    G --> H[Reavaliação XAI e rastreabilidade]
    H --> I[Relatório científico CPCA A1]
```

---

## 13. Expected scientific outputs

Os resultados académicos esperados derivados da execução deste pipeline no CPCA A1 incluem:
- **Dataset semântico BIM/IFC v0.1**: conjunto de dados público enriquecido e validado sob esquema rígido.
- **Protocolo de benchmark**: suite de testes estandardizada de conformidade e replay.
- **Relatório comparativo de modelos**: análise profunda de precisão semântica de múltiplos LLMs.
- **Taxonomia de alucinações**: mapeamento de tipos de falhas de classificação em classes IFC.
- **Avaliação de explicabilidade**: estudo sobre a coerência lógica dos traces gerados pelos modelos.
- **Protótipo experimental afinado**: pesos dos adaptadores LoRA/QLoRA otimizados para conceitos de construção.
- **Relatório de compressão computacional**: análise da relação de perda de precisão sob efeito de quantização/QAT.
- **Artigos científicos**: submissão de relatórios e artigos sobre os resultados a conferências especializadas da área AECO/Computing.

---

## 14. Limitations and safeguards

- **Amostra pública restrita**: o dataset público inicial é uma versão restrita para demonstração de estrutura conceitual.
- **Sem inserção direta não supervisionada**: o preview 3D e os dados gerados possuem fins experimentais; não substituem a revisão humana de segurança por engenheiros civis qualificados.
- **Sem dados sensíveis**: os repositórios públicos não armazenam credenciais, segredos, ou código de arquitetura interna privada.
- **Não comercial**: o projeto é de natureza estritamente científica e de investigação aplicada.

---

## 15. Public artifacts and role in CPCA A1

Os artefactos preliminares públicos atualmente disponíveis são:
- **GitHub public semantic repository**: aloja a lógica de validação estrutural do contrato.
- **Hugging Face replay demo**: plataforma visual que permite carregar ficheiros de previsões e validar o dataset.
- **Hugging Face interactive guided harness**: página interativa para teste guiado de inputs por utilizadores sem conhecimentos de programação.

Estes artefactos preliminares servem como evidência de maturidade metodológica e de engenharia de software da equipa. Comprovam que a estrutura básica do contrato de dados, o algoritmo de validação e a visualização conceitual já se encontram desenvolvidos, necessitando apenas da capacidade computacional fornecida pela infraestrutura CPCA A1 para escalar a sua validação e afinação a conjuntos de dados massivos.

---

## 16. Take-home message

A candidatura CPCA A1 permitirá transformar uma evidência preliminar pública e sanitizada em um protocolo experimental mais amplo para avaliar IA semântica BIM/IFC, combinando dataset curado, benchmark reprodutível, adaptação leve de modelos e avaliação de explicabilidade técnica orientada à engenharia civil.
