import pandas as pd
import os
import numpy as np

#isso aqui é apenas teste, pode apagar o arquivo depois.

print("--- Iniciando teste de carregamento de dados ---")

# 1. Definir o caminho para a pasta de dados brutos e o nome do arquivo.
#    Esta forma de juntar os caminhos com os.path.join funciona bem em qualquer sistema operacional.
DATA_RAW_PATH = os.path.join("data", "raw")
FILE_NAME = "campeonato-brasileiro-full.csv"
full_path = os.path.join(DATA_RAW_PATH, FILE_NAME)

# 2. Usar um bloco try...except para lidar com o caso do arquivo não existir.
#    Isso torna o script mais robusto e dá uma mensagem de erro clara.
try:
    # 3. Carregar o arquivo CSV usando a biblioteca Pandas.
    print(f"Carregando o arquivo: {full_path}")
    df = pd.read_csv(full_path)
    
    # 4. Usar o método .tail(5) para selecionar as 5 últimas linhas do DataFrame.
    print("\nAs 5 últimas linhas do arquivo são:")
    ultimas_linhas = df.tail(5)
    
    # 5. Imprimir o resultado na tela.
    print(ultimas_linhas)
    
    print("\n--- Teste finalizado com sucesso! ---")

except FileNotFoundError:
    print("\n--- ERRO ---")
    print(f"O arquivo não foi encontrado no caminho esperado: {full_path}")
    print("Verifique se você baixou o dataset e o colocou na pasta 'data/raw'.")

print("Iniciando a limpeza e preparação dos dados...")
print("-" * 30)

df['datetime'] = pd.to_datetime(df['data'] + ' ' + df['hora'], format='%d/%m/%Y %H:%M')
df = df[df['datetime'].dt.year >= 2013].copy() 
df = df.sort_values(by='datetime', ascending=True) 

colunas_essenciais = [
    'datetime',
    'mandante',
    'visitante',
    'mandante_Placar',
    'visitante_Placar'
]
df_clean = df[colunas_essenciais].copy()

# Criacao da nossa variável-alvo (target) - O "Resultado" Esta é a coluna que nosso modelo de classificação tentará prever.

conditions = [
    df_clean['mandante_Placar'] > df_clean['visitante_Placar'], 
    df_clean['mandante_Placar'] < df_clean['visitante_Placar'], 
    df_clean['mandante_Placar'] == df_clean['visitante_Placar']
]

choices = ['Vitoria_Mandante', 'Vitoria_Visitante', 'Empate']
df_clean['resultado'] = np.select(conditions, choices, default='Indefinido')

print("Tabela limpa e preparada:")
print(df_clean.tail(10))
print("-" * 30)
print("Informações técnicas da nova tabela (df_clean.info()):")
df_clean.info()