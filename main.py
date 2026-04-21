import os
import sys
import streamlit as st
import extra_streamlit_components as stx

# --- ANCORAGEM DE DIRETÓRIO ---
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
if dname not in sys.path:
    sys.path.insert(0, dname)

# --- IMPORTAÇÃO DO MOTOR ---
try:
    from lay_2_ypo import gera_poema
except ImportError as e:
    st.error(f"Erro Crítico: Motor lay_2_ypo.py não localizado: {e}")
    st.stop()

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilo da Sidebar (300px) e Botões
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
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- FUNÇÕES DE INTERFACE INTEGRADAS (Para evitar erros de importação) ---
def local_load_md(file_name):
    """Carrega info das páginas sem depender do tools.py"""
    path = os.path.join("md_files", file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- INICIALIZAÇÃO DE ESTADOS ---
if "tema" not in st.session_state: st.session_state.tema = "amor"
if "eureka_word" not in st.session_state: st.session_state.eureka_word = ""
if "lang" not in st.session_state: st.session_state.lang = "pt"

# --- NAVEGAÇÃO PRINCIPAL ---

def main():
    # Barra de Abas
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Reconstrução da Sidebar
    with st.sidebar:
        # Controles Técnicos
        st.session_state.lang = st.selectbox("Idioma", ["pt", "en", "es", "fr", "it"])
        st.session_state.draw = st.checkbox("Mostrar Arte", value=True)
        st.session_state.talk = st.checkbox("Voz", value=False)
        
        st.divider()
        
        menu_map = {
            "1":"MINI", "2":"YPOEMAS", "3":"EUREKA", 
            "4":"OFF-MACHINA", "5":"BOOKS", "6":"POLY", "7":"ABOUT"
        }
        tag = menu_map.get(chosen_id, "YPOEMAS")
        
        # Arte da Página
        img_path = f"img_{tag.lower()}.jpg"
        if os.path.exists(img_path):
            st.image(img_path)
        
        # Info da Página (Markdown)
        info_text = local_load_md(f"INFO_{tag}.md")
        if info_text:
            st.info(info_text)
        
        st.divider()
        st.caption("yPoemas - a Machina de fazer Poesia")

    # --- ACIONAMENTO DO MOTOR (Palco Central) ---
    if chosen_id == "3":
        st.session_state.eureka_word = st.text_input(
            "Léxico (Sufixo ou Radical):", 
            st.session_state.eureka_word
        )
        if st.button("Acionar Eureka"):
            gera_poema(st.session_state.tema, st.session_state.eureka_word)
                
    elif chosen_id == "2":
        # Se houver uma lista de temas no diretório, podemos carregar aqui
        # Caso contrário, o motor gera com base no estado atual
        if st.button("Gerar Novo yPoema"):
            gera_poema(st.session_state.tema, "")
    
    elif chosen_id == "7":
        # Exemplo de aba About carregando direto do MD
        st.markdown(local_load_md("INFO_ABOUT.md"))

    else:
        st.write(f"Interface {tag} aguardando comando do motor.")

if __name__ == "__main__":
    main()
