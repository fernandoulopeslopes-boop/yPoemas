import streamlit as st
import os
import random

# --- AMBIENTE E CONFIGURAÇÃO ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS para os botões de 116px e alinhamento da Machina
st.markdown("""
    <style>
    div.stButton > button {
        width: 116px !important;
        height: 42px;
        border-radius: 4px;
        font-weight: bold;
    }
    /* Estilo para os botões menores (min_buttons) */
    .min-btn > div > button {
        width: 54px !important;
        height: 30px !important;
        font-size: 11px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
if 'page' not in st.session_state:
    st.session_state.page = "Poesia"

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

# --- SIDEBAR AVANÇADA ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("### @fernandoulopeslopes-boop's Machina")
    st.markdown("---")
    st.write(f"Página Atual: **{st.session_state.page}**")
    st.markdown("---")
    if st.button("RESET MACHINA"):
        st.cache_data.clear()
        st.rerun()

# --- INTERFACE DE NAVEGAÇÃO PRINCIPAL ---

# 1. Navegador de PÁGINAS (Botões de 116px)
p1, p2, p3, p4, p5, p6 = st.columns(6)
with p1: 
    if st.button("POESIA"): st.session_state.page = "Poesia"
with p2: 
    if st.button("MINI"): st.session_state.page = "page_mini"
with p3: 
    if st.button("VOZ"): st.session_state.page = "Voz"
with p4: 
    if st.button("SOBRE"): st.session_state.page = "Sobre"
with p5: 
    if st.button("CONFIG"): st.session_state.page = "Config"
with p6: 
    if st.button("HELP"): st.session_state.page = "Help"

# 2. Navegador de TEMAS/CONTROLE (Logo abaixo)
t1, t2, t3, t4, t5, t6 = st.columns(6)
with t1: st.button("+") # more
with t2: st.button("<") # last
with t3: st.button("*") # rand
with t4: st.button(">") # nest
with t5: st.button("?") # help
with t6: st.button("@") # love

st.markdown("---")

# --- LÓGICA DE PÁGINAS ---

if st.session_state.page == "Poesia":
    col_main, col_opt = st.columns([4, 1])
    
    with col_main:
        tema = st.text_input("Comando de Tema:", placeholder="Insira o tema da variação...")
        if st.button("EXECUTAR PERMUTAÇÃO", use_container_width=True):
            res = abre(tema.lower().strip())
            if res:
                st.text_area("Resultado da Machina", value=gerar_poema(res), height=450)
            else:
                st.error(f"Arquivo '{tema}.txt' não localizado.")

    with col_opt:
        st.write("Variações")
        st.markdown('<div class="min-btn">', unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1: st.button("v1")
        with m2: st.button("v2")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "page_mini":
    st.subheader("📟 Modo Mini-Interface")
    # Conteúdo da page_mini que estávamos finalizando
    tema_mini = st.text_input("Tema reduzido:", key="mini")
    if tema_mini:
        res_m = abre(tema_mini.lower().strip())
        if res_m:
            st.text_area("Saída", value=gerar_poema(res_m), height=250)

elif st.session_state.page == "Voz":
    st.subheader("🎙️ Módulo de Voz (Próxima Implementação)")
    st.write("Preparando integração com gTTS...")

# --- MANDALA FINAL ---
st.markdown("---")
st.markdown("✨ *A ordem nasce do caos. @fernandoulopeslopes-boop's Machina está ativa.*")
