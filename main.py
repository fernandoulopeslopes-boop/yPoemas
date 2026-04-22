import os
import sys
import random
import streamlit as st
import extra_streamlit_components as stx

# --- ANCORAGEM E IMPORTAÇÃO ---
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
if dname not in sys.path:
    sys.path.insert(0, dname)

try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("Erro: lay_2_ypo.py não encontrado.")
    st.stop()

# --- CONFIGURAÇÃO ---
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CSS: ESTERILIZAÇÃO E IDENTIDADE ---
st.markdown(
    """
    <style>
    /* Ocultar botão de colapsar (<<) e navegação padrão */
    [data-testid="collapsedControl"], [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Tipografia Courier New 15px */
    html, body, [class*="css"], .stMarkdown, p, div, [data-testid="stSidebar"] * {
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 15px;
    }

    /* Centralização dos controles Arte/Voz na Sidebar */
    [data-testid="stSidebar"] [data-testid="column"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }
    
    /* Ajuste de largura da Sidebar */
    [data-testid="stSidebar"] {
        min-width: 300px;
        max-width: 300px;
    }

    /* Botões de comando */
    .stButton>button {
        width: 100%;
        border-radius: 2px;
        border: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- FUNÇÕES DE APOIO ---
def load_md_file(filename):
    path = os.path.join("md_files", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"Conteúdo de {filename} não localizado."

def get_random_tema():
    path = "rol_todos os temas.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
            return random.choice(temas) if temas else "Poesia"
    return "Poesia"

# --- LÓGICA DE PÁGINAS ---

def page_abouts():
    """Hub de navegação baseado no ypo_seguro.py"""
    abouts_list = [
        "comments", "prefácio", "machina", "off-machina", "outros", 
        "traduttore", "bibliografia", "imagens", "samizdát", 
        "notes", "license", "index"
    ]
    
    options = list(range(len(abouts_list)))
    # Menu de seleção interno do About
    opt_abouts = st.selectbox(
        "↓ sobre",
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    choice = abouts_list[opt_abouts].upper()
    
    # Palco central com sangria lateral
    _, col_central, _ = st.columns([1, 4, 1])
    
    with col_central:
        if choice == "MACHINA":
            # Estrutura sanduíche da Machina
            st.markdown(load_md_file("ABOUT_MACHINA_A.md"))
            st.divider()
            # O yPoema é gerado entre as explicações
            gera_poema(st.session_state.tema, "")
            st.divider()
            st.markdown(load_md_file("ABOUT_MACHINA_D.md"))
        else:
            # Carregamento padrão
            content = load_md_file(f"ABOUT_{choice}.md")
            st.markdown(content)

# --- ESTADO INICIAL ---
if "tema" not in st.session_state: st.session_state.tema = get_random_tema()
if "lang" not in st.session_state: st.session_state.lang = "pt"

# --- MAIN ---
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

    # --- SIDEBAR (Ordem: Seletores -> Info -> Imagem) ---
    with st.sidebar:
        # 1. Seleção de Idioma
        st.session_state.lang = st.selectbox("Idioma", ["pt", "en", "es", "fr", "it", "de"])
        
        # 2. Checkboxes Centralizados
        c1, c2 = st.columns(2)
        with c1: st.checkbox("Arte", value=True, key="draw")
        with c2: st.checkbox("Voz", value=False, key="talk")
        
        st.divider()
        
        # 3. Informação Contextual (INFO_*.md)
        menu_map = {"1":"MINI", "2":"YPOEMAS", "3":"EUREKA", "4":"OFF-MACH", "5":"BOOKS", "6":"COMMENTS", "7":"ABOUT"}
        tag = menu_map.get(chosen_id, "YPOEMAS")
        
        info_path = os.path.join("md_files", f"INFO_{tag}.md")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.info(f.read())
        
        st.divider()

        # 4. Imagem de Rodapé
        img_path = f"img_{tag.lower()}.jpg"
        if os.path.exists(img_path):
            st.image(img_path)

    # --- PALCO CENTRAL ---
    if chosen_id == "7": # ABOUT
        page_abouts()
        
    elif chosen_id == "6": # COMMENTS (Atalho direto)
        _, col, _ = st.columns([1, 4, 1])
        with col: st.markdown(load_md_file("ABOUT_COMMENTS.md"))

    elif chosen_id == "2": # YPOEMAS
        _, col, _ = st.columns([1, 6, 1])
        with col:
            if st.button("Gerar Novo yPoema"):
                gera_poema(st.session_state.tema, "")

    # Adicionar lógica para MINI e EUREKA seguindo o padrão...

if __name__ == "__main__":
    main()
