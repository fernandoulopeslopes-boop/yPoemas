import streamlit as st
import os
import random
import time
from datetime import datetime

# --- IMPORTAÇÃO DO MOTOR ---
# Certifique-se de que o arquivo lay_2_ypo.py esteja na mesma pasta
from lay_2_ypo import gera_poema, translate, talk, have_internet

# =================================================================
# 🛠️ CONFIGURAÇÕES PRO & CACHE (Timeline Atualizada)
# =================================================================

st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    page_icon="ツ",
    layout="centered",
    initial_sidebar_state="expanded",
)

@st.cache_data(show_spinner=False)
def load_md_file(file_name):
    try:
        with open(os.path.join("./base", file_name), "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

# --- ESTILIZAÇÃO CSS (Otimizada) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { width: 310px; }
    .main .block-container { padding-top: 1rem; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 🧭 NAVEGAÇÃO NATIVA (Substituindo stx.TabBar)
# =================================================================

def main():
    if 'lang' not in st.session_state: st.session_state.lang = "pt"
    
    # Menu lateral com botões nativos para evitar erro de pkg_resources
    st.sidebar.title("ツ Machina")
    
    menu = {
        "1": "Mini",
        "2": "yPoemas",
        "3": "Eureka",
        "4": "Off-Machina",
        "5": "Books",
        "6": "Poly",
        "7": "About"
    }
    
    # Seleção de Navegação
    chosen_id = st.sidebar.radio(
        "Navegação", 
        options=list(menu.keys()), 
        format_func=lambda x: menu[x],
        index=1
    )

    # --- BOTÕES DE AÇÃO NA SIDEBAR ---
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Talk"):
            st.session_state.talk = True
    with col2:
        if st.button("Arte"):
            st.session_state.draw = True

    # --- LÓGICA DE PÁGINAS ---
    if chosen_id == "1":
        st.sidebar.info(load_md_file("INFO_MINI.md"))
        render_page("mini")
    elif chosen_id == "2":
        st.sidebar.info(load_md_file("INFO_YPOEMAS.md"))
        render_page("ypoemas")
    elif chosen_id == "3":
        st.sidebar.info(load_md_file("INFO_EUREKA.md"))
        render_page("eureka")
    # ... (repetir lógica para os demais IDs)

def render_page(tipo):
    st.title(f"Modo: {tipo.capitalize()}")
    # Aqui chama as funções de geração que estão no lay_2_ypo
    if st.button("Gerar Poema"):
        poema = gera_poema(tipo)
        for linha in poema:
            st.write(linha)

if __name__ == "__main__":
    main()
