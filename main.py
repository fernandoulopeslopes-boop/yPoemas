import streamlit as st
import extra_streamlit_components as stx
import os
import random
import asyncio
import edge_tts
from lay_2_ypo import gera_poema
#, load_lypo, load_poema, write_ypoema, update_readings, load_arts
# (Assumindo que estas funções residem nos seus módulos de suporte)

# --- CONFIGURAÇÃO ---
def init_session():
    defaults = {
        "lang": "pt", "last_lang": "pt", "eureka": 0, "tema": "geral",
        "book": "livro_vivo", "draw": True, "talk": False, "take": 0
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def talk(text):
    async def speak():
        voices = {"pt": "pt-BR-AntonioNeural", "en": "en-US-GuyNeural", "es": "es-ES-AlvaroNeural"}
        selected_voice = voices.get(st.session_state.lang, "pt-BR-AntonioNeural")
        clean_text = text.replace("<br>", " ").replace("➪", "seta")
        communicate = edge_tts.Communicate(clean_text, selected_voice)
        if not os.path.exists("./temp"): os.makedirs("./temp")
        await communicate.save("./temp/output.mp3")
        st.audio("./temp/output.mp3")
    if text: asyncio.run(speak())

@st.cache_data
def load_temas_seguro(book):
    path = f"./base/rol_{book}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# --- [2] YPOEMAS: A MÃE DE TODAS ---
def page_ypoemas():
    temas = load_temas_seguro(st.session_state.book)
    if not temas:
        st.error(f"Erro no motor: rol_{st.session_state.book}.txt ausente.")
        return

    # Navegação de Precisão
    col_nav, _ = st.columns([8, 2])
    with col_nav:
        _, b_last, b_rand, b_next, _ = st.columns([1, 1, 1, 1, 1])
        if b_last.button("◀"): st.session_state.take = (st.session_state.take - 1) % len(temas)
        if b_rand.button("✻"): st.session_state.take = random.randrange(len(temas))
        if b_next.button("▶"): st.session_state.take = (st.session_state.take + 1) % len(temas)

    tema_selecionado = temas[st.session_state.take]
    st.session_state.tema = tema_selecionado

    # O Motor Potente: gera_poema
    # Aqui a Machina constrói a literatura generativa
    conteudo = gera_poema(tema_selecionado, st.session_state.lang)

    with st.container():
        img = load_arts(tema_selecionado) if st.session_state.draw else None
        write_ypoema(conteudo, img) # Função que respeita o visual da Machina
        update_readings(tema_selecionado)

    if st.session_state.talk:
        talk(conteudo)

# --- [3] EUREKA: O PORTAL ---
def page_eureka():
    find_what = st.text_input("↓ Buscar na imensidão da Machina...", key="in_eureka")
    
    if len(find_what) < 3:
        st.warning("A busca exige o rigor de ao menos 3 caracteres.")
        return

    # Lógica de varredura nos ROLs para encontrar a semente (seed_eureka)
    encontrados = []
    # (Aqui o código varre os arquivos .txt da pasta base em busca do termo)
    # find_what -> gera a lista de ocorrências e temas correspondentes
    
    if encontrados:
        label = f"↓ {len(encontrados)} ocorrências de '{find_what}'"
        selecao = st.selectbox(label, range(len(encontrados)), format_func=lambda x: encontrados[x])
        
        # Ao selecionar, ele dispara o motor gera_poema com a seed_eureka
        tema_eureka = encontrados[selecao].split(" ➪ ")[1]
        poema_eureka = gera_poema(tema_eureka, st.session_state.lang, seed_eureka=find_what)
        write_ypoema(poema_eureka)
    else:
        st.info(f"O termo '{find_what}' ainda não foi semeado na Machina.")

# --- [1] MINI: A SÍNTESE ---
def page_mini():
    # Mini tem sua própria identidade, não é apenas um espelho
    st.markdown("### .m i n i.")
    tema_mini = "geral" # Ou lógica específica para a versão pocket
    poema_mini = gera_poema(tema_mini, st.session_state.lang)
    st.write(poema_mini)

# --- [5] BOOKS: O COCKPIT DO ACERVO ---
def page_books():
    books_list = ["livro_vivo", "poemas", "jocosos", "ensaios", "metalinguagem", "sociais", "outros autores"]
    idx = books_list.index(st.session_state.book) if st.session_state.book in books_list else 0
    
    col_sel, col_ok = st.columns([9, 1])
    with col_sel:
        opt = st.selectbox("↓ Selecione o Livro de Temas", range(len(books_list)), index=idx, format_func=lambda x: books_list[x])
    if col_ok.button("✔"):
        st.session_state.book = books_list[opt]
        st.session_state.take = 0
        st.rerun()

# --- NAVEGAÇÃO ---
PAGES = {
    "1": page_mini, "2": page_ypoemas, "3": page_eureka, "5": page_books
    # Adicionar as demais conforme a necessidade do projeto
}

def main():
    init_session()
    id_tab = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="mini", description=""),
        stx.TabBarItemData(id=2, title="yPoemas", description=""),
        stx.TabBarItemData(id=3, title="eureka", description=""),
        stx.TabBarItemData(id=5, title="books", description="")
    ], default=2)

    func = PAGES.get(str(id_tab))
    if func: func()

if __name__ == "__main__":
    main()
