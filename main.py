import streamlit as st
import extra_streamlit_components as stx
import random
import os

# --- ARQUITETURA DE DIRETÓRIOS ---
PATH_DATA = r"data"
PATH_MD = r"md_files"
PATH_BASE = r"base"
PATH_OFF = r"off-maquina"

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

# --- MOTOR DE ÍTIMOS (.YPO) ---
def get_verso_ypo(tema, seed=None):
    path = os.path.join(PATH_DATA, f"{tema}.ypo")
    if not os.path.exists(path):
        return f"Erro: {tema}.ypo ausente."
    
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        linhas = [l.strip() for l in f if l.startswith("|")]
        
        if seed:
            target_id = f"{tema}_{seed}"
            for l in linhas:
                p = l.split("|")
                if len(p) >= 4 and p[3].strip() == target_id:
                    return p[7].strip() if len(p) >= 8 else ""

        pool = []
        for l in linhas:
            p = l.split("|")
            if len(p) >= 8:
                txt = p[7].strip()
                if txt and txt != "?": pool.append(txt)
        return random.choice(pool) if pool else "Silêncio."

def render_display(texto, tema):
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# --- PÁGINAS ---
def page_eureka():
    st.subheader("🔍 Busca Eureka")
    query = st.text_input("Verbete:").strip().lower()
    path_lexico = os.path.join(PATH_BASE, "lexico.txt")
    
    if len(query) >= 3 and os.path.exists(path_lexico):
        hits = []
        with open(path_lexico, "r", encoding="utf-8", errors="ignore") as f:
            for linha in f:
                if ":" in linha and query in linha.lower():
                    partes = linha.split(":")
                    end = partes[1].strip()
                    if "_" in end:
                        t, s = end.split("_")
                        hits.append({"v": partes[0].strip(), "t": t, "s": s})
        
        if hits:
            sel = st.selectbox(f"Encontrados: {len(hits)}", range(len(hits)),
                               format_func=lambda i: f"{hits[i]['v']} -> {hits[i]['t']}")
            h = hits[sel]
            txt = get_verso_ypo(h['t'], h['s'])
            render_display(txt.replace(query, f" « {query} » "), h['t'])

def page_ypoemas():
    livro = st.session_state.get('current_book', 'poemas')
    temas = get_rol(livro)
    if not temas: return
    if 'idx_y' not in st.session_state: st.session_state.idx_y = 0
    
    c = st.columns([1,1,2,1,1])
    if c[0].button("➕", key="y1"): st.rerun()
    if c[1].button("◀", key="y2"): st.session_state.idx_y -= 1
    if c[2].button("✻", key="y3"): st.session_state.idx_y = random.randrange(len(temas))
    if c[3].button("▶", key="y4"): st.session_state.idx_y += 1
    
    st.session_state.idx_y %= len(temas)
    t = temas[st.session_state.idx_y]
    render_display(get_verso_ypo(t), t)

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

def page_off_machina():
    livros = [f.replace(".txt", "") for f in os.listdir(PATH_OFF) if f.endswith(".txt")]
    if livros:
        sel = st.selectbox("Obra:", livros)
        c1, c2 = st.columns([1, 2])
        capa = os.path.join(PATH_OFF, f"{sel}.jpg")
        if os.path.exists(capa): c1.image(capa, width=200)
        with open(os.path.join(PATH_OFF, f"{sel}.txt"), "r", encoding="utf-8") as f:
            c2.text_area("Texto", f.read(), height=400)

def page_books():
    rois = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
    st.session_state.current_book = st.radio("Acervo:", rois)

# --- ORQUESTRAÇÃO ---
def main():
    if 'current_book' not in st.session_state: st.session_state.current_book = "poemas"
    try: st.set_page_config(layout="wide", page_title="yPoemas")
    except: pass

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
    ], default="2")

    pages = {"1": page_mini, "2": page_ypoemas, "3": page_eureka, "4": page_off_machina, "5": page_books}
    
    with st.sidebar:
        st.info(get_md("INFO_YPOEMAS.md"))
        if st.button("Limpar Cache"): st.cache_data.clear()

    if chosen_id in pages: pages[chosen_id]()

if __name__ == "__main__":
    main()
