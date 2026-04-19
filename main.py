import streamlit as st
import os
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="a Machina de Fazer Poesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: Justificativa correta e largura fixa
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

# 4. SIDEBAR (AUDITADA)
with st.sidebar:
    # MUDANÇA 1: Leitura obrigatória da lista externa
    path_idiomas = os.path.join("ypo", "lista_idiomas.TXT")
    try:
        with open(path_idiomas, "r", encoding="utf-8") as f:
            idiomas_pcc = [linha.strip() for linha in f.readlines() if linha.strip()]
    except:
        idiomas_pcc = ["Erro ao ler TXT"]

    st.selectbox("Idioma", idiomas_pcc, label_visibility="collapsed")
    
    st.divider()

    # MUDANÇA 2: Radio buttons HORIZONTAIS
    # MUDANÇA 3: Expurgo total do lixo (Semente/Input sumiram)
    st.radio(
        "Modo", 
        ["[]som", "[]arte", "[]vídeo"], 
        label_visibility="collapsed", 
        horizontal=True
    )
        
    st.divider()
    st.caption("Copyright © 1983-2026 Nando Lopes")

# 5. RENDERIZAÇÃO
def main():
    pagina = st.session_state.pagina_ativa
    _, col_main, _ = st.columns([1, 4, 1])
    
    with col_main:
        if pagina == "mini":
            try:
                import mini as pg_mini
                pg_mini.exibir()
            except: st.error("Módulo 'mini' ausente.")
            
        elif pagina == "yPoemas":
            if st.session_state.poema_atual:
                with st.container(border=True):
                    for v in st.session_state.poema_atual:
                        if v == "\n": st.write("")
                        else: st.markdown(v, unsafe_allow_html=True)
                        
        elif pagina == "eureka":
            try:
                import eureka as pg_eureka
                pg_eureka.exibir()
            except: st.error("Módulo 'eureka' ausente.")
            
        elif pagina == "books":
            st.subheader("Biblioteca de Temas")
            if st.toggle("confirmar escolha do leitor"):
                try:
                    livros = [f for f in os.listdir("./base/") if f.startswith("Rol_") and f.endswith(".TXT")]
                    for livro in livros:
                        with st.expander(livro.replace("Rol_", "").replace(".TXT", "")):
                            with open(f"./base/{livro}", "r", encoding="utf-8") as f:
                                st.text(f.read())
                except: st.error("Erro ao ler diretório base.")
            else:
                st.info("Ative o toggle para ler.")

        elif pagina == "comments":
            try:
                import comments as pg_comments
                pg_comments.exibir()
            except: st.error("Módulo 'comments' ausente.")
            
        elif pagina == "about":
            try:
                import about as pg_about
                pg_about.exibir()
            except: st.error("Módulo 'about' ausente.")

if __name__ == "__main__":
    main()
