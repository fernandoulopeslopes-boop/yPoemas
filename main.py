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
    """Carrega textos informativos de forma otimizada."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception:
        pass
    return ""

def get_image_path(base_name, folder="images"):
    """
    Localiza a imagem ignorando a capitalização da extensão.
    Busca por img_nome.* (jpg, JPG, png, etc)
    """
    if not os.path.exists(folder):
        return None
    try:
        files = os.listdir(folder)
        for f in files:
            # Compara o nome base ignorando case
            if f.upper().startswith(base_name.upper()):
                return os.path.join(folder, f)
    except Exception:
        pass
    return None

# --- CSS PERSONALIZADO (REVISADO) ---
st.markdown(
    """
    <style>
    /* Ajuste de padding superior */
    .block-container { padding-top: 2rem !important; }
    
    /* Largura da Sidebar */
    [data-testid="stSidebar"] { width: 310px !important; }
    
    /* Mantém o header visível para não perder o botão '>>' (toggle) */
    /* Mas remove a decoração e o menu de hambúrguer desnecessário */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { background: transparent !important; }
    
    /* Estilização do texto informativo */
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
    
    # Renderização da barra de abas
    chosen_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=i, title=t, description="") for t, i in tabs_data],
        default="2"
    )

    # Fallback de segurança para evitar que o app trave se o componente falhar
    if chosen_id is None:
        chosen_id = "2"

    # Identifica o nome amigável da página
    page_name = next((t for t, i in tabs_data if i == chosen_id), "yPoemas")

    # 3. SIDEBAR (Estrutura Visual)
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

        # Localização dinâmica da Arte: images/img_nome.JPG (ou .jpg)
        img_base = f"img_{page_name}"
        img_found = get_image_path(img_base)

        if img_found:
            st.image(img_found, use_container_width=True)
        else:
            st.caption(f"Aguardando arte: {img_base}.jpg")
        
        # Texto Informativo: texts/info_nome.md
        txt_path = f"texts/info_{page_name}.md"
        info_content = load_txt(txt_path)
        
        # Exibição com o marcador visual >>
        if info_content:
            st.markdown(f"<div class='sidebar-info'><b>>></b> {info_content}</div>", unsafe_allow_html=True)

        st.write("---")
        
        # Rodapé de Contatos
        st.markdown(
            "<div style='text-align: center; opacity: 0.5; font-size: 0.7rem;'>"
            "fb | ig | wa | mail</div>", 
            unsafe_allow_html=True
        )

    # 4. ÁREA DE CONTEÚDO (Placeholders por etapa)
    if chosen_id == "1":
        st.write("### mini-Machina")
        # Implementação futura da página mini
    elif chosen_id == "2":
        st.write("### yPoemas - A Machina")
        # Implementação futura da página yPoemas
    else:
        st.write(f"### {page_name}")

if __name__ == "__main__":
    main()
