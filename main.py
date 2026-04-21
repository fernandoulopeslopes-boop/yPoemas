import os
import sys
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

# CSS CUSTOMIZADO (Temperatura Zero)
st.markdown(
    """
    <style>
    /* Sidebar fixa em 300px */
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 300px;
        max-width: 300px;
    }
    /* Tipografia de Máquina: Courier New */
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 15px;
    }
    /* Estilização de Botões */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3.2em;
        font-weight: 600;
        border: 1px solid #d1d1d1;
        background-color: #fcfcfc;
    }
    /* Balanceamento de colunas de checkbox na sidebar */
    [data-testid="stVerticalBlock"] > div:has(div.stCheckbox) {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- FUNÇÕES DE SUPORTE LOCAIS ---
def load_sidebar_info(tag):
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
        # Dicionário de Idiomas Completo (Alfabeto Ocidental)
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
        
        lista_siglas = list(idiomas_dict.keys())
        st.session_state.lang = st.selectbox(
            "Idioma", 
            lista_siglas, 
            index=lista_siglas.index(st.session_state.lang) if st.session_state.lang in lista_siglas else 0,
            format_func=lambda x: f"{x} - {idiomas_dict[x]}"
        )
        
        # Alinhamento Horizontal Balanceado: Arte e Voz
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
                
        elif chosen_id == "1": # MINI
            if st.button("Gerar Mini"):
                gera_poema("mini", "")

        elif chosen_id == "4": # OFF-MACH
            if st.button("Aceder aos Arquivos Off-Mach"):
                gera_poema("off-mach", "")

        elif chosen_id == "5": # BOOKS
            if st.button("Abrir Livros"):
                gera_poema("books", "")

        elif chosen_id == "6": # COMMENTS
            # Habilita ocupação do palco para comentários
            st.markdown(load_sidebar_info("COMMENTS"))
            if st.button("Ver Comentários"):
                gera_poema("comments", "")

        elif chosen_id == "7": # ABOUT
            # Habilita ocupação do palco para about
            about_text = load_sidebar_info("ABOUT")
            if about_text:
                st.markdown(about_text)
            if st.button("Info do Sistema"):
                gera_poema("about", "")

        else:
            st.write(f"Interface {tag} operacional.")

if __name__ == "__main__":
    main()
