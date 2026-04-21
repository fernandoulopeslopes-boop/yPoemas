import os
import sys
import streamlit as st
import extra_streamlit_components as stx

# --- ANCORAGEM E INTEGRIDADE DO AMBIENTE ---
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
if dname not in sys.path:
    sys.path.insert(0, dname)

# --- CONEXÃO COM A ESTRUTURA DA MACHINA ---
try:
    # Se o motor é o coração, tentamos buscar as ferramentas nele primeiro
    # ou no tools.py caso existam lá.
    from lay_2_ypo import gera_poema
    
    # Tentativa de importação flexível das ferramentas de interface
    try:
        from lay_2_ypo import load_md_file, show_icons, pick_lang, draw_check_buttons
    except ImportError:
        try:
            from tools import load_md_file, show_icons, pick_lang, draw_check_buttons
        except ImportError:
            # Fallback silencioso para não travar a abertura da página
            def load_md_file(x): return ""
            def show_icons(): pass
            def pick_lang(): pass
            def draw_check_buttons(): pass
            
except ImportError as e:
    st.error(f"Erro Crítico: O motor lay_2_ypo.py não foi encontrado: {e}")
    st.stop()

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilização da Sidebar (300px)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 300px;
        max-width: 300px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- INICIALIZAÇÃO DE ESTADOS ---
if "tema" not in st.session_state: st.session_state.tema = "amor"
if "eureka_word" not in st.session_state: st.session_state.eureka_word = ""

# --- ESTRUTURA DE NAVEGAÇÃO ---

def main():
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    with st.sidebar:
        pick_lang()
        draw_check_buttons()
        st.divider()
        
        menu_map = {
            "1":"MINI", "2":"YPOEMAS", "3":"EUREKA", 
            "4":"OFF-MACHINA", "5":"BOOKS", "6":"POLY", "7":"ABOUT"
        }
        tag = menu_map.get(chosen_id, "YPOEMAS")
        
        try:
            st.image(f"img_{tag.lower()}.jpg")
        except:
            pass
        
        info_content = load_md_file(f"INFO_{tag}.md")
        if info_content:
            st.info(info_content)

    # --- PALCO DA MACHINA ---
    if chosen_id == "3":
        st.session_state.eureka_word = st.text_input(
            "Léxico:", 
            st.session_state.eureka_word,
            placeholder="sufixo ou radical..."
        )
        if st.button("Acionar Eureka"):
            gera_poema(st.session_state.tema, st.session_state.eureka_word)
                
    elif chosen_id == "2":
        if st.button("Gerar Novo yPoema"):
            gera_poema(st.session_state.tema, "")
    else:
        st.write(f"Interface {tag} ativa.")

    show_icons()

if __name__ == "__main__":
    main()
