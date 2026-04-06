import streamlit as st
import extra_streamlit_components as stx
import random
import os

# ==========================================
# 1. MOTOR DE DADOS
# ==========================================

PATH_TEMAS = "temas"

def load_temas(book_name="todos os temas"):
    try:
        if not os.path.exists(PATH_TEMAS): return []
        arquivos = [f.replace(".txt", "") for f in os.listdir(PATH_TEMAS) if f.endswith(".txt")]
        if book_name != "todos os temas":
            return sorted([f for f in arquivos if book_name.lower() in f.lower()])
        return sorted(arquivos)
    except: return []

def load_poema(tema):
    try:
        file_path = os.path.join(PATH_TEMAS, f"{tema}.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f if l.strip()]
            return random.choice(linhas) if linhas else ""
    except: return ""

def load_md_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def render_display(texto, tema):
    st.session_state.last_poem = {"texto": texto, "tema": tema}
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# ==========================================
# 2. INTERFACE (NAVEGAÇÃO: + < * > ?)
# ==========================================

def draw_navigation_bar(temas, label_info):
    if not temas: return None
    maxy = len(temas)
    if 'take' not in st.session_state: st.session_state.take = 0
    
    cols = st.columns([1, 1, 2, 1, 1])
    
    if cols[0].button("➕", key=f"p_{label_info}"): st.session_state.take += 1
    if cols[1].button("◀", key=f"l_{label_info}"): st.session_state.take -= 1
    if cols[2].button("✻", key=f"s_{label_info}"): st.session_state.take = random.randrange(maxy)
    if cols[3].button("▶", key=f"r_{label_info}"): st.session_state.take += 1
    if cols[4].button("❓", key=f"i_{label_info}"): 
        st.toast(f"{label_info}: {st.session_state.take % maxy + 1}/{maxy}")

    st.session_state.take %= maxy
    return temas[st.session_state.take]

# ==========================================
# 3. PÁGINAS
# ==========================================

def page_mini():
    temas = load_temas()
    tema = draw_navigation_bar(temas, "Mini")
    if tema: render_display(load_poema(tema), tema)

def page_ypoemas():
    livro = st.session_state.get('book', 'todos os temas')
    temas = load_temas(livro)
    tema = draw_navigation_bar(temas, f"yPoemas ({livro})")
    if tema: render_display(load_poema(tema), tema)

def page_eureka():
    termo = st.text_input("Busca Eureka:")
    if len(termo) >= 3:
        todos = load_temas()
        for t in todos:
            p = load_poema(t)
            if termo.lower() in p.lower():
                st.write(f"**{t}**: {p}")

def page_off_machina():
    if 'last_poem' in st.session_state:
        render_display(st.session_state.last_poem['texto'], st.session_state.last_poem['tema'])

def page_books():
    opcoes = ["todos os temas", "poemas", "jocosos", "livro vivo"]
    st.session_state.book = st.radio("Livros:", opcoes)

def page_poly():
    st.write("Configurações de Idioma.")

# ==========================================
# 4. EXECUÇÃO
# ==========================================

def main():
    try: st.set_page_config(layout="wide")
    except: pass

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    pages = {
        "1": ("INFO_MINI.md", page_mini),
        "2": ("INFO_YPOEMAS.md", page_ypoemas),
        "3": ("INFO_EUREKA.md", page_eureka),
        "4": ("INFO_OFF-MACHINA.md", page_off_machina),
        "5": ("INFO_BOOKS.md", page_books),
        "6": ("INFO_POLY.md", page_poly),
        "7": ("INFO_ABOUT.md", lambda: st.markdown(load_md_file("INFO_ABOUT.md")))
    }

    if chosen_id in pages:
        info_file, func = pages[chosen_id]
        with st.sidebar:
            if info_file: st.info(load_md_file(info_file))
            st.markdown("---")
            st.info(load_md_file("INFO_BEST.md"))
            st.markdown(load_md_file("INFO_MEDIA.md"))
        
        if callable(func): func()

if __name__ == "__main__":
    main()
    
