import streamlit as st
import extra_streamlit_components as stx
import random
import os

# ==============================================================================
# 1. MOTOR DE DADOS (DIRETÓRIOS REAIS)
# ==============================================================================

PATH_DATA = "data"          # 45.000 verbetes (.txt)
PATH_MANUAIS = "md_files"   # Manuais (.md)
PATH_BASE = "base"          # Listas de livros (rol_*.txt)
PATH_OFF = "off-maquina"    # Livros off-machina

def load_md_content(file_name):
    """Busca os manuais estritamente na pasta \md_files."""
    path = os.path.join(PATH_MANUAIS, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"Erro: {file_name} não encontrado em {PATH_MANUAIS}"

def load_book_list(book_name):
    """Carrega os temas de um livro da pasta \base."""
    # Garante o prefixo 'rol_' conforme sua estrutura
    file_name = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("[")]
    return []

def load_poema(tema):
    """Lê um verso aleatório de um tema na pasta \data."""
    path = os.path.join(PATH_DATA, f"{tema}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
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
# 2. INTERFACE (+ < * > ?)
# ==============================================================================

def draw_navigation_bar(temas, label_info):
    if not temas: 
        st.error(f"Lista de temas vazia para: {label_info}")
        return None
    
    if 'take' not in st.session_state: st.session_state.take = 0
    maxy = len(temas)
    
    cols = st.columns([1, 1, 2, 1, 1])
    if cols[0].button("➕", key=f"p_{label_info}", help="Nova variação"): st.rerun()
    if cols[1].button("◀", key=f"l_{label_info}", help="Tema anterior"): st.session_state.take -= 1
    if cols[2].button("✻", key=f"s_{label_info}", help="Tema aleatório"): st.session_state.take = random.randrange(maxy)
    if cols[3].button("▶", key=f"r_{label_info}", help="Próximo tema"): st.session_state.take += 1
    if cols[4].button("❓", key=f"i_{label_info}"): 
        st.toast(f"{label_info}: {st.session_state.take % maxy + 1}/{maxy}")

    st.session_state.take %= maxy
    return temas[st.session_state.take]

# ==============================================================================
# 3. PÁGINAS (CONTEÚDO E REGRAS)
# ==============================================================================

def page_mini():
    temas = load_book_list("temas_mini")
    tema = draw_navigation_bar(temas, "Mini")
    if tema: render_display(load_poema(tema), tema)

def page_ypoemas():
    livro = st.session_state.get('current_book', 'poemas')
    temas = load_book_list(livro)
    tema = draw_navigation_bar(temas, f"yPoemas: {livro}")
    if tema: render_display(load_poema(tema), tema)

def page_eureka():
    st.subheader("🔍 Busca Eureka")
    termo = st.text_input("Pesquisar nos 45.000 verbetes (min. 3 letras):")
    if len(termo) >= 3:
        resultados = []
        # Varredura real na pasta \data
        for arq in [f for f in os.listdir(PATH_DATA) if f.endswith(".txt")]:
            tema_nome = arq.replace(".txt", "")
            with open(os.path.join(PATH_DATA, arq), "r", encoding="utf-8") as f:
                for linha in f:
                    if termo.lower() in linha.lower():
                        texto_h = linha.strip().replace(termo, f" « {termo} » ")
                        resultados.append({"verso": texto_h, "tema": tema_nome})
        if resultados:
            idx = st.selectbox(f"Encontrados: {len(resultados)}", range(len(resultados)),
                               format_func=lambda i: f"{resultados[i]['verso'][:60]}... [{resultados[i]['tema']}]")
            render_display(resultados[idx]['verso'], resultados[idx]['tema'])
        else: st.info("Nenhum termo correspondente localizado.")

def page_off_machina():
    st.subheader("🌑 Off-Machina")
    if os.path.exists(PATH_OFF):
        livros = [f.replace(".txt", "") for f in os.listdir(PATH_OFF) if f.endswith(".txt")]
        if livros:
            escolha = st.selectbox("Selecione o livro:", livros)
            col1, col2 = st.columns([1, 2])
            capa = os.path.join(PATH_OFF, f"{escolha}.jpg")
            if os.path.exists(capa): col1.image(capa, width=200)
            
            with open(os.path.join(PATH_OFF, f"{escolha}.txt"), "r", encoding="utf-8") as f:
                col2.markdown(f"**{escolha}**")
                col2.text_area("", f.read(), height=400)
        else: st.info("Pasta off-maquina vazia.")

def page_books():
    st.subheader("📚 Bibliotecas")
    if os.path.exists(PATH_BASE):
        opcoes = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
        st.session_state.current_book = st.radio("Selecione o acervo para o yPoemas:", opcoes)

def page_poly():
    st.subheader("🌐 Poly")
    st.info("Utilize as siglas na sidebar para tradução.")

# ==============================================================================
# 4. MAIN (MANDALA E SIDEBAR FIXA)
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

    pages = {
        "1": ("INFO_MINI.md", page_mini),
        "2": ("INFO_YPOEMAS.md", page_ypoemas),
        "3": ("INFO_EUREKA.md", page_eureka),
        "4": ("INFO_OFF-MACHINA.md", page_off_machina),
        "5": ("INFO_BOOKS.md", page_books),
        "6": ("INFO_POLY.md", page_poly),
        "7": ("INFO_ABOUT.md", lambda: st.markdown(load_md_content("INFO_ABOUT.md")))
    }

    if chosen_id in pages:
        info_file, func = pages[chosen_id]
        
        # SIDEBAR TOTALMENTE POPULADA
        with st.sidebar:
            st.write("🌍 **Idiomas**")
            b1, b2, b3, b4, b5, b6 = st.columns(6)
            if b1.button("pt", key=1, help="Português"): st.session_state.lang = "pt"
            if b2.button("es", key=2, help="Español"): st.session_state.lang = "es"
            if b3.button("it", key=3, help="Italiano"): st.session_state.lang = "it"
            if b4.button("fr", key=4, help="Français"): st.session_state.lang = "fr"
            if b5.button("en", key=5, help="English"): st.session_state.lang = "en"
            if b6.button("⚒️", key=6, help=st.session_state.poly_name): st.session_state.lang = "xy"
            
            st.markdown("---")
            # Carrega o manual da aba atual da pasta \md_files
            st.info(load_md_content(info_file))
            st.markdown("---")
            # Manuais fixos de rodapé
            st.info(load_md_content("INFO_BEST.md"))
            st.markdown(load_md_content("INFO_MEDIA.md"))
        
        if callable(func): func()

if __name__ == "__main__":
    main()
