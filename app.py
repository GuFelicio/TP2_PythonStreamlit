import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import pydeck as pdk

from plotly.subplots import make_subplots
import plotly.graph_objects as go

#Exercício 2
st.markdown("**Gráfico de Barras: Evolução Semanal dos Casos Novos de COVID-19 em São Paulo**")

data_url = 'D:\\Faculdade\\2 Semestre\\Python + Front\\TP2\\HIST_PAINEL_COVIDBR_2020_Parte1_30ago2024.csv'
data = pd.read_csv(data_url)

estado = 'SP'
dados_estado = data[data['estado'] == estado]

dados_agrupados = dados_estado.groupby('semana_epidemiologica')['casos_novos'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(dados_agrupados['semana_epidemiologica'], dados_agrupados['casos_novos'], color='skyblue')
plt.xlabel('Semana Epidemiológica')
plt.ylabel('Casos Novos')
plt.title(f'Evolução Semanal dos Casos Novos de COVID-19 em {estado}')
plt.xticks(rotation=45)

st.pyplot(plt)

st.markdown("_____")

#______________________________________________________________________________________________________________________
#Exercício 3

# Título
st.markdown("**Gráfico de Linha: Óbitos Acumulados por COVID-19 ao Longo das Semanas Epidemiológicas no Brasil**")

# Filtrando e preparando os dados para o Brasil
dados_brasil = data.groupby('semana_epidemiologica')['obitos'].sum().reset_index()
dados_brasil['obitos_acumulados'] = dados_brasil['obitos'].cumsum()

# Criando o gráfico de linha
plt.figure(figsize=(10, 6))
plt.plot(dados_brasil['semana_epidemiologica'], dados_brasil['obitos_acumulados'], marker='o', linestyle='-')
plt.xlabel('Semana Epidemiológica')
plt.ylabel('Óbitos Acumulados')
plt.title('Óbitos Acumulados por COVID-19 no Brasil ao Longo das Semanas Epidemiológicas')
plt.xticks(rotation=45)

# Exibindo o gráfico no Streamlit
st.pyplot(plt)

# Linha para finalizar o exercício
st.markdown("_____")

#______________________________________________________________________________________________________________________
#Exercício 4

# Título
st.markdown("**Gráfico de Área: Comparação da Evolução dos Casos Acumulados de COVID-19 em SP, RJ e MG**")

# Escolhendo três estados para comparação
estados = ['SP', 'RJ', 'MG']

# Filtrando dados para os três estados
dados_estados = data[data['estado'].isin(estados)]

# Agrupando por estado e semana epidemiológica
dados_agrupados = dados_estados.groupby(['estado', 'semana_epidemiologica'])['casos_acumulados'].sum().reset_index()

# Preparando os dados para o gráfico de área
plt.figure(figsize=(10, 6))

for estado in estados:
    dados_estado = dados_agrupados[dados_agrupados['estado'] == estado]
    plt.fill_between(dados_estado['semana_epidemiologica'], dados_estado['casos_acumulados'], alpha=0.5, label=estado)

plt.xlabel('Semana Epidemiológica')
plt.ylabel('Casos Acumulados')
plt.title('Evolução dos Casos Acumulados de COVID-19 em SP, RJ e MG')
plt.legend(title='Estado')
plt.xticks(rotation=45)

# Exibindo o gráfico no Streamlit
st.pyplot(plt)

# Linha para finalizar o exercício
st.markdown("_____")


#______________________________________________________________________________________________________________________
#Exercício 5

# Título
st.markdown("**Mapa Interativo: Distribuição dos Casos Acumulados de COVID-19 por Município em São Paulo (SP)**")

# Filtrando dados para o estado de São Paulo
estado_escolhido = 'SP'
dados_municipios_sp = data[data['estado'] == estado_escolhido]

# Selecionando apenas as colunas necessárias (latitude, longitude e casos acumulados)
dados_mapa = dados_municipios_sp[['municipio', 'casos_acumulados', 'latitude', 'longitude']].dropna()

# Exibindo o mapa interativo
st.map(dados_mapa)

# Linha para finalizar o exercício
st.markdown("_____")


#______________________________________________________________________________________________________________________
#Exercício 6

# Título
st.markdown("**Gráfico de Barras: Comparação entre Casos Novos e Óbitos Novos de COVID-19 por Estado na Semana Epidemiológica Mais Recente**")

# Encontrando a semana epidemiológica mais recente
semana_recente = data['semana_epidemiologica'].max()

# Filtrando dados para a semana mais recente
dados_semana_recente = data[data['semana_epidemiologica'] == semana_recente]

# Agrupando os dados por estado para calcular casos e óbitos novos
dados_por_estado = dados_semana_recente.groupby('estado')[['casos_novos', 'obitos_novos']].sum().reset_index()

# Criando o gráfico de barras
fig, ax = plt.subplots(figsize=(12, 6))
bar_width = 0.4
indices = range(len(dados_por_estado))

ax.bar(indices, dados_por_estado['casos_novos'], width=bar_width, label='Casos Novos', color='skyblue')
ax.bar([i + bar_width for i in indices], dados_por_estado['obitos_novos'], width=bar_width, label='Óbitos Novos', color='salmon')

# Configurando o gráfico
ax.set_xlabel('Estado')
ax.set_ylabel('Número de Casos/Óbitos')
ax.set_title('Casos Novos vs Óbitos Novos de COVID-19 por Estado na Semana Epidemiológica Mais Recente')
ax.set_xticks([i + bar_width / 2 for i in indices])
ax.set_xticklabels(dados_por_estado['estado'], rotation=45)
ax.legend()

# Exibindo o gráfico no Streamlit
st.pyplot(fig)

# Linha para finalizar o exercício
st.markdown("_____")


#______________________________________________________________________________________________________________________
#Exercício 7

# Título
st.markdown("**Boxplot: Distribuição dos Casos Novos de COVID-19 por Semana Epidemiológica nas Regiões Norte, Nordeste e Sudeste**")

# Criando um mapeamento de estados para regiões
regioes = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP']
}

# Adicionando a coluna de região aos dados
data['regiao'] = data['estado'].map(lambda x: next((regiao for regiao, estados in regioes.items() if x in estados), None))

# Filtrando dados para as três regiões selecionadas
dados_regioes = data[data['regiao'].isin(['Norte', 'Nordeste', 'Sudeste'])]

# Criando o boxplot com Seaborn
plt.figure(figsize=(12, 6))
sns.boxplot(x='semana_epidemiologica', y='casos_novos', hue='regiao', data=dados_regioes, palette='Set2')

plt.xlabel('Semana Epidemiológica')
plt.ylabel('Casos Novos')
plt.title('Distribuição dos Casos Novos de COVID-19 por Semana Epidemiológica nas Regiões Norte, Nordeste e Sudeste')
plt.xticks(rotation=45)

# Exibindo o gráfico no Streamlit
st.pyplot(plt)

# Linha para finalizar o exercício
st.markdown("_____")

#______________________________________________________________________________________________________________________
#Exercício 8

# Título
st.markdown("**Gráfico de Área: Evolução dos Casos Novos de COVID-19 por Semana Epidemiológica na Região Nordeste**")

# Filtrando dados para a Região Nordeste
regiao_escolhida = 'Nordeste'
dados_nordeste = data[data['regiao'] == regiao_escolhida]

# Agrupando os dados por semana epidemiológica
dados_agrupados = dados_nordeste.groupby('semana_epidemiologica')['casos_novos'].sum().reset_index()

# Criando o gráfico de área com Altair
grafico_area = alt.Chart(dados_agrupados).mark_area(opacity=0.5).encode(
    x='semana_epidemiologica:O',
    y='casos_novos:Q',
    tooltip=['semana_epidemiologica', 'casos_novos']
).properties(
    title='Evolução dos Casos Novos de COVID-19 na Região Nordeste por Semana Epidemiológica',
    width=600,
    height=400
)

# Exibindo o gráfico no Streamlit
st.altair_chart(grafico_area)

# Linha para finalizar o exercício
st.markdown("_____")

#______________________________________________________________________________________________________________________
#Exercício 9

# Título
st.markdown("**Heatmap: Correlação entre Casos Novos, Óbitos Novos e Leitos Ocupados em São Paulo (SP)**")

# Filtrando dados para o estado de São Paulo
estado_escolhido = 'SP'
dados_sp = data[data['estado'] == estado_escolhido]

# Selecionando as colunas relevantes para a correlação
# Certifique-se de que a coluna 'leitos_ocupados' esteja presente nos dados
dados_correlação = dados_sp[['casos_novos', 'obitos_novos', 'leitos_ocupados']].dropna()

# Calculando a correlação entre os dados
correlacao = dados_correlação.corr().reset_index().melt('index')

# Renomeando as colunas para a construção do heatmap
correlacao.columns = ['Variável 1', 'Variável 2', 'Correlação']

# Criando o heatmap com Altair
heatmap = alt.Chart(correlacao).mark_rect().encode(
    x='Variável 1:O',
    y='Variável 2:O',
    color=alt.Color('Correlação:Q', scale=alt.Scale(scheme='viridis')),
    tooltip=['Variável 1', 'Variável 2', 'Correlação']
).properties(
    title='Correlação entre Casos Novos, Óbitos Novos e Leitos Ocupados em São Paulo (SP)',
    width=400,
    height=400
)

# Exibindo o heatmap no Streamlit
st.altair_chart(heatmap)

# Linha para finalizar o exercício
st.markdown("_____")


#______________________________________________________________________________________________________________________
#Exercício 10

# Título
st.markdown("**Gráfico de Pizza: Distribuição Percentual dos Casos Acumulados de COVID-19 entre as Regiões do Brasil**")

# Agrupando dados por região para calcular o total de casos acumulados
dados_por_regiao = data.groupby('regiao')['casos_acumulados'].sum().reset_index()

# Criando o gráfico de pizza com Plotly
fig = px.pie(dados_por_regiao, values='casos_acumulados', names='regiao',
             title='Distribuição Percentual dos Casos Acumulados de COVID-19 por Região',
             color_discrete_sequence=px.colors.sequential.Viridis)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig)

# Linha para finalizar o exercício
st.markdown("_____")

#______________________________________________________________________________________________________________________
#Exercício 11

# Título
st.markdown("**Subplots: Comparação dos Casos Novos e Óbitos Novos de COVID-19 por Semana Epidemiológica nas Regiões Sudeste e Nordeste**")

# Filtrando dados para as regiões escolhidas
regioes_comparacao = ['Sudeste', 'Nordeste']
dados_comparacao = data[data['regiao'].isin(regioes_comparacao)]

# Agrupando dados por região e semana epidemiológica
dados_agrupados = dados_comparacao.groupby(['regiao', 'semana_epidemiologica'])[['casos_novos', 'obitos_novos']].sum().reset_index()

# Criando subplots com Plotly
fig = make_subplots(rows=1, cols=2, subplot_titles=('Sudeste', 'Nordeste'))

# Adicionando gráficos de barras para a Região Sudeste
dados_sudeste = dados_agrupados[dados_agrupados['regiao'] == 'Sudeste']
fig.add_trace(
    go.Bar(x=dados_sudeste['semana_epidemiologica'], y=dados_sudeste['casos_novos'], name='Casos Novos - Sudeste', marker_color='blue'),
    row=1, col=1
)
fig.add_trace(
    go.Bar(x=dados_sudeste['semana_epidemiologica'], y=dados_sudeste['obitos_novos'], name='Óbitos Novos - Sudeste', marker_color='red'),
    row=1, col=1
)

# Adicionando gráficos de barras para a Região Nordeste
dados_nordeste = dados_agrupados[dados_agrupados['regiao'] == 'Nordeste']
fig.add_trace(
    go.Bar(x=dados_nordeste['semana_epidemiologica'], y=dados_nordeste['casos_novos'], name='Casos Novos - Nordeste', marker_color='blue'),
    row=1, col=2
)
fig.add_trace(
    go.Bar(x=dados_nordeste['semana_epidemiologica'], y=dados_nordeste['obitos_novos'], name='Óbitos Novos - Nordeste', marker_color='red'),
    row=1, col=2
)

# Atualizando layout do gráfico
fig.update_layout(
    title_text='Comparação dos Casos Novos e Óbitos Novos de COVID-19 por Semana Epidemiológica',
    showlegend=False,
    width=1000,
    height=500
)

# Exibindo os subplots no Streamlit
st.plotly_chart(fig)

# Linha para finalizar o exercício
st.markdown("_____")

#______________________________________________________________________________________________________________________
#Exercício 12

# Título para diferenciar o começo do exercício
st.markdown("**Mapa Interativo: Densidade Populacional Ajustada para Casos Acumulados de COVID-19 por Município na Região Sudeste**")

# Filtrando dados para a Região Sudeste
regiao_escolhida = 'Sudeste'
dados_sudeste = data[data['regiao'] == regiao_escolhida]

# Filtrando as colunas necessárias (municipio, casos acumulados, latitude, longitude e população)
dados_mapa = dados_sudeste[['municipio', 'casos_acumulados', 'latitude', 'longitude', 'populacao']].dropna()

# Calculando casos ajustados por densidade populacional
dados_mapa['casos_por_100k'] = (dados_mapa['casos_acumulados'] / dados_mapa['populacao']) * 100000

# Configurando o mapa com PyDeck
layer = pdk.Layer(
    "ScatterplotLayer",
    data=dados_mapa,
    get_position='[longitude, latitude]',
    get_radius=1000,
    get_fill_color='[255, 0, 0, 140]',
    pickable=True,
    extruded=True,
    radius_scale=10,
)

view_state = pdk.ViewState(
    latitude=dados_mapa['latitude'].mean(),
    longitude=dados_mapa['longitude'].mean(),
    zoom=6,
    pitch=40
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{municipio}\nCasos por 100k: {casos_por_100k:.2f}"}
)

# Exibindo o mapa no Streamlit
st.pydeck_chart(r)

# Linha para finalizar o exercício
st.markdown("_____")