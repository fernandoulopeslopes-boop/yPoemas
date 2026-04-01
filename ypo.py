import streamlit as st
import os
import random
import streamlit.components.v1 as components

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO WIDE (SIDEBAR TRAVADA)
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

    /* Centraliza o palco para a poesia não espalhar */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 850px !important;
        margin: 0 auto !important;
    }

    .stButton>button { width: 100%; border-radius: 4px; height: 3em; }
    
    /* Estética do texto poético */
    .poema-container {
        font-family: 'Crimson Pro', serif;
        font-size: 24px;
        line-height: 1.4;
        color: #222;
        white-space: pre-wrap;
    }
    </style> """,
    unsafe_allow_html=True,
)

try:
    from lay_2_ypo import gera_poema
except:
    def gera_poema(t, s=""): return ["Motor em manutenção..."]

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
    # Lógica de Temas
    lista = ["Fatos", "Tempo", "Anjos"] # Fallback
    path = os.path.join("base", f"rol_{st.session_state.book}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lista = [l.strip() for l in f if l.strip()]
    
    idx = st.session_state.take % len(lista)
    st.session_state.tema = lista[idx]

    # Farol de Navegação
    n1, n2, n3, n4, n_help = st.columns([1, 1, 1, 1, 1])
    if n1.button("✚"): st.session_state.take = random.randint(0, 99999); st.rerun()
    if n2.button("◀"): st.session_state.take -= 1; st.rerun()
    if n3.button("✻"): st.session_state.take = random.randint(0, 99999); st.rerun()
    if n4.button("▶"): st.session_state.take += 1; st.rerun()
    with n_help:
        with st.popover("?"): st.write("Matriz: Préfacil")

    st.divider()
    
    # Chama o motor
    poema_raw = gera_poema(st.session_state.tema, str(st.session_state.take))
    
    # --- LIMPEZA DE SAÍDA (CORREÇÃO DO BUG DO DICIONÁRIO) ---
    st.write(f"### {st.session_state.tema}")
    
    texto_limpo = ""
    if isinstance(poema_raw, dict):
        texto_limpo = "\n".join([str(v) for v in poema_raw.values()])
    elif isinstance(poema_raw, list):
        texto_limpo = "\n".join([str(p) for p in poema_raw])
    else:
        texto_limpo = str(poema_raw)
    
    st.markdown(f'<div class="poema-container">{texto_limpo}</div>', unsafe_allow_html=True)

# Mocks para as outras salas
def simple_page(nome):
    st.title(nome)
    st.write("Em calibração poética...")

# ==========================================
# 4º ANDAR: O MOTOR (MAIN)
# ==========================================
def main():
    # Inicialização
    states = {'take': 0, 'book': "livro vivo", 'lang': "Português", 'sala': "yPoemas"}
    for k, v in states.items():
        if k not in st.session_state: st.session_state[k] = v

    mapa_artes = {
        "mini": "img_mini.jpg",
        "yPoemas": "img_ypoemas.jpg",
        "eureka": "img_eureka.jpg",
        "off-machina": "img_off-machina.jpg",
        "books": "img_books.jpg",
        "poly": "img_poly.jpg",
        "sobre": "img_about.jpg"
    }

    # Menu Horizontal de Botões
    salas = list(mapa_artes.keys())
    cols_menu = st.columns(len(salas))
    for i, nome_sala in enumerate(salas):
        if cols_menu[i].button(nome_sala.upper(), key=f"btn_{nome_sala}"):
            st.session_state.sala = nome_sala
            st.rerun()
    st.write("---")

    # Sidebar
    pick_lang()
    draw_check_buttons()
    
    with st.sidebar:
        st.write("---")
        img_path = mapa_artes.get(st.session_state.sala)
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)

    # Roteamento
    if st.session_state.sala == "yPoemas":
        page_ypoemas()
    else:
        simple_page(st.session_state.sala)

if __name__ == "__main__":
    main()
    
