import streamlit as st
import os
from deep_translator import GoogleTranslator

# MOTOR REAL: Importação mandatória do motor da Machina
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, p=""): return ["Erro: lay_2_ypo.py não encontrado na raiz."]

# --- 1. CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

def nav_to(p, h):
    st.session_state.page = p
    st.session_state.show_help = h

# --- 2. CSS: ARQUITETURA TOTAL & LYPO-TYPO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Lateral Fixo (Esquerda) */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important; 
        top: 1rem; left: 1rem; width: 210px !important; 
        z-index: 1000;
        background: white;
    }
    
    /* Palco de Conteúdo (Direita) */
    [data-testid="column"]:nth-child(3) { 
        margin-left: 250px !important; 
        width: calc(100% - 270px) !important;
    }

    /* LYPO & TYPO: Integridade do Poema */
    .lypo-container { margin-top: 5px; padding: 5px; }
    .typo-verse { 
        font-family: 'Georgia', serif; 
        font-size: 1.65rem; 
        line-height: 1.7; 
        color: #1a1a1a; 
        min-height: 1.5rem;
    }

    /* Régua de Navegação [ + < * > ? ] */
    .nav-rim { margin-top: 5px; margin-bottom: 10px; }
    .nav-rim button {
        background: transparent !important;
        border: 1px solid #f0f0f0 !important;
        color: #999 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    .nav-rim button:hover { color: #000 !important; border-color: #ccc !important; }
    
    .stButton button { width: 100% !important; height: 38px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & TRADUÇÃO ---
@st.cache_data
def get_acervo():
    path = "base"
    if not os.path.exists(path): return {}
    files = sorted([f for f in os.listdir(path) if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def traduzir_poema(lista_versos, destino):
    mapa = {"Português": "pt", "Español": "es", "English": "en", "Deutsch": "de", "Nederlands": "nl", "Français": "fr", "Italiano": "it", "Català": "ca", "Ελληνικά": "el", "Türkçe": "tr", "العربية": "ar", "ע Hebrew": "he", "हिन्दी": "hi"}
    target = mapa.get(destino, "pt")
    if target == "pt": return lista_versos
    try:
        translator = GoogleTranslator(source='auto', target=target)
        return [translator.translate(v) if v.strip() and v != '\n' else v for v in lista_versos]
    except: return lista_versos

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 4. INTERFACE: PAINEL DE CONTROLE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    st.write("### controles")
    ic = st.columns(3)
    som = ic[0].button("🔈", key="v_on")
    art = ic[1].button("🎨", key="a_on")
    vid = ic[2].button("🎬", key="m_on")
    st.divider()
    
    l_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sl")
    tema_escolhido = "-"
    if ACERVO:
        with open(os.path.join("base", ACERVO[l_sel]), "r", encoding="utf-8") as f:
            ts = [l.strip() for l in f if l.strip()]
        tema_escolhido = st.selectbox("temas", ts, key="st")
    
    i_sel = st.selectbox("idioma", IDIOMAS, key="si")

with c2:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # 4.1 Navegação Superior (Páginas)
    cn = st.columns(pesos)
    for i, p in enumerate(pgs):
        cn[i].button(p.lower() if p != "yPoemas" else p, key=f"n_{i}", on_click=nav_to, args=(p, False))
    
    # 4.2 Stars (Documentação)
    cs = st.columns(pesos)
    for i, p in enumerate(pgs):
        cs[i].button("★", key=f"s_{i}", on_click=nav_to, args=(p, True))

    # 4.3 Régua de Navegação Inferior [ + < * > ? ]
    st.markdown('<div class="nav-rim">', unsafe_allow_html=True)
    nav_cols = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 8])
    b_add = nav_cols[0].button("+", key="cmd_add")
    b_prev = nav_cols[1].button("<", key="cmd_prev")
    b_rand = nav_cols[2].button("*", key="cmd_rand")
    b_next = nav_cols[3].button(">", key="cmd_next")
    b_help = nav_cols[4].button("?", key="cmd_help")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # --- 5. RENDERIZAÇÃO: O PALCO (DEMO) ---
    p_atual = st.session_state.page
    h_mode = st.session_state.show_help

    if p_atual == "demo" and not h_mode:
        # CHAMADA AO MOTOR REAL
        poema_bruto = gera_poema(tema_escolhido, "")
        
        # Tradução estruturada preservando a lista
        versos_exibicao = traduzir_poema(poema_bruto, i_sel)

        # EXECUÇÃO DO PAR LYPO-TYPO
        st.markdown('<div class="lypo-container">', unsafe_allow_html=True)
        for verso in versos_exibicao:
            if verso == '\n':
                st.write("") # LYPO: Preservando o respiro/quebra de linha
            else:
                # TYPO: Aplicando a tipografia sem ruído
                st.markdown(f'<div class="typo-verse">{verso}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Triggers de mídia e navegação
        if som: st.toast("🔉 Som")
        if b_rand: st.rerun()

    elif h_mode:
        st.markdown(f"### Manual: {p_atual.upper()}")
        st.write("Exibição de arquivos .md (em construção)")
    else:
        st.write(f"Página {p_atual.lower()} ativa.")
