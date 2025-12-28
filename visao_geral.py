#importando as bibliotecas necessarias
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import plotly.graph_objects as go
import plotly.express as px

#carregando os dados
df = pd.read_csv('/home/alvaro/Documentos/alvaro/comunidadeds/projetos/projeto_zomato/dataset/zomato.csv')
df1 = df.copy()

#===========limpando os dados=============
#Arrancando a coluna 'Switch to order menu'
df1 = df.drop(columns=['Switch to order menu'])

#Eliminando linhas vazias
df1 = df1.dropna()

#Eliminando linhas duplicadas
df1=df1.drop_duplicates()
df1=df1.reset_index(drop=True)
print(df1.head())
print('estou aqui')

#===========Inicio do projeto=============
#restaurantes cadastrados
restaurantes = df1.loc[:,'Restaurant ID'].nunique()
print(restaurantes)

#paises cadastrados
paises = df1.loc[:,'Country Code'].nunique()
print(paises)

#cidades cadastrados
cidades = df1.loc[:,'City'].nunique()
print(cidades)

#avaliaçoes totais
avaliacoes = df1['Votes'].sum()
print(avaliacoes)

#Culinarias cadastradas
culinaria = df1.loc[:,'Cuisines'].nunique()
print(culinaria)

#Mapa com a localização e avaliação dos restaurantes
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS.get(color_code, 'gray') # Use .get() for safe access with a default for unknown codes

locali = df1.loc[:, ['Restaurant Name','City','Aggregate rating','Latitude','Longitude', 'Rating color']]

mapa = folium.Map(
    location=[0, 0],
    zoom_start=3,
    tiles='CartoDB dark_matter'
)

marker_cluster = MarkerCluster().add_to(mapa)

for _, location_info in locali.iterrows():
    marker_color = color_name(location_info['Rating color'])
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

mapa.save('mapa_restaurantes.html') #testando o mapa, funcionou perfeitamente