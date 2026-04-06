import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==============================================================================
# 1. MOTOR DE DADOS (INFRAESTRUTURA)
# ==============================================================================

PATH_TEMAS = "temas"

def load_temas(book_name="todos os temas"):
    """Lê fisicamente os arquivos .txt na pasta /temas."""
    try:
        if not os.path.exists(PATH_TEMAS):
            return []
        arquivos = sorted([f.replace(".txt", "") for f in os.listdir(PATH_TEMAS) if f.endswith(".txt")])
        if book_name != "todos os temas":
            # Filtra arquivos que contenham a tag do livro no nome
            return [f for f in arquivos if book_name.lower() in f.lower()]
        return arquivos
    except:
        return []

def load_poema(tema):
    """Extrai uma linha aleatória do arquivo correspondente."""
    try:
        file_path = os.path.join(PATH_TEMAS, f"{tema}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                linhas = [l.strip() for l in f if l.strip()]
                return random.choice(linhas) if linhas else "Fragmento não encontrado."
        return f"Arquivo {tema} ausente."
    except:
        return "Erro na leitura do tema."

def load_md_file(file_path):
    """Carrega os arquivos de auxílio da sidebar."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    return ""

def render_display(texto, tema):
    """Exibição centralizada com registro em cache para Off-Machina."""
    st.session_state.last_poem = {"texto": texto, "tema": tema}
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# ==============================================================================
# 2. CONSOLE DE NAVEGAÇÃO (+ < * > ?)
# ==============================================================================

def draw_navigation_bar(temas, label_info):
    """A sequência lógica, prática e funcional solicitada."""
    if not temas:
        return None
    
    if 'take' not in st.session_state:
        st.session_state.take = 0
    
    maxy = len(temas)
    c_plus, c_prev, c_rand, c_next, c_info = st.columns([1, 1, 2, 1, 1])
    
    # + (Nova variação do mesmo tema ou incremento)
    if c_plus.button("➕", key=f"p_{label_info}"):
        st.session_state.take += 0 # Mantém o tema, força o rerun para novo random.choice

    # < (Voltar tema)
    if c_prev.button("◀", key=f"l_{label_info}"):
        st.session_state.take -= 1

    # * (Tema aleatório)
    if c_rand.button("✻ Aleatório", key=f"s_{label_info}"):
        st.session_state.take = random.randrange(maxy)

    # > (Próximo tema)
    if c_next.button("▶", key=f"r_{label_info}"):
        st.session_state.take += 1

    # ? (Informação/Status)
    if c_info.button("❓", key=f"i_{label_info}"):
        st.toast(f"{label_info} | Índice: {st.session_state.take % maxy + 1} de {maxy}")

    st.session_state.take %= maxy
    return temas[st.session_state.take]

# ==============================================================================
# 3. PÁGINAS DA MANDALA
# ==============================================================================

def page_mini():
    temas = load_temas()
    tema = draw_navigation_bar(temas, "Mini")
    if tema:
        render_display(load_poema(tema), tema)

def page_ypoemas():
    livro = st.session_state.get('book', 'todos os temas')
    temas = load_temas(livro)
    tema = draw_navigation_bar(temas, f"yPoemas ({livro})")
    if tema:
        render_display(load_poema(tema), tema)

def page_eureka():
    st.markdown("### 🔍 Busca Eureka")
    termo = st.text_input("Palavra-chave (min. 3 letras):")
    if len(termo) >= 3:
        # Varredura real nos arquivos
        arquivos = [f for f in os.listdir(PATH_TEMAS) if f.endswith(".txt")]
        resultados = []
        for arq in arquivos:
            t_nome = arq.replace(".txt", "")
            with open(os.path.join(PATH_TEMAS, arq), "r", encoding="utf-8") as f:
                for linha in f:
                    if termo.lower() in linha.lower():
                        # Destaca o termo conforme INFO_EUREKA.md
                        destaque = linha.strip().replace(termo, f" « {termo} » ")
                        resultados.append({"verso": destaque, "tema": t_nome})
        
        if resultados:
            escolha = st.selectbox("Ocorrências encontradas:", range(len(resultados)),
                                  format_func=lambda i: f"{resultados[i]['verso'][:60]}... [{resultados[i]['tema']}]")
            item = resultados[escolha]
            render_display(item['verso'], item['tema'])
        else:
            st.info("Nenhum fragmento encontrado com este termo.")

def page_off_machina():
    st.markdown("### 🌑 Modo Off-Machina")
    if 'last_poem' in st.session_state:
        st.info("Exibindo fragmento persistente do cache local:")
        render_display(st.session_state.last_poem['texto'], st.session_state.last_poem['tema'])
    else:
        st.warning("A memória da máquina está vazia. Navegue para carregar poemas.")

def page_books():
    st.markdown("### 📚 Seleção de Acervo")
    opcoes = ["todos os temas", "poemas", "jocosos", "livro vivo"]
    st.session_state.book = st.radio("Selecione o livro para filtrar os temas no yPoemas:", opcoes)

def page_poly():
    st.markdown("### 🌐 Configurações Poly")
    # Simulação da lista de idiomas citada no INFO_POLY.md
    st.selectbox("Selecione o idioma de destino (+97 disponíveis):", ["Português", "English", "Español", "Français", "Italiano", "Deutsch"])
    st.info("A tradução será aplicada aos motores de geração (Em desenvolvimento).")

# ==============================================================================
# 4. ORQUESTRAÇÃO FINAL (MAIN)
# ==============================================================================

def main():
    try:
        st.set_page_config(layout="wide", page_title="a Máquina de Fazer Poesia", page_icon="📜")
    except:
        pass

    # Barra de abas (A Mandala)
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Mapeamento de arquivos MD e funções
    pages = {
        "1": ("INFO_MINI.md", page_mini),
        "2": ("INFO_YPOEMAS.md", page_ypoemas),
        "3": ("INFO_EUREKA.md", page_eureka),
        "4": ("INFO_OFF-MACHINA.md", page_off_machina),
        "5": ("INFO_BOOKS.md", page_books),
        "6": ("INFO_POLY.md", page_poly),
        "7": ("INFO_ABOUT.md", st.markdown(load_md_file("INFO_ABOUT.md")))
    }

    if chosen_id in pages:
        info_file, func = pages[chosen_id]
        
        # Sidebar com os 3 níveis de informação exigidos
        with st.sidebar:
            if info_file:
                st.info(load_md_file(info_file))
            st.markdown("---")
            st.info(load_md_file("INFO_BEST.md"))
            st.markdown(load_md_file("INFO_MEDIA.md"))
            st.markdown("---")
            st.caption("Máquina de Fazer Poesia © 2026")

        # Execução da página selecionada
        if callable(func):
            func()

if __name__ == "__main__":
    main()
