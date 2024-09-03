import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import pydeck as pdk

from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Carregar o arquivo CSV com o delimitador correto
file_path = r'D:\Faculdade\2 Semestre\Python + Front\TP2\HIST_PAINEL_COVIDBR_2020_Parte1_30ago2024.csv'
data = pd.read_csv(file_path, sep=';', on_bad_lines='skip')

# Verificar os nomes das colunas
st.write(data.columns)

#________________________________________________________________________________________________________________________
# Exercício 2

st.markdown("**Gráfico de Barras: Evolução Semanal dos Casos Novos de COVID-19 em São Paulo**")
estado = 'SP'
dados_estado = data[data['estado'] == estado]
dados_agrupados = dados_estado.groupby('semanaEpi')['casosNovos'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(dados_agrupados['semanaEpi'], dados_agrupados['casosNovos'], color='skyblue')
plt.xlabel('Semana Epidemiológica')
plt.ylabel('Casos Novos')
plt.title(f'Evolução Semanal dos Casos Novos de COVID-19 em {estado}')
plt.xticks(rotation=45)
st.pyplot(plt)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 3

st.markdown("**Gráfico de Linha: Óbitos Acumulados por COVID-19 ao Longo das Semanas Epidemiológicas no Brasil**")
dados_brasil = data.groupby('semanaEpi')['obitosNovos'].sum().reset_index()
dados_brasil['obitos_acumulados'] = dados_brasil['obitosNovos'].cumsum()

plt.figure(figsize=(10, 6))
plt.plot(dados_brasil['semanaEpi'], dados_brasil['obitos_acumulados'], marker='o', linestyle='-')
plt.xlabel('Semana Epidemiológica')
plt.ylabel('Óbitos Acumulados')
plt.title('Óbitos Acumulados por COVID-19 no Brasil ao Longo das Semanas Epidemiológicas')
plt.xticks(rotation=45)
st.pyplot(plt)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 4

st.markdown("**Gráfico de Área: Comparação da Evolução dos Casos Acumulados de COVID-19 em SP, RJ e MG**")
estados = ['SP', 'RJ', 'MG']
dados_estados = data[data['estado'].isin(estados)]
dados_agrupados = dados_estados.groupby(['estado', 'semanaEpi'])['casosAcumulado'].sum().reset_index()

plt.figure(figsize=(10, 6))
for estado in estados:
    dados_estado = dados_agrupados[dados_agrupados['estado'] == estado]
    plt.fill_between(dados_estado['semanaEpi'], dados_estado['casosAcumulado'], alpha=0.5, label=estado)

plt.xlabel('Semana Epidemiológica')
plt.ylabel('Casos Acumulados')
plt.title('Evolução dos Casos Acumulados de COVID-19 em SP, RJ e MG')
plt.legend(title='Estado')
plt.xticks(rotation=45)
st.pyplot(plt)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 5

st.markdown("**Mapa Interativo: Distribuição dos Casos Acumulados de COVID-19 por Município em São Paulo (SP)**")

estado_escolhido = 'SP'
dados_municipios_sp = data[data['estado'] == estado_escolhido]

# Criando um dicionário de coordenadas de alguns municípios de São Paulo para exemplo
coordenadas_sp = {
    'São Paulo': {'lat': -23.55052, 'long': -46.633308},
    'Campinas': {'lat': -22.90556, 'long': -47.06083},
    'Santos': {'lat': -23.96083, 'long': -46.33361},
    'São José dos Campos': {'lat': -23.1896, 'long': -45.8841},
    'Sorocaba': {'lat': -23.5015, 'long': -47.4526}
}

# Adicionando as coordenadas ao DataFrame
dados_municipios_sp['lat'] = dados_municipios_sp['municipio'].map(lambda x: coordenadas_sp[x]['lat'] if x in coordenadas_sp else None)
dados_municipios_sp['long'] = dados_municipios_sp['municipio'].map(lambda x: coordenadas_sp[x]['long'] if x in coordenadas_sp else None)

# Removendo linhas sem coordenadas
dados_mapa_sp = dados_municipios_sp.dropna(subset=['lat', 'long'])

# Exibindo o mapa interativo
st.map(dados_mapa_sp)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 6

st.markdown("**Gráfico de Barras: Comparação entre Casos Novos e Óbitos Novos de COVID-19 por Estado na Semana Epidemiológica Mais Recente**")
semana_recente = data['semanaEpi'].max()
dados_semana_recente = data[data['semanaEpi'] == semana_recente]
dados_por_estado = dados_semana_recente.groupby('estado')[['casosNovos', 'obitosNovos']].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
bar_width = 0.4
indices = range(len(dados_por_estado))
ax.bar(indices, dados_por_estado['casosNovos'], width=bar_width, label='Casos Novos', color='skyblue')
ax.bar([i + bar_width for i in indices], dados_por_estado['obitosNovos'], width=bar_width, label='Óbitos Novos', color='salmon')

ax.set_xlabel('Estado')
ax.set_ylabel('Número de Casos/Óbitos')
ax.set_title('Casos Novos vs Óbitos Novos de COVID-19 por Estado na Semana Epidemiológica Mais Recente')
ax.set_xticks([i + bar_width / 2 for i in indices])
ax.set_xticklabels(dados_por_estado['estado'], rotation=45)
ax.legend()
st.pyplot(fig)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 7

st.markdown("**Boxplot: Distribuição dos Casos Novos de COVID-19 por Semana Epidemiológica nas Regiões Norte, Nordeste e Sudeste**")
regioes = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP']
}
data['regiao'] = data['estado'].map(lambda x: next((regiao for regiao, estados in regioes.items() if x in estados), None))
dados_regioes = data[data['regiao'].isin(['Norte', 'Nordeste', 'Sudeste'])]

plt.figure(figsize=(12, 6))
sns.boxplot(x='semanaEpi', y='casosNovos', hue='regiao', data=dados_regioes, palette='Set2')
plt.xlabel('Semana Epidemiológica')
plt.ylabel('Casos Novos')
plt.title('Distribuição dos Casos Novos de COVID-19 por Semana Epidemiológica nas Regiões Norte, Nordeste e Sudeste')
plt.xticks(rotation=45)
st.pyplot(plt)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 8

st.markdown("**Gráfico de Área: Evolução dos Casos Novos de COVID-19 por Semana Epidemiológica na Região Nordeste**")
regiao_escolhida = 'Nordeste'
dados_nordeste = data[data['regiao'] == regiao_escolhida]
dados_agrupados = dados_nordeste.groupby('semanaEpi')['casosNovos'].sum().reset_index()

grafico_area = px.area(dados_agrupados, x='semanaEpi', y='casosNovos', title='Evolução dos Casos Novos de COVID-19 na Região Nordeste')
st.plotly_chart(grafico_area)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 9

st.markdown("**Heatmap: Correlação entre Casos Novos, Óbitos Novos e Leitos Ocupados em São Paulo (SP)**")
estado_escolhido = 'SP'
dados_sp = data[data['estado'] == estado_escolhido]
dados_correlação = dados_sp[['casosNovos', 'obitosNovos', 'Recuperadosnovos']].dropna()

correlacao = dados_correlação.corr().reset_index().melt('index')
correlacao.columns = ['Variável 1', 'Variável 2', 'Correlação']

heatmap = px.density_heatmap(correlacao, x='Variável 1', y='Variável 2', z='Correlação', color_continuous_scale='viridis')
st.plotly_chart(heatmap)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 10

st.markdown("**Gráfico de Pizza: Distribuição Percentual dos Casos Acumulados de COVID-19 entre as Regiões do Brasil**")
dados_por_regiao = data.groupby('regiao')['casosAcumulado'].sum().reset_index()
fig = px.pie(dados_por_regiao, values='casosAcumulado', names='regiao', title='Distribuição Percentual dos Casos Acumulados de COVID-19 por Região')
st.plotly_chart(fig)
st.markdown("_____")

#________________________________________________________________________________________________________________________
# Exercício 11

st.markdown("**Subplots: Comparação dos Casos Novos e Óbitos Novos de COVID-19 por Semana Epidemiológica nas Regiões Sudeste e Nordeste**")

# Filtrando dados para as regiões escolhidas
regioes_comparacao = ['Sudeste', 'Nordeste']
dados_comparacao = data[data['regiao'].isin(regioes_comparacao)]

# Agrupando dados por região e semana epidemiológica
dados_agrupados = dados_comparacao.groupby(['regiao', 'semanaEpi'])[['casosNovos', 'obitosNovos']].sum().reset_index()

# Criando subplots com Plotly
fig = make_subplots(rows=1, cols=2, subplot_titles=('Sudeste', 'Nordeste'))

# Adicionando gráficos de barras para a Região Sudeste
dados_sudeste = dados_agrupados[dados_agrupados['regiao'] == 'Sudeste']
fig.add_trace(
    go.Bar(x=dados_sudeste['semanaEpi'], y=dados_sudeste['casosNovos'], name='Casos Novos - Sudeste', marker_color='blue'),
    row=1, col=1
)
fig.add_trace(
    go.Bar(x=dados_sudeste['semanaEpi'], y=dados_sudeste['obitosNovos'], name='Óbitos Novos - Sudeste', marker_color='red'),
    row=1, col=1
)

# Adicionando gráficos de barras para a Região Nordeste
dados_nordeste = dados_agrupados[dados_agrupados['regiao'] == 'Nordeste']
fig.add_trace(
    go.Bar(x=dados_nordeste['semanaEpi'], y=dados_nordeste['casosNovos'], name='Casos Novos - Nordeste', marker_color='blue'),
    row=1, col=2
)
fig.add_trace(
    go.Bar(x=dados_nordeste['semanaEpi'], y=dados_nordeste['obitosNovos'], name='Óbitos Novos - Nordeste', marker_color='red'),
    row=1, col=2
)

# Atualizando layout do gráfico
fig.update_layout(
    title_text='Comparação dos Casos Novos e Óbitos Novos de COVID-19 por Semana Epidemiológica',
    showlegend=True,
    width=1000,
    height=500
)

# Exibindo os subplots no Streamlit
st.plotly_chart(fig)
st.markdown("_____")


#_______________________________________________________________________________________________________________________
# Exercício 12

# Exercício 12
st.markdown("**Mapa Interativo: Densidade Populacional Ajustada para Casos Acumulados de COVID-19 por Município na Região Sudeste**")

# Filtrando dados para a Região Sudeste
regiao_escolhida = 'Sudeste'
dados_sudeste = data[data['regiao'] == regiao_escolhida]

# Criando um dicionário de coordenadas de alguns municípios da Região Sudeste para exemplo
coordenadas_sudeste = {
    'São Paulo': {'lat': -23.55052, 'long': -46.633308},
    'Rio de Janeiro': {'lat': -22.906847, 'long': -43.172896},
    'Belo Horizonte': {'lat': -19.916681, 'long': -43.934493},
    'Campinas': {'lat': -22.90556, 'long': -47.06083},
    'Vitória': {'lat': -20.3155, 'long': -40.3128}
}

# Adicionando as coordenadas ao DataFrame
dados_sudeste['lat'] = dados_sudeste['municipio'].map(lambda x: coordenadas_sudeste[x]['lat'] if x in coordenadas_sudeste else None)
dados_sudeste['long'] = dados_sudeste['municipio'].map(lambda x: coordenadas_sudeste[x]['long'] if x in coordenadas_sudeste else None)

# Removendo linhas sem coordenadas
dados_mapa = dados_sudeste.dropna(subset=['lat', 'long', 'populacaoTCU2019'])

# Calculando casos ajustados por densidade populacional
dados_mapa['casos_por_100k'] = (dados_mapa['casosAcumulado'] / dados_mapa['populacaoTCU2019']) * 100000

# Configurando o mapa com PyDeck
layer = pdk.Layer(
    "ScatterplotLayer",
    data=dados_mapa,
    get_position='[long, lat]',
    get_radius=1000,
    get_fill_color='[255, 0, 0, 140]',
    pickable=True,
    extruded=True,
    radius_scale=10,
)

view_state = pdk.ViewState(
    latitude=dados_mapa['lat'].mean(),
    longitude=dados_mapa['long'].mean(),
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
st.markdown("_____")


