import streamlit as st
import os
import time
import traceback

# --- CONEXÃO COM O MOTOR ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("Erro Crítico: Motor 'lay_2_ypo.py' não identificado.")
    st.stop()

# =================================================================
# ⚙️ CONFIGURAÇÕES DE AMBIENTE
# =================================================================

st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    page_icon="ツ",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Estilo e Largura da Sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] { width: 310px; }
    .main .block-container { padding-top: 1.5rem; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de Estados
if "auto_run" not in st.session_state: st.session_state.auto_run = False
if "action" not in st.session_state: st.session_state.action = None

# =================================================================
# 🧭 NAVEGAÇÃO & SIDEBAR
# =================================================================

def sidebar_machina():
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
    
    chosen_id = st.sidebar.radio(
        "Navegação", 
        options=list(menu.keys()), 
        format_func=lambda x: menu[x].upper(),
        index=0
    )

    st.sidebar.markdown("---")
    
    # Controles de Interface
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Talk"): st.session_state.action = "talk"
    if col2.button("Arte"): st.session_state.action = "draw"

    # Carregamento de INFO dinâmico da pasta /base
    info_map = {
        "1": "INFO_MINI.md", "2": "INFO_YPOEMAS.md", "3": "INFO_EUREKA.md",
        "4": "INFO_OFF-MACHINA.md", "5": "INFO_BOOKS.md", "6": "INFO_POLY.md",
        "7": "INFO_ABOUT.md"
    }
    
    info_path = os.path.join("./base", info_map.get(chosen_id, ""))
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            st.sidebar.info(f.read())

    return menu[chosen_id]

# =================================================================
# 🖋️ RENDERIZAÇÃO PRINCIPAL
# =================================================================

def main():
    tema = sidebar_machina()
    
    # Parâmetros específicos por página
    seed_eureka = ""
    if tema == "Eureka":
        seed_eureka = st.text_input("Semente ➪ Coords:", value="")
    
    # Modo Automático (Apenas na Sidebar para não poluir)
    if tema in ["Mini", "yPoemas"]:
        st.session_state.auto_run = st.sidebar.checkbox("MODO AUTO", value=st.session_state.auto_run)
        delay = st.sidebar.slider("Intervalo", 5, 60, 15)

    # Execução
    if st.button(f"Gerar {tema}") or st.session_state.auto_run:
        with st.spinner(""):
            try:
                # O Motor processa e retorna a lista de versos
                resultado = gera_poema(tema, seed_eureka)
                
                if resultado:
                    st.markdown("---")
                    # Renderização conforme o retorno do Motor (lista ou string)
                    if isinstance(resultado, list):
                        for linha in resultado:
                            st.subheader(linha)
                    else:
                        st.write(resultado)
                    st.markdown("---")
                
                # Controle de Loop Seguro (evita tela branca)
                if st.session_state.auto_run:
                    time.sleep(delay)
                    st.rerun()

            except Exception:
                st.error("Falha na execução do motor poético.")
                st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
