#importando as bibliotecas necessarias
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium
import base64

#-----------------------------------------
#FUNÇÕES
#-----------------------------------------
def set_bg_with_overlay(image_path, opacity=0.6):
    #Função para transformar em imagem de fundo
    #Abre a imagem com o base64, para abrir a imagem no modo binário
        # f.read() → lê a imagem inteira em bytes
        # base64.b64encode(...) → converte os bytes em Base64
        # .decode() → transforma em string (texto)
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(0, 0, 0, {opacity}),
                    rgba(0, 0, 0, {opacity})
                ),
                url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_with_overlay(
    "/home/alvaro/Documentos/alvaro/comunidadeds/projetos/projeto_zomato/imagens/fundo.jpg",
    opacity=0.7
)

def avg_fottwo(df1):
  #MÉDIA DE PREÇO DE UM PRATO PARA DOIS POR PAÍS
  avg_for_two = df1.loc[:,['Country name', 'Currency','Average Cost for two']].groupby(['Country name', 'Currency']).mean('Average Cost for two').sort_values('Average Cost for two', ascending = False)
  avg_for_two = avg_for_two.reset_index().head(7)
  fig = px.bar(avg_for_two, x='Country name', y= 'Average Cost for two', labels={'Country name': 'Países', 'Average Cost for two': 'Média de Preço de um Prato para Dois'}, color='Country name')
  return fig

def hating_country(df1):
  #MÉDIA DE AVALIAÇÕES FEITAS POR PAÍS
  avali_pais = df1.loc[:,['Country name','Votes']].groupby('Country name').mean('Votes').sort_values('Votes', ascending=False).head(7).reset_index()
  fig = px.bar(avali_pais, x='Country name', y='Votes', labels={'Country name': 'Países', 'Votes': 'Média de Avaliações'}, color='Country name')
  return fig

def city_country(df1):
  #QUANTIDADE DE CIDADES REGISTRADAS POR PAIS
  cc = df1.loc[:,['Country name','City']].groupby('Country name')['City'].nunique().sort_values(ascending=False).reset_index().head(7)
#Gráfico
  fig = px.bar(cc, x= 'Country name', y='City', labels = {'Country name': 'Países', 'City':'Cidades registradas'}, color='Country name')
  return fig

def rest_pais(df1):
  #QUANTIDADE DE RESTAURANTES CADASTRADOS POR PAIS
  pais_rest = df1.loc[:,['Country name', 'Restaurant ID']].groupby('Country name')['Restaurant ID'].nunique().sort_values(ascending=False)
  pais_rest = pais_rest.reset_index().head(7)
#grafico
  fig = px.bar (pais_rest, x='Country name', y='Restaurant ID', labels={'Country name':'Países', 'Restaurant ID': 'Quantidade de Resutaurantes'}, color = "Country name")
  return fig

def clean_code( df ):
  #===========limpando os dados=============
  #Arrancando a coluna 'Switch to order menu'
  df1 = df.drop(columns=['Switch to order menu'])

  #Eliminando linhas vazias
  df1 = df1.dropna()
  df1.reset_index(drop=True, inplace=True)

  #Eliminando linhas duplicadas
  df1=df1.drop_duplicates()
  df1=df1.reset_index(drop=True)

  #COLOCANDO NOMES NOS PAÍSES
  COUNTRIES = {
  1: "India",
  14: "Australia",
  30: "Brazil",
  37: "Canada",
  94: "Indonesia",
  148: "New Zeland",
  162: "Philippines",
  166: "Qatar",
  184: "Singapure",
  189: "South Africa",
  191: "Sri Lanka",
  208: "Turkey",
  214: "United Arab Emirates",
  215: "England",
  216: "United States of America",
  }
  def country_name(country_id):
      return COUNTRIES[country_id]
  df1['Country name'] = df1['Country Code'].apply(country_name)

  #TRANSFORMANDO STRING E NUMEROS
  df1['Restaurant ID'] = df1['Restaurant ID'].astype(float)
  df1['Average Cost for two'] = df1['Average Cost for two'].astype(float)
  df1['Average Cost for two'] = df1['Average Cost for two'].astype(float)
  df1['Restaurant Name'] = df1['Restaurant Name'].astype(str)
  df1['City'] = df1['City'].astype(str)
  df1['Address'] = df1['Address'].astype(str)
  df1['Cuisines'] = df1['Cuisines'].astype(str)
  df1['Currency'] = df1['Currency'].astype(str)
  df1['Rating color'] = df1['Rating color'].astype(str)
  df1['Rating text'] = df1['Rating text'].astype(str)
  df1['Country name'] = df1['Country name'].astype(str)

  #ELIMINANDO OUTLIERS
  # Para remover a linha na posição de índice 356, você deve passar o rótulo do índice diretamente.
  df1 = df1.drop(index=356)
  df1 = df1.drop(index=5566)
  # Reindexar o DataFrame após a remoção, para manter os índices sequenciais se necessário.
  df1 = df1.reset_index(drop=True)

  return df1

#=================INICIO DA ESTRUTURA LÓGICA DO CÓDIGO======================
#==================
#IMPORT DATASET
df = pd.read_csv('/home/alvaro/Documentos/alvaro/comunidadeds/projetos/projeto_zomato/dataset/zomato.csv')

#==================
#LIMPANDO OS DADOS
df1= clean_code( df )

#===========================================
#BARRA LATERAL NO STREAMLIT
#===========================================
#configurando a página
st.set_page_config(page_title='Visão Países', layout='wide')

#criando a barra lateral
st.sidebar.markdown("# Filtros")
st.sidebar.markdown("### Selecione os países para visualizar o dados:")
st.sidebar.markdown("""---""")

country_options = st.sidebar.multiselect("Escolha os países:",
                      options=df1['Country name'].unique().tolist(),
                      default=df1['Country name'].unique().tolist(),
                      key='paises')
#filtrando os dados com base na seleção do usuário
linhas_selecionadas = df1['Country name'].isin(country_options)

df1 = df1.loc[linhas_selecionadas, :]

#===========================================
#LAYOUT NO STREAMLIT
#===========================================
#IMAGEM DE FUNDO
set_bg_with_overlay(
    "/home/alvaro/Documentos/alvaro/comunidadeds/projetos/projeto_zomato/imagens/fundo.jpg",
    opacity=0.7
)

st.markdown("# VISÃO PAÍSES")

with st.container():
  st.markdown("## Quantidade de restaurantes registrados por país")
#QUANTIDADE DE RESTAURANTES CADASTRADOS POR PAIS
  fig = rest_pais(df1)
  fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0.5)",
    plot_bgcolor="rgba(0,0,0,0.5)"
)
  st.plotly_chart(fig, use_container_width=True)

#---------------------------------------
with st.container():
  st.markdown("""---""")
  st.markdown("## Quantidade de cidades registradas por país")
  #QUANTIDADE DE CIDADES REGISTRADAS POR PAIS
  fig = city_country(df1)
  fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0.5)",
    plot_bgcolor="rgba(0,0,0,0.5)"
) 
  st.plotly_chart(fig, use_container_width=True)

#---------------------------------------
st.markdown("""---""")
st.markdown("## Outros indicadores por país",text_alignment="center")
with st.container():
  col1, col2 = st.columns(2)

  with col1:
    st.markdown("##### Média de avaliações feitas por país", text_alignment="center")
#MÉDIA DE AVALIAÇÕES FEITAS POR PAÍS
    fig = hating_country(df1)
    fig.update_layout(
      paper_bgcolor="rgba(0,0,0,0.5)",
      plot_bgcolor="rgba(0,0,0,0.5)"
)
    st.plotly_chart(fig, use_container_width=True)

  with col2:
    st.markdown("##### Média de preço de um prato para dois por país, na moeda local", text_alignment="center")
#MÉDIA DE PREÇO DE UM PRATO PARA DOIS POR PAÍS
    fig = avg_fottwo(df1)
    fig.update_layout(
      paper_bgcolor="rgba(0,0,0,0.5)",
      plot_bgcolor="rgba(0,0,0,0.5)"
)
    st.plotly_chart(fig, use_container_width=True)