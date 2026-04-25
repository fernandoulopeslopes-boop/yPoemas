import os
import random
import asyncio
import edge_tts
import streamlit as st
from deep_translator import GoogleTranslator

# --- 1 & 4. LISTA OFICIAL E TRADUÇÃO DE NOMES ---
# Lista oficial conforme o CPC/Original
BOOKS_LIST = [
    "todos os temas", "livro vivo", "poemas", "ensaios", "sociais", 
    "jocosos", "variações", "metalinguagem", "outros autores", 
    "signos_fem", "signos_mas", "todos os signos"
]

def language_selector():
    """ Item 3 & 4: Dropdown oficial com prioridade para last_lang """
    # Lista baseada no seu poly_pt.txt e histórico
    poly_options = [
        "pt : português", "en : english", "es : español", "fr : français", 
        "it : italiano", "de : deutsch", "ca : català", "gl : galego"
    ]
    
    # Reordenar para que o last_lang/atual apareça primeiro (Item 3)
    current_entry = next((s for s in poly_options if f": {st.session_state.lang}" in s or f"{st.session_state.lang} :" in s), poly_options[0])
    
    selected_poly = st.selectbox(
        "↓ " + translate("idioma"),
        poly_options,
        index=poly_options.index(current_entry),
        key="poly_selector"
    )
    
    new_lang = selected_poly.split(" : ")[0].strip()
    if new_lang != st.session_state.lang:
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = new_lang
        st.rerun()

# --- 2. ÍCONES SOCIAIS ---
def show_icons():
    """ Item 2: Facebook | Email | Instagram | WhatsApp """
    st.write("---")
    # Usando HTML para garantir que fiquem na mesma linha com esmero visual
    social_html = """
    <div style="display: flex; justify-content: center; gap: 20px; font-size: 24px;">
        <a href="https://facebook.com" target="_blank">📘</a>
        <a href="mailto:contato@ypoemas.com" target="_blank">✉️</a>
        <a href="https://instagram.com" target="_blank">📸</a>
        <a href="https://wa.me/seunumeroaqui" target="_blank">💬</a>
    </div>
    """
    st.markdown(social_html, unsafe_allow_html=True)

# --- 3. PÁGINA EUREKA (Ajuste de Largura) ---
def page_eureka():
    # ... (lógica de carregamento de help_tips)
    
    # Aumentando a proporção da coluna 'occurrences' (Item 3: de 4 para 5 ou ajuste de pixels via CSS)
    # No Streamlit, controlamos a largura relativa nas colunas:
    seed, more, rand, manu, occurrences = st.columns([2.5, 1.2, 1.2, 0.7, 5.5]) # Aumentado o peso da lista

    with seed:
        find_what = st.text_input(label=translate("digite algo para buscar..."))
    
    # ... (restante da lógica de busca)

# --- 4. PÁGINA OFF-MACHINA (Restauração de Livros) ---
def page_off_machina():
    # Garante que todos os livros do original apareçam aqui
    off_books_list = load_all_offs() # Esta função deve ler sua pasta /off_machina/
    
    if not off_books_list:
        off_books_list = ["livro_vivo", "outras_maquinas"] # Fallback caso a pasta falhe

    options = list(range(len(off_books_list)))
    opt_off_book = st.selectbox(
        "↓ " + translate("lista de Livros"),
        options,
        index=st.session_state.off_book,
        format_func=lambda x: off_books_list[x]
    )
    # ... (restante da lógica de navegação ◀ ✻ ▶ ❤ ?)

# --- 5. NAVEGAÇÃO PRINCIPAL (Books -> Livros) ---
def main():
    # No seu TabBar ou Menu:
    # stx.TabBarItemData(id=5, title="livros", description="") # Mudado de "books" para "livros"
    
    with st.sidebar:
        # Inserindo a Dropdown de idiomas no topo da sidebar (Item 4)
        language_selector()
        st.write("---")
        # Imagem lateral (magy) conforme sua lógica original
        
    # Chamada das páginas conforme o ID escolhido
    # ...
    
    show_icons() # Ícones sociais no rodapé (Item 2)

if __name__ == "__main__":
    if not os.path.exists("./temp"): os.makedirs("./temp")
    main()
