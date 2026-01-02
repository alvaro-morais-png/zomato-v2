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
df1.reset_index(drop=True, inplace=True)

#Eliminando linhas duplicadas
df1=df1.drop_duplicates()
df1=df1.reset_index(drop=True)

#INSIRINDO A LISTA DE NOMES DE CADA PAIS DE ACORDO COM O CÓDIGO

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

#===========Inicio do projeto=================
#Top restaurants
top_rest = df1.loc[:,['Restaurant Name', 'Country name', 'City','Cuisines', 'Currency','Average Cost for two' ,'Aggregate rating', 'Votes']].sort_values('Aggregate rating', ascending = False)
top_rest

#------------------------------------------------
# Analisando as 10 culinárias com as melhores avaliações médias
top10_cuisines = df1.loc[:,['Cuisines','Aggregate rating']].groupby('Cuisines').mean('Aggregate rating').sort_values('Aggregate rating', ascending=False).reset_index().head(10)

fig = px.bar(top10_cuisines, x= 'Cuisines', y='Aggregate rating', labels={'Cuisines':'Culinária', 'Aggregate rating':'Ranking'})
fig

#------------------------------------------------
# Analisando as 10 culinárias com as piores avaliações médias

# Filter out rows where 'Aggregate rating' is 0
filtered_df1 = df1.loc[df1['Aggregate rating'] != 0]

# Group by 'Cuisines' and calculate the mean of 'Aggregate rating'
piores_cuisines = filtered_df1.groupby('Cuisines')['Aggregate rating'].mean().sort_values(ascending=False).reset_index().tail(10)

fig = px.bar(piores_cuisines, x= 'Cuisines', y='Aggregate rating', labels={'Cuisines':'Culinária', 'Aggregate rating':'Ranking'})
fig

