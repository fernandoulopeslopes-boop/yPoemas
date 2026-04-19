import streamlit as st
import os
import importlib

# 1. SETUP & CSS (Cockpit Fixo)
st.set_page_config(
    page_title="a Machina de Fazer Poesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        [data-testid="stSidebar"] { min-width: 300px; max-width: 300px; }
        .stMarkdown p { text-align: justify; }
        .stButton button { width: 100%; padding: 0px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONTROLE DE ESTADO
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = "yPoemas"
if 'sw_som' not in st.session_state: st.session_state.sw_som = False
if 'sw_art' not in st.session_state: st.session_state.sw_art = False
if 'sw_pic' not in st.session_state: st.session_state.sw_pic = False

# 3. NAV SUPERIOR (Grafia Exata)
t1, t2, t3, t4, t5, t6 = st.columns(6)
btns = ["mini", "yPoemas", "eureka", "off-mach", "commnets", "about"]

for i, col in enumerate([t1, t2, t3, t4, t5, t6]):
    if col.button(btns[i]):
        st.session_state.pagina_ativa = btns[i]

st.divider()

# 4. SIDEBAR (Cockpit Técnico)
with st.sidebar:
    # Idiomas (Sem rodeios)
    path_idiomas = os.path.join("ypo", "lista_idiomas.TXT")
    try:
        with open(path_idiomas, "r", encoding="utf-8") as f:
            idiomas = [l.strip() for l in f.readlines() if l.strip()]
    except:
        idiomas = ["Português"]
    
    st.selectbox("Idioma", idiomas, label_visibility="collapsed")
    st.divider()

    # som, art, pic
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("som"): 
                st.session_state.sw_som = not st.session_state.sw_som
                st.rerun()
            if st.session_state.sw_som: st.caption("·on·")
        with c2:
            if st.button("art"): 
                st.session_state.sw_art = not st.session_state.sw_art
                st.rerun()
            if st.session_state.sw_art: st.caption("·on·")
        with c3:
            if st.button("pic"): 
                st.session_state.sw_pic = not st.session_state.sw_pic
                st.rerun()
            if st.session_state.sw_pic: st.caption("·on·")

    st.divider()
    st.caption("Copyright © 1983-2026 Nando Lopes")

# 5. EXECUÇÃO DOS MÓDULOS REAIS
def ligar_modulo(nome):
    """ Importa e roda a função exibir() de cada arquivo """
    try:
        # Resolve a grafia 'off-mach' para o nome do arquivo 'off_mach.py'
        modulo_nome = nome.replace("-", "_")
        mod = importlib.import_module(modulo_nome)
        mod.exibir()
    except Exception as e:
        st.error(f"Falha ao carregar {nome}.py: {e}")

# Renderização Central
_, col_main, _ = st.columns([1, 4, 1])
with col_main:
    p = st.session_state.pagina_ativa
    
    if p == "yPoemas":
        # Se houver módulo yPoemas.py ele carrega, senão exibe o estado atual
        if os.path.exists("yPoemas.py"):
            ligar_modulo("yPoemas")
        elif 'poema_atual' in st.session_state:
            for v in st.session_state.poema_atual:
                st.markdown(v, unsafe_allow_html=True)
    else:
        ligar_modulo(p)
