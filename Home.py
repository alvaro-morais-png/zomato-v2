#BIBLIOTECAS
import streamlit as st
import base64

#configurando a página
st.set_page_config(page_title='Home', layout='wide')

#===========================================
#BARRA LATERAL NO STREAMLIT
#===========================================

#criando a barra lateral
st.sidebar.markdown("# Projeto Zomato")
st.sidebar.markdown("### Analisando culinária, entre cidades e países")
st.sidebar.markdown("""---""")

#===========================================
#LAYOUT STREAMLIT
#===========================================
# image_path = r'/home/alvaro/Documentos/alvaro/comunidadeds/projetos/projeto_zomato/imagens/fundo.jpg'
# fundo = Image.open(image_path)
# st.image(fundo)

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
    "./imagens/fundo.jpg",
    opacity=0.7
)

st.write("# Projeto Zomato - Dashbord sobre culinária mundial")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """ 
            ### A análise do dataset do Zomato é uma ferramenta muito útil para os amantes da gastronomia que desejam experimentar as melhores culinárias em várias partes do mundo.
            ### O conjunto de dados permite que os usuários encontrem os restaurantes mais populares em suas respectivas cidades ao redor do globo.
            ### Também permite fazer leitura dos diferentes tipos de culinárias por cidade e por pais.""" 
        )

