import streamlit as st

st.set_page_config(
    page_title="Home"

)

#===========================================
#BARRA LATERAL NO STREAMLIT
#===========================================
#configurando a página
st.set_page_config(page_title='Visão Entregadores', layout='wide')

#criando a barra lateral
st.sidebar.markdown("# Projeto Zomato")
st.sidebar.markdown("### Analisando culinária, entre cidades e países")
st.sidebar.markdown("""---""")

st.write("# Projeto Zomato - Dashbord sobre culinária mundial")
st.markdown(
    """ 
    ### A análise do dataset do Zomato é uma ferramenta muito útil para os amantes da gastronomia que desejam experimentar as melhores culinárias em várias partes do mundo.
    ### O conjunto de dados permite que os usuários encontrem os restaurantes mais populares em suas respectivas cidades ao redor do globo.
    ### Também permite fazer leitura dos diferentes tipos de culinárias por cidade e por pais."""
)

