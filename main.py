import streamlit as st
import extra_streamlit_components as stx
import random
import os
from PIL import Image

# --- âncora: ypoemas_changes (Protocolo Blindado) ---
PATH_DATA = r"data"
PATH_MD = r"md_files"
PATH_BASE = r"base"
PATH_OFF = r"off-maquina"
PATH_LOGO = "image_0.png" 

def load_logo(width=None):
    if os.path.exists(PATH_LOGO):
        img = Image.open(PATH_LOGO)
        if width:
            w_percent = (width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((width, h_size), Image.Resampling.LANCZOS)
        return img
    return None

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

# 2. Refatorado: Tema, não verso. 3. Retorno "descontinuado"
def get_itimo_ypo(tema, seed=None): 
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

def render_display(texto, tema):
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# --- COCKPIT DO LEITOR ---
def page_mini():
    temas = get_rol("temas_mini")
    if not temas: return
    if 'idx_m' not in st.session_state: st.session_state.idx_m = 0
    c = st.columns([1,1,2,1,1])
    if c[0].button("✚", key="m1"): st.rerun() 
    if c[1].button("◀", key="m2"): st.session_state.idx_m -= 1
    if c[2].button("✻", key="m3"): st.session_state.idx_m = random.randrange(len(temas))
    if c[3].button("▶", key="m4"): st.session_state.idx_m += 1
    st.session_state.idx_m %= len(temas)
    t = temas[st.session_state.idx_m]
    render_display(get_itimo_ypo(t), t)

def page_ypoemas():
    livro = st.session_state.get('current_book', 'poemas')
    temas = get_rol(livro)
    if not temas: return
    key = f"idx_{livro}"
    if key not in st.session_state: st.session_state[key] = 0
    c = st.columns([1,1,2,1,1])
    if c[0].button("✚", key="y1"): st.rerun() 
    if c[1].button("◀", key="y2"): st.session_state[key] -= 1
    if c[2].button("✻", key="y3"): st.session_state[key] = random.randrange(len(temas))
    if c[3].button("▶", key="y4"): st.session_state[key] += 1
    st.session_state[key] %= len(temas)
    t = temas[st.session_state[key]]
    render_display(get_itimo_ypo(t), t)

def page_eureka():
    st.subheader("🔍 Eureka")
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
            sel = st.selectbox(f"Encontrados: {len(hits)}", range(len(hits)), format_func=lambda i: f"{hits[i]['v']} -> {hits[i]['t']}")
            h = hits[sel]
            txt = get_itimo_ypo(h['t'], h['s'])
            render_display(txt.replace(query, f" « {query} » "), h['t'])

def page_off():
    st.subheader("🌑 Off-Machina")
    livros = [f.replace(".txt", "") for f in os.listdir(PATH_OFF) if f.endswith(".txt")] if os.path.exists(PATH_OFF) else []
    if livros:
        sel = st.selectbox("Obra:", livros)
        c1, c2 = st.columns([1, 2])
        capa = os.path.join(PATH_OFF, f"{sel}.jpg")
        if os.path.exists(capa): c1.image(capa, width=200)
        with open(os.path.join(PATH_OFF, f"{sel}.txt"), "r", encoding="utf-8") as f:
            c2.text_area("Texto", f.read(), height=450)

def page_books():
    st.subheader("📚 Bibliotecas")
    rois = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
    if rois:
        st.session_state.current_book = st.radio("Acervo:", rois, index=rois.index(st.session_state.current_book) if st.session_state.current_book in rois else 0)

def page_under_construction(title):
    st.subheader(f"🛠️ {title}")
    st.info("Página em desenvolvimento (Under Construction).")
    logo = load_logo(width=200)
    if logo: st.image(logo)

# 1. Páginas Reais Comments e About
def page_comments():
    st.subheader("💬 Comment's")
    conteudo = get_md("INFO_COMMENTS.md")
    if conteudo: st.markdown(conteudo)
    else: st.write("Deixe seu comentário sobre a Machina...")

def page_about():
    st.subheader("ℹ️ About")
    logo = load_logo(width=120)
    if logo: st.image(logo)
    conteudo = get_md("INFO_ABOUT.md")
    if conteudo: st.markdown(conteudo)
    else: st.info("yPoemas: Uma máquina de fazer poesia. Criada por quem entende que o acaso é uma ferramenta de precisão.")

# --- MAIN ---
def main():
    if 'current_book' not in st.session_state: st.session_state.current_book = "poemas"
    try: st.set_page_config(layout="wide", page_title="yPoemas", page_icon=PATH_LOGO)
    except: pass

    # Barra Lateral: Cockpit e Idiomas
    with st.sidebar:
        logo = load_logo(width=180)
        if logo: st.image(logo)
        
        st.markdown("### 🌍 Idiomas")
        c_lang = st.columns(5)
        for i, l in enumerate(["PT", "ES", "IT", "FR", "EN"]):
            if c_lang[i].button(l): st.toast(f"Idioma: {l}")
        
        st.markdown("---")
        st.info(get_md("INFO_YPOEMAS.md"))
        if st.button("🔄 Reiniciar Machina"): st.rerun()

    # Tab Bar Expandida
    tab = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="talk", description=""),
        stx.TabBarItemData(id="6", title="arts", description=""),
        stx.TabBarItemData(id="7", title="vídeo", description=""),
        stx.TabBarItemData(id="8", title="books", description=""),
        stx.TabBarItemData(id="9", title="comments", description=""),
        stx.TabBarItemData(id="10", title="about", description=""),
    ], default="2")

    pages = {
        "1": page_mini, "2": page_ypoemas, "3": page_eureka, "4": page_off,
        "5": lambda: page_under_construction("Talk"),
        "6": lambda: page_under_construction("Arts"),
        "7": lambda: page_under_construction("Vídeo"),
        "8": page_books, "9": page_comments, "10": page_about
    }

    if tab in pages: pages[tab]()

if __name__ == "__main__":
    main()
