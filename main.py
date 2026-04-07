import streamlit as st
import extra_streamlit_components as stx
import random
import os

# --- CONFIGURAÇÃO DE CAMINHOS ---
PATH_DATA = r"data"
PATH_MD = r"md_files"
PATH_BASE = r"base"
PATH_OFF = r"off-maquina"
PATH_LOGO = "image_0.png"

# --- AUXILIARES DE INTERFACE ---
def render_page_header(page_name):
    """Busca a arte da página e o texto informativo correspondente."""
    col1, col2 = st.columns([1, 3])
    
    # Arte da Página (ex: md_files/mini.jpg)
    img_path = os.path.join(PATH_MD, f"{page_name}.jpg")
    if os.path.exists(img_path):
        col1.image(img_path, use_container_width=True)
    
    # Texto Informativo (ex: md_files/INFO_MINI.md)
    info_path = os.path.join(PATH_MD, f"INFO_{page_name.upper()}.md")
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            col2.markdown(f.read())
    else:
        col2.subheader(f"Página: {page_name.capitalize()}")

def get_itimo_ypo(tema, seed=None):
    path = os.path.join(PATH_DATA, f"{tema}.ypo")
    if not os.path.exists(path): return f"{tema}.ypo descontinuado."
    
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

# --- NAVEGADOR DE TEXTOS PADRONIZADO (BOTÃO ✚) ---
def text_navigator(temas, key_prefix):
    if not temas: return
    idx_key = f"idx_{key_prefix}"
    if idx_key not in st.session_state: st.session_state[idx_key] = 0
    
    c = st.columns([1,1,2,1,1])
    if c[0].button("✚", key=f"btn_plus_{key_prefix}"): st.rerun()
    if c[1].button("◀", key=f"btn_prev_{key_prefix}"): st.session_state[idx_key] -= 1
    if c[2].button("✻", key=f"btn_rand_{key_prefix}"): st.session_state[idx_key] = random.randrange(len(temas))
    if c[3].button("▶", key=f"btn_next_{key_prefix}"): st.session_state[idx_key] += 1
    
    st.session_state[idx_key] %= len(temas)
    tema_atual = temas[st.session_state[idx_key]]
    
    st.markdown("---")
    st.markdown(f"### {tema_atual.upper()}")
    st.markdown(f"#### {get_itimo_ypo(tema_atual)}")
    st.markdown("---")

# --- PÁGINAS ---
def page_mini():
    render_page_header("mini")
    from main_utils import get_rol # Exemplo de import do Backup
    text_navigator(get_rol("temas_mini"), "mini")

def page_ypoemas():
    render_page_header("ypoemas")
    livro = st.session_state.get('current_book', 'poemas')
    from main_utils import get_rol
    text_navigator(get_rol(livro), f"ypo_{livro}")

# --- MAIN / SIDEBAR ---
def main():
    st.set_page_config(layout="wide", page_title="yPoemas", page_icon=PATH_LOGO)

    # 1. SIDEBAR RECOLHIDA COM DROPDOWN DE IDIOMAS
    with st.sidebar:
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, width=150)
        
        st.selectbox("🌍 Idioma / Language", ["Português", "Español", "Italiano", "Français", "English"], key="lang_sel")
        
        st.markdown("---")
        if st.button("🔄 Reiniciar Machina"):
            for key in st.session_state.keys(): del st.session_state[key]
            st.rerun()

    tab_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="mini", title="mini", description=""),
        stx.TabBarItemData(id="ypoemas", title="yPoemas", description=""),
        stx.TabBarItemData(id="eureka", title="eureka", description=""),
        stx.TabBarItemData(id="books", title="books", description=""),
    ], default="ypoemas")

    if tab_id == "mini": page_mini()
    elif tab_id == "ypoemas": page_ypoemas()
    # ... demais elifs seguindo o mesmo padrão de render_page_header

if __name__ == "__main__":
    main()
