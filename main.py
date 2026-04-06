import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==============================================================================
# 1. FUNÇÕES DE INFRAESTRUTURA (O ALICERCE)
# ==============================================================================

def load_md_file(file_path):
    """Lê arquivos Markdown com tratamento de erro e verificação de existência."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return f"Aviso: O arquivo `{file_path}` não foi encontrado no servidor."
    except Exception as e:
        return f"Erro ao carregar `{file_path}`: {str(e)}"

def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

def pick_lang():
    """Gerencia a seleção de idiomas na barra lateral."""
    if 'lang' not in st.session_state:
        st.session_state.lang = "pt"
    
    langs = {"pt": "🇧🇷", "en": "🇺🇸", "es": "🇪🇸", "fr": "🇫🇷", "it": "🇮🇹"}
    cols = st.sidebar.columns(5)
    for i, (lang, flag) in enumerate(langs.items()):
        if cols[i].button(flag, key=f"lang_{lang}"):
            st.session_state.lang = lang
            st.rerun()

def draw_check_buttons():
    """Controles globais de áudio e imagem na sidebar."""
    with st.sidebar:
        st.markdown("### ⚙️ Configurações")
        st.session_state.talk = st.checkbox("📢 Voz", value=st.session_state.get('talk', False))
        st.session_state.draw = st.checkbox("🖼️ Imagens", value=st.session_state.get('draw', True))
        st.session_state.auto = st.checkbox("🔄 Auto", value=st.session_state.get('auto', False))

def show_icons():
    """Rodapé da barra lateral."""
    st.sidebar.markdown("---")
    st.sidebar.caption("Máquina de Fazer Poesia © 2026")

# ==============================================================================
# 2. MOTOR DE CONTEÚDO (DEPENDENTE DAS FUNÇÕES ACIMA)
# ==============================================================================

def get_processed_content(tema, seed=""):
    # IMPORTANTE: Garanta que load_poema, load_lypo e translate estejam acessíveis
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

# ==============================================================================
# 3. DEFINIÇÃO DAS PÁGINAS (DEPENDENTES DO MOTOR)
# ==============================================================================

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
        tema = temas_list[st.session_state.mini]
        render_display(get_processed_content(tema), tema)

def page_ypoemas():
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    if col1.button("◀"): st.session_state.take = st.session_state.get('take', 0) - 1
    if col2.button("✻ Aleatório"): st.session_state.take = random.randrange(0, maxy)
    if col3.button("▶"): st.session_state.take = st.session_state.get('take', 0) + 1
    
    st.session_state.take = st.session_state.get('take', 0) % maxy
    tema = temas_list[st.session_state.take]
    render_display(get_processed_content(tema), tema)

# ==============================================================================
# 4. FUNÇÃO PRINCIPAL (MAIN) - CONCENTRA A ORQUESTRAÇÃO
# ==============================================================================

def main():
    # Primeira instrução obrigatória do Streamlit
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
    except:
        pass

    # Componente de Tabs (TabBar)
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="about", description=""),
    ], default="2")

    # Chamadas seguras: Todas as funções abaixo já foram definidas acima
    pick_lang()
    draw_check_buttons()

    # Mapeamento de funções de página
    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", lambda: st.write("Busca Eureka")),
        "4": ("INFO_ABOUT.md", "img_about.jpg", lambda: st.markdown(load_md_file("INFO_ABOUT.md")))
    }

    if chosen_id in pages:
        info_file, img_file, page_func = pages[chosen_id]
        with st.sidebar:
            # load_md_file está garantida no namespace agora
            st.info(load_md_file(info_file))
            if os.path.exists(img_file):
                st.image(img_file)
        
        # Executa a lógica da página selecionada
        page_func()

    show_icons()

# ==============================================================================
# 5. EXECUÇÃO (O ÚNICO COMANDO EM NÍVEL DE MÓDULO NO FINAL)
# ==============================================================================

if __name__ == "__main__":
    main()
