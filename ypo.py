import streamlit as st
import os
import random
import streamlit.components.v1 as components
import extra_streamlit_components as stx

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO E CSS (O RIGOR DOS 310PX)
# ==========================================
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide", # Usamos wide para travar a sidebar, mas centralizamos o conteúdo via CSS
    initial_sidebar_state="auto",
)

st.markdown(
    """ 
    <style> 
    /* Força a largura da Sidebar conforme seu layout original */
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px !important;
    }
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }

    /* Centraliza o palco da poesia para manter a estética centered */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 900px !important;
        margin: 0 auto !important;
    }

    .stButton>button { width: 100%; border-radius: 4px; }
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
# 2º ANDAR: COMPONENTES DA SIDEBAR (SEU LAYOUT)
# ==========================================
def draw_check_buttons():
    # Organiza os botões de check em colunas na sidebar conforme seu trecho
    draw_col, talk_col, vyde_col = st.sidebar.columns([3.8, 3.2, 3])
    
    # Usando os emojis como labels compactas para o seu layout enxuto
    st.session_state.draw = draw_col.checkbox("🖼️", value=st.session_state.get('draw', False), key="draw_machina")
    st.session_state.talk = talk_col.checkbox("🔊", value=st.session_state.get('talk', False), key="talk_machina")
    st.session_state.video = vyde_col.checkbox("🎬", value=st.session_state.get('video', False), key="vyde_machina")

def pick_lang():
    st.sidebar.selectbox("Idioma", ["Português", "English", "Español"], key="lang")

# ==========================================
# 3º ANDAR: AS SALAS (PÁGINAS)
# ==========================================
def page_ypoemas():
    # Lógica de Temas (Farol)
    if 'take' not in st.session_state: st.session_state.take = 0
    
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1,1,1,1,1])
    if col_f1.button("✚"): st.session_state.take = random.randint(0, 9999); st.rerun()
    if col_f2.button("◀"): st.session_state.take -= 1; st.rerun()
    if col_f3.button("✻"): st.session_state.take = random.randint(0, 9999); st.rerun()
    if col_f4.button("▶"): st.session_state.take += 1; st.rerun()
    with col_f5:
        with st.popover("?"): st.write("Matriz: Préfacil")
    
    st.divider()
    poema = gera_poema("Fatos", str(st.session_state.take))
    st.write(f"### Poema N. {st.session_state.take}")
    st.write(poema)

# Mocks para as outras salas
def page_mini(): st.write("### Sala Mini-Mundos")
def page_eureka(): st.write("### Sala Eureka")
def page_off_machina(): st.write("### Sala Off-Machina")
def page_books(): st.write("### Sala Books")
def page_polys(): st.write("### Sala Poly-Gens")
def page_abouts(): st.write("### Sobre")

# ==========================================
# 4º ANDAR: O MOTOR (ROTEAMENTO ORIGINAL)
# ==========================================
def main():
    # Inicialização de estados
    if 'lang' not in st.session_state: st.session_state.lang = "Português"
    if 'draw' not in st.session_state: st.session_state.draw = False
    if 'talk' not in st.session_state: st.session_state.talk = False
    if 'video' not in st.session_state: st.session_state.video = False

    # MENU TAB BAR (O CORAÇÃO DA NAVEGAÇÃO)
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

    # Executa componentes da Sidebar
    pick_lang()
    draw_check_buttons()

    # Roteamento conforme sua lógica de IDs
    magy = "img_ypoemas.jpg" # Default

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

    # Imagem da Sidebar no final, conforme seu script
    with st.sidebar:
        st.write("---")
        st.image(magy, use_column_width=True)

if __name__ == "__main__":
    main()
    
