import streamlit as st
import os
import random
import streamlit.components.v1 as components

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO E CSS UNIFICADO
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
    /* FONTE ÚNICA E LIMPA PARA A ÁREA DE LEITURA */
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600&display=swap');

    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }

    [data-testid="stAppViewBlockContainer"] {
        max-width: 850px !important;
        margin: 0 auto !important;
    }

    /* Padronização dos Botões */
    .stButton>button { 
        width: 100%; 
        border-radius: 4px; 
        height: 2.8em; 
        font-family: sans-serif;
    }

    /* Container do Poema para evitar fontes misturadas */
    .poema-box {
        font-family: 'Crimson Pro', serif !important;
        font-size: 26px !important;
        line-height: 1.4 !important;
        color: #111 !important;
        white-space: pre-wrap;
        margin-top: 20px;
    }
    </style> """,
    unsafe_allow_html=True,
)

try:
    from lay_2_ypo import gera_poema
except:
    def gera_poema(t, s=""): return ["Motor em manutenção..."]

# ==========================================
# 2º ANDAR: COMPONENTES DE INTERFACE (SIDEBAR)
# ==========================================
def draw_check_buttons():
    draw_col, talk_col, vyde_col = st.sidebar.columns([1, 1, 1])
    st.session_state.draw = draw_col.checkbox("🖼️", value=st.session_state.get('draw', False), key="draw_machina")
    st.session_state.talk = talk_col.checkbox("🔊", value=st.session_state.get('talk', False), key="talk_machina")
    st.session_state.video = vyde_col.checkbox("🎬", value=st.session_state.get('video', False), key="vyde_machina")

def pick_lang():
    st.sidebar.selectbox("Idioma", ["Português", "English", "Español"], key="lang")

# ==========================================
# 3º ANDAR: A ESTRUTURA DA PÁGINA (HIERARQUIA SOLICITADA)
# ==========================================
def main():
    # Inicialização de Estados
    if 'take' not in st.session_state: st.session_state.take = 0
    if 'sala' not in st.session_state: st.session_state.sala = "yPoemas"
    if 'lang' not in st.session_state: st.session_state.lang = "Português"

    # --- A. BOTÕES DE NAVEGAÇÃO (FAROL) NO TOPO ---
    n1, n2, n3, n4, n_help = st.columns([1, 1, 1, 1, 1])
    if n1.button("✚"): st.session_state.take = random.randint(0, 99999); st.rerun()
    if n2.button("◀"): st.session_state.take -= 1; st.rerun()
    if n3.button("✻"): st.session_state.take = random.randint(0, 99999); st.rerun()
    if n4.button("▶"): st.session_state.take += 1; st.rerun()
    with n_help:
        with st.popover("?"): st.write("Matriz: Préfacil")

    st.write("") # Respiro

    # --- B. BUTTONS DAS PÁGINAS (MENU HORIZONTAL) ---
    mapa_artes = {
        "mini": "img_mini.jpg",
        "yPoemas": "img_ypoemas.jpg",
        "eureka": "img_eureka.jpg",
        "off-machina": "img_off-machina.jpg",
        "books": "img_books.jpg",
        "poly": "img_poly.jpg",
        "sobre": "img_about.jpg"
    }
    salas = list(mapa_artes.keys())
    cols_menu = st.columns(len(salas))
    for i, nome_sala in enumerate(salas):
        if cols_menu[i].button(nome_sala.upper(), key=f"btn_{nome_sala}"):
            st.session_state.sala = nome_sala
            st.rerun()
    
    st.divider()

    # --- C. ÁREA DE LEITURA ---
    if st.session_state.sala == "yPoemas":
        poema_raw = gera_poema("Fatos", str(st.session_state.take))
        
        # Tratamento para garantir que o texto saia limpo (sem lixo de dicionário/lista)
        if isinstance(poema_raw, dict):
            texto_final = "\n".join([str(v) for v in poema_raw.values()])
        elif isinstance(poema_raw, list):
            texto_final = "\n".join([str(p) for p in poema_raw])
        else:
            texto_final = str(poema_raw)

        # Exibição com fonte unificada
        st.markdown(f'<div class="poema-box">{texto_final}</div>', unsafe_allow_html=True)
    else:
        st.subheader(f"Sala {st.session_state.sala.upper()}")
        st.write("Conteúdo em fase de processamento...")

    # --- SIDEBAR (VARIÁVEIS GLOBAIS + IMAGEM) ---
    pick_lang()
    draw_check_buttons()
    with st.sidebar:
        st.write("---")
        img_path = mapa_artes.get(st.session_state.sala)
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)

if __name__ == "__main__":
    main()
    

