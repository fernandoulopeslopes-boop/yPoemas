import os
import streamlit as st
from extra_streamlit_components import TabBar as stx

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="a Machina de fazer Poesia - yPoemas",
    page_icon="★",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- 2. UTILITÁRIOS E CACHE ---
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

# --- 3. CSS (LIMPO E ESTRUTURAL) ---
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
    .poema-box {
        background-color: #fcfcfc;
        padding: 25px;
        border-radius: 5px;
        border: 1px solid #eee;
        font-family: 'serif';
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    # Estados de Sessão
    if "lang" not in st.session_state: st.session_state.lang = "pt"
    if "draw" not in st.session_state: st.session_state.draw = False
    if "talk" not in st.session_state: st.session_state.talk = False

    # Navegação Superior
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

    # --- 4. SIDEBAR ---
    with st.sidebar:
        langs = ["pt", "es", "it", "fr", "en", "⚒️", "de", "nl", "da", "sv", "no", "fi", "pl", "cs", "sk", "hu", "ro", "ca", "gl", "eu", "el"]
        current_index = langs.index(st.session_state.lang) if st.session_state.lang in langs else 0
        
        selected_lang = st.selectbox("idiomas disponíveis...", langs, index=current_index)
        if selected_lang != st.session_state.lang:
            st.session_state.lang = selected_lang
            st.rerun()
        
        st.write("---")
        c1, c2 = st.columns(2)
        st.session_state.draw = c1.checkbox("arte", st.session_state.draw)
        st.session_state.talk = c2.checkbox("audio", st.session_state.talk)
        
        st.write("---")
        img_base = f"img_{page_name}"
        img_found = get_image_path(img_base)
        if img_found:
            st.image(img_found, use_container_width=True)
        
        txt_path = f"texts/info_{page_name}.md"
        info_content = load_txt(txt_path)
        if info_content:
            st.markdown(f"<div class='sidebar-info'><b>>></b> {info_content}</div>", unsafe_allow_html=True)

        st.write("---")
        st.markdown("<div style='text-align: center; opacity: 0.5; font-size: 0.7rem;'>fb | ig | wa | mail</div>", unsafe_allow_html=True)

    # --- 5. ÁREA DE CONTEÚDO ---
    
    # PÁGINA 1: MINI-MACHINA
    if chosen_id == "1":
        st.title("mini-Machina")
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.write("### ⚙️")
            tema = st.selectbox("tema", ["Amor", "Morte", "Tempo", "Mar", "Eterno", "Nada"])
            btn_gerar = st.button("gerar poema", use_container_width=True)
            
        with col1:
            if btn_gerar:
                # Placeholder de lógica para Página Mini
                st.markdown(f"""
                <div class="poema-box">
                    <i>{tema}...</i><br><br>
                    O verso que a machina traça,<br>
                    na brevidade do instante.<br>
                    Toda forma é uma fumaça,<br>
                    no cálculo do errante.
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.talk:
                    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Placeholder
            else:
                st.info("Aguardando comando para processar.")

    # PÁGINA 2: YPOEMAS (PRINCIPAL)
    elif chosen_id == "2":
        st.title("yPoemas")
        st.write("A Machina de Fazer Poesia")
        # Desenvolvimento da lógica principal aguardando próximo passo.

if __name__ == "__main__":
    main()
