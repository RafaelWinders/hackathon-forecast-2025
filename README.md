
# Hackathon Forecast Big Data 2025 - Modelo de Previsão de Vendas

## 🎯 Objetivo

Este projeto foi desenvolvido para o **Desafio Técnico – Hackathon Forecast Big Data 2025**. O objetivo é criar um modelo de previsão de vendas (forecast) para apoiar o varejo na reposição de produtos.

A tarefa consiste em prever a **quantidade semanal de vendas por PDV (Ponto de Venda) e SKU (Unidade de Manutenção de Estoque)** para as cinco semanas de janeiro de 2023, utilizando como base o histórico de vendas de 2022.

-----

## ⚙️ Instalação e Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### 1\. Pré-requisitos

  - **Python 3.9+**
  - **Git**

### 2\. Clonar o Repositório

### 3\. Criar e Ativar o Ambiente Virtual

É altamente recomendado usar um ambiente virtual para isolar as dependências.

  * **Para Windows:**
    ```cmd
    # 1. Criar o ambiente virtual
    py -m venv venv

    # 2. Ativar o ambiente
    .\venv\Scripts\activate
    ```
  * **Para Linux/macOS:**
    ```bash
    # 1. Criar o ambiente virtual
    python3 -m venv venv

    # 2. Ativar o ambiente
    source venv/bin/activate
    ```

### 4\. Instalar as Dependências

Todas as bibliotecas necessárias estão listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

*Observação: A instalação pode levar de 5 a 10 minutos, dependendo da sua conexão com a internet.*

### 5\. Configurar o Kernel do Jupyter

Para garantir que os notebooks usem o ambiente virtual correto, execute o comando abaixo:

```bash
python -m ipykernel install --user --name=hackathon-forecast --display-name="Python (hackathon-forecast)"
```

Após executar os notebooks, lembre-se de selecionar o kernel **"Python (hackathon-forecast)"** no canto superior direito da interface do Jupyter.

### 6\. Testar a Instalação

Para verificar se todas as bibliotecas foram instaladas corretamente, execute o script de teste:

```bash
python test_env.py
```

A saída deve mostrar "OK" para todas as importações.

### 7\. Baixar os Dados

Os dados brutos fornecidos pelo desafio devem ser colocados na pasta `/data`. Certifique-se de que os seguintes arquivos estejam presentes:

  - `data/part-00000-tid-2779033056155408584-f6316110-4c9a-4061-ae48-69b77c7c8c36-4-1-c000.snappy.parquet`
  - `data/part-00000-tid-5196563791502273604-c90d3a24-52f2-4955-b4ec-fb143aae74d8-4-1-c000.snappy.parquet`
  - `data/part-00000-tid-7173294866425216458-eae53fbf-d19e-4130-ba74-78f96b9675f1-4-1-c000.snappy.parquet`

-----

## 🚀 Como Gerar as Submissões (Fluxos de Execução)

O projeto oferece duas estratégias de submissão: uma com modelo vanilla e outra com hiperparâmetros otimizados pelo Optuna.

---

### 📋 **SUBMISSÃO 1: Modelo LightGBM Vanilla**

#### Passo 1: Engenharia de Features

Abra e execute todas as células do notebook:
▶️ **`notebooks/02-Feature-Engineering-Dask.ipynb`**

  - **O que ele faz?** Este notebook carrega os dados brutos, aplica todo o pré-processamento e a engenharia de features, e salva os datasets de treino e teste processados na pasta `data/`.
  - **Resultado:** Arquivos processados.

#### Passo 2: Treinamento e Geração da Submissão

Após a conclusão do Passo 1, abra e execute todas as células do notebook:
▶️ **`notebooks/04-Final-Pipeline.ipynb`**

  - **O que ele faz?** Carrega os dados processados, treina o modelo LightGBM final e gera o arquivo de previsão para as 5 semanas de janeiro de 2023.
  - **Resultado:** O arquivo `submission.parquet` será salvo na pasta submissions.

#### Passo 3: Conversão para Formato Final

Após a conclusão do Passo 2, abra e execute todas as células do notebook:
▶️ **`notebooks/05-Submission-Converter.ipynb`**

  - **O que ele faz?** Carrega o arquivo `submission.parquet` completo, remove as previsões de venda zero para atender ao limite de linhas da plataforma, e salva o resultado final nos formatos `submission_final.csv` e `submission_final.parquet`, prontos para serem enviados.
  - **Resultado:** Os arquivos `submission_final.csv` e `submission_final.parquet` serão salvos na pasta submissions.

---

### 🎯 **SUBMISSÃO 2: Modelo LightGBM Otimizado (Optuna)**

#### Passo 1: Engenharia de Features

Execute o mesmo notebook da Submissão 1:
▶️ **`notebooks/02-Feature-Engineering-Dask.ipynb`**

  - **Pré-requisito:** Gera os mesmos dados processados necessários para qualquer estratégia de modelagem.

#### Passo 2: Verificação dos Parâmetros Otimizados

Verifique se o arquivo de parâmetros otimizados está presente:
📁 **`data/best_lgbm_params_optuna.pkl`**

  - **Fonte:** Este arquivo foi gerado pelo notebook `06-Otimizacao-Hiperparametros-Optuna.ipynb` (processo demorado).
  - **Nota:** O arquivo já deve estar presente no repositório para evitar re-execução da otimização.

#### Passo 3: Treinamento e Submissão Final Otimizada

Execute o notebook principal da segunda submissão:
▶️ **`notebooks/08-Final-Optuna.ipynb`**

  - **O que ele faz?** Carrega os dados processados, utiliza os parâmetros otimizados pelo Optuna, treina o modelo LightGBM final e gera diretamente os arquivos de submissão filtrados (sem zeros).
  - **Resultado:** Os arquivos `submission_final_optuna.csv` e `submission_final_optuna.parquet` serão salvos na pasta submissions.
  - **Vantagem:** Pipeline integrado que já remove automaticamente as previsões zero, gerando arquivos prontos para submissão.

-----

## 📂 Estrutura do Projeto

```
.
├── data/                  # Dados brutos e processados
│   ├── best_lgbm_params_optuna.pkl      # Parâmetros otimizados pelo Optuna
│   └── [outros arquivos processados]    # Dados de features e modelos
├── notebooks/             # Jupyter Notebooks com a análise e desenvolvimento
│   ├── 01-EDA.ipynb       # Análise Exploratória dos Dados
│   ├── 02-Feature-Engineering-Dask.ipynb # PASSO 1: Gera os dados de treino/teste
│   ├── 03-Modeling-Experiments.ipynb     # Documentação da escolha e comparação de modelos
│   ├── 04-Final-Pipeline.ipynb           # SUBMISSÃO 1: Modelo vanilla
│   ├── 05-Submission-Converter.ipynb     # SUBMISSÃO 1: Converte para formato final
│   ├── 06-Otimizacao-Hiperparametros-Optuna.ipynb # Otimização de hiperparâmetros
│   ├── 07-Optuna-Experiments.ipynb       # Experimentos com Optuna
│   └── 08-Final-Optuna.ipynb             # SUBMISSÃO 2: Modelo otimizado
├── submissions/           # Arquivos de submissão gerados
│   ├── submission_final.csv              # Submissão 1 (modelo vanilla)
│   └── submission_final_optuna.csv       # Submissão 2 (modelo otimizado)
├── .gitignore             # Arquivos ignorados pelo Git
├── requirements.txt       # Lista de dependências Python
├── test_env.py            # Script para verificar a instalação do ambiente
└── README.md              # Documentação do projeto
```

-----

## 🛠️ Metodologia Aplicada

A solução foi desenvolvida seguindo uma abordagem estruturada com duas estratégias de submissão.

### 🔬 **Desenvolvimento Base**

1.  **Análise Exploratória (`01-EDA.ipynb`):** Investigação profunda dos dados para entender distribuições, sazonalidades e tendências, guiando a engenharia de features.
2.  **Engenharia de Features Escalável (`02-Feature-Engineering-Dask.ipynb`):** Uso de **Dask** e **Polars** para processar grande volume de dados. Foram criadas features temporais, de lag e estatísticas móveis.
3.  **Modelagem e Documentação (`03-Modeling-Experiments.ipynb`):** Este notebook serve como um "diário de bordo", documentando os testes com diferentes algoritmos (XGBoost, LightGBM) e justificando a escolha do **LightGBM** como modelo final devido ao seu equilíbrio entre performance, velocidade e eficiência de memória.

### 🎯 **Estratégias de Submissão**

#### **Submissão 1: Modelo Vanilla**
- **Pipeline Final (`04-Final-Pipeline.ipynb`):** LightGBM com parâmetros padrão otimizados manualmente.
- **Conversão (`05-Submission-Converter.ipynb`):** Remove predições zero para atender limites da plataforma.
- **Foco:** Baseline sólida e rápida implementação.

#### **Submissão 2: Modelo Otimizado**
- **Otimização de Hiperparâmetros (`06-Otimizacao-Hiperparametros-Optuna.ipynb`):** Uso do **Optuna** para encontrar a melhor combinação de hiperparâmetros através de busca bayesiana.
- **Pipeline Integrado (`08-Final-Optuna.ipynb`):** LightGBM com parâmetros otimizados e pipeline completo integrado.
- **Foco:** Máxima performance através de otimização automática de hiperparâmetros.

## Team
- Developer: Rafael Winders