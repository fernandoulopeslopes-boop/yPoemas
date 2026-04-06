import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==========================================
# 1. FUNÇÕES DE SUPORTE (DEFINIDAS PRIMEIRO)
# ==========================================

def load_md_file(file_path):
    """Lê arquivos Markdown de forma segura."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao carregar {file_path}: {e}"

def pick_lang():
    if 'lang' not in st.session_state:
        st.session_state.lang = "pt"

def draw_check_buttons():
    st.sidebar.markdown("### Configurações")
    st.session_state.talk = st.sidebar.checkbox("Voz", value=st.session_state.get('talk', False))
    st.session_state.draw = st.sidebar.checkbox("Imagens", value=st.session_state.get('draw', True))

def show_icons():
    st.sidebar.markdown("---")
    st.sidebar.write("Máquina de Fazer Poesia © 2026")

def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

# ==========================================
# 2. DEFINIÇÃO DAS PÁGINAS
# ==========================================

def page_mini():
    # ... lógica da página mini ...
    st.write("Página Mini")

def page_ypoemas():
    # ... lógica da página ypoemas ...
    st.write("Página yPoemas")

# ==========================================
# 3. FUNÇÃO PRINCIPAL (MAIN)
# ==========================================

def main():
    # Configuração de página (Sempre a primeira chamada)
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
    except:
        pass

    # Tabs
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
    ], default="2")

    # Chamadas globais (Agora seguras porque as funções estão acima)
    pick_lang()
    draw_check_buttons()

    # Mapeamento de conteúdo
    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
    }

    if chosen_id in pages:
        info_file, img_file, page_func = pages[chosen_id]
        
        # Execução segura: load_md_file já existe para o Python aqui
        st.sidebar.info(load_md_file(info_file))
        
        if os.path.exists(img_file):
            st.sidebar.image(img_file)
            
        page_func()

    show_icons()

# ==========================================
# 4. DISPARO DO SCRIPT
# ==========================================

if __name__ == "__main__":
    main()
