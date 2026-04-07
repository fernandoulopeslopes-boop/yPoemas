import streamlit as st
import extra_streamlit_components as stx
import random
import os

# --- ypoemas_changes: Protocolo de Fidelidade ---
PATH_DATA = r"data"
PATH_MD = r"md_files"
PATH_BASE = r"base"
PATH_LOGO = "image_0.png" 

# Ícone solicitado: Lâmpada de bulbo antiga amarela
BULB_ICON = "💡" 

def get_rol(book_name):
    target = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, target)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return []

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

# --- INTERFACE ---
def render_page_header(page_id):
    """Arte e Info centralizados no palco."""
    img_path = os.path.join(PATH_MD, f"{page_id}.jpg")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    
    info_path = os.path.join(PATH_MD, f"INFO_{page_id.upper()}.md")
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            st.markdown(f"<div style='text-align: center; margin-top: 15px;'>{f.read()}</div>", unsafe_allow_html=True)

def text_navigator(temas, key_prefix):
    """Cockpit ✚ para Ítimos."""
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #666;'>{t.upper()}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{get_itimo_ypo(t)}</h2>", unsafe_allow_html=True)

# --- MAIN ---
def main():
    # Estética: Sidebar 300px
    st.markdown("<style>[data-testid='stSidebar'] { width: 300px !important; min-width: 300px !important; }</style>", unsafe_allow_html=True)
    
    tabs_list = ["mini", "ypoemas", "eureka", "off", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'current_book' not in st.session_state: st.session_state.current_book = "poemas"

    try: st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: pass

    # --- SIDEBAR (O Coração da Resposta) ---
    with st.sidebar:
        # Logo e Ícone da Lâmpada (Cereja Visual)
        cols_side = st.columns([1, 4])
        cols_side[0].markdown(f"### {BULB_ICON}")
        if os.path.exists(PATH_LOGO):
            cols_side[1].image(PATH_LOGO, width=120)
        
        st.markdown("---")
        
        # Idiomas (PT, ES, IT, FR, EN, CA)
        st.selectbox("🌍 Idioma", ["PT", "ES", "IT", "FR", "EN", "CA"], key="lang_sel")
        
        st.markdown("---")
        
        # CONTEÚDO DINÂMICO (Popula conforme a página)
        active_tab = tabs_list[st.session_state.current_tab_idx]
        
        if active_tab == "ypoemas":
            st.write("📚 **Acervo Ativo**")
            rois = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
            if rois:
                st.session_state.current_book = st.radio("Mudar Biblioteca:", rois, 
                                                        index=rois.index(st.session_state.current_book) if st.session_state.current_book in rois else 0,
                                                        label_visibility="collapsed")
        
        elif active_tab == "mini":
            st.info("Modo Minimalista: Foco total no Ítimo.")
            
        elif active_tab == "eureka":
            st.write("🔍 **Busca Lexicográfica**")
            st.caption("Refine sua busca no palco central.")

        st.markdown("---")
        
        # Navegação de Páginas (CR)
        st.write("🕹️ Navegação")
        cn1, cn2 = st.columns(2)
        if cn1.button("« Ant"): 
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(tabs_list)
            st.rerun()
        if cn2.button("Próx »"): 
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(tabs_list)
            st.rerun()

    # --- PALCO ---
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    st.session_state.current_tab_idx = tabs_list.index(tab_id)
    render_page_header(tab_id)

    if tab_id == "mini":
        text_navigator(get_rol("temas_mini"), "mini")
    elif tab_id == "ypoemas":
        text_navigator(get_rol(st.session_state.current_book), "ypo")
    elif tab_id == "books":
        st.write("Gerencie seus acervos na sidebar.")

if __name__ == "__main__":
    main()
