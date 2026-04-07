import streamlit as st
import extra_streamlit_components as stx
import random
import os

# --- DIRETRIZES E CAMINHOS ---
PATH_DATA = r"data"
PATH_MD = r"md_files"
PATH_BASE = r"base"
PATH_LOGO = "image_0.png"
BULB_ICON = "💡"

# --- LINHA ZERO: IDIOMAS ABC ---
IDIOMAS_ABC = ["PT", "ES", "IT", "FR", "DE", "EN", "CA", "GL", "RO"]

def get_rol(book_name):
    target = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, target)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return []

def get_itimo_ypo(tema):
    path = os.path.join(PATH_DATA, f"{tema}.ypo")
    if not os.path.exists(path): return f"{tema}.ypo descontinuado."
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        linhas = [l.strip() for l in f if l.startswith("|")]
        pool = []
        for l in linhas:
            p = l.split("|")
            if len(p) >= 8:
                txt = p[7].strip()
                if txt and txt != "?":
                    if "|" in txt: pool.extend([v.strip() for v in txt.split("|")])
                    else: pool.append(txt)
        return random.choice(pool) if pool else "..."

def main():
    st.markdown("<style>[data-testid='stSidebar'] { width: 300px !important; min-width: 300px !important; }</style>", unsafe_allow_html=True)
    
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'current_book' not in st.session_state: st.session_state.current_book = "poemas"
    
    tabs_list = ["mini", "ypoemas", "eureka", "off", "books", "comments", "about"]
    active_tab = tabs_list[st.session_state.current_tab_idx]

    try: st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: pass

    # --- HEADER: LINHA ZERO ---
    c_zero = st.columns([8, 2])
    with c_zero[1]:
        st.selectbox("Idiomas ABC", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- SIDEBAR: IDENTIDADE + INFO ---
    with st.sidebar:
        # Bloco I: Identidade
        col_s1, col_s2 = st.columns([1, 3])
        col_s1.markdown(f"## {BULB_ICON}")
        if os.path.exists(PATH_LOGO):
            col_s2.image(PATH_LOGO, width=120)
        
        st.markdown("---")
        
        # Bloco II: INFO (Texto explicativo da página selecionada)
        info_path = os.path.join(PATH_MD, f"INFO_{active_tab.upper()}.md")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        
        st.markdown("<br>" * 8, unsafe_allow_html=True)
        st.markdown("---")
        
        # Bloco III: Navegação CR
        st.write("🕹️ Navegação")
        cn1, cn2 = st.columns(2)
        if cn1.button("« Anterior"): 
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(tabs_list)
            st.rerun()
        if cn2.button("Próxima »"): 
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(tabs_list)
            st.rerun()

    # --- PALCO CENTRAL ---
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    st.session_state.current_tab_idx = tabs_list.index(tab_id)

    # Arte da Página
    img_path = os.path.join(PATH_MD, f"{tab_id}.jpg")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

    # Conteúdo Específico
    if tab_id == "mini":
        temas = get_rol("temas_mini")
        render_navigator(temas, "mini")
    
    elif tab_id == "ypoemas":
        # Seletor de Acervo no Palco (Abaixo da Arte)
        rois = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
        if rois:
            st.session_state.current_book = st.selectbox("Acervo Ativo:", rois, 
                                                        index=rois.index(st.session_state.current_book) if st.session_state.current_book in rois else 0)
        temas = get_rol(st.session_state.current_book)
        render_navigator(temas, "ypo")

def render_navigator(temas, key_prefix):
    """Navegador Padrão: ( ✚    ◀    ✻     ▶   ? )"""
    if not temas: return
    idx_key = f"idx_{key_prefix}"
    if idx_key not in st.session_state: st.session_state[idx_key] = 0
    
    st.markdown("<br>", unsafe_allow_html=True)
    c = st.columns([1, 1, 1, 1, 1])
    
    # Ordem rigorosa: ✚ ◀ ✻ ▶ ?
    if c[0].button("✚", key=f"btn_add_{key_prefix}"): st.rerun()
    if c[1].button("◀", key=f"btn_prev_{key_prefix}"): st.session_state[idx_key] -= 1
    if c[2].button("✻", key=f"btn_rnd_{key_prefix}"): st.session_state[idx_key] = random.randrange(len(temas))
    if c[3].button("▶", key=f"btn_next_{key_prefix}"): st.session_state[idx_key] += 1
    if c[4].button("?", key=f"btn_hlp_{key_prefix}"): st.info("Contexto da Navegação Ativo")
    
    st.session_state[idx_key] %= len(temas)
    t = temas[st.session_state[idx_key]]
    
    st.markdown(f"<h3 style='text-align: center; color: #555;'>{t.upper()}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{get_itimo_ypo(t)}</h2>", unsafe_allow_html=True)
    st.markdown("---")

if __name__ == "__main__":
    main()
    
