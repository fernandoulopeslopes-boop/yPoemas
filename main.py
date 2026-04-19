import streamlit as st
import os
import importlib

# 1. SETUP & UI (Trava de largura e estilo do cockpit)
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

# 2. ESTADOS DE SESSÃO
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = "yPoemas"
if 'sw_som' not in st.session_state: st.session_state.sw_som = False
if 'sw_art' not in st.session_state: st.session_state.sw_art = False
if 'sw_pic' not in st.session_state: st.session_state.sw_pic = False

# 3. NAV SUPERIOR (Grafia exata solicitada)
# : mini : yPoemas : eureka ; off-mach : commnets : about
t1, t2, t3, t4, t5, t6 = st.columns(6)
btns = ["mini", "yPoemas", "eureka", "off-mach", "commnets", "about"]
for i, col in enumerate([t1, t2, t3, t4, t5, t6]):
    if col.button(btns[i]):
        st.session_state.pagina_ativa = btns[i]

st.divider()

# 4. SIDEBAR (Cockpit e Idioma)
with st.sidebar:
    path_idiomas = os.path.join("ypo", "lista_idiomas.TXT")
    idiomas_pcc = ["Português"]
    if os.path.exists(path_idiomas):
        with open(path_idiomas, "r", encoding="utf-8") as f:
            idiomas_pcc = [l.strip() for l in f.readlines() if l.strip()]
    st.selectbox("Idioma", idiomas_pcc, label_visibility="collapsed")
    
    st.divider()

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

# 5. MOTOR DE NAVEGAÇÃO REAL
def render_pagina(nome_modulo):
    """Importa dinamicamente e executa a função exibir() do módulo"""
    try:
        # Substitui hífen por underline para o import se necessário (Python não gosta de hífens em nomes de arquivo)
        nome_arquivo = nome_modulo.replace("-", "_")
        modulo = importlib.import_module(nome_arquivo)
        modulo.exibir()
    except ModuleNotFoundError:
        st.error(f"Erro: O arquivo '{nome_modulo}.py' não foi encontrado no diretório.")
    except AttributeError:
        st.error(f"Erro: O módulo '{nome_modulo}' não possui a função 'exibir()'.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar a página: {e}")

# Execução centralizada
_, col_main, _ = st.columns([1, 4, 1])
with col_main:
    pagina = st.session_state.pagina_ativa
    
    if pagina == "yPoemas":
        # Se você tiver um módulo yPoemas.py, ele carrega aqui. 
        # Caso contrário, ele roda o motor interno que já testamos.
        if os.path.exists("yPoemas.py"):
            render_pagina("yPoemas")
        else:
            if 'poema_atual' in st.session_state and st.session_state.poema_atual:
                with st.container(border=True):
                    for v in st.session_state.poema_atual:
                        if v == "\n": st.write("")
                        else: st.markdown(v, unsafe_allow_html=True)
    else:
        render_pagina(pagina)
