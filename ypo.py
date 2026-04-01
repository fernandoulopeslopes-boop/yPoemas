import streamlit as st
import os
import random
import streamlit.components.v1 as components

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO EM WIDE (A VERSÃO QUE DEU CERTO)
# ==========================================
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide", 
    initial_sidebar_state="auto",
)

st.markdown(
    """ 
    <style> 
    /* Trava a Sidebar em 310px */
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }

    /* Centraliza o conteúdo no meio da tela wide */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 900px !important;
        margin: 0 auto !important;
        padding-top: 2rem !important;
    }

    .stButton>button { width: 100%; border-radius: 4px; }
    
    .main .block-container {
        padding-top: 1rem !important;
    }
    </style> """,
    unsafe_allow_html=True,
)

try:
    from lay_2_ypo import gera_poema
except:
    def gera_poema(t, s=""): return ["Motor em manutenção..."]

def load_md_file(file):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f: return f.read()
    return ""

# ==========================================
# 2º ANDAR: COMPONENTES DE INTERFACE
# ==========================================
def draw_check_buttons():
    draw_col, talk_col, vyde_col = st.sidebar.columns([1, 1, 1])
    st.session_state.draw = draw_col.checkbox("🖼️", value=st.session_state.get('draw', False), key="draw_machina")
    st.session_state.talk = talk_col.checkbox("🔊", value=st.session_state.get('talk', False), key="talk_machina")
    st.session_state.video = vyde_col.checkbox("🎬", value=st.session_state.get('video', False), key="vyde_machina")

def pick_lang():
    st.sidebar.selectbox("Idioma", ["Português", "English", "Español"], key="lang")

# ==========================================
# 3º ANDAR: AS SALAS (PÁGINAS)
# ==========================================
def page_ypoemas():
    path = os.path.join("base", f"rol_{st.session_state.book}.txt")
    lista = ["Fatos", "Tempo", "Anjos"]
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lista = [l.strip() for l in f if l.strip()]
    
    idx = st.session_state.take % len(lista)
    st.session_state.tema = lista[idx]

    # Farol de Navegação
    n1, n2, n3, n4, n_help = st.columns([1, 1, 1, 1, 1])
    if n1.button("✚"): st.session_state.take = random.randint(0, 9999); st.rerun()
    if n2.button("◀"): st.session_state.take -= 1; st.rerun()
    if n3.button("✻"): st.session_state.take = random.randint(0, 9999); st.rerun()
    if n4.button("▶"): st.session_state.take += 1; st.rerun()
    with n_help:
        with st.popover("?"): st.write("Matriz: Préfacil")

    st.divider()
    
    poema = gera_poema(st.session_state.tema, str(st.session_state.take))
    
    st.write(f"### {st.session_state.tema}")
    if isinstance(poema, list):
        for linha in poema: st.write(linha)
    else:
        st.write(poema)

def page_mini(): st.title("Mini-Mundos")
def page_eureka(): st.title("Eureka")
def page_off_machina(): st.title("Off-Machina")
def page_books(): st.title("Biblioteca")
def page_polys(): st.title("Poly-Gens")
def page_abouts(): st.title("Sobre")

# ==========================================
# 4º ANDAR: O MOTOR (MAIN)
# ==========================================
def main():
    if 'take' not in st.session_state: st.session_state.take = 0
    if 'book' not in st.session_state: st.session_state.book = "livro vivo"
    if 'lang' not in st.session_state: st.session_state.lang = "Português"
    if 'sala' not in st.session_state: st.session_state.sala = "yPoemas"

    mapa_artes = {
        "mini": "img_mini.jpg",
        "yPoemas": "img_ypoemas.jpg",
        "eureka": "img_eureka.jpg",
        "off-machina": "img_off-machina.jpg",
        "books": "img_books.jpg",
        "poly": "img_poly.jpg",
        "sobre": "img_about.jpg"
    }

    # MENU DE BOTÕES (O QUE FUNCIONA)
    salas = list(mapa_artes.keys())
    cols_menu = st.columns(len(salas))
    for i, nome_sala in enumerate(salas):
        if cols_menu[i].button(nome_sala, key=f"btn_{nome_sala}"):
            st.session_state.sala = nome_sala
            st.rerun()
    st.write("---")

    # SIDEBAR
    pick_lang()
    draw_check_buttons()
    
    with st.sidebar:
        st.write("---")
        img_path = mapa_artes.get(st.session_state.sala)
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)

    # ROTEAMENTO
    if st.session_state.sala == "yPoemas":
        page_ypoemas()
    elif st.session_state.sala == "mini":
        page_mini()
    elif st.session_state.sala == "eureka":
        page_eureka()
    elif st.session_state.sala == "off-machina":
        page_off_machina()
    elif st.session_state.sala == "books":
        page_books()
    elif st.session_state.sala == "poly":
        page_polys()
    elif st.session_state.sala == "sobre":
        page_abouts()

if __name__ == "__main__":
    main()
