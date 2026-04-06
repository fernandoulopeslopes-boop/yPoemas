import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==========================================
# 1. FUNÇÕES DE SUPORTE (DEFINIÇÃO OBRIGATÓRIA)
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
        st.session_state.rand = st.checkbox("🎲 Aleatório", value=st.session_state.get('rand', False))

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
    # Presumindo que load_poema, load_lypo, translate e update_readings 
    # estão em um arquivo separado ou definidas no seu ambiente
    try:
        curr = load_poema(tema, seed)
        curr = load_lypo()
        if st.session_state.lang != "pt":
            curr = translate(curr)
        update_readings(tema)
        return normalize_text(curr)
    except NameError:
        return f"Erro: Funções de carregamento/tradução não encontradas. Verifique seus imports."

def render_display(texto, tema):
    try:
        image = load_arts(tema) if st.session_state.draw else None
        write_ypoema(texto, image)
        if st.session_state.talk:
            talk(texto)
    except NameError:
        st.write(texto)

# ==========================================
# 2. DEFINIÇÃO DAS PÁGINAS
# ==========================================

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    wait_time = st.sidebar.slider("Tempo (s):", 5, 60, 10)
    
    placeholder = st.empty()
    if st.session_state.get('auto', False):
        st.session_state.mini = random.randrange(0, maxy)
        tema = temas_list[st.session_state.mini]
        texto = get_processed_content(tema)
        with placeholder.container(): render_display(texto, tema)
        time.sleep(wait_time)
        st.rerun()
    else:
        st.session_state.mini = st.session_state.get('mini', 0) % maxy
        tema = temas_list[st.session_state.mini]
        render_display(get_processed_content(tema), tema)

def page_ypoemas():
    # Implementação simplificada para garantir funcionamento
    st.write("### Livro de Poemas")
    page_mini() 

def page_eureka():
    st.write("### Busca Eureka")
    pass

def page_off_machina():
    st.write("### Off-Machina")
    pass

def page_books():
    st.write("### Biblioteca")
    pass

def page_polys():
    st.write("### Poliglotismo")
    pass

def page_abouts():
    st.markdown(load_md_file("INFO_ABOUT.md"))

# ==========================================
# 3. EXECUÇÃO PRINCIPAL
# ==========================================

def main():
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia", page_icon="📜")
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

    # Chamadas seguras: Funções agora definidas no topo
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
