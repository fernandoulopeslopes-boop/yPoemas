import streamlit as st
import extra_streamlit_components as stx
import random
import os

# ==============================================================================
# 1. ARQUITETURA DE DADOS E DIRETÓRIOS (RIGOR TOTAL)
# ==============================================================================
PATH_DATA = "data"          # Onde estão os 45.000 verbetes (.txt)
PATH_MD = "md_files"        # Manuais (.md) e Artes (.jpg)
PATH_BASE = "base"          # Listas de livros (rol_*.txt)
PATH_OFF = "off-maquina"    # Acervo estático (.txt e .jpg)

def get_md(file_name):
    """Carrega manuais da pasta md_files com tratamento de erro."""
    path = os.path.join(PATH_MD, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"⚠️ {file_name} ausente em {PATH_MD}"

def get_rol_list(book_name):
    """Extrai os temas de um arquivo rol_ na pasta base."""
    # Garante o prefixo 'rol_' para busca precisa
    target = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, target)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            # Filtra linhas vazias e comentários
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return []

def get_verso(tema):
    """Busca um fragmento aleatório no diretório de dados."""
    path = os.path.join(PATH_DATA, f"{tema}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f if l.strip()]
            return random.choice(linhas) if linhas else ""
    return ""

def display_content(texto, tema):
    """Renderização central e registro de cache."""
    st.session_state.last_poem = {"texto": texto, "tema": tema}
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# ==============================================================================
# 2. CONSOLE DE NAVEGAÇÃO (+ < * > ?)
# ==============================================================================
def nav_control(lista, label):
    """Interface de controle com persistência de índice por página."""
    if not lista:
        st.error(f"Erro Crítico: Lista '{label}' não encontrada.")
        return None
    
    key_idx = f"idx_{label}"
    if key_idx not in st.session_state:
        st.session_state[key_idx] = 0
    
    c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])
    
    if c1.button("➕", key=f"btn_p_{label}", help="Nova variação"): 
        st.rerun() 
    if c2.button("◀", key=f"btn_l_{label}", help="Anterior"): 
        st.session_state[key_idx] -= 1
    if c3.button("✻", key=f"btn_s_{label}", help="Aleatório"): 
        st.session_state[key_idx] = random.randrange(len(lista))
    if c4.button("▶", key=f"btn_r_{label}", help="Próximo"): 
        st.session_state[key_idx] += 1
    if c5.button("❓", key=f"btn_i_{label}"): 
        st.toast(f"{label}: {st.session_state[key_idx] % len(lista) + 1}/{len(lista)}")

    st.session_state[key_idx] %= len(lista)
    return lista[st.session_state[key_idx]]

# ==============================================================================
# 3. PÁGINAS DO SISTEMA
# ==============================================================================
def page_mini():
    temas = get_rol_list("temas_mini")
    tema = nav_control(temas, "Mini")
    if tema: display_content(get_verso(tema), tema)

def page_ypoemas():
    livro = st.session_state.get('current_book', 'poemas')
    temas = get_rol_list(livro)
    tema = nav_control(temas, f"yPoemas_{livro}")
    if tema: display_content(get_verso(tema), tema)

def page_eureka():
    st.subheader("🔍 Busca Eureka")
    q = st.text_input("Localizar nos 45.000 verbetes (min. 3 letras):")
    if len(q) >= 3:
        hits = []
        for f in [arq for arq in os.listdir(PATH_DATA) if arq.endswith(".txt")]:
            with open(os.path.join(PATH_DATA, f), "r", encoding="utf-8") as file:
                for line in file:
                    if q.lower() in line.lower():
                        hits.append({"v": line.strip().replace(q, f" « {q} » "), "t": f.replace(".txt", "")})
        if hits:
            idx = st.selectbox(f"Resultados: {len(hits)}", range(len(hits)), 
                               format_func=lambda i: f"{hits[i]['v'][:65]}... [{hits[i]['t']}]")
            display_content(hits[idx]['v'], hits[idx]['t'])
        else: st.info("Nenhum fragmento encontrado.")

def page_off_machina():
    st.subheader("🌑 Off-Machina")
    livros = [f.replace(".txt", "") for f in os.listdir(PATH_OFF) if f.endswith(".txt")]
    if livros:
        sel = st.selectbox("Livro:", livros)
        c1, c2 = st.columns([1, 2])
        capa = os.path.join(PATH_OFF, f"{sel}.jpg")
        if os.path.exists(capa): c1.image(capa, width=220)
        with open(os.path.join(PATH_OFF, f"{sel}.txt"), "r", encoding="utf-8") as f:
            c2.text_area(f"Obra: {sel}", f.read(), height=450)

def page_books():
    st.subheader("📚 Bibliotecas")
    acervos = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir(PATH_BASE) if f.startswith("rol_")]
    st.session_state.current_book = st.radio("Acervo ativo para yPoemas:", acervos)

# ==============================================================================
# 4. ORQUESTRAÇÃO (MANDALA & SIDEBAR)
# ==============================================================================
def main():
    if 'current_book' not in st.session_state: st.session_state.current_book = "poemas"
    if 'poly_name' not in st.session_state: st.session_state.poly_name = "Català"
    
    try: st.set_page_config(layout="wide", page_title="yPoemas", page_icon="📜")
    except: pass

    # Mandala (TabBar)
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Mapeamento: (Manual, Função, Arte)
    mapa = {
        "1": ("INFO_MINI.md", page_mini, "ARTE_MINI.jpg"),
        "2": ("INFO_YPOEMAS.md", page_ypoemas, "ARTE_YPOEMAS.jpg"),
        "3": ("INFO_EUREKA.md", page_eureka, "ARTE_EUREKA.jpg"),
        "4": ("INFO_OFF-MACHINA.md", page_off_machina, "ARTE_OFF-MACHINA.jpg"),
        "5": ("INFO_BOOKS.md", page_books, "ARTE_BOOKS.jpg"),
        "6": ("INFO_POLY.md", lambda: st.info("Idiomas na sidebar."), "ARTE_POLY.jpg"),
        "7": ("INFO_ABOUT.md", lambda: st.markdown(get_md("INFO_ABOUT.md")), "ARTE_ABOUT.jpg")
    }

    if chosen_id in mapa:
        info_file, func, arte_file = mapa[chosen_id]
        
        with st.sidebar:
            # 1. ARTE DA PÁGINA (Pasta md_files)
            path_arte = os.path.join(PATH_MD, arte_file)
            if os.path.exists(path_arte):
                st.image(path_arte, use_container_width=True)
            
            # 2. SELETOR POLY (Siglas)
            st.write("🌍 **Tradução**")
            b = st.columns(6)
            if b[0].button("pt", help="Português"): st.session_state.lang = "pt"
            if b[1].button("es", help="Español"): st.session_state.lang = "es"
            if b[2].button("it", help="Italiano"): st.session_state.lang = "it"
            if b[3].button("fr", help="Français"): st.session_state.lang = "fr"
            if b[4].button("en", help="English"): st.session_state.lang = "en"
            if b[5].button("⚒️", help=st.session_state.poly_name): st.session_state.lang = "xy"
            
            st.markdown("---")
            # 3. MANUAIS DINÂMICOS E FIXOS (Pasta md_files)
            st.info(get_md(info_file))
            st.markdown("---")
            st.info(get_md("INFO_BEST.md"))
            st.markdown(get_md("INFO_MEDIA.md"))
            st.caption("Máquina de Fazer Poesia © 2026")

        if callable(func): func()

if __name__ == "__main__":
    main()
