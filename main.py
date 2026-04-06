import streamlit as st
import extra_streamlit_components as stx
import random
import os

# --- DIRETRIZES CONSOLIDADAS (ypoemas_changes) ---
PATH_DATA = r"data"          # Conteúdo .ypo
PATH_MD = r"md_files"        # Manuais e Artes
PATH_BASE = r"base"          # léxico e rol_*.txt
PATH_OFF = r"off-maquina"    # Acervo estático

def get_md(file_name):
    path = os.path.join(PATH_MD, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""

def get_rol(book_name):
    target = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, target)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return []

def get_verso_ypo(tema, seed=None):
    """Motor de Ítimos: extrai a 7ª coluna com suporte a variantes."""
    path = os.path.join(PATH_DATA, f"{tema}.ypo")
    if not os.path.exists(path): return f"Ítimo {tema} ausente."
    
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

def render_display(texto, tema):
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# --- PÁGINAS ---
def page_mini():
    temas = get_rol("temas_mini")
    if not temas: return
    if 'idx_m' not in st.session_state: st.session_state.idx_m = 0
    c = st.columns([1,1,2,1,1])
    if c[0].button("➕", key="m1"): st.rerun()
    if c[1].button("◀", key="m2"): st.session_state.idx_m -= 1
    if c[2].button("✻", key="m3"): st.session_state.idx_m = random.randrange(len(temas))
    if c[3].button("▶", key="m4"): st.session_state.idx_m += 1
    st.session_state.idx_m %= len(temas)
    t = temas[st.session_state.idx_m]
    render_display(get_verso_ypo(t), t)

def page_ypoemas():
    livro = st.session_state.get('current_book', 'poemas')
    temas = get_rol(livro)
    if not temas: return
    key = f"idx_{livro}"
    if key not in st.session_state: st.session_state[key] = 0
    c = st.columns([1,1,2,1,1])
    if c[0].button("➕", key="y1"): st.rerun()
    if c[1].button("◀", key="y2"): st.session_state[key] -= 1
    if c[2].button("✻", key="y3"): st.session_state[key] = random.randrange(len(temas))
    if c[3].button("▶", key="y4"): st.session_state[key] += 1
    st.session_state[key] %= len(temas)
    t = temas[st.session_state[key]]
    render_display(get_verso_ypo(t), t)

def page_eureka():
    query = st.text_input("Verbete:").strip().lower()
    path = os.path.join(PATH_BASE, "lexico.txt")
    if len(query) >= 3 and os.path.exists(path):
        hits = []
        with open(path, "r", encoding="utf-8") as f:
            for l in f:
                if ":" in l and query in l.lower():
                    p = l.split(":")
                    end = p[1].strip()
                    if "_" in end:
                        t, s = end.split("_")
                        hits.append({"v": p[0].strip(), "t": t, "s": s})
        if hits:
            sel = st.selectbox(f"Encontrados: {len(hits)}", range(len(hits)), 
                               format_func=lambda i: f"{hits[i]['v']} em {hits[i]['t']}")
            h = hits[sel]
            txt = get_verso_ypo(h['t'], h['s'])
            render_display(txt.replace(query, f" « {query} » "), h['t'])

def page_off():
    livros = [f.replace(".txt", "") for f in os.listdir(PATH_OFF) if f.endswith(".txt")] if os.path.exists(PATH_OFF) else []
    if livros:
        sel = st.selectbox("Obra:", livros)
        c1, c2 = st.columns([1, 2])
        capa = os.path.join(PATH_OFF, f"{sel}.jpg")
        if os.path.exists(capa): c1.image(capa, width=200)
        with open(os.path.join(PATH_OFF, f"{sel}.txt"), "r", encoding="utf-8") as f:
            c2.text_area("Texto", f.read(), height=450)

def page_books():
    rois = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
    if rois:
        st.session_state.current_book = st.radio("Acervo:", rois, 
                                                index=rois.index(st.session_state.current_book) if st.session_state.current_book in rois else 0)

def page_comments(): st.markdown(get_md("INFO_COMMENTS.md"))
def page_about(): st.markdown(get_md("INFO_ABOUT.md"))

# --- MAIN ---
def main():
    if 'current_book' not in st.session_state: st.session_state.current_book = "poemas"
    try: st.set_page_config(layout="wide", page_title="yPoemas")
    except: pass

    tab = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="comments", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    pages = {"1": page_mini, "2": page_ypoemas, "3": page_eureka, "4": page_off, "5": page_books, "6": page_comments, "7": page_about}

    with st.sidebar:
        st.info(get_md("INFO_YPOEMAS.md"))
        if st.button("🔄 Reiniciar"): st.rerun()

    if tab in pages: pages[tab]()

if __name__ == "__main__":
    main()
