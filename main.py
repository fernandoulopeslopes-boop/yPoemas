import streamlit as st
import os
from lay_2_ypo import gera_poema

# 1. SETUP & CSS
st.set_page_config(
    page_title="a Machina de Fazer Poesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        [data-testid="stSidebar"] { min-width: 300px; max-width: 300px; }
        .stMarkdown p { text-align: justify; }
        .stButton button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. ESTADOS
if 'poema_atual' not in st.session_state: st.session_state.poema_atual = []
if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = "yPoemas"

# Interruptores de Modo (Som, Arte, Pic)
if 'sw_som' not in st.session_state: st.session_state.sw_som = False
if 'sw_arte' not in st.session_state: st.session_state.sw_arte = False
if 'sw_pic' not in st.session_state: st.session_state.sw_pic = False

# 3. NAV SUPERIOR
t1, t2, t3, t4, t5, t6 = st.columns(6)
btns = ["mini", "yPoemas", "Eureka", "Books", "Comments", "About"]
for i, col in enumerate([t1, t2, t3, t4, t5, t6]):
    if col.button(btns[i]):
        st.session_state.pagina_ativa = btns[i].lower()

st.divider()

# 4. SIDEBAR (CONTAINER PIC)
with st.sidebar:
    # IDIOMAS (Path: ypo/)
    path_idiomas = os.path.join("ypo", "lista_idiomas.TXT")
    idiomas_pcc = ["Português"]
    if os.path.exists(path_idiomas):
        with open(path_idiomas, "r", encoding="utf-8") as f:
            idiomas_pcc = [l.strip() for l in f.readlines() if l.strip()]

    st.selectbox("Idioma", idiomas_pcc, label_visibility="collapsed")
    
    st.divider()

    # COCKPIT: SOM | ARTE | PIC
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            lbl_som = "Som [ON]" if st.session_state.sw_som else "Som"
            if st.button(lbl_som):
                st.session_state.sw_som = not st.session_state.sw_som
                st.rerun()

        with c2:
            lbl_arte = "Arte [ON]" if st.session_state.sw_arte else "Arte"
            if st.button(lbl_arte):
                st.session_state.sw_arte = not st.session_state.sw_arte
                st.rerun()

        with c3:
            lbl_pic = "PIC [ON]" if st.session_state.sw_pic else "PIC"
            if st.button(lbl_pic):
                st.session_state.sw_pic = not st.session_state.sw_pic
                st.rerun()

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
            
            # As camadas agem conforme os estados sw_som, sw_arte e sw_pic

        elif pagina == "books":
            st.subheader("Biblioteca")
            if st.toggle("confirmar leitura"):
                try:
                    livros = [f for f in os.listdir("./base/") if f.startswith("Rol_") and f.endswith(".TXT")]
                    for livro in livros:
                        with st.expander(livro.replace("Rol_", "").replace(".TXT", "")):
                            with open(f"./base/{livro}", "r", encoding="utf-8") as f:
                                st.text(f.read())
                except: st.error("Erro na pasta /base")

if __name__ == "__main__":
    main()
