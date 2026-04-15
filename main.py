import streamlit as st
import os

# --- 1. CONFIGURAÇÃO SOBERANA ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS: ANCORAGEM FIXA E REBALANCEAMENTO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    
    /* Coluna de Controles (Fixed Top-Left) */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 18% !important;
        z-index: 1000;
    }

    /* Palco (Margem para não bater no fixo) */
    [data-testid="column"]:nth-child(3) { margin-left: 21% !important; }

    /* Estilo dos Botões e Estrelas */
    .stButton button { height: 35px !important; color: #31333F !important; font-size: 14px !important; }
    .bottom-star button {
        height: 25px !important;
        color: #FFD700 !important; 
        background-color: transparent !important;
        border: none !important;
        font-size: 20px !important;
        margin-top: -8px !important;
    }
    .bottom-star button:hover { color: #FFEA00 !important; }

    /* Renderização MD (Estilos baseados nos modelos enviados) */
    .md-render { font-family: 'Georgia', serif; line-height: 1.6; margin-top: 25px; }
    .md-render blockquote { border-left: 3px solid #FFD700; padding-left: 15px; font-style: italic; color: #555; }
    .md-render hr { border: 0; border-top: 1px solid #ddd; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTÃO DE ACERVO REAL (PASTA \BASE) ---
@st.cache_data
def carregar_acervo_real():
    pasta = "base"
    if not os.path.exists(pasta): return {}
    # Captura os 13 livros (rol_*.txt)
    arquivos = [f for f in os.listdir(pasta) if f.startswith("rol_") and f.endswith(".txt")]
    # Dicionário: { "Nome Limpo": "rol_arquivo.txt" }
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in arquivos}

def obter_temas(arquivo):
    caminho = os.path.join("base", arquivo)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["vazio"]

# --- 4. ENGINE DE HELP (TRI-MODULAR) ---
def carregar_help(pagina, prefixos=["ABOUT", "INFO", "MANUAL"]):
    conteudo = ""
    nome = "COMMENTS" if pagina == "opinião" else pagina.upper()
    
    for pre in prefixos:
        caminho = os.path.join("md_files", f"{pre}_{nome}.md")
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo += f.read() + "\n\n---\n\n"
    
    return conteudo if conteudo else f"*Documentação para {pagina} em processamento.*"

# --- 5. EXECUÇÃO ---
if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

ACERVO = carregar_acervo_real()
IDIOMAS = ["Português", "Español", "English", "Français", "Italiano", "Català", "Deutsch", "Русский", "中文", "日本語"]

c_painel, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="s_on", use_container_width=True)
    i2.button("🎨", key="a_on", use_container_width=True)
    i3.button("💬", key="t_on", use_container_width=True)
    st.divider()
    
    livro_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["Aguardando..."])
    temas_lista = obter_temas(ACERVO[livro_sel]) if ACERVO else ["-"]
    st.selectbox("temas", temas_lista)
    st.selectbox("idioma", IDIOMAS)

with c_palco:
    # Rédea de pesos equilibrada: off-mach com 1.2 para respiro
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Linha 1: Texto
    cols_t = st.columns(pesos)
    for i, item in enumerate(paginas):
        with cols_t[i]:
            label = "yPoemas" if item == "yPoemas" else item.lower()
            if st.button(label, key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, False
                st.rerun()

    # Linha 2: Stars (Bottom-Star)
    cols_s = st.columns(pesos)
    for i, item in enumerate(paginas):
        with cols_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"h_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- RENDERIZAÇÃO ---
    p, h = st.session_state.page, st.session_state.show_help
    st.markdown('<div class="md-render">', unsafe_allow_html=True)
    
    if h:
        st.markdown(carregar_help(p))
    else:
        # Exemplo de conteúdo funcional para off-mach
        if p == "off-mach":
            st.info(f"Livro: {livro_sel} | Tema: {temas_lista[0]}")
            st.write("> Aqui a máquina recita o que o Pai escreveu.")
        elif p == "opinião": st.markdown(carregar_help("opinião", ["ABOUT"]))
        elif p == "sobre": st.markdown(carregar_help("sobre", ["ABOUT"]))
        else: st.write(f"### {p.lower()} em operação")
    st.markdown('</div>', unsafe_allow_html=True)
