import os
import streamlit as st
from extra_streamlit_components import TabBar as stx

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="a Machina de fazer Poesia - yPoemas",
    page_icon="★",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- UTILITÁRIOS DE ARQUIVO ---
@st.cache_data
def load_txt(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception:
        pass
    return ""

def get_image_path(base_name, folder="images"):
    if not os.path.exists(folder):
        return None
    try:
        files = os.listdir(folder)
        for f in files:
            if f.upper().startswith(base_name.upper()):
                return os.path.join(folder, f)
    except Exception:
        pass
    return None

# --- CSS PERSONALIZADO ---
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem !important; }
    [data-testid="stSidebar"] { width: 310px !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { background: transparent !important; }
    .sidebar-info {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
        line-height: 1.4;
        text-align: justify;
        padding: 10px 0;
    }
    /* Estilo para a grade de idiomas */
    .stButton > button {
        width: 100%;
        padding: 2px;
        font-size: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    # 1. Estados de Sessão
    if "lang" not in st.session_state: st.session_state.lang = "pt"
    if "draw" not in st.session_state: st.session_state.draw = False
    if "talk" not in st.session_state: st.session_state.talk = False

    # 2. Navegação Superior
    tabs_data = [
        ("mini", "1"), ("yPoemas", "2"), ("eureka", "3"),
        ("off-machina", "4"), ("books", "5"), ("poly", "6"), ("about", "7")
    ]
    chosen_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=i, title=t, description="") for t, i in tabs_data],
        default="2"
    )
    if chosen_id is None: chosen_id = "2"
    page_name = next((t for t, i in tabs_data if i == chosen_id), "yPoemas")

    # 3. SIDEBAR
    with st.sidebar:
        st.caption("idiomas disponíveis...")
        
        # Grade de 21 Idiomas (6 originais + 15 ocidente)
        langs = [
            "pt", "es", "it", "fr", "en", "⚒️", 
            "de", "nl", "da", "sv", "no", "fi", 
            "pl", "cs", "sk", "hu", "ro", "ca", 
            "gl", "eu", "el"
        ]
        
        # Renderização em grade de 6 colunas
        for i in range(0, len(langs), 6):
            cols = st.columns(6)
            for j, lang in enumerate(langs[i:i+6]):
                if cols[j].button(lang, key=f"lang_{lang}"):
                    st.session_state.lang = lang
                    st.rerun()
        
        st.write("---")

        # Controles: arte e audio
        c1, c2 = st.columns(2)
        st.session_state.draw = c1.checkbox("arte", st.session_state.draw)
        st.session_state.talk = c2.checkbox("audio", st.session_state.talk)
        
        st.write("---")

        # Arte da página (img_nome_da_pagina.jpg/JPG)
        img_base = f"img_{page_name}"
        img_found = get_image_path(img_base)

        if img_found:
            st.image(img_found, use_container_width=True)
        else:
            st.caption(f"Aguardando arte: {img_base}.jpg")
        
        # Texto Informativo
        txt_path = f"texts/info_{page_name}.md"
        info_content = load_txt(txt_path)
        if info_content:
            st.markdown(f"<div class='sidebar-info'><b>>></b> {info_content}</div>", unsafe_allow_html=True)

        st.write("---")
        
        st.markdown(
            "<div style='text-align: center; opacity: 0.5; font-size: 0.7rem;'>"
            "fb | ig | wa | mail</div>", 
            unsafe_allow_html=True
        )

    # 4. ÁREA DE CONTEÚDO
    if chosen_id == "1":
        st.write("### mini-Machina")
    elif chosen_id == "2":
        st.write("### yPoemas - A Machina")

if __name__ == "__main__":
    main()
