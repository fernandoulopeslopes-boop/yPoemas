import streamlit as st
import extra_streamlit_components as stx
import random
import os

# ==============================================================================
# 1. MOTOR DE DADOS (FUNCIONAL E ROBUSTO)
# ==============================================================================

PATH_TEMAS = "temas"

def ensure_path():
    """Garante a existência do diretório para evitar erros de execução."""
    if not os.path.exists(PATH_TEMAS):
        os.makedirs(PATH_TEMAS)

def load_temas(book_name="todos os temas"):
    ensure_path()
    try:
        # Lista arquivos .txt e limpa a extensão
        arquivos = sorted([f.replace(".txt", "") for f in os.listdir(PATH_TEMAS) if f.endswith(".txt")])
        if book_name != "todos os temas":
            # Filtro por livro baseado no nome do arquivo
            return [f for f in arquivos if book_name.lower() in f.lower()]
        return arquivos
    except:
        return []

def load_poema(tema):
    ensure_path()
    try:
        file_path = os.path.join(PATH_TEMAS, f"{tema}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                linhas = [l.strip() for l in f if l.strip()]
                return random.choice(linhas) if linhas else "O tema existe, mas está vazio."
        return f"Arquivo '{tema}' não encontrado."
    except:
        return "Erro técnico ao ler o fragmento."

def load_md_file(file_path):
    """Lê os manuais .md reais do seu repositório."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return f"Erro ao ler {file_path}"
    return f"Manual {file_path} não localizado."

def render_display(texto, tema):
    """Renderiza o poema e alimenta o cache persistente."""
    st.session_state.last_poem = {"texto": texto, "tema": tema}
    st.markdown("---")
    st.markdown(f"### {tema.upper()}")
    st.markdown(f"#### {texto}")
    st.markdown("---")

# ==============================================================================
# 2. CONSOLE DE NAVEGAÇÃO (+ < * > ?) - A SEQUÊNCIA LÓGICA
# ==============================================================================

def draw_navigation_bar(temas, label_info):
    if not temas:
        st.warning(f"Nenhum arquivo .txt encontrado para {label_info} na pasta /temas.")
        return None
    
    if 'take' not in st.session_state:
        st.session_state.take = 0
    
    maxy = len(temas)
    c_plus, c_prev, c_rand, c_next, c_info = st.columns([1, 1, 2, 1, 1])
    
    # + Gera nova variação para o mesmo tema
    if c_plus.button("➕", key=f"p_{label_info}"):
        st.rerun()

    # < Volta um tema na lista
    if c_prev.button("◀", key=f"l_{label_info}"):
        st.session_state.take -= 1

    # * Escolhe um tema aleatório
    if c_rand.button("✻ Aleatório", key=f"s_{label_info}"):
        st.session_state.take = random.randrange(maxy)

    # > Avança um tema na lista
    if c_next.button("▶", key=f"r_{label_info}"):
        st.session_state.take += 1

    # ? Status e Informação
    if c_info.button("❓", key=f"i_{label_info}"):
        st.toast(f"{label_info}: {st.session_state.take % maxy + 1} de {maxy}")

    st.session_state.take %= maxy
    return temas[st.session_state.take]

# ==============================================================================
# 3. PÁGINAS (IMPLEMENTAÇÃO COMPLETA)
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
    st.subheader("🔍 Busca Eureka")
    termo = st.text_input("Pesquisar palavra ou trecho em toda a obra:")
    if len(termo) >= 3:
        ensure_path()
        arquivos = [f for f in os.listdir(PATH_TEMAS) if f.endswith(".txt")]
        resultados = []
        for arq in arquivos:
            t_nome = arq.replace(".txt", "")
            try:
                with open(os.path.join(PATH_TEMAS, arq), "r", encoding="utf-8") as f:
                    for linha in f:
                        if termo.lower() in linha.lower():
                            # Implementação do destaque « » solicitado
                            destaque = linha.strip().replace(termo, f" « {termo} » ")
                            resultados.append({"verso": destaque, "tema": t_nome})
            except: continue
        
        if resultados:
            idx = st.selectbox("Fragmentos encontrados:", range(len(resultados)),
                               format_func=lambda i: f"{resultados[i]['verso'][:60]}... [{resultados[i]['tema']}]")
            item = resultados[idx]
            render_display(item['verso'], item['tema'])
        else:
            st.info("Nenhum termo correspondente foi localizado nos arquivos.")

def page_off_machina():
    st.subheader("🌑 Modo Off-Machina")
    if 'last_poem' in st.session_state:
        st.markdown("Recuperando o último fragmento gerado pela máquina:")
        render_display(st.session_state.last_poem['texto'], st.session_state.last_poem['tema'])
    else:
        st.info("Navegue pelas outras abas para que a máquina registre poemas na memória local.")

def page_books():
    st.subheader("📚 Seleção de Biblioteca")
    opcoes = ["todos os temas", "poemas", "jocosos", "livro vivo"]
    st.session_state.book = st.radio("Escolha o acervo para o yPoemas:", opcoes)

def page_poly():
    st.subheader("🌐 Tradutor Poly")
    st.write("Abaixo, selecione o idioma de destino para os motores de tradução:")
    st.selectbox("Idiomas (+97 disponíveis):", ["English", "Español", "Français", "Italiano", "Deutsch", "Português"])

# ==============================================================================
# 4. ORQUESTRAÇÃO FINAL (MAIN)
# ==============================================================================

def main():
    try:
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="📜")
    except: pass

    # Tab Bar com 7 posições
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Mapeamento Real de Arquivos e Funções
    mapping = {
        "1": ("INFO_MINI.md", page_mini),
        "2": ("INFO_YPOEMAS.md", page_ypoemas),
        "3": ("INFO_EUREKA.md", page_eureka),
        "4": ("INFO_OFF-MACHINA.md", page_off_machina),
        "5": ("INFO_BOOKS.md", page_books),
        "6": ("INFO_POLY.md", page_poly),
        "7": ("INFO_ABOUT.md", lambda: st.markdown(load_md_file("INFO_ABOUT.md")))
    }

    if chosen_id in mapping:
        info_file, func = mapping[chosen_id]
        
        # Sidebar: Conteúdo Real e Rodapés
        with st.sidebar:
            st.info(load_md_file(info_file))
            st.markdown("---")
            st.info(load_md_file("INFO_BEST.md"))
            st.markdown(load_md_file("INFO_MEDIA.md"))
            st.caption("Máquina de Fazer Poesia © 2026")
        
        # Execução da função da página
        if callable(func):
            func()

if __name__ == "__main__":
    main()
