import streamlit as st
import os
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="a Machina de Fazer Poesia",
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
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "yPoemas"
# Estados para os botões de modo (multisseleção)
if 'modo_som' not in st.session_state: st.session_state.modo_som = False
if 'modo_arte' not in st.session_state: st.session_state.modo_arte = False
if 'modo_video' not in st.session_state: st.session_state.modo_video = False

# 3. NAVEGAÇÃO SUPERIOR
t1, t2, t3, t4, t5, t6 = st.columns(6)
with t1:
    if st.button("mini"): st.session_state.pagina_ativa = "mini"
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

# 4. SIDEBAR (SUBSTITUIÇÃO: RADIO -> BUTTONS)
with st.sidebar:
    # ITEM 1: Dropdown de Idiomas (Path: ypo/)
    path_idiomas = os.path.join("ypo", "lista_idiomas.TXT")
    try:
        with open(path_idiomas, "r", encoding="utf-8") as f:
            idiomas_pcc = [l.strip() for l in f.readlines() if l.strip()]
    except:
        idiomas_pcc = ["Português", "Español", "Italiano", "Français", "English"]

    st.selectbox("Idioma", idiomas_pcc, label_visibility="collapsed")
    
    st.divider()

    # ITEM 2: Botões de Modo (Multisseleção)
    # Usando colunas dentro da sidebar para horizontalizar os botões
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Som"): st.session_state.modo_som = not st.session_state.modo_som
        st.caption("ON" if st.session_state.modo_som else "OFF")
    with c2:
        if st.button("Arte"): st.session_state.modo_arte = not st.session_state.modo_arte
        st.caption("ON" if st.session_state.modo_arte else "OFF")
    with c3:
        if st.button("Vídeo"): st.session_state.modo_video = not st.session_state.modo_video
        st.caption("ON" if st.session_state.modo_video else "OFF")

    st.divider()
    st.caption("Copyright © 1983-2026 Nando Lopes")

# 5. RENDERIZAÇÃO
def main():
    pagina = st.session_state.pagina_ativa
    _, col_main, _ = st.columns([1, 4, 1])
    
    with col_main:
        if pagina == "yPoemas":
            if st.session_state.poema_atual:
                with st.container(border=True):
                    for v in st.session_state.poema_atual:
                        if v == "\n": st.write("")
                        else: st.markdown(v, unsafe_allow_html=True)
            
            # Aqui entrará a lógica de Som + Arte dependendo dos botões ON
            if st.session_state.modo_arte:
                st.write("---")
                st.info("Camada de ARTE ativa.")
                
        elif pagina == "mini":
            st.write("Página Mini") # Placeholder para o import
        elif pagina == "books":
            st.subheader("Biblioteca")
            # (...) lógica de leitura da pasta base mantida
