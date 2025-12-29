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
# Top 20 cidades com mais restaurantes
city_rest = df1.loc[:,[ 'City','Country name', 'Restaurant ID']].groupby(['City', 'Country name'])['Restaurant ID'].count().sort_values(ascending=False).reset_index().head(20)
# Gráfico de barras
px.bar(city_rest, x='City', y='Restaurant ID', labels = {'City':'Cidade', 'Restaurant ID': 'Restaurantes registrados'}, color='Country name').show()

#-------------------------------------------------
#top 7 CIDADES COM RESTAURANTE COM MÉDIA DE AVALIAÇÃO MAIOR QUE 4
city_rayting2 = df1.loc[df1['Aggregate rating']>4]
city_rayting2 = city_rayting2.loc[:,['City','Restaurant ID', 'Aggregate rating', 'Country name']]#.groupby(['City','Restaurant Name'])['Aggregate rating'].count().sort_values('Aggregate rating', ascending = False).reset_index()
ct3 = city_rayting2.groupby(['Country name','City'])['Restaurant ID'].count().sort_values(ascending=False).reset_index().head(7)
# Gráfico de barras
fig = px.bar(ct3, x='City', y='Restaurant ID', labels = {'Restaurant ID':'Restaurantes com média acima de 4', 'City':'Cidades' }, color='Country name')
fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray': ct3['City'].tolist()})
fig.show()

#-------------------------------------------------
#top 7 CIDADES COM RESTAURANTE COM MÉDIA DE AVALIAÇÃO ABAIXO DE 2.5
city_rayting3 = df1.loc[df1['Aggregate rating']<2.5]
city_rayting3 = city_rayting3.loc[:,['City','Restaurant ID', 'Aggregate rating', 'Country name']]#.groupby(['City','Restaurant Name'])['Aggregate rating'].count().sort_values('Aggregate rating', ascending = False).reset_index()
ct4 = city_rayting3.groupby(['City', 'Country name'])['Restaurant ID'].count().sort_values(ascending=False).reset_index().head(7)
# Gráfico de barras
fig = px.bar(ct4, x='City', y='Restaurant ID', labels = {'Restaurant ID':'Restaurantes com média abaixo de 2.5', 'City':'Cidades' }, color='Country name')
fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray': ct4['City'].tolist()})
fig.show()

#-------------------------------------------------
#Top 10 CIDADES COM MAIS RESTAURANTES COM TIPOS CULINÁRIOS DISTINTOS
city_culi = df1.loc[:,['Restaurant ID','Cuisines','City', 'Country name']].groupby(['City','Country name']).nunique('Cuisines').sort_values('Cuisines', ascending=False).reset_index().head(10)

fig = px.bar(city_culi, x= 'City', y= 'Cuisines', labels = {'City':'Cidades', 'Cuisines':'Quantidade de tipos culinários únicos'}, color='Country name')
fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray': city_culi['City'].tolist()})
fig.show()