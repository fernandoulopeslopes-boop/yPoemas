import streamlit as st
import os
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: Fixar largura da sidebar (300px) e justificar textos
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
    st.session_state.pagina_ativa = "Palco"

# 3. NAVEGAÇÃO SUPERIOR (Original)
t1, t2, t3, t4, t5, t6 = st.columns(6)
with t1:
    if st.button("Palco"): st.session_state.pagina_ativa = "Palco"
with t2:
    if st.button("Livros"): st.session_state.pagina_ativa = "Livros"
with t3:
    if st.button("Talk"): st.session_state.pagina_ativa = "Talk"
with t4:
    if st.button("Arts"): st.session_state.pagina_ativa = "Arts"
with t5:
    if st.button("Eureka"): st.session_state.pagina_ativa = "Eureka"
with t6:
    if st.button("Sobre"): st.session_state.pagina_ativa = "Sobre"

st.divider()

# 4. SIDEBAR (Com as alterações solicitadas)
with st.sidebar:
    # Itens 1 e 2: Dropdown de idiomas PCC
    idiomas_pcc = ["Português", "Español", "Italiano", "Français", "English", "Català", "Deutsch", "Nederlands", "Dansk", "Svenska", "Norsk"]
    idioma_selecionado = st.selectbox("Idioma", idiomas_pcc, label_visibility="collapsed")
    
    with st.container():
        # Item 4 e 5: Listagem dinâmica de livros em ./base/ (Rol_*.TXT)
        try:
            arquivos_base = os.listdir("./base/")
            livros = sorted([f.replace("Rol_", "").replace(".TXT", "") for f in arquivos_base if f.startswith("Rol_") and f.endswith(".TXT")])
        except FileNotFoundError:
            livros = ["Jocosos", "Anima", "Machina", "Poesia"]

        livro_sidebar = st.selectbox("selecione o livro", livros)
        
        # Seleção de Temas em ./data/
        try:
            arquivos_data = os.listdir("./data/")
            temas = sorted([f.replace(".ypo", "") for f in arquivos_data if f.endswith(".ypo")])
        except FileNotFoundError:
            temas = ["FATOS"]

        tema_escolhido = st.selectbox(
            "Escolha o Tema", 
            temas, 
            index=temas.index(st.session_state.tema_selecionado) if st.session_state.tema_selecionado in temas else 0
        )
        
        st.divider()
        # Item 3: Radio_chk []som []arte []vídeo
        modo_interacao = st.radio("Modo", ["[]som", "[]arte", "[]vídeo"], label_visibility="collapsed")
        
        st.divider()
        seed = st.text_input("Semente", placeholder="")

    st.divider()
    st.caption("Copyright © 1983-2026 Nando Lopes")

# 5. RENDERIZAÇÃO DAS PÁGINAS (As Is)
def main():
    col_l, col_main, col_r = st.columns([1, 4, 1])
    
    with col_main:
        if st.session_state.pagina_ativa == "Palco":
            if st.session_state.poema_atual:
                with st.container(border=True):
                    for verso in st.session_state.poema_atual:
                        if verso == "\n": st.write("")
                        else: st.markdown(verso, unsafe_allow_html=True)
        
        elif st.session_state.pagina_ativa == "Livros":
            st.markdown(f"### Biblioteca: {livro_sidebar}")
            # Lógica original da página Livros
            
        elif st.session_state.pagina_ativa == "Talk":
            st.markdown("### Interatividade Vocal")
            # Lógica original da página Talk
            
        elif st.session_state.pagina_ativa == "Arts":
            st.markdown("### Galeria Generativa")
            # Lógica original da página Arts

        elif st.session_state.pagina_ativa == "Eureka":
            st.markdown("### Eureka")
            # Lógica original da página Eureka

        elif st.session_state.pagina_ativa == "Sobre":
            st.markdown("### Sobre a Máquina")

if __name__ == "__main__":
    main()
