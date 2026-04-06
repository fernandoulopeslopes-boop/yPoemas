import streamlit as st
import extra_streamlit_components as stx
import random
import os

# ==============================================================================
# 1. MOTOR DE BUSCA E DIRETÓRIOS (REVISÃO DE PRECISÃO)
# ==========================================
PATH_DATA = "data"          # Verbetes
PATH_MD = "md_files"        # Manuais e Artes
PATH_BASE = "base"          # Róis (rol_*.txt)
PATH_OFF = "off-maquina"    # Estáticos

def get_md(file_name):
    path = os.path.join(PATH_MD, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return f"⚠️ {file_name} não encontrado."

def get_rol_list(book_name):
    target = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, target)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return []

def get_verso(tema):
    path = os.path.join(PATH_DATA, f"{tema}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            linhas = [l.strip() for l in f if l.strip()]
            return random.choice(linhas) if linhas else ""
    return ""

def render_display(texto, tema):
    st.session_state.last_poem = {"texto": texto, "tema": tema}
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# ==============================================================================
# 2. CONSOLE DE NAVEGAÇÃO (+ < * > ?)
# ==========================================
def navigation_console(lista, label):
    if not lista: return None
    key_idx = f"idx_{label}"
    if key_idx not in st.session_state: st.session_state[key_idx] = 0
    
    max_len = len(lista)
    c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])
    
    if c1.button("➕", key=f"p_{label}"): st.rerun()
    if c2.button("◀", key=f"l_{label}"): st.session_state[key_idx] -= 1
    if c3.button("✻", key=f"s_{label}"): st.session_state[key_idx] = random.randrange(max_len)
    if c4.button("▶", key=f"r_{label}"): st.session_state[key_idx] += 1
    if c5.button("❓", key=f"i_{label}"): st.toast(f"{label}: {st.session_state[key_idx]%max_len+1}/{max_len}")

    st.session_state[key_idx] %= max_len
    return lista[st.session_state[key_idx]]

# ==============================================================================
# 3. PÁGINAS (FOCO EUREKA)
# ==========================================
def page_mini():
    temas = get_rol_list("temas_mini")
    tema = navigation_console(temas, "Mini")
    if tema: render_display(get_verso(tema), tema)

def page_ypoemas():
    livro = st.session_state.get('current_book', 'poemas')
    temas = get_rol_list(livro)
    tema = navigation_console(temas, f"yPoemas_{livro}")
    if tema: render_display(get_verso(tema), tema)

def page_eureka():
    st.subheader("🔍 Busca Eureka")
    # Limpamos o termo de busca para evitar espaços acidentais
    query = st.text_input("Localizar termo nos 45.000 verbetes:").strip()
    
    if len(query) >= 3:
        hits = []
        if not os.path.exists(PATH_DATA):
            st.error(f"Erro: Pasta {PATH_DATA} não localizada.")
            return

        # Busca exaustiva
        for f_name in [a for a in os.listdir(PATH_DATA) if a.endswith(".txt")]:
            t_name = f_name.replace(".txt", "")
            full_path = os.path.join(PATH_DATA, f_name)
            
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                    for line in file:
                        clean_line = line.strip()
                        if query.lower() in clean_line.lower():
                            # Destaque visual « »
                            highlighted = clean_line.replace(query, f" « {query} » ")
                            hits.append({"v": highlighted, "t": t_name})
            except: continue
            
        if hits:
            sel = st.selectbox(f"Fragmentos encontrados: {len(hits)}", range(len(hits)), 
                               format_func=lambda i: f"{hits[i]['v'][:60]}... [{hits[i]['t']}]")
            render_display(hits[sel]['v'], hits[sel]['t'])
        else:
            st.info(f"Nenhum fragmento contendo '{query}' foi encontrado nos arquivos de data/.")

def page_off_machina():
    st.subheader("🌑 Off-Machina")
    livros = [f.replace(".txt", "") for f in os.listdir(PATH_OFF) if f.endswith(".txt")]
    if livros:
        sel = st.selectbox("Obra:", livros)
        c1, c2 = st.columns([1, 2])
        capa = os.path.join(PATH_OFF, f"{sel}.jpg")
        if os.path.exists(capa): c1.image(capa, width=220)
        with open(os.path.join(PATH_OFF, f"{sel}.txt"), "r", encoding="utf-8", errors="ignore") as f:
            c2.text_area("Texto", f.read(), height=450)

def page_books():
    st.subheader("📚 Bibliotecas")
    rois = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
    st.session_state.current_book = st.radio("Livro ativo:", rois)

# ==============================================================================
# 4. MAIN (MANDALA & SIDEBAR)
# ==========================================
def main():
    if 'current_book' not in st.session_state: st.session_state.current_book = "poemas"
    if 'poly_name' not in st.session_state: st.session_state.poly_name = "Català"
    
    try: st.set_page_config(layout="wide", page_title="yPoemas", page_icon="📜")
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

    mapa = {
        "1": ("INFO_MINI.md", page_mini, "ARTE_MINI.jpg"),
        "2": ("INFO_YPOEMAS.md", page_ypoemas, "ARTE_YPOEMAS.jpg"),
        "3": ("INFO_EUREKA.md", page_eureka, "ARTE_EUREKA.jpg"),
        "4": ("INFO_OFF-MACHINA.md", page_off_machina, "ARTE_OFF-MACHINA.jpg"),
        "5": ("INFO_BOOKS.md", page_books, "ARTE_BOOKS.jpg"),
        "6": ("INFO_POLY.md", lambda: st.info("Idiomas na lateral."), "ARTE_POLY.jpg"),
        "7": ("INFO_ABOUT.md", lambda: st.markdown(get_md("INFO_ABOUT.md")), "ARTE_ABOUT.jpg")
    }

    if chosen_id in mapa:
        info_file, func, arte_file = mapa[chosen_id]
        
        with st.sidebar:
            # Arte (md_files/)
            path_arte = os.path.join(PATH_MD, arte_file)
            if os.path.exists(path_arte):
                st.image(path_arte, use_container_width=True)
            
            # Poly
            st.write("🌍 **Idiomas**")
            b = st.columns(6)
            if b[0].button("pt"): st.session_state.lang = "pt"
            if b[1].button("es"): st.session_state.lang = "es"
            if b[2].button("it"): st.session_state.lang = "it"
            if b[3].button("fr"): st.session_state.lang = "fr"
            if b[4].button("en"): st.session_state.lang = "en"
            if b[5].button("⚒️", help=st.session_state.poly_name): st.session_state.lang = "xy"
            
            st.markdown("---")
            st.info(get_md(info_file))
            st.markdown("---")
            st.info(get_md("INFO_BEST.md"))
            st.markdown(get_md("INFO_MEDIA.md"))

        if callable(func): func()

if __name__ == "__main__":
    main()
