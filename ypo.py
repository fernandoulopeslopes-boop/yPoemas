import streamlit as st
import os
import random
import streamlit.components.v1 as components
import extra_streamlit_components as stx

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO EM WIDE (PARA DOMAR SIDEBAR)
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
    /* 1. TRAVA A SIDEBAR EM 310PX (SEM NEGOCIAÇÃO) */
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }

    /* 2. CENTRALIZA O CONTEÚDO (SIMULA O LAYOUT CENTERED) */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 900px !important;
        margin: 0 auto !important;
        padding-top: 2rem !important;
    }

    /* 3. AJUSTES GERAIS */
    .stButton>button { width: 100%; border-radius: 4px; }
    
    /* Remove espaços inúteis no topo */
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
    draw_col, talk_col, vyde_col = st.sidebar.columns([3.8, 3.2, 3])
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
    if n1.button("✚", help="Variação"): st.session_state.take = random.randint(0, 9999); st.rerun()
    if n2.button("◀", help="Anterior"): st.session_state.take -= 1; st.rerun()
    if n3.button("✻", help="Sorteio"): st.session_state.take = random.randint(0, 9999); st.rerun()
    if n4.button("▶", help="Próximo"): st.session_state.take += 1; st.rerun()
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

    # Tab Bar Horizontal
    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id="1", title="mini", description=""),
            stx.TabBarItemData(id="2", title="yPoemas", description=""),
            stx.TabBarItemData(id="3", title="eureka", description=""),
            stx.TabBarItemData(id="4", title="off-machina", description=""),
            stx.TabBarItemData(id="5", title="books", description=""),
            stx.TabBarItemData(id="6", title="poly", description=""),
            stx.TabBarItemData(id="7", title="sobre", description=""),
        ],
        default="2",
    )

    pick_lang()
    draw_check_buttons()

    magy = "img_ypoemas.jpg"

    if chosen_id == "1":
        st.sidebar.info(load_md_file("INFO_MINI.md"))
        magy = "img_mini.jpg"; page_mini()
    elif chosen_id == "2":
        st.sidebar.info(load_md_file("INFO_YPOEMAS.md"))
        magy = "img_ypoemas.jpg"; page_ypoemas()
    elif chosen_id == "3":
        st.sidebar.info(load_md_file("INFO_EUREKA.md"))
        magy = "img_eureka.jpg"; page_eureka()
    elif chosen_id == "4":
        st.sidebar.info(load_md_file("INFO_OFF-MACHINA.md"))
        magy = "img_off-machina.jpg"; page_off_machina()
    elif chosen_id == "5":
        st.sidebar.info(load_md_file("INFO_BOOKS.md"))
        magy = "img_books.jpg"; page_books()
    elif chosen_id == "6":
        st.sidebar.info(load_md_file("INFO_POLY.md"))
        magy = "img_poly.jpg"; page_polys()
    elif chosen_id == "7":
        st.sidebar.info(load_md_file("INFO_ABOUT.md"))
        magy = "img_about.jpg"; page_abouts()

    with st.sidebar:
        st.image(magy, use_column_width=True)

if __name__ == "__main__":
    main()
    
