import os
import sys
import streamlit as st
import extra_streamlit_components as stx

# --- ANCORAGEM DE DIRETÓRIO (Protocolo de Estabilidade CPC) ---
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
if dname not in sys.path:
    sys.path.insert(0, dname)

# --- CONEXÃO COM O MOTOR INTOCÁVEL ---
try:
    from lay_2_ypo import gera_poema
except ImportError as e:
    st.error(f"Erro Crítico: O motor lay_2_ypo.py não foi detectado: {e}")
    st.stop()

# --- CONFIGURAÇÃO DE INTERFACE E IDENTIDADE VISUAL ---
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# CSS CUSTOMIZADO (Temperatura Zero: Precisão de Design)
st.markdown(
    """
    <style>
    /* Sidebar fixa em 300px */
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 300px;
        max-width: 300px;
    }
    /* Tipografia de Máquina: Courier New para todo o sistema */
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 15px;
    }
    /* Estilização de Botões: Retangulares e Sóbrios */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3.2em;
        font-weight: 600;
        border: 1px solid #d1d1d1;
        background-color: #fcfcfc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- FUNÇÕES DE SUPORTE LOCAIS ---
def load_sidebar_info(tag):
    """Carrega as instruções de cada aba da pasta md_files."""
    path = os.path.join("md_files", f"INFO_{tag}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- INICIALIZAÇÃO DE ESTADO ---
if "tema" not in st.session_state: st.session_state.tema = "amor"
if "eureka_word" not in st.session_state: st.session_state.eureka_word = ""
if "lang" not in st.session_state: st.session_state.lang = "pt"

# --- NAVEGAÇÃO DE ABAS ---

def main():
    # Abas conforme especificação atualizada do projeto
    tabs = [
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-mach", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="comments", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ]
    
    chosen_id = stx.tab_bar(data=tabs, default="2")

    # --- SIDEBAR (CONTRÔLES TÉCNICOS) ---
    with st.sidebar:
        # Lista Curada de Idiomas (Alfabeto Ocidental)
        idiomas = [
            "pt", "en", "es", "fr", "it", "de", "nl", "af", "sq", "an", 
            "ast", "az", "eu", "bs", "br", "ca", "co", "hr", "cs", "da", 
            "et", "fo", "fi", "fy", "gl", "gd", "gv", "is", "id", "ia", 
            "ga", "la", "lb", "ms", "mg", "mt", "mi", "no", "oc", "pl", 
            "pt-br", "ro", "rm", "se", "sk", "sl", "so", "sw", "sv", "tk", 
            "vi", "wa", "cy", "zu"
        ]
        
        st.session_state.lang = st.selectbox(
            "Idioma", 
            idiomas, 
            index=idiomas.index(st.session_state.lang) if st.session_state.lang in idiomas else 0
        )
        
        # Alinhamento Horizontal: Arte e Voz
        col_tec1, col_tec2 = st.columns(2)
        with col_tec1:
            st.session_state.draw = st.checkbox("Arte", value=True)
        with col_tec2:
            st.session_state.talk = st.checkbox("Voz", value=False)
        
        st.divider()
        
        menu_map = {
            "1":"MINI", "2":"YPOEMAS", "3":"EUREKA", 
            "4":"OFF-MACH", "5":"BOOKS", "6":"COMMENTS", "7":"ABOUT"
        }
        tag = menu_map.get(chosen_id, "YPOEMAS")
        
        # Imagem e Info
        img_name = f"img_{tag.lower()}.jpg"
        if os.path.exists(img_name):
            st.image(img_name)
        
        info_content = load_sidebar_info(tag)
        if info_content:
            st.info(info_content)
        
        st.divider()
        st.caption("yPoemas - a Machina de fazer Poesia © 2026")

    # --- PALCO CENTRAL: INTERAÇÃO COM O MOTOR (lay_2_ypo) ---
    
    container_motor = st.container()

    with container_motor:
        if chosen_id == "3": # EUREKA
            st.session_state.eureka_word = st.text_input(
                "Busca no Léxico (radical/sufixo):", 
                st.session_state.eureka_word
            )
            if st.button("Acionar Engenharia Eureka"):
                gera_poema(st.session_state.tema, st.session_state.eureka_word)
                
        elif chosen_id == "2": # YPOEMAS
            if st.button("Gerar Novo yPoema"):
                gera_poema(st.session_state.tema, "")
                
        elif chosen_id == "4": # OFF-MACH
            if st.button("Aceder aos Arquivos Off-Mach"):
                gera_poema("off-mach", "")

        elif chosen_id == "1": # MINI
            if st.button("Gerar Mini"):
                gera_poema("mini", "")

        elif chosen_id == "7": # ABOUT
            about_text = load_sidebar_info("ABOUT")
            if about_text:
                st.markdown(about_text)

        else:
            st.write(f"Interface {tag} operacional. Aguardando comando.")

if __name__ == "__main__":
    main()
