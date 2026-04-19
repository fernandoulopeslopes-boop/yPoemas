import streamlit as st
import os
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: Trava largura e justificativa
st.markdown("""
    <style>
        [data-testid="stSidebar"] { min-width: 300px; max-width: 300px; }
        .stMarkdown p { text-align: justify; }
        .stButton button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. ESTADO DA SESSÃO
if 'poema_atual' not in st.session_state:
    st.session_state.poema_atual = []
if 'tema_selecionado' not in st.session_state:
    st.session_state.tema_selecionado = "FATOS"
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "yPoemas"

# 3. NAVEGAÇÃO SUPERIOR
t1, t2, t3, t4, t5, t6 = st.columns(6)
with t1:
    if st.button("Mini"): st.session_state.pagina_ativa = "mini"
with t2:
    if st.button("yPoemas"): st.session_state.pagina_ativa = "yPoemas"
with t3:
    if st.button("Eureka"): st.session_state.pagina_ativa = "eureka"
with t4:
    if st.button("Books"): st.session_state.pagina_ativa = "books"
with t5:
    if st.button("Comments"): st.session_state.pagina_ativa = "comments"
with t6:
    if st.button("About"): st.session_state.pagina_ativa = "about"

st.divider()

# 4. SIDEBAR (TODO [TEST] - REVISÃO FINAL)
with st.sidebar:
    # ITEM 1: Dropdown de Idiomas (Topo Absoluto)
    idiomas_pcc = ["Português", "Español", "Italiano", "Français", "English", "Català", "Deutsch", "Nederlands", "Dansk", "Svenska", "Norsk"]
    st.selectbox("Idioma", idiomas_pcc, label_visibility="collapsed")
    
    st.divider()
    
    with st.container():
        # Listagem de Livros (Arquivos Rol_*.TXT em ./base/)
        try:
            arquivos_base = os.listdir("./base/")
            livros_lista = sorted([f.replace("Rol_", "").replace(".TXT", "") for f in arquivos_base if f.startswith("Rol_") and f.endswith(".TXT")])
        except FileNotFoundError:
            livros_lista = []

        st.selectbox("selecione o livro", livros_lista)
        
        # Temas (.ypo em ./data/)
        try:
            arquivos_data = os.listdir("./data/")
            temas = sorted([f.replace(".ypo", "") for f in arquivos_data if f.endswith(".ypo")
