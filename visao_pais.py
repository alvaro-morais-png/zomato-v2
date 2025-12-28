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

#=============Inicio do projeto=============
#QUANTIDADE DE RESTAURANTES CADASTRADOS POR PAIS
pais_rest = df1.loc[:,['Country name', 'Restaurant ID']].groupby('Country name')['Restaurant ID'].nunique().sort_values(ascending=False)
pais_rest = pais_rest.reset_index().head(7)

# Encontrar a linha com o maior número de restaurantes
linha_mais_restaurantes = pais_rest.loc[pais_rest['Restaurant ID'].idxmax()]
#grafico
px.bar (pais_rest, x='Country name', y='Restaurant ID', labels={'Country name':'Países', 'Restaurant ID': 'Quantidade de Resutaurantes'})

#---------------------------------------
#QUANTIDADE DE CIDADE REGISTRADAS POR PAIS
cc = df1.loc[:,['Country name','City']].groupby('Country name')['City'].nunique().sort_values(ascending=False).reset_index().head(7)

#Gráfico
px.bar(cc, x= 'Country name', y='City', labels = {'Country name': 'Países', 'City':'Cidades registradas'})

#---------------------------------------
#MÉDIA DE AVALIAÇÕES FEITAS POR PAÍS
avali_pais = df1.loc[:,['Country name','Votes']].groupby('Country name').mean('Votes').sort_values('Votes', ascending=False).head(7).reset_index()

px.bar(avali_pais, x='Country name', y='Votes', labels={'Country name': 'Países', 'Votes': 'Média de Avaliações'})

#---------------------------------------
#MÉDIA DE PREÇO DE UM PRATO PARA DOIS POR PAÍS
avg_for_two = df1.loc[:,['Country name', 'Currency','Average Cost for two']].groupby(['Country name', 'Currency']).mean('Average Cost for two').sort_values('Average Cost for two', ascending = False)
avg_for_two = avg_for_two.reset_index().head(7)
px.bar(avg_for_two, x='Country name', y= 'Average Cost for two', labels={'Country name': 'Países', 'Average Cost for two': 'Média de Preço de um Prato para Dois'}).show()
