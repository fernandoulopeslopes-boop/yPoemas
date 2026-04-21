import os
import sys
import streamlit as st
import extra_streamlit_components as stx

# --- ANCORAGEM E INTEGRIDADE DO AMBIENTE ---
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
if dname not in sys.path:
    sys.path.insert(0, dname)

# --- CONEXÃO COM O MOTOR E FERRAMENTAS ---
# O motor (lay_2_ypo) é o coração; tools fornece a infraestrutura de interface.
try:
    from lay_2_ypo import gera_poema
    from tools import load_md_file, show_icons, pick_lang, draw_check_buttons
except ImportError as e:
    st.error(f"Erro de conexão com os módulos da Machina: {e}")
    st.stop()

# --- CONFIGURAÇÃO DA INTERFACE (IDENTIDADE PRESERVADA) ---
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilização da Sidebar (300px) e botões de comando
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 300px;
        max-width: 300px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- INICIALIZAÇÃO DE ESTADOS ---
if "tema" not in st.session_state: st.session_state.tema = "amor"
if "eureka_word" not in st.session_state: st.session_state.eureka_word = ""

# --- ESTRUTURA DE NAVEGAÇÃO PRINCIPAL ---

def main():
    # Componente de Abas Horizontal
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Sidebar: O Painel de Controlo da Machina
    with st.sidebar:
        pick_lang()
        draw_check_buttons()
        st.divider()
        
        # Mapeamento para carregar as informações certas de cada página
        menu_map = {
            "1":"MINI", "2":"YPOEMAS", "3":"EUREKA", 
            "4":"OFF-MACHINA", "5":"BOOKS", "6":"POLY", "7":"ABOUT"
        }
        tag = menu_map.get(chosen_id, "YPOEMAS")
        
        # Arte e Info correspondente à aba selecionada
        try:
            st.image(f"img_{tag.lower()}.jpg")
        except:
            pass
        
        st.info(load_md_file(f"INFO_{tag}.md"))

    # --- ACIONAMENTO DO MOTOR (INTERAÇÃO COM lay_2_ypo.py) ---
    
    # Área central onde o motor irá renderizar a arte e a poesia
    container_machina = st.container()

    with container_machina:
        if chosen_id == "3":
            # Página EUREKA: O utilizador define a seed para busca no léxico
            st.session_state.eureka_word = st.text_input(
                "Léxico (digite o sufixo ou radical):", 
                st.session_state.eureka_word,
                placeholder="ex: oço, osso, alma..."
            )
            if st.button("Acionar Engenharia Eureka"):
                # Chama o motor passando a palavra de busca
                gera_poema(st.session_state.tema, st.session_state.eureka_word)
                
        elif chosen_id == "2":
            # Página yPoemas: Geração fluida por tema
            if st.button("Gerar Novo yPoema"):
                # Chama o motor com seed vazia para geração padrão
                gera_poema(st.session_state.tema, "")

        elif chosen_id == "1":
            st.info("Página MINI: A carregar estrutura do motor...")
            if st.button("Gerar Mini"):
                gera_poema("mini", "")

        else:
            # Para as demais abas (off-machina, books, etc), 
            # mantemos a moldura pronta para o motor assumir.
            st.write(f"Interface {tag} conectada ao motor.")

    # Rodapé de ícones e créditos (tools.py)
    show_icons()

if __name__ == "__main__":
    main()
