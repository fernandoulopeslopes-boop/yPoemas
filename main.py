import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==========================================
# 1. FUNÇÕES DE SUPORTE (DEFINIÇÃO OBRIGATÓRIA ANTES DO MAIN)
# ==========================================

def pick_lang():
    """Define o idioma na sessão."""
    if 'lang' not in st.session_state:
        st.session_state.lang = "pt"
    # Lógica de seleção de idioma aqui...

def draw_check_buttons():
    """Desenha os controles globais (Som, Imagem, etc)."""
    st.sidebar.markdown("### Configurações")
    st.session_state.talk = st.sidebar.checkbox("Voz", value=st.session_state.get('talk', False))
    st.session_state.draw = st.sidebar.checkbox("Imagens", value=st.session_state.get('draw', True))

def show_icons():
    """Exibe ícones de rodapé ou redes sociais."""
    st.sidebar.markdown("---")
    st.sidebar.write("Máquina de Fazer Poesia © 2026")

def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

def get_processed_content(tema, seed=""):
    curr_ypoema = load_poema(tema, seed)
    curr_ypoema = load_lypo()
    if st.session_state.lang != "pt":
        curr_ypoema = translate(curr_ypoema)
    update_readings(tema)
    return normalize_text(curr_ypoema)

def render_display(texto, tema):
    image = load_arts(tema) if st.session_state.draw else None
    write_ypoema(texto, image)
    if st.session_state.talk:
        talk(texto)

# ==========================================
# 2. DEFINIÇÃO DAS PÁGINAS
# ==========================================

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    wait_time = st.sidebar.slider(translate("tempo de exibição:"), 5, 60, 10)
    
    col_rand, col_auto = st.columns([1, 1])
    if col_rand.button("✻"):
        st.session_state.mini = random.randrange(0, maxy)
    
    st.session_state.auto = col_auto.checkbox("auto", value=st.session_state.get('auto', False))
    
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
        st.session_state.mini %= maxy
        tema = temas_list[st.session_state.mini]
        texto = get_processed_content(tema)
        with placeholder.container():
            render_display(texto, tema)

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    st.session_state.take %= (maxy + 1)
    
    col_nav = st.columns([1, 1, 1, 1])
    if col_nav[0].button("◀"): st.session_state.take -= 1
    if col_nav[1].button("✻"): st.session_state.take = random.randrange(0, maxy)
    if col_nav[2].button("▶"): st.session_state.take += 1
    
    tema = temas_list[st.session_state.take]
    texto = get_processed_content(tema)
    render_display(texto, tema)

# (Defina as demais páginas page_eureka, page_books aqui...)

# ==========================================
# 3. FUNÇÃO PRINCIPAL (MAIN)
# ==========================================

def main():
    # Inicialização do Streamlit
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
    except:
        pass

    # Componente de Abas
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Chamadas de interface agora seguras (definidas acima)
    pick_lang()
    draw_check_buttons()

    # Mapeamento
    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        # Adicione as outras chaves conforme necessário
    }

    if chosen_id in pages:
        info_file, img_file, page_func = pages[chosen_id]
        st.sidebar.info(load_md_file(info_file))
        st.sidebar.image(img_file)
        page_func()

    show_icons()

# ==========================================
# 4. DISPARO FINAL
# ==========================================

if __name__ == "__main__":
    main()
