import streamlit as st
import os
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: Fixar largura da sidebar (300px) e customização técnica
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
        .stMarkdown p {
            text-align: justify;
        }
        .stButton button {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

# 2. ESTADO DA SESSÃO
if 'poema_atual' not in st.session_state:
    st.session_state.poema_atual = []
if 'tema_selecionado' not in st.session_state:
    st.session_state.tema_selecionado = "FATOS"
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "yPoemas"

# 3. NAVEGAÇÃO SUPERIOR (As 6 Páginas)
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

# 4. SIDEBAR (TODO [TEST] CUMPRIDO)
with st.sidebar:
    # ITEM 1: Dropdown list com os idiomas PCC (Topo Esquerdo/Largura Total)
    idiomas_pcc = ["Português", "Español", "Italiano", "Français", "English", "Català", "Deutsch", "Nederlands", "Dansk", "Svenska", "Norsk"]
    st.selectbox("Selecione o Idioma", idiomas_pcc, label_visibility="collapsed")
    
    # ITEM 2: (Botoes de idiomas antigos eliminados conforme solicitado)
    
    st.divider()
    
    with st.container():
        # Listagem dinâmica de livros em ./base/
        try:
            arquivos_base = os.listdir("./base/")
            livros_lista = sorted([f.replace("Rol_", "").replace(".TXT", "") for f in arquivos_base if f.startswith("Rol_") and f.endswith(".TXT")])
        except FileNotFoundError:
            livros_lista = []

        st.selectbox("selecione o livro", livros_lista)
        
        # Temas em ./data/
        try:
            arquivos_data = os.listdir("./data/")
            temas = sorted([f.replace(".ypo", "") for f in arquivos_data if f.endswith(".ypo")])
        except FileNotFoundError:
            temas = ["FATOS"]

        st.selectbox(
            "Escolha o Tema", 
            temas, 
            index=temas.index(st.session_state.tema_selecionado) if st.session_state.tema_selecionado in temas else 0
        )
        
        st.divider()
        
        # ITEM 3: radio_chk []som []arte []vídeo
        st.radio("Modo", ["[]som", "[]arte", "[]vídeo"], label_visibility="collapsed")
        
        st.divider()
        st.text_input("Semente", placeholder="")

    # ITEM 4: Restante da sidebar preservado
    st.divider()
    st.caption("Copyright © 1983-2026 Nando Lopes")

# 5. RENDERIZAÇÃO (PPP)
def main():
    pagina = st.session_state.pagina_ativa
    col_l, col_main, col_r = st.columns([1, 4, 1])
    
    with col_main:
        if pagina == "mini":
            import mini as pg_mini
            pg_mini.exibir()
        elif pagina == "yPoemas":
            if st.session_state.poema_atual:
                with st.container(border=True):
                    for v in st.session_state.poema_atual:
                        if v == "\n": st.write("")
                        else: st.markdown(v, unsafe_allow_html=True)
        elif pagina == "eureka":
            import eureka as pg_eureka
            pg_eureka.exibir()
        elif pagina == "books":
            import books as pg_books
            pg_books.exibir()
        elif pagina == "comments":
            import comments as pg_comments
            pg_comments.exibir()
        elif pagina == "about":
            import about as pg_about
            pg_about.exibir()

if __name__ == "__main__":
    main()
