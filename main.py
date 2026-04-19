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
if 'tema_selecionado' not in st.session_state:
    st.session_state.tema_selecionado = "FATOS"
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "yPoemas"

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

# 4. SIDEBAR (TODO [TEST] - REVISÃO FINAL)
with st.sidebar:
    # ITEM 1: Dropdown de Idiomas (Topo Absoluto)
    idiomas_pcc = ["Português", "Español", "Italiano", "Français", "English", "Català", "Deutsch", "Nederlands", "Dansk", "Svenska", "Norsk"]
    st.selectbox("Idioma", idiomas_pcc, label_visibility="collapsed")
    
#    st.divider()
    with st.container():
        # ITEM 3: radio_chk (Sem botões extras)
        st.radio(["[]som", "[]arte", "[]vídeo"], label_visibility="expanded")
        
    st.caption("Copyright © 1983-2026 Nando Lopes")

# 5. RENDERIZAÇÃO
def main():
    pagina = st.session_state.pagina_ativa
    col_l, col_main, col_r = st.columns([1, 4, 1])
    
    with col_main:
        if pagina == "mini":
            try: import mini as pg_mini; pg_mini.exibir()
            except ImportError: st.error("Módulo 'mini' não encontrado.")
            
        elif pagina == "yPoemas":
            if st.session_state.poema_atual:
                with st.container(border=True):
                    for v in st.session_state.poema_atual:
                        if v == "\n": st.write("")
                        else: st.markdown(v, unsafe_allow_html=True)
                        
        elif pagina == "eureka":
            try: import eureka as pg_eureka; pg_eureka.exibir()
            except ImportError: st.error("Módulo 'eureka' não encontrado.")
            
        elif pagina == "books":
            # Lógica interna para Books (Substitui o arquivo books.py inexistente)
            st.subheader("Biblioteca de Temas")
            confirmar = st.toggle("confirmar escolha do leitor")
            
            try:
                arquivos_base = os.listdir("./base/")
                livros = [f for f in arquivos_base if f.startswith("Rol_") and f.endswith(".TXT")]
                if confirmar:
                    for livro in livros:
                        with st.expander(livro.replace("Rol_", "").replace(".TXT", "")):
                            with open(f"./base/{livro}", "r", encoding="utf-8") as f:
                                st.text(f.read())
                else:
                    st.info("Ative o toggle para visualizar o conteúdo dos livros.")
            except Exception as e:
                st.error(f"Erro ao carregar biblioteca: {e}")

        elif pagina == "comments":
            try: import comments as pg_comments; pg_comments.exibir()
            except ImportError: st.error("Módulo 'comments' não encontrado.")
            
        elif pagina == "about":
            try: import about as pg_about; pg_about.exibir()
            except ImportError: st.error("Módulo 'about' não encontrado.")

if __name__ == "__main__":
    main()
