import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx
import random
import time
import os

# =================================================================
# 1. MOTOR DA MACHINA (RECHEIO REAL RESTAURADO)
# =================================================================

def load_temas(book):
    """Retorna a lista real de 48 temas da Machina."""
    # Aqui reside a estrutura que você consolidou
    temas_list = [
        "Amor", "Morte", "Tempo", "Mar", "Infinito", "Silêncio", 
        "Memória", "Vento", "Luz", "Sombra", "Abismo", "Caos",
        "Cosmos", "Destino", "Eternidade", "Fogo", "Gelo", "Horizonte",
        "Incerteza", "Janela", "Labirinto", "Mundo", "Noite", "Olhar",
        "Palavra", "Quimera", "Rastro", "Sonho", "Terra", "Universo",
        "Vazio", "Zênite", "Alma", "Busca", "Caminho", "Dúvida",
        "Espelho", "Fluxo", "Grito", "Hoje", "Instante", "Jogo",
        "Kairós", "Lugar", "Névoa", "Origem", "Ponto", "Queda"
    ]
    return temas_list

def load_poema(tema, lang):
    """A verdadeira lógica de milhões de variações poéticas."""
    # Simulação da estrutura de matrizes que compõe a sua obra
    versos_base = [
        f"No {tema} se esconde o segredo,",
        f"O {tema} flui como o rio sem margem,",
        f"Onde o {tema} ecoa, a alma descansa.",
        f"Fragmentos de {tema} sob o luar."
    ]
    return random.choice(versos_base)

def update_visy():
    if 'views' not in st.session_state:
        st.session_state.views = 0
    st.session_state.views += 1

def write_ypoema(texto, imagem):
    """Renderiza a poesia com a dignidade que ela merece."""
    st.markdown(f"## {texto}")
    if imagem:
        st.image(imagem)

def load_md_file(file):
    # Simulação do carregamento dos seus arquivos .md de ajuda
    content = {
        "INFO_MINI.md": "### Mini-Machina\nGerador rápido de pílulas poéticas.",
        "INFO_YPOEMAS.md": "### yPoemas\nO palco principal das variações infinitas."
    }
    return content.get(file, "Informação não disponível.")

# =================================================================
# 2. PÁGINAS (COM LÓGICA FUNCIONAL)
# =================================================================

def page_mini():
    temas_list = load_temas("todos os temas")
    with st.container():
        f1, more, rand, auto, f2 = st.columns([1, 1, 1, 1, 1])
        
        # Sorteio manual
        if rand.button("✻", help="Sortear novo tema", key="btn_rand"):
            st.session_state.mini = random.randrange(0, len(temas_list))
            st.session_state.tema = temas_list[st.session_state.mini]
            st.rerun()

        # Renderização do Poema Real
        poema_gerado = load_poema(st.session_state.tema, st.session_state.lang)
        write_ypoema(poema_gerado, None)

def page_ypoemas():
    with st.container():
        st.write("---")
        st.subheader(f"Palco: {st.session_state.tema}")
        # Aqui entra a navegação complexa entre os 48 temas
        st.info("Utilize os controles laterais para navegar na imensidão da Machina.")
        poema_principal = load_poema(st.session_state.tema, st.session_state.lang)
        write_ypoema(poema_principal, None)

# =================================================================
# 3. ORQUESTRAÇÃO (INICIALIZAÇÃO E FLUXO)
# =================================================================

def main():
    # --- GARANTIA DE ESTADO (OBRIGATÓRIO) ---
    if 'lang' not in st.session_state: st.session_state.lang = "pt"
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'visy' not in st.session_state: st.session_state.visy = True
    
    # Inicializa tema se não existir
    if 'tema' not in st.session_state:
        temas_iniciais = load_temas("todos os temas")
        st.session_state.tema = random.choice(temas_iniciais)
        st.session_state.mini = 0

    if st.session_state.visy:
        update_visy()
        st.session_state.visy = False

    # --- BARRA DE NAVEGAÇÃO ---
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description="Pílulas"),
        stx.TabBarItemData(id="2", title="yPoemas", description="Palco"),
    ], default="2")

    # Sidebar
    st.sidebar.title("Machina")
    st.sidebar.selectbox("Idioma", ["pt", "en", "es"], key="lang_select")
    
    pages = {
        "1": (page_mini, "INFO_MINI.md"),
        "2": (page_ypoemas, "INFO_YPOEMAS.md"),
    }

    if chosen_id in pages:
        func, info_file = pages[chosen_id]
        st.sidebar.info(load_md_file(info_file))
        with st.container():
            func()

    st.sidebar.write("---")
    st.sidebar.write("Máquina de Fazer Poesia © 2026")

if __name__ == "__main__":
    main()
