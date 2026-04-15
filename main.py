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

# --- 2. CSS: PRUMO E ESTRUTURA ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Lateral Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important; top: 1rem; left: 1rem; width: 190px !important; z-index: 1001;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 220px !important; }

    .scroll-stage { height: 75vh; overflow-y: auto; border-top: 1px solid #eee; padding-top: 15px; }
    .stButton button { width: 100% !important; height: 38px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & MOTOR DE TRADUÇÃO ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def traduzir_seguro(texto, destino):
    mapa = {
        "Português": "pt", "Español": "es", "English": "en", "Deutsch": "de", 
        "Nederlands": "nl", "Français": "fr", "Italiano": "it", "Català": "ca", 
        "Ελληνικά": "el", "Türkçe": "tr", "العربية": "ar", "ע Hebrew": "he", "हिन्दी": "hi"
    }
    target = mapa.get(destino, "en")
    if target == "pt": return texto
    try:
        return GoogleTranslator(source='auto', target=target).translate(texto)
    except Exception:
        return f"{texto} [Tradução indisponível]"

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    st.write("### controles")
    # Botões de Arte, Som e Vídeo
    ic1, ic2, ic3 = st.columns(3)
    som = ic1.button("🔈", key="t_btn")
    art = ic2.button("🎨", key="a_btn")
    vid = ic3.button("🎬", key="v_btn")
    
    st.divider()
    
    l_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sl")
    if ACERVO:
        with open(os.path.join("base", ACERVO[l_sel]), "r", encoding="utf-8") as f:
            ts = [line.strip() for line in f if line.strip()]
        st.selectbox("temas", ts, key="st")
    
    i_sel = st.selectbox("idioma", IDIOMAS, key="si")

with c2:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    cp = st.columns(pesos)
    for i, p in enumerate(pgs):
        cp[i].button(p.lower() if p != "yPoemas" else p, key=f"n_{i}", on_click=nav_to, args=(p, False))

    cs = st.columns(pesos)
    for i, p in enumerate(pgs):
        cs[i].button("★", key=f"s_{i}", on_click=nav_to, args=(p, True))

    st.divider()

    # --- 5. PALCO DE RENDERIZAÇÃO ---
    st.markdown('<div class="scroll-stage">', unsafe_allow_html=True)
    p_atual = st.session_state.page
    h_mode = st.session_state.show_help

    if p_atual == "demo":
        st.subheader("Módulo de Demonstração")
        demo_txt = "A Máquina de Fazer Poesia habita o espaço entre o código e o verbo."
        
        # Execução da Tradução
        texto_final = traduzir_seguro(demo_txt, i_sel)
        
        st.info(f"Idioma atual: {i_sel}")
        st.markdown(f"> {texto_final}")
        
        # Feedback dos Botões de Mídia
        if som: st.success("🔊 TTS (Som) acionado.")
        if art: st.success("🖼️ Arts (Imagem) acionado.")
        if vid: st.success("🎞️ Video (Motion) acionado.")

    elif h_mode:
        st.write(f"### Ajuda: {p_atual.upper()}")
        st.write("Conteúdo da documentação em construção.")
    else:
        st.write(f"### {p_atual.lower()}")
        st.write("Aguardando parametrização.")
        
    st.markdown('</div>', unsafe_allow_html=True)
