import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==========================================
# 1. FUNÇÕES DE CARREGAMENTO E LÓGICA (SUPORTE)
# ==========================================

def load_temas(book_name):
    """Carrega a lista de temas baseada no livro selecionado."""
    # Simulação da lógica de carregamento de temas
    # Substitua pela sua lógica real de leitura de arquivos/diretórios
    return ["amor", "morte", "tempo", "natureza", "infinito"]

def load_poema(tema, seed=""):
    """Carrega o texto bruto do poema."""
    return f"Poema sobre {tema} {seed}"

def load_lypo():
    """Carrega metadados ou variações do poema."""
    return ""

def translate(text):
    """Interface para tradução (ex: deep_translator)."""
    return text

def update_readings(tema):
    """Log de leitura/estatísticas."""
    pass

def load_arts(tema):
    """Busca o caminho da imagem associada ao tema."""
    return None

def write_ypoema(texto, image=None):
    """Renderiza o texto e a imagem no Streamlit."""
    if image:
        st.image(image)
    st.markdown(f"### {texto}")

def talk(texto):
    """Interface para TTS (ex: gTTS)."""
    pass

def translate_ui(label):
    """Tradução simples para strings da interface."""
    return label

# ==========================================
# 2. FUNÇÕES DE INTERFACE (SIDEBAR E COMPONENTES)
# ==========================================

def pick_lang():
    if 'lang' not in st.session_state:
        st.session_state.lang = "pt"
    
    langs = {"pt": "🇧🇷", "en": "🇺🇸", "es": "🇪🇸", "fr": "🇫🇷", "it": "🇮🇹"}
    cols = st.sidebar.columns(5)
    for i, (lang, flag) in enumerate(langs.items()):
        if cols[i].button(flag, key=f"lang_{lang}"):
            st.session_state.lang = lang
            st.rerun()

def draw_check_buttons():
    with st.sidebar:
        st.markdown("### ⚙️ Configurações")
        st.session_state.talk = st.checkbox("📢 Voz", value=st.session_state.get('talk', False))
        st.session_state.draw = st.checkbox("🖼️ Imagens", value=st.session_state.get('draw', True))
        st.session_state.auto = st.checkbox("🔄 Auto", value=st.session_state.get('auto', False))

def show_icons():
    st.sidebar.markdown("---")
    st.sidebar.caption("Máquina de Fazer Poesia © 2026")

def load_md_file(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return f"Aviso: {file_path} não disponível."
    except: return "Erro ao carregar texto."

def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

def get_processed_content(tema, seed=""):
    curr = load_poema(tema, seed)
    curr += load_lypo()
    if st.session_state.lang != "pt":
        curr = translate(curr)
    update_readings(tema)
    return normalize_text(curr)

def render_display(texto, tema):
    image = load_arts(tema) if st.session_state.draw else None
    write_ypoema(texto, image)
    if st.session_state.talk:
        talk(texto)

# ==========================================
# 3. DEFINIÇÃO DAS PÁGINAS
# ==========================================

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    wait_time = st.sidebar.slider("Segundos:", 5, 60, 10)
    
    placeholder = st.empty()
    
    if st.session_state.auto:
        st.session_state.mini = random.randrange(0, maxy)
        tema = temas_list[st.session_state.mini]
        texto = get_processed_content(tema)
        with placeholder.container():
            render_display(texto, tema)
        time.sleep(wait_time)
        st.rerun()
    else:
        st.session_state.mini = st.session_state.get('mini', 0) % maxy
        if st.button("✻ Aleatório"):
            st.session_state.mini = random.randrange(0, maxy)
            st.rerun()
        tema = temas_list[st.session_state.mini]
        render_display(get_processed_content(tema), tema)

def page_ypoemas():
    # Livro de Poemas completo
    if 'book' not in st.session_state:
        st.session_state.book = "todos os temas"
    
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    if col1.button("◀"): st.session_state.take = st.session_state.get('take', 0) - 1
    if col2.button("✻"): st.session_state.take = random.randrange(0, maxy)
    if col3.button("▶"): st.session_state.take = st.session_state.get('take', 0) + 1
    
    st.session_state.take = st.session_state.get('take', 0) % maxy
    tema = temas_list[st.session_state.take]
    render_display(get_processed_content(tema), tema)

def page_eureka():
    find_what = st.text_input("Buscar termo:")
    if len(find_what) >= 3:
        st.info(f"Resultados para: {find_what}")
        # Lógica de busca load_eureka iria aqui

def page_off_machina():
    st.write("### Modo Off-Machina")

def page_books():
    books = ["livro vivo", "poemas", "jocosos", "todos os temas"]
    opt = st.selectbox("Escolha o Livro:", books)
    if st.button("Carregar"):
        st.session_state.book = opt
        st.session_state.take = 0
        st.success(f"Livro '{opt}' carregado.")

def page_polys():
    st.write(f"Idioma atual: {st.session_state.lang}")

def page_abouts():
    st.markdown(load_md_file("INFO_ABOUT.md"))

# ==========================================
# 4. EXECUÇÃO PRINCIPAL (MAIN)
# ==========================================

def main():
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
    except: pass

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    pick_lang()
    draw_check_buttons()

    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", page_eureka),
        "4": ("INFO_OFF.md", "img_off.jpg", page_off_machina),
        "5": ("INFO_BOOKS.md", "img_books.jpg", page_books),
        "6": ("INFO_POLY.md", "img_poly.jpg", page_polys),
        "7": ("INFO_ABOUT.md", "img_about.jpg", page_abouts)
    }

    if chosen_id in pages:
        info_file, img_file, page_func = pages[chosen_id]
        with st.sidebar:
            st.info(load_md_file(info_file))
            if os.path.exists(img_file):
                st.image(img_file)
        page_func()

    show_icons()

if __name__ == "__main__":
    main()
