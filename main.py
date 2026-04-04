import streamlit as st
import os
import random

# --- CONFIGURAÇÃO DO AMBIENTE ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS para fixar a largura dos botões de navegação (116px) e estilo da Machina
st.markdown("""
    <style>
    div.stButton > button {
        width: 116px !important;
        height: 40px;
        border-radius: 2px;
    }
    /* Estilo para os min_buttons da page_mini */
    .stButton > button[kind="secondary"] {
        width: 60px !important;
        font-size: 10px;
    }
    </style>
""", unsafe_allow_html=True)

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

# --- SIDEBAR ESTRUTURADA ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("### @fernandoulopeslopes-boop's Machina")
    st.markdown("---")
    
    # Navegador de Páginas
    pagina = st.radio(
        "Selecione a Interface:",
        ["Principal", "page_mini", "Configurações", "Ajuda"],
        index=0
    )
    
    st.markdown("---")
    st.info("Próxima implementação: Módulo de Voz (gTTS)")

# --- LÓGICA DE NAVEGAÇÃO ---

if pagina == "Principal":
    st.title("🌀 Machina de Poesia")
    
    # Navegador Superior (116px)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.button("+")
    with c2: st.button("<")
    with c3: st.button("*")
    with c4: st.button(">")
    with c5: st.button("?")
    with c6: st.button("@")
    
    st.markdown("---")
    
    tema = st.text_input("Input Tema:", placeholder="Digite aqui...")
    if st.button("GERAR"):
        res = abre(tema.lower().strip())
        if res:
            st.text_area("", value=gerar_poema(res), height=500)

elif pagina == "page_mini":
    st.subheader("📟 Machina - Mini View")
    
    # Estrutura da page_mini com min_buttons
    col_view, col_ctrl = st.columns([3, 1])
    
    with col_view:
        tema_mini = st.text_input("Tema:", key="mini_tema")
        if tema_mini:
            res_mini = abre(tema_mini.lower().strip())
            if res_mini:
                st.text_area("Output", value=gerar_poema(res_mini), height=300)

    with col_ctrl:
        st.write("Variações")
        m1, m2 = st.columns(2)
        with m1: st.button("v1", key="m1")
        with m2: st.button("v2", key="m2")
        m3, m4 = st.columns(2)
        with m3: st.button("v3", key="m3")
        with m4: st.button("v4", key="m4")

# --- RODAPÉ MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala ativa: A ordem renasce do caos.*")
