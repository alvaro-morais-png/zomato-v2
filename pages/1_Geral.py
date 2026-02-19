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


def m(df1):
    with st.spinner('🌎 Renderizando o mapa e agrupando restaurantes... Aguarde um instante devido ao tamanho da base de dados'):
        locali = df1.loc[:, ['Restaurant Name','City','Aggregate rating','Latitude','Longitude', 'Rating color']]

        mapa = folium.Map(
            location=[0, 0],
            zoom_start=3,
            tiles='CartoDB dark_matter',
            prefer_canvas=True
        )

        marker_cluster = MarkerCluster().add_to(mapa)

        for _, location_info in locali.iterrows():
            marker_color = color_function(location_info['Rating color'])
            folium.CircleMarker(
                location=[
                    location_info['Latitude'],
                    location_info['Longitude']
                ],
                radius=6,
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.8,
                popup=(
                    f"<b>Restaurante:</b> {location_info['Restaurant Name']}<br>"
                    f"<b>Avaliação:</b> {location_info['Aggregate rating']}"
                )
            ).add_to(marker_cluster)

        fig = st_folium(mapa, width=None, height = 600)
        return fig

def color_function(color_code):
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    }
    
    return COLORS.get(color_code, "gray")

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

st.markdown("# Projeto Zomato")
st.markdown("### O Melhor lugar para encontrar seu mais novo restaurante favorito!")

with st.container():
    st.title("Restaurantes cadastrados ao redor do mundo:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("##### Restaurantes cadastrados")
        restaurantes = df1.loc[:,'Restaurant ID'].nunique()
        col1.metric("restaurantes",restaurantes)
    with col2:
        st.markdown("##### Países cadastrados")
        paises = df1.loc[:,'Country Code'].nunique()
        col2.metric("países",paises)
    with col3:
        st.markdown("##### Cidades cadastradas")
        cidades = df1.loc[:,'City'].nunique()
        col3.metric("cidades",cidades)
    with col4:
        st.markdown("##### Avaliações totais")
        avaliacoes = df1['Votes'].sum()
        col4.metric("avaliações",avaliacoes)
    with col5:
        st.markdown("##### Culinárias cadastradas")
        culinaria = df1.loc[:,'Cuisines'].nunique()
        col5.metric("culinárias",culinaria)

#---------------------------------------------------
with st.container():
    st.markdown("""---""")
    fig = m(df1)
