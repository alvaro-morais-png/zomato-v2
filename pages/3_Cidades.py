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

def culinaria_distintos(df1):
    #Top 10 CIDADES COM MAIS RESTAURANTES COM TIPOS CULINÁRIOS DISTINTOS
    city_culi = df1.loc[:,['Restaurant ID','Cuisines','City', 'Country name']].groupby(['City','Country name']).nunique('Cuisines').sort_values('Cuisines', ascending=False).reset_index().head(10)

    fig = px.bar(city_culi, x= 'City', y= 'Cuisines', labels = {'City':'Cidades', 'Cuisines':'Quantidade de tipos culinários únicos'}, color='Country name')
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray': city_culi['City'].tolist()})
    return fig

def avg_menor(df1):
    #top 7 CIDADES COM RESTAURANTE COM MÉDIA DE AVALIAÇÃO ABAIXO DE 2.5
    city_rayting3 = df1.loc[df1['Aggregate rating']<2.5]
    city_rayting3 = city_rayting3.loc[:,['City','Restaurant ID', 'Aggregate rating', 'Country name']]#.groupby(['City','Restaurant Name'])['Aggregate rating'].count().sort_values('Aggregate rating', ascending = False).reset_index()
    ct4 = city_rayting3.groupby(['City', 'Country name'])['Restaurant ID'].count().sort_values(ascending=False).reset_index().head(7)
    # Gráfico de barras
    fig = px.bar(ct4, x='City', y='Restaurant ID', labels = {'Restaurant ID':'Restaurantes com média abaixo de 2.5', 'City':'Cidades' }, color='Country name')
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray': ct4['City'].tolist()})
    return fig

def avg_maior(df1):
    #top 7 CIDADES COM RESTAURANTE COM MÉDIA DE AVALIAÇÃO MAIOR QUE 4
    city_rayting2 = df1.loc[df1['Aggregate rating']>4]
    city_rayting2 = city_rayting2.loc[:,['City','Restaurant ID', 'Aggregate rating', 'Country name']]#.groupby(['City','Restaurant Name'])['Aggregate rating'].count().sort_values('Aggregate rating', ascending = False).reset_index()
    ct3 = city_rayting2.groupby(['Country name','City'])['Restaurant ID'].count().sort_values(ascending=False).reset_index().head(7)
    # Gráfico de barras
    fig = px.bar(ct3, x='City', y='Restaurant ID', labels = {'Restaurant ID':'Restaurantes com média acima de 4', 'City':'Cidades' }, color='Country name')
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray': ct3['City'].tolist()})
    return fig

def city_rest(df1):
    # TOP 60 CIDADES COM MAIS RESTAURANTES
    city_rest = df1.loc[:,[ 'City','Country name', 'Restaurant ID']].groupby(['City', 'Country name'])['Restaurant ID'].count().sort_values(ascending=False).reset_index().head(60)
# Gráfico de barras
    fig = px.bar(city_rest, x='City', y='Restaurant ID', labels = {'City':'Cidade', 'Restaurant ID': 'Restaurantes registrados'}, color='Country name')
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
df = pd.read_csv('./dataset/zomato.csv')


#==================
#LIMPANDO OS DADOS
df1= clean_code( df )

#===========================================
#BARRA LATERAL NO STREAMLIT
#===========================================


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
    "./imagens/fundo.jpg",
    opacity=0.7
)

st.markdown("# VISÃO CIDADE")
# TOP 60 CIDADES COM MAIS RESTAURANTES
with st.container():
    st.markdown("## Top 60 cidades com mais restaurantes")
    fig = city_rest(df1)
    fig.update_layout(
      paper_bgcolor="rgba(0,0,0,0.5)",
      plot_bgcolor="rgba(0,0,0,0.5)"
)
    st.plotly_chart(fig, use_container_width=True)

#-------------------------------------------------
#CIDADES COM MAIS RESTAURANTES COM MÉDIA DE AVALIAÇÃO MENOR QUE 2.5 E MAIOR QUE 4
with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns(2)
#top 7 CIDADES COM RESTAURANTE COM MÉDIA DE AVALIAÇÃO MAIOR QUE 4
    with col1:
      st.markdown("## Top 7 cidades com mais restaurantes com média de avaliação acima de 4")
      fig = avg_maior(df1)
      fig.update_layout(
         paper_bgcolor="rgba(0,0,0,0.5)",
         plot_bgcolor="rgba(0,0,0,0.5)"
)
      st.plotly_chart(fig, use_container_width=True)

    with col2:
#-------------------------------------------------
#top 7 CIDADES COM RESTAURANTE COM MÉDIA DE AVALIAÇÃO ABAIXO DE 2.5
      st.markdown("## Top 7 cidades com mais restaurantes com média de avaliação abaixo de 2.5")
      fig = avg_menor(df1)
      fig.update_layout(
         paper_bgcolor="rgba(0,0,0,0.5)",
         plot_bgcolor="rgba(0,0,0,0.5)"
)
      st.plotly_chart(fig, use_container_width=True)

#-------------------------------------------------
with st.container():
    st.markdown("""---""")
    st.markdown("## Top 10 cidades com mais tipos culinários distintos")
    #Top 10 CIDADES COM MAIS RESTAURANTES COM TIPOS CULINÁRIOS DISTINTOS
    fig = culinaria_distintos(df1)
    fig.update_layout(
      paper_bgcolor="rgba(0,0,0,0.5)",
      plot_bgcolor="rgba(0,0,0,0.5)"
)
    st.plotly_chart(fig, use_container_width=True)
