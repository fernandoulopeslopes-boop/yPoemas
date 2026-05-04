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

# --- FUNÇÕES DE CARREGAMENTO ---
@st.cache_data
def load_txt(file_path):
    """Carrega textos informativos com tratamento de erro."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception:
        pass
    return "Conteúdo informativo em breve."

# --- CSS PERSONALIZADO ---
st.markdown(
    """
    <style>
    .block-container { padding-top: 1rem !important; }
    [data-testid="stSidebar"] { width: 310px !important; }
    header { visibility: hidden; height: 0px; }
    footer { visibility: hidden; }
    .sidebar-info {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
        line-height: 1.4;
        text-align: justify;
        padding: 10px 0;
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

    # 2. Navegação Superior (Tabs)
    tabs_data = [
        ("mini", "1"), ("yPoemas", "2"), ("eureka", "3"),
        ("off-machina", "4"), ("books", "5"), ("poly", "6"), ("about", "7")
    ]
    
    chosen_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=i, title=t, description="") for t, i in tabs_data],
        default="2"
    )

    # Identifica o nome da página atual para o padrão de imagem
    page_name = next((t for t, i in tabs_data if i == chosen_id), "ypoemas")

    # 3. SIDEBAR (Design e Estrutura)
    with st.sidebar:
        # Seleção de Idiomas
        st.write("### 🌐 Language")
        cols = st.columns(6)
        langs = ["pt", "es", "it", "fr", "en", "⚒️"]
        for i, l in enumerate(langs):
            if cols[i].button(l, key=f"btn_{l}"):
                st.session_state.lang = l
                st.rerun()
        
        st.write("---")

        # Toggles de Funcionalidade
        c1, c2 = st.columns(2)
        st.session_state.draw = c1.checkbox("Imagem", st.session_state.draw)
        st.session_state.talk = c2.checkbox("Áudio", st.session_state.talk)
        
        st.write("---")

        # MAPEAMENTO DE CONTEÚDO (Imagens e Textos)
        # Padronização: images/img_nome_da_pagina.JPG
        img_path = f"images/img_{page_name}.JPG"
        txt_path = f"texts/info_{page_name}.md"

        # Renderização da Arte
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning(f"Arquivo não encontrado: {img_path}")
        
        # Renderização do Texto Informativo
        info_text = load_txt(txt_path)
        st.markdown(f"<div class='sidebar-info'>{info_text}</div>", unsafe_allow_html=True)

        st.write("---")
        
        # Rodapé de Contato
        st.markdown(
            "<div style='text-align: center; opacity: 0.5; font-size: 0.7rem;'>"
            "fb | ig | wa | mail</div>", 
            unsafe_allow_html=True
        )

    # 4. ÁREA DE CONTEÚDO (Aguardando GO)
    if chosen_id == "1":
        st.write(f"### {page_name}")
    elif chosen_id == "2":
        st.write(f"### {page_name}")
    # ...

if __name__ == "__main__":
    main()
