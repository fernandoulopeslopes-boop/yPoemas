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

# Interruptores de Modo
if 'sw_som' not in st.session_state: st.session_state.sw_som = False
if 'sw_arte' not in st.session_state: st.session_state.sw_arte = False
if 'sw_video' not in st.session_state: st.session_state.sw_video = False

# 3. NAVEGAÇÃO SUPERIOR
t1, t2, t3, t4, t5, t6 = st.columns(6)
paginas = ["mini", "yPoemas", "Eureka", "Books", "Comments", "About"]
for i, col in enumerate([t1, t2, t3, t4, t5, t6]):
    if col.button(paginas[i]):
        st.session_state.pagina_ativa = paginas[i].lower()

st.divider()

# 4. SIDEBAR (COM CONTAINER PARA OS BOTÕES)
with st.sidebar:
    # IDIOMAS (Caminho: ypo/)
    path_idiomas = os.path.join("ypo", "lista_idiomas.TXT")
    try:
        with open(path_idiomas, "r", encoding="utf-8") as f:
            idiomas_pcc = [l.strip() for l in f.readlines() if l.strip()]
    except:
        idiomas_pcc = ["Português", "Español", "Italiano"]

    st.selectbox("Idioma", idiomas_pcc, label_visibility="collapsed")
    
    st.divider()

    # CONTAINER DOS MODOS
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if st.button("Som"):
                st.session_state.sw_som = not st.session_state.sw_som
            st.caption("✅" if st.session_state.sw_som else "❌")

        with c2:
            if st.button("Arte"):
                st.session_state.sw_arte = not st.session_state.sw_arte
            st.caption("✅" if st.session_state.sw_arte else "❌")

        with c3:
            if st.button("Vídeo"):
                st.session_state.sw_video = not st.session_state.sw_video
            st.caption("✅" if st.session_state.sw_video else "❌")

    st.divider()
    st.caption("Copyright © 1983-2026 Nando Lopes")

# 5. RENDERIZAÇÃO
def main():
    pagina = st.session_state.pagina_ativa
    _, col_main, _ = st.columns([1, 4, 1])
    
    with col_main:
        if pagina == "ypoemas":
            if st.session_state.poema_atual:
                with st.container(border=True):
                    for v in st.session_state.poema_atual:
                        if v == "\n": st.write("")
                        else: st.markdown(v, unsafe_allow_html=True)
            
            # Feedback Visual das Camadas
            if st.session_state.sw_som or st.session_state.sw_arte or st.session_state.sw_video:
                with st.status("Camadas Ativas"):
                    if st.session_state.sw_som: st.write("Som ativado.")
                    if st.session_state.sw_arte: st.write("Arte ativada.")
                    if st.session_state.sw_video: st.write("Vídeo ativado.")

if __name__ == "__main__":
    main()
