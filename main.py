import os
import streamlit as st
from extra_streamlit_components import TabBar as stx

# --- CONFIGURAÇÃO DA PÁGINA (Clean Design) ---
st.set_page_config(
    page_title="a Machina de fazer Poesia - yPoemas",
    page_icon="★",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- CACHE DE ARQUIVOS (Otimizado) ---
@st.cache_data
def load_txt(file_path):
    """Carrega textos informativos de forma otimizada."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Conteúdo não encontrado."

# --- CSS PERSONALIZADO (Visual Clean) ---
st.markdown(
    """
    <style>
    /* Remove espaçamentos excessivos no topo */
    .block-container { padding-top: 1rem !important; }
    
    /* Largura fixa da Sidebar para manter o design */
    [data-testid="stSidebar"] { width: 310px !important; }
    
    /* Esconde elementos nativos para interface limpa */
    header { visibility: hidden; height: 0px; }
    footer { visibility: hidden; }
    
    /* Estilização dos ícones e textos da sidebar */
    .sidebar-info {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
        line-height: 1.4;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LÓGICA DE INTERFACE ---
def main():
    # 1. Inicialização de Estados
    if "lang" not in st.session_state:
        st.session_state.lang = "pt"
    if "draw" not in st.session_state:
        st.session_state.draw = False
    if "talk" not in st.session_state:
        st.session_state.talk = False

    # 2. Navegação Superior (Tabs)
    tabs = [
        ("mini", "1"), ("yPoemas", "2"), ("eureka", "3"),
        ("off-machina", "4"), ("books", "5"), ("poly", "6"), ("about", "7")
    ]
    chosen_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=i, title=t, description="") for t, i in tabs],
        default="2"
    )

    # 3. CONSTRUÇÃO DA SIDEBAR (Foco: Arte e Texto)
    with st.sidebar:
        # Seleção de Idiomas (Horizontal)
        st.write("### 🌐")
        cols = st.columns(6)
        langs = ["pt", "es", "it", "fr", "en", "⚒️"]
        for i, l in enumerate(langs):
            if cols[i].button(l):
                st.session_state.lang = l
                st.rerun()
        
        st.write("---")

        # Configurações Adicionais
        c1, c2 = st.columns(2)
        st.session_state.draw = c1.checkbox("Imagem", st.session_state.draw)
        st.session_state.talk = c2.checkbox("Áudio", st.session_state.talk)
        
        st.write("---")

        # MAPEAMENTO DINÂMICO (Página -> Arte + Texto)
        # Cada página define sua imagem e seu arquivo de texto
        sidebar_content = {
            "1": {"img": "art_mini.jpg", "txt": "info_mini.md"},
            "2": {"img": "art_ypoemas.jpg", "txt": "info_ypoemas.md"},
            "3": {"img": "art_eureka.jpg", "txt": "info_eureka.md"},
            "4": {"img": "art_off.jpg", "txt": "info_off.md"},
            "5": {"img": "art_books.jpg", "txt": "info_books.md"},
            "6": {"img": "art_poly.jpg", "txt": "info_poly.md"},
            "7": {"img": "art_about.jpg", "txt": "info_about.md"},
        }

        # Renderização da Arte da Página Selecionada
        content = sidebar_content.get(chosen_id)
        if content:
            st.image(f"assets/{content['img']}", use_container_width=True)
            st.markdown(f"<div class='sidebar-info'>{load_txt(f'texts/{content[ 'txt']}')}</div>", unsafe_allow_html=True)

        st.write("---")
        
        # Ícones Sociais (Rodapé da Sidebar)
        st.markdown(
            """
            <div style='text-align: center; opacity: 0.6; font-size: 0.8rem;'>
                fb | ig | wa | mail
            </div>
            """,
            unsafe_allow_html=True
        )

    # 4. ÁREA DE CONTEÚDO (Placeholders para as próximas etapas)
    if chosen_id == "1":
        # Aguardando GO para implementar page_mini()
        st.title("Página Mini")
    elif chosen_id == "2":
        st.title("yPoemas - A Machina")
    # ... demais condições

if __name__ == "__main__":
    main()
