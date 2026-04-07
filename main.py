import streamlit as st
import extra_streamlit_components as stx
import random
import os

# --- CONFIGURAÇÃO DE CAMINHOS (ypoemas_changes) ---
PATH_DATA = r"data"
PATH_MD = r"md_files"
PATH_BASE = r"base"
PATH_OFF = r"off-maquina"
PATH_LOGO = "image_0.png"

# --- MOTOR DE DADOS ---
def get_rol(book_name):
    """Recupera a lista de temas do acervo selecionado."""
    target = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, target)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return []

def get_itimo_ypo(tema, seed=None):
    """Extrai o ítimo/texto da 7ª coluna do arquivo .ypo."""
    path = os.path.join(PATH_DATA, f"{tema}.ypo")
    if not os.path.exists(path): 
        return f"{tema}.ypo descontinuado."
    
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        linhas = [l.strip() for l in f if l.startswith("|")]
        if seed:
            target = f"{tema}_{seed}"
            for l in linhas:
                p = l.split("|")
                if len(p) >= 4 and p[3].strip() == target:
                    res = p[7].strip()
                    return random.choice(res.split("|")) if "|" in res else res
        
        pool = []
        for l in linhas:
            p = l.split("|")
            if len(p) >= 8:
                txt = p[7].strip()
                if txt and txt != "?":
                    if "|" in txt: pool.extend([v.strip() for v in txt.split("|")])
                    else: pool.append(txt)
        return random.choice(pool) if pool else "..."

# --- INTERFACE E REFORÇO VISUAL ---
def render_page_header(page_id):
    """Muda a arte e o texto informativo conforme a página selecionada."""
    col1, col2 = st.columns([1, 2])
    
    # Arte da página
    img_path = os.path.join(PATH_MD, f"{page_id}.jpg")
    if os.path.exists(img_path):
        col1.image(img_path, use_container_width=True)
    
    # Texto informativo
    info_path = os.path.join(PATH_MD, f"INFO_{page_id.upper()}.md")
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            col2.markdown(f.read())
    else:
        col2.subheader(f"Explorando {page_id.capitalize()}")

def text_navigator(temas, key_prefix):
    """Navegador universal com o botão ✚."""
    if not temas: return
    idx_key = f"idx_{key_prefix}"
    if idx_key not in st.session_state: st.session_state[idx_key] = 0
    
    c = st.columns([1,1,2,1,1])
    if c[0].button("✚", key=f"btn_p_{key_prefix}"): st.rerun()
    if c[1].button("◀", key=f"btn_l_{key_prefix}"): st.session_state[idx_key] -= 1
    if c[2].button("✻", key=f"btn_r_{key_prefix}"): st.session_state[idx_key] = random.randrange(len(temas))
    if c[3].button("▶", key=f"btn_n_{key_prefix}"): st.session_state[idx_key] += 1
    
    st.session_state[idx_key] %= len(temas)
    t = temas[st.session_state[idx_key]]
    
    st.markdown("---")
    st.markdown(f"### {t.upper()}")
    st.markdown(f"#### {get_itimo_ypo(t)}")
    st.markdown("---")

# --- PÁGINAS ---
def page_mini():
    render_page_header("mini")
    text_navigator(get_rol("temas_mini"), "mini")

def page_ypoemas():
    render_page_header("ypoemas")
    livro = st.session_state.get('current_book', 'poemas')
    text_navigator(get_rol(livro), f"ypo_{livro}")

# --- MAIN ---
def main():
    # Estética: Sidebar fixa em 300px
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
        </style>
    """, unsafe_allow_html=True)

    if 'current_book' not in st.session_state: st.session_state.current_book = "poemas"

    try: st.set_page_config(layout="wide", page_title="yPoemas", page_icon=PATH_LOGO)
    except: pass

    with st.sidebar:
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, width=150)
        
        # Dropdown com os 6 idiomas ativos
        st.selectbox("🌍 Idioma", ["PT", "ES", "IT", "FR", "EN", "DE"], key="lang_sel")
        st.markdown("---")

    # Cockpit: Tab Bar
    tab_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="mini", title="mini", description=""),
        stx.TabBarItemData(id="ypoemas", title="yPoemas", description=""),
        stx.TabBarItemData(id="eureka", title="eureka", description=""),
        stx.TabBarItemData(id="off", title="off-machina", description=""),
        stx.TabBarItemData(id="talk", title="talk", description=""),
        stx.TabBarItemData(id="arts", title="arts", description=""),
        stx.TabBarItemData(id="video", title="video", description=""),
        stx.TabBarItemData(id="books", title="books", description=""),
        stx.TabBarItemData(id="comments", title="comments", description=""),
        stx.TabBarItemData(id="about", title="about", description=""),
    ], default="ypoemas")

    # Direcionamento de fluxo
    if tab_id == "mini": page_mini()
    elif tab_id == "ypoemas": page_ypoemas()
    elif tab_id in ["eureka", "off", "talk", "arts", "video", "books", "comments", "about"]:
        render_page_header(tab_id)
        if tab_id == "books":
            rois = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
            if rois:
                st.session_state.current_book = st.radio("Acervo:", rois, index=rois.index(st.session_state.current_book) if st.session_state.current_book in rois else 0)

if __name__ == "__main__":
    main()
