# ==============================================================================
# SCRIPT FINAL - HACKATHON FORECAST BIG DATA 2025
#
# Objetivo: Consolidar o pipeline de dados e modelagem para gerar o
#           arquivo de submissão final.
#
# Autor: Rafael Winders
# Modelo: LightGBM
# ==============================================================================

import pandas as pd
import numpy as np
import lightgbm as lgb
import polars as pl
import os
import gc
import pickle
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÕES E CONSTANTES ---
print(">> 1. Configurando o ambiente...")
DATA_PATH = './data/'
SUBMISSIONS_PATH = './submissions/'

# Nomes dos arquivos de dados brutos (ajuste se necessário)
TRANSACOES_FILE = 'part-00000-tid-5196563791502273604-c90d3a24-52f2-4955-b4ec-fb143aae74d8-4-1-c000.snappy.parquet'
PRODUTOS_FILE = 'part-00000-tid-7173294866425216458-eae53fbf-d19e-4130-ba74-78f96b9675f1-4-1-c000.snappy.parquet'
PDVS_FILE = 'part-00000-tid-2779033056155408584-f6316110-4c9a-4061-ae48-69b77c7c8c36-4-1-c000.snappy.parquet'

TARGET = 'quantidade'

# Garante que a pasta de submissões exista
os.makedirs(SUBMISSIONS_PATH, exist_ok=True)

# --- 2. FUNÇÕES AUXILIARES ---
# (Funções de engenharia de features e modelagem)

def criar_features_temporais(df):
    """Cria features baseadas na data."""
    df = df.with_columns([
        pl.col("semana").dt.month().alias("mes"),
        pl.col("semana").dt.year().alias("ano"),
        pl.col("semana").dt.week().alias("semana_ano"),
    ])
    # Features Cíclicas para Mês
    df = df.with_columns([
        (np.sin(2 * np.pi * pl.col("mes") / 12)).alias("mes_sin"),
        (np.cos(2 * np.pi * pl.col("mes") / 12)).alias("mes_cos"),
    ])
    return df

def criar_features_lag_rolling(df):
    """Cria features de lag e rolling window."""
    # Ordena para garantir a sequência temporal correta
    df = df.sort(["pdv_id", "produto_id", "semana"])

    # Features de Lag
    for lag in [1, 2, 3, 4]:
        df = df.with_columns(
            pl.col(TARGET).shift(lag).over(["pdv_id", "produto_id"]).alias(f"{TARGET}_lag_{lag}")
        )

    # Features de Rolling Window (Média Móvel de 4 semanas)
    df = df.with_columns(
        pl.col(TARGET).rolling_mean(window_size=4, min_periods=1).over(["pdv_id", "produto_id"]).alias(f'{TARGET}_media_4w'),
        pl.col(TARGET).rolling_std(window_size=4, min_periods=1).over(["pdv_id", "produto_id"]).fill_null(0).alias(f'{TARGET}_std_4w'),
        pl.col(TARGET).rolling_max(window_size=4, min_periods=1).over(["pdv_id", "produto_id"]).alias(f'{TARGET}_max_4w'),
        pl.col(TARGET).rolling_min(window_size=4, min_periods=1).over(["pdv_id", "produto_id"]).alias(f'{TARGET}_min_4w')
    )
    return df

def otimizar_memoria(df_pd):
    """Aplica downcasting para reduzir o uso de memória."""
    print(">> Otimizando uso de memória (Downcasting)...")
    for col in df_pd.select_dtypes(include=[np.number]).columns:
        if df_pd[col].dtype.kind == 'i':
            df_pd[col] = pd.to_numeric(df_pd[col], downcast='integer')
        else:
            df_pd[col] = pd.to_numeric(df_pd[col], downcast='float')

    for col in df_pd.select_dtypes(include=['object']).columns:
         if col not in ['semana']:
            if df_pd[col].nunique() / len(df_pd) < 0.5:
                df_pd[col] = df_pd[col].astype('category')
    return df_pd


# --- 3. PIPELINE DE ENGENHARIA DE FEATURES ---
print("\n>> 2. Iniciando pipeline de engenharia de features...")

# Carregamento dos dados brutos
transacoes = pl.read_parquet(os.path.join(DATA_PATH, TRANSACOES_FILE))
produtos = pl.read_parquet(os.path.join(DATA_PATH, PRODUTOS_FILE))
pdvs = pl.read_parquet(os.path.join(DATA_PATH, PDVS_FILE))

# Renomeando colunas para consistência
transacoes = transacoes.rename({
    'internal_store_id': 'pdv_id',
    'internal_product_id': 'produto_id',
    'transaction_date': 'data',
    'quantity': 'quantidade',
    'gross_value': 'valor'
})
produtos = produtos.rename({'produto': 'produto_id'})
pdvs = pdvs.rename({'pdv': 'pdv_id'})

# Agregação semanal
transacoes = transacoes.with_columns(
    pl.col("data").str.to_datetime().dt.truncate("1w", offset="-0d").alias("semana")
)
agregado_semanal = transacoes.group_by(["semana", "pdv_id", "produto_id"]).agg([
    pl.col("quantidade").sum(),
    pl.col("valor").sum(),
    pl.count().alias("num_transacoes")
])

# Criação do grid completo (PDVs x Produtos x Semanas)
semanas = agregado_semanal.select(pl.col("semana").unique()).sort("semana")
combinacoes_unicas = agregado_semanal.select(["pdv_id", "produto_id"]).unique()
grid_completo = combinacoes_unicas.join(semanas, how="cross")

# Merge com dados agregados
dados_completos = grid_completo.join(
    agregado_semanal, on=["semana", "pdv_id", "produto_id"], how="left"
).with_columns(
    pl.col(TARGET).fill_null(0) # Vendas zero para combinações sem transação
)

# Merge com dados cadastrais
dados_completos = dados_completos.join(pdvs, on="pdv_id", how="left")
dados_completos = dados_completos.join(produtos.select(['produto_id', 'categoria']), on="produto_id", how="left")

# Criação das features
print(">> Criando features temporais, de lag e rolling...")
dados_features = criar_features_temporais(dados_completos)
dados_features = criar_features_lag_rolling(dados_features)

# Limpeza e tratamento final
dados_features = dados_features.filter(pl.col('quantidade_lag_4').is_not_null())
dados_features = dados_features.fill_null(0) # Preenche NaNs restantes

# Conversão para Pandas para o LightGBM e otimização
df_final = dados_features.to_pandas()
df_final = otimizar_memoria(df_final)

del dados_completos, dados_features, transacoes, produtos, pdvs, agregado_semanal, grid_completo
gc.collect()

print(">> Engenharia de features concluída!")
print(f">> Shape do dataset de treino final: {df_final.shape}")


# --- 4. TREINAMENTO DO MODELO FINAL ---
print("\n>> 3. Treinando o modelo LightGBM final...")

# Definir features e target
features = [col for col in df_final.columns if col not in [
    'semana', 'pdv_id', 'produto_id', TARGET, 'valor', 'num_transacoes', 'ano'
]]
X_treino = df_final[features]
y_treino = df_final[TARGET]

# Parâmetros do LightGBM (os mesmos do seu notebook de experimentação)
lgb_params = {
    'objective': 'regression_l1',
    'metric': 'mae',
    'boosting_type': 'gbdt',
    'n_estimators': 3000, # Aumentado para o treino final com dados completos
    'learning_rate': 0.05,
    'num_leaves': 31,
    'max_depth': -1,
    'seed': 42,
    'n_jobs': -1,
    'verbose': -1,
    'colsample_bytree': 0.8,
    'subsample': 0.8,
}

# Treinar o modelo com todos os dados de 2022
modelo_final = lgb.LGBMRegressor(**lgb_params)
modelo_final.fit(X_treino, y_treino,
                 categorical_feature=[col for col in X_treino.columns if X_treino[col].dtype.name == 'category'])


print(">> Treinamento concluído!")

# --- 5. GERAÇÃO DAS PREVISÕES PARA JANEIRO/2023 ---
print("\n>> 4. Gerando previsões para Janeiro/2023...")

# Criar o DataFrame de teste para as 5 semanas de Janeiro/2023
datas_predicao = pd.to_datetime([
    '2023-01-02', '2023-01-09', '2023-01-16', '2023-01-23', '2023-01-30'
])

# Usar as combinações PDV/Produto do último período de treino conhecido
df_teste_base = df_final[df_final['semana'] == df_final['semana'].max()][['pdv_id', 'produto_id'] + features].copy()

# DataFrames para cada semana de previsão
dfs_para_prever = []
df_historico_pred = df_final.copy() # Histórico que será atualizado com as previsões

for i, data_semana in enumerate(datas_predicao):
    print(f">> Preparando dados para a semana {i+1} de Jan/2023...")

    df_pred_semana = combinacoes_unicas.to_pandas()
    df_pred_semana['semana'] = data_semana

    # Merge com dados cadastrais
    df_pred_semana = pd.merge(df_pred_semana, pdvs.to_pandas(), on='pdv_id', how='left')
    df_pred_semana = pd.merge(df_pred_semana, produtos.select(['produto_id', 'categoria']).to_pandas(), on='produto_id', how='left')
    
    # Criar features temporais para a semana da previsão
    df_pred_semana['mes'] = df_pred_semana['semana'].dt.month
    df_pred_semana['semana_ano'] = df_pred_semana['semana'].dt.isocalendar().week
    df_pred_semana['mes_sin'] = np.sin(2 * np.pi * df_pred_semana['mes'] / 12)
    df_pred_semana['mes_cos'] = np.cos(2 * np.pi * df_pred_semana['mes'] / 12)

    # Pegar histórico recente para calcular lags e rollings
    df_historico_pred = df_historico_pred.sort_values(by=['pdv_id', 'produto_id', 'semana'])
    
    # Criar features de lag e rolling com base no histórico + previsões anteriores
    for lag in [1, 2, 3, 4]:
        lag_data = df_historico_pred.groupby(['pdv_id', 'produto_id'])[TARGET].shift(lag-1).rename(f'{TARGET}_lag_{lag}')
        df_pred_semana = df_pred_semana.merge(
            lag_data.reset_index().rename(columns={'index':'original_index'}).drop_duplicates(subset=['original_index']),
            left_on=['pdv_id', 'produto_id'],
            right_on=['pdv_id', 'produto_id'],
            how='left'
        )
        df_pred_semana = df_pred_semana.drop(columns=['original_index'])


    rolling_feats = df_historico_pred.groupby(['pdv_id', 'produto_id'])[TARGET].rolling(window=4, min_periods=1).agg(['mean', 'std', 'max', 'min']).reset_index()
    rolling_feats = rolling_feats.rename(columns={'mean':f'{TARGET}_media_4w', 'std':f'{TARGET}_std_4w', 'max':f'{TARGET}_max_4w', 'min':f'{TARGET}_min_4w'})
    
    df_pred_semana = pd.merge(df_pred_semana, rolling_feats, on=['pdv_id', 'produto_id'], how='left')
    df_pred_semana = df_pred_semana.fill_null(0)

    # Previsão
    X_teste = df_pred_semana[features]
    X_teste = otimizar_memoria(X_teste)
    
    previsao = modelo_final.predict(X_teste)
    previsao = np.maximum(0, previsao).astype(int) # Arredondar e garantir não-negatividade
    
    df_pred_semana[TARGET] = previsao
    df_pred_semana['semana_num'] = i + 1
    
    # Adicionar previsão ao histórico para a próxima iteração
    df_historico_pred = pd.concat([df_historico_pred, df_pred_semana], ignore_index=True)

    dfs_para_prever.append(df_pred_semana[['semana_num', 'pdv_id', 'produto_id', TARGET]])


# Concatenar todas as previsões
df_submissao = pd.concat(dfs_para_prever, ignore_index=True)

# Renomear colunas para o formato final
df_submissao = df_submissao.rename(columns={
    'semana_num': 'semana',
    'produto_id': 'produto',
    'pdv_id': 'pdv',
    'quantidade': 'quantidade'
})


# --- 6. SALVAR ARQUIVOS DE SUBMISSÃO ---
print("\n>> 5. Salvando arquivos de submissão...")

# Formato CSV
csv_path = os.path.join(SUBMISSIONS_PATH, 'submission.csv')
df_submissao[['semana', 'pdv', 'produto', 'quantidade']].to_csv(
    csv_path,
    sep=';',
    index=False,
    header=False, # O desafio não especifica header, então removemos
    encoding='utf-8'
)
print(f">> Submissão em CSV salva em: {csv_path}")

# Formato Parquet
parquet_path = os.path.join(SUBMISSIONS_PATH, 'submission.parquet')
df_submissao[['semana', 'pdv', 'produto', 'quantidade']].to_parquet(parquet_path, index=False)
print(f">> Submissão em Parquet salva em: {parquet_path}")

print("\n>> PROCESSO FINALIZADO COM SUCESSO!")