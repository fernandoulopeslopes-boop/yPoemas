import streamlit as st
import os
from deep_translator import GoogleTranslator

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

def nav_to(p, h):
    st.session_state.page = p
    st.session_state.show_help = h

# --- 2. MOTOR DE POESIA (SIMULAÇÃO DA LÓGICA DO USUÁRIO) ---
# Aqui deve estar sua função real. Se estiver em outro arquivo, use: from motor import gera_poema
def gera_poema(tema, params=""):
    # Mock da sua função principal para garantir que o código rode
    return f"Poema gerado sobre {tema}: O verbo flui no vácuo do {tema}."

# --- 3. CSS: POSICIONAMENTO E LIMPEZA ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    [data-testid="column"]:nth-child(1) {position: fixed !important; top: 1rem; left: 1rem; width: 200px !important; z-index: 1000;}
    [data-testid="column"]:nth-child(3) {margin-left: 240px !important;}
    .md-render { font-family: 'Georgia', serif; font-size: 1.6rem; line-height: 1.6; color: #1a1a1a; margin-top: 20px; }
    .stButton button { width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. DADOS & TRADUÇÃO ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def traduzir_direto(texto, destino):
    mapa = {"Português": "pt", "Español": "es", "English": "en", "Deutsch": "de", "Nederlands": "nl", "Français": "fr", "Italiano": "it", "Català": "ca", "Ελληνικά": "el", "Türkçe": "tr", "العربية": "ar", "ע Hebrew": "he", "हिन्दी": "hi"}
    target = mapa.get(destino, "pt")
    if target == "pt": return texto
    try:
        return GoogleTranslator(source='auto', target=target).translate(texto)
    except:
        return texto

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 5. INTERFACE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    ic1, ic2, ic3 = st.columns(3)
    som = ic1.button("🔈", key="t_btn")
    art = ic2.button("🎨", key="a_btn")
    vid = ic3.button("🎬", key="v_btn")
    st.divider()
    l_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sl")
    tema_escolhido = "-"
    if ACERVO:
        with open(os.path.join("base", ACERVO[l_sel]), "r", encoding="utf-8") as f:
            ts = [line.strip() for line in f if line.strip()]
        tema_escolhido = st.selectbox("temas", ts, key="st")
    i_sel = st.selectbox("idioma", IDIOMAS, key="si")

with c2:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    cp = st.columns(pesos); cs = st.columns(pesos)
    for i, p in enumerate(pgs):
        cp[i].button(p.lower() if p != "yPoemas" else p, key=f"n_{i}", on_click=nav_to, args=(p, False))
        cs[i].button("★", key=f"s_{i}", on_click=nav_to, args=(p, True))

    st.divider()

    # --- 6. EXECUÇÃO DA MÁQUINA (PÁGINA DEMO) ---
    p_atual = st.session_state.page
    h_mode = st.session_state.show_help

    if p_atual == "demo" and not h_mode:
        # CHAMADA PARA A FUNÇÃO REAL DA MÁQUINA
        poema_original = gera_poema(tema_escolhido, "")
        
        # Tradução do resultado gerado
        poema_final = traduzir_direto(poema_original, i_sel)
        
        # Exibição limpa
        st.markdown(f'<div class="md-render">{poema_final}</div>', unsafe_allow_html=True)
        
        if som: st.toast("🔈")
        if art: st.toast("🎨")
        if vid: st.toast("🎬")
