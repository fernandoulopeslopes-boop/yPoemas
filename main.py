import streamlit as st
import extra_streamlit_components as stx
import random
import os

# ==============================================================================
# 1. CONSTANTES DE DIRETÓRIO (ESTRUTURA FIXA)
# ==============================================================================
PATH_DATA = "data"          # Arquivos de conteúdo (ex: Pedidos.txt)
PATH_MD = "md_files"        # Manuais e Artes
PATH_BASE = "base"          # lexico.txt e rol_*.txt
PATH_OFF = "off-maquina"    # Livros e capas

def get_md(file_name):
    """Carrega manuais com fallback de erro."""
    path = os.path.join(PATH_MD, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return f"⚠️ {file_name} não localizado."

def get_rol(book_name):
    """Carrega listas de temas (rol_)."""
    target = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, target)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return []

# ==============================================================================
# 2. MOTOR DE RECUPERAÇÃO (O CORAÇÃO DO PROJETO)
# ==============================================================================
def get_verso_by_seed(tema, seed=None):
    """
    Busca o verso exato baseado na seed (ex: 0201 -> linha 2)
    ou um aleatório se a seed for nula.
    """
    path = os.path.join(PATH_DATA, f"{tema}.txt")
    if not os.path.exists(path):
        return f"Arquivo {tema}.txt não encontrado em {PATH_DATA}."
        
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        linhas = [l.strip() for l in f if l.strip()]
        if not linhas: return ""

        if seed and len(seed) >= 2:
            try:
                # O endereço 0201 indica: linha 02.
                # Convertendo para índice zero-based (linha 02 = índice 1)
                idx = int(seed[:2]) - 1
                if 0 <= idx < len(linhas):
                    return linhas[idx]
            except ValueError:
                pass
        
        return random.choice(linhas)

def render_display(texto, tema):
    """Exibição formatada."""
    st.session_state.last_poem = {"texto": texto, "tema": tema}
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# ==============================================================================
# 3. PÁGINAS (EUREKA FIEL AO LÉXICO)
# ==============================================================================
def page_eureka():
    st.subheader("🔍 Busca Eureka")
    query = st.text_input("Verbete:").strip().lower()
    
    path_lexico = os.path.join(PATH_BASE, "lexico.txt")
    if not os.path.exists(path_lexico):
        st.error("Erro: base/lexico.txt não localizado.")
        return

    if len(query) >= 3:
        hits = []
        with open(path_lexico, "r", encoding="utf-8", errors="ignore") as f:
            for linha in f:
                # Estrutura: "amorosos : Pedidos_0201"
                if ":" in linha and query in linha.lower():
                    partes = linha.split(":")
                    verbete = partes[0].strip()
                    # endereco = "Pedidos_0201"
                    endereco = partes[1].strip()
                    
                    if "_" in endereco:
                        tema_alvo, seed = endereco.split("_")
                        hits.append({"v": verbete, "t": tema_alvo, "s": seed})

        if hits:
            # Seleção baseada no verbete e localização
            sel = st.selectbox(f"Encontrados: {len(hits)}", range(len(hits)),
                               format_func=lambda i: f"« {hits[i]['v']} » em {hits[i]['t']} ({hits[i]['s']})")
            
            h = hits[sel]
            txt = get_verso_by_seed(h['t'], h['s'])
            # Destaque do verbete no texto original
            txt_highlight = txt.replace(query, f" « {query} » ")
            render_display(txt_highlight, h['t'])
        else:
            st.info("Nenhuma ocorrência no léxico.")

def page_mini():
    temas = get_rol("temas_mini")
    # Navegação local + < * > ?
    if 'idx_mini' not in st.session_state: st.session_state.idx_mini = 0
    
    c = st.columns([1,1,2,1,1])
    if c[0].button("➕", key="p_m"): st.rerun()
    if c[1].button("◀", key="l_m"): st.session_state.idx_mini -= 1
    if c[2].button("✻", key="s_m"): st.session_state.idx_mini = random.randrange(len(temas))
    if c[3].button("▶", key="r_m"): st.session_state.idx_mini += 1
    
    st.session_state.idx_mini %= len(temas)
    tema = temas[st.session_state.idx_mini]
    render_display(get_verso_by_seed(tema), tema)

def page_ypoemas():
    livro = st.session_state.get('current_book', 'poemas')
    temas = get_rol(livro)
    if 'idx_y' not in st.session_state: st.session_state.idx_y = 0
    
    c = st.columns([1,1,2,1,1])
    if c[0].button("➕", key="p_y"): st.rerun()
    if c[1].button("◀", key="l_y"): st.session_state.idx_y -= 1
    if c[2].button("✻", key="s_y"): st.session_state.idx_y = random.randrange(len(temas))
    if c[3].button("▶", key="r_y"): st.session_state.idx_y += 1
    
    st.session_state.idx_y %= len(temas)
    tema = temas[st.session_state.idx_y]
    render_display(get_verso_by_seed(tema), tema)

def page_off_machina():
    st.subheader("🌑 Off-Machina")
    livros = [f.replace(".txt", "") for f in os.listdir(PATH_OFF) if f.endswith(".txt")]
    if livros:
        escolha = st.selectbox("Obra:", livros)
        col1, col2 = st.columns([1, 2])
        capa = os.path.join(PATH_OFF, f"{escolha}.jpg")
        if os.path.exists(capa): col1.image(capa, width=220)
        with open(os.path.join(PATH_OFF, f"{escolha}.txt"), "r", encoding="utf-8") as f:
            col2.text_area("Leitura", f.read(), height=450)

def page_books():
    st.subheader("📚 Bibliotecas")
    rois = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
    st.session_state.current_book = st.radio("Livro para yPoemas:", rois)

# ==============================================================================
# 4. ORQUESTRAÇÃO (MANDALA & SIDEBAR)
# ==============================================================================
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
            # Arte da página
            path_arte = os.path.join(PATH_MD, arte_file)
            if os.path.exists(path_arte): st.image(path_arte, use_container_width=True)
            
            # Seletor Poly
            st.write("🌍 **Tradução**")
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
