import streamlit as st
import os
import random

# --- CONFIGURAÇÃO DE AMBIENTE (WIDE & PERSISTENCE) ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS Avançado: Botões de 116px, Mini-Buttons e Estética Industrial
st.markdown("""
    <style>
    div.stButton > button {
        width: 116px !important;
        height: 40px !important;
        border-radius: 0px;
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        font-weight: bold;
    }
    /* Estilo específico para os min_buttons da page_mini */
    .min-btn-container div.stButton > button {
        width: 54px !important;
        height: 30px !important;
        font-size: 10px !important;
        margin: 1px !important;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #f0f2f6;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO (SESSION STATE) ---
if 'page' not in st.session_state:
    st.session_state.page = "POESIA"
if 'last_tema' not in st.session_state:
    st.session_state.last_tema = ""
if 'poema_atual' not in st.session_state:
    st.session_state.poema_atual = ""

@st.cache_data
def abre(tema_alvo):
    base_path = os.path.dirname(os.path.abspath(__file__))
    pasta_temas = "temas" 
    full_name = os.path.join(base_path, pasta_temas, f"{tema_alvo}.txt")
    try:
        with open(full_name, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None

def gerar_poema(conteudo):
    if not conteudo: return ""
    linhas = [l.strip() for row in conteudo.strip().split('\n') if (l := row.strip())]
    random.shuffle(linhas)
    return "\n".join(linhas)

# --- SIDEBAR (CONTROLE E STATUS) ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("### @fernandoulopeslopes-boop's Machina")
    st.markdown("---")
    st.write(f"**Modo Ativo:** {st.session_state.page}")
    st.write(f"**Último Tema:** {st.session_state.last_tema}")
    st.markdown("---")
    if st.button("RESET CACHE"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    st.info("Próxima Página: VOZ (gTTS Integration)")

# --- NAVEGADORES DE TOPO (LAYOUT DUPLO) ---

# 1. Navegador de PÁGINAS (Fixo no topo)
p_cols = st.columns(6)
pages = ["POESIA", "MINI", "VOZ", "SOBRE", "CONFIG", "HELP"]
for i, p_name in enumerate(pages):
    with p_cols[i]:
        if st.button(p_name, key=f"page_{p_name}"):
            st.session_state.page = p_name

# 2. Navegador de OPERAÇÃO (More / Last / Rand / Nest / Help / Love)
t_cols = st.columns(6)
symbols = ["+", "<", "*", ">", "?", "@"]
for i, sym in enumerate(symbols):
    with t_cols[i]:
        st.button(sym, key=f"op_{sym}")

st.markdown("---")

# --- LÓGICA DE PÁGINAS (O PALCO) ---

if st.session_state.page == "POESIA":
    # Interface Principal com Temas no Palco
    c_main, c_side = st.columns([4, 1])
    
    with c_main:
        tema = st.text_input("COMANDO DE TEMA", value=st.session_state.last_tema, placeholder="Digite o tema para a Machina...")
        
        if st.button("EXECUTAR PERMUTAÇÃO", use_container_width=True):
            if tema:
                st.session_state.last_tema = tema
                conteudo = abre(tema.lower().strip())
                if conteudo:
                    st.session_state.poema_atual = gerar_poema(conteudo)
                else:
                    st.error(f"ERRO: {tema}.txt não encontrado na pasta 'temas'.")
        
        st.text_area("SAÍDA DA MACHINA", value=st.session_state.poema_atual, height=500)

    with c_side:
        st.markdown("**VARIAÇÕES**")
        # Grid de min_buttons para variações rápidas
        st.markdown('<div class="min-btn-container">', unsafe_allow_html=True)
        for r in range(4):
            m_cols = st.columns(2)
            with m_cols[0]: st.button(f"v{r*2+1}", key=f"v{r*2+1}")
            with m_cols[1]: st.button(f"v{r*2+2}", key=f"v{r*2+2}")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "MINI":
    st.subheader("📟 PAGE_MINI (ACTIVE)")
    col_mini_main, col_mini_ctrl = st.columns([3, 1])
    with col_mini_main:
        m_tema = st.text_input("TEMA MINI:", key="in_mini")
        if m_tema:
            res_mini = abre(m_tema.lower().strip())
            if res_mini:
                st.text_area("OUTPUT", value=gerar_poema(res_mini), height=300)
    with col_mini_ctrl:
        st.write("Params")
        st.toggle("Auto-Refresh")
        st.toggle("Compact Mode", value=True)

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: A ordem nasce do caos. @fernandoulopeslopes-boop's Machina ativa.*")
