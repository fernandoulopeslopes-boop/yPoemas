import os
import sys
import random
import streamlit as st
import extra_streamlit_components as stx

# --- ANCORAGEM DE DIRETÓRIO (Protocolo CPC) ---
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

# CSS CUSTOMIZADO (Unificação de Fontes e Balanço de Widgets)
st.markdown(
    """
    <style>
    /* Sidebar 320px Fixa */
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 320px;
        max-width: 320px;
    }
    
    /* UNIFICAÇÃO TOTAL: Sidebar e Palco com a mesma tipografia Courier */
    html, body, [class*="css"], .stMarkdown, p, div, [data-testid="stSidebar"] * {
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 15px;
    }

    /* Estilização de Botões CPC */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3.2em;
        font-weight: 600;
        border: 1px solid #d1d1d1;
        background-color: #fcfcfc;
    }

    /* Ajuste de alinhamento dos Checkboxes na Sidebar */
    [data-testid="stSidebar"] .stCheckbox {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- FUNÇÕES DE SUPORTE (Fidelidade ao ypo_seguro.py) ---
def get_random_tema():
    """Lê o rol oficial: base/rol_todos os temas.txt"""
    path_temas = os.path.join("base", "rol_todos os temas.txt")
    try:
        with open(path_temas, "r", encoding="utf-8") as f:
            temas = [line.strip() for line in f if line.strip()]
            if temas:
                return random.choice(temas)
            else:
                st.error("O arquivo de temas está vazio.")
                st.stop()
    except FileNotFoundError:
        st.error(f"Erro Crítico: Arquivo não localizado em {path_temas}")
        st.stop()

def render_md_page(tag):
    """PAGINAÇÃO FIEL: Ocupação de palco centralizada com sangria [1, 4, 1]"""
    path = os.path.join("md_files", f"INFO_{tag}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        _, col_central, _ = st.columns([1, 4, 1])
        with col_central:
            st.markdown(content)
    else:
        st.warning(f"Arquivo md_files/INFO_{tag}.md não encontrado.")

def load_sidebar_info(tag):
    """Carrega o fragmento informativo para a sidebar."""
    path = os.path.join("md_files", f"INFO_{tag}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- INICIALIZAÇÃO DE ESTADO ---
if "tema" not in st.session_state: 
    st.session_state.tema = get_random_tema()
if "eureka_word" not in st.session_state: 
    st.session_state.eureka_word = ""
if "lang" not in st.session_state: 
    st.session_state.lang = "pt"

# --- NAVEGAÇÃO ---
def main():
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

    # --- SIDEBAR ---
    with st.sidebar:
        idiomas_dict = {
            "pt": "Português", "en": "English", "es": "Español", "fr": "Français", "it": "Italiano",
            "de": "Deutsch", "nl": "Nederlands", "af": "Afrikaans", "sq": "Shqip", "an": "Aragonés",
            "ast": "Asturianu", "az": "Azərbaycanca", "eu": "Euskara", "bs": "Bosanski", "br": "Brezhoneg",
            "ca": "Català", "co": "Corsu", "hr": "Hrvatski", "cs": "Čeština", "da": "Dansk",
            "et": "Eesti", "fo": "Føroyskt", "fi": "Suomi", "fy": "Frysk", "gl": "Galego",
            "gd": "Gàidhlig", "gv": "Gaelg", "is": "Íslenska", "id": "Bahasa Indonesia", "ia": "Interlingua",
            "ga": "Gaeilge", "la": "Latina", "lb": "Lëtzebuergesch", "ms": "Bahasa Melayu", "mg": "Malagasy",
            "mt": "Malti", "mi": "Māori", "no": "Norsk", "oc": "Occitan", "pl": "Polski",
            "pt-br": "Português (Brasil)", "ro": "Română", "rm": "Rumantsch", "se": "Sápmi", "sk": "Slovenčina",
            "sl": "Slovenščina", "so": "Soomaali", "sw": "Kiswahili", "sv": "Svenska", "tk": "Türkmençe",
            "vi": "Tiếng Việt", "wa": "Walon", "cy": "Cymraeg", "zu": "isiZulu"
        }
        
        # CORREÇÃO DO INDEX: Agora passa o inteiro correto
        keys_list = list(idiomas_dict.keys())
        st.session_state.lang = st.selectbox(
            "Idioma", 
            keys_list, 
            index=keys_list.index(st.session_state.lang),
            format_func=lambda x: f"{x} - {idiomas_dict[x]}"
        )
        
        # Colunas Balanceadas para Arte e Voz
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.session_state.draw = st.checkbox("Arte", value=True)
        with col_btn2:
            st.session_state.talk = st.checkbox("Voz", value=False)
        
        st.divider()
        
        menu_map = {"1":"MINI", "2":"YPOEMAS", "3":"EUREKA", "4":"OFF-MACH", "5":"BOOKS", "6":"COMMENTS", "7":"ABOUT"}
        tag = menu_map.get(chosen_id, "YPOEMAS")
        
        # Arte e Info da Sidebar
        img_name = f"img_{tag.lower()}.jpg"
        if os.path.exists(img_name):
            st.image(img_name)
        
        info_side = load_sidebar_info(tag)
        if info_side:
            st.info(info_side)
        
        st.divider()

    # --- PALCO CENTRAL ---
    if chosen_id == "2": # YPOEMAS
        _, col_mid, _ = st.columns([1, 8, 1])
        with col_mid:
            if st.button("Gerar Novo yPoema"):
                gera_poema(st.session_state.tema, "")

    elif chosen_id == "3": # EUREKA
        _, col_mid, _ = st.columns([1, 8, 1])
        with col_mid:
            st.session_state.eureka_word = st.text_input("Busca no Léxico:", st.session_state.eureka_word)
            if st.button("Acionar Engenharia Eureka"):
                gera_poema(st.session_state.tema, st.session_state.eureka_word)
                
    elif chosen_id == "1": # MINI
        _, col_mid, _ = st.columns([1, 8, 1])
        with col_mid:
            if st.button("Gerar Mini"):
                gera_poema(st.session_state.tema, "mini")

    elif chosen_id == "6": # COMMENTS
        render_md_page("COMMENTS")

    elif chosen_id == "7": # ABOUT
        render_md_page("ABOUT")

if __name__ == "__main__":
    main()
