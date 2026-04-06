import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==========================================
# 1. INFRAESTRUTURA E UTILITÁRIOS (PRECEDÊNCIA TOTAL)
# ==========================================

def load_md_file(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return f"Aviso: {file_path} não encontrado."
    except: return "Erro ao carregar documento."

def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

def get_processed_content(tema, seed=""):
    """Motor central de conteúdo: Carrega, Traduz e Normaliza."""
    curr = load_poema(tema, seed)
    curr = load_lypo()
    if st.session_state.lang != "pt":
        curr = translate(curr)
    update_readings(tema)
    return normalize_text(curr)

def render_display(texto, tema):
    """Renderização unificada de Imagem + Poema."""
    image = load_arts(tema) if st.session_state.draw else None
    write_ypoema(texto, image)
    if st.session_state.talk:
        talk(texto)

# ==========================================
# 2. TODAS AS PÁGINAS (PROJETO COMPLETO)
# ==========================================

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    wait_time = st.sidebar.slider(translate("tempo de exibição:"), 5, 60, 10)
    col_rand, col_auto = st.columns([1, 1])
    
    if col_rand.button("✻"): st.session_state.mini = random.randrange(0, maxy)
    st.session_state.auto = col_auto.checkbox("auto", value=st.session_state.get('auto', False))
    
    placeholder = st.empty()
    if st.session_state.auto:
        st.session_state.mini = random.randrange(0, maxy)
        tema = temas_list[st.session_state.mini]
        texto = get_processed_content(tema)
        with placeholder.container(): render_display(texto, tema)
        time.sleep(wait_time)
        st.rerun()
    else:
        st.session_state.mini %= maxy
        tema = temas_list[st.session_state.mini]
        render_display(get_processed_content(tema), tema)

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    st.session_state.take %= (maxy + 1)
    col_nav = st.columns([1, 1, 1, 1])
    if col_nav[0].button("◀"): st.session_state.take -= 1
    if col_nav[1].button("✻"): st.session_state.take = random.randrange(0, maxy)
    if col_nav[2].button("▶"): st.session_state.take += 1
    tema = temas_list[st.session_state.take]
    render_display(get_processed_content(tema), tema)

def page_eureka():
    find_what = st.text_input(label=translate("buscar..."))
    if len(find_what) >= 3:
        eureka_list = load_eureka(find_what)
        if eureka_list:
            seed_data = [{"display": f"{line.partition(' : ')[0]} ➪ {line.partition(' : ')[2]}", 
                          "tema": line.partition(' : ')[2][0:-5], 
                          "seed": line} for line in eureka_list]
            idx = st.selectbox("Ocorrências", range(len(seed_data)), format_func=lambda x: seed_data[x]["display"])
            item = seed_data[idx]
            render_display(get_processed_content(item["tema"], item["seed"]), item["tema"])

def page_off_machina():
    offs = load_all_offs()
    choice = st.selectbox(translate("Livros Off"), range(len(offs)), format_func=lambda x: offs[x])
    # Lógica específica de navegação off-machina aqui
    st.info("Navegação Off-Machina Ativa")

def page_books():
    books = ["livro vivo", "poemas", "jocosos", "ensaios", "variações", "metalinguagem", "sociais", "todos os temas"]
    opt = st.selectbox(translate("Seleção de Livro"), range(len(books)), format_func=lambda x: books[x])
    if st.button("Confirmar Seleção"):
        st.session_state.book = books[opt]
        st.session_state.take = 0
        st.success(f"Livro atual: {books[opt]}")

def page_polys():
    st.subheader(translate("Configurações de Idioma"))
    # pick_lang() já lida com a lógica, aqui apenas exibimos se necessário
    st.write(f"Idioma atual: {st.session_state.lang}")

def page_abouts():
    st.markdown(load_md_file("INFO_ABOUT.md"))

# ==========================================
# 3. CORE EXECUTION (O MESTRE NO COMANDO)
# ==========================================

def main():
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
    except: pass

    # Tab Bar centralizada
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Funções de Setup UI (Assegure que pick_lang e draw_check_buttons existam)
    pick_lang()
    draw_check_buttons()

    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", page_eureka),
        "4": ("INFO_OFF.md", "img_off.jpg", page_off_machina),
        "5": ("INFO_BOOKS.md", "img_books.jpg", page_books),
        "6": ("INFO_POLY.md", "img_poly.jpg", page_polys),
