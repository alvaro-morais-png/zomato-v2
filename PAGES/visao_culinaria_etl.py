#importando as bibliotecas necessarias
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium

#-----------------------------------------
#FUNÇÕES
#-----------------------------------------
def top_cuisines_avg( df1 ):
    # Analisando as 10 culinárias com as melhores avaliações médias
    top10_cuisines = df1.loc[:,['Cuisines','Country name','Votes', 'Aggregate rating']].groupby('Cuisines').mean('Aggregate rating').sort_values(['Aggregate rating', 'Votes'], ascending=False).reset_index().head(10)
    fig = px.bar(top10_cuisines, x= 'Cuisines', y='Aggregate rating', labels={'Cuisines':'Culinária', 'Aggregate rating':'Ranking'}, color='Votes')
    return  top10_cuisines, fig

def top_10rest( df1 ):
    votos_rest = df1.loc[df1['Votes']>1500,['Restaurant Name', 'Country name', 'City','Cuisines', 'Currency','Average Cost for two' ,'Aggregate rating', 'Votes']]
    top_rest = votos_rest.loc[:,['Restaurant Name', 'Country name', 'City','Cuisines', 'Currency','Average Cost for two' ,'Aggregate rating', 'Votes']].sort_values(['Aggregate rating', 'Votes'], ascending = False)
    return top_rest

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
st.set_page_config(page_title='Visão Culinária', layout='wide')

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
with st.container():
    st.markdown("# VISÃO CULINÁRIA")
    st.markdown("## Top restaurantes")
    st.markdown("##### Os restaurantes com mais de 1500 votos e melhores avaliações")
#Top restaurants
 #   votos_rest = df1.loc[df1['Votes']>1500,['Restaurant Name', 'Country name', 'City','Cuisines', 'Currency','Average Cost for two' ,'Aggregate rating', 'Votes']]
#    top_rest = votos_rest.loc[:,['Restaurant Name', 'Country name', 'City','Cuisines', 'Currency','Average Cost for two' ,'Aggregate rating', 'Votes']].sort_values(['Aggregate rating', 'Votes'], ascending = False)
    top_rest = top_10rest(df1)
    st.dataframe(top_rest)

#------------------------------------------------
with st.container():
    st.markdown("""---""")
    st.markdown("## Top 10 culinárias com as melhores avaliações médias")
    st.markdown("##### Melhores avaliações médias e maiores quantidade de votos  ")
# Analisando as 10 culinárias com as melhores avaliações médias
    top10_cuisines, fig = top_cuisines_avg(df1)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top10_cuisines)

#------------------------------------------------
with st.container():
    st.markdown("""---""")
    st.markdown("## Top 10 culinárias com as piores avaliações médias")
    st.markdown("##### Piores avaliações médias e maiores quantidade de votos  ")
# Analisando as 10 culinárias com as piores avaliações médias

# Filter out rows where 'Aggregate rating' is 0
    filtered_df1 = df1.loc[(df1['Aggregate rating'] != 0) & (df1['Votes'] > 100)]

# Group by 'Cuisines' and calculate the mean of 'Aggregate rating'
    #piores_cuisines = filtered_df1.groupby('Cuisines')['Aggregate rating'].mean().sort_values(['Aggregate rating','Votes'], ascending=False).reset_index().tail(10)
    piores_cuisines = (
    filtered_df1
    .groupby('Cuisines')
    .agg({
        'Aggregate rating': 'mean',
        'Votes': 'sum'   # ou sum, se fizer mais sentido
    })
    .sort_values(
        by=['Aggregate rating', 'Votes'],
        ascending=[False, False]
    )
    .reset_index()
    .tail(10)
)

    fig = px.bar(piores_cuisines, x= 'Cuisines', y='Aggregate rating', labels={'Cuisines':'Culinária', 'Aggregate rating':'Ranking', 'Votes':'Quantidade de votos'}, color='Aggregate rating', color_continuous_scale=px.colors.sequential.Reds[::-1])
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(piores_cuisines)

