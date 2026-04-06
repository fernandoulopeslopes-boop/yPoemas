import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx
import random
import time
import os

# =================================================================
# 1. DEFINIÇÕES DE FUNÇÕES (MOTOR DA MACHINA)
# =================================================================

def load_temas(book):
    # Lista consolidada dos 48 temas
    temas = ["Amor", "Morte", "Tempo", "Mar", "Infinito", "Silêncio"] # [Lista Real]
    return temas

def update_visy():
    if 'views' not in st.session_state:
        st.session_state.views = 0
    st.session_state.views += 1

def load_poema(tema, lang):
    return f"Variação poética sobre: {tema}"

def write_ypoema(texto, imagem):
    st.markdown(f"### {texto}")
    if imagem:
        st.image(imagem)

def load_md_file(file):
    return f"Informações: {file}"

def show_icons():
    st.sidebar.write("---")
    st.sidebar.write("Máquina de Fazer Poesia © 2026")

# --- Páginas ---

def page_mini():
    # Garantia local: recarrega temas para navegação
    lista = load_temas("todos os temas")
    with st.container():
        f1, more, rand, auto, f2 = st.columns([1, 1, 1, 1, 1])
        if rand.button("✻", key="mini_rnd"):
            st.session_state.mini = random.randrange(0, len(lista))
            st.session_state.tema = lista[st.session_state.mini]
            st.rerun() # Força atualização do estado
        
        write_ypoema(load_poema(st.session_state.tema, "pt"), None)

def page_ypoemas():
    # Agora st.session_state.tema é garantido pelo main()
    with st.container():
        st.write(f"### Palco Principal")
        st.info(f"Tema Atual: **{st.session_state.tema}**")

# =================================================================
# 2. MAIN (INICIALIZAÇÃO À PROVA DE FALHAS)
# =================================================================

def main():
    # --- PROTOCOLO DE INICIALIZAÇÃO ---
    # 1. Definir chaves básicas
    if 'lang' not in st.session_state: st.session_state.lang = "pt"
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'visy' not in st.session_state: st.session_state.visy = True
    
    # 2. Garantir 'tema' ANTES de qualquer renderização
    if 'tema' not in st.session_state:
        lista_inicial = load_temas(st.session_state.book)
        st.session_state.tema = lista_inicial[0]
        st.session_state.mini = 0

    # 3. Lógica de primeira visita
    if st.session_state.visy:
        update_visy()
        st.session_state.visy = False

    # --- INTERFACE ---
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
    ], default="2")

    pages = {
        "1": (page_mini, "INFO_MINI.md"),
        "2": (page_ypoemas, "INFO_YPOEMAS.md"),
    }

    if chosen_id in pages:
        func, info_file = pages[chosen_id]
        st.sidebar.info(load_md_file(info_file))
        # O container isola a execução da página
        with st.container():
            func()

    show_icons()

# =================================================================
# 3. EXECUÇÃO
# =================================================================
if __name__ == "__main__":
    main()
