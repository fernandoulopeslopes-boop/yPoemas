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

# --- 2. CSS: ESTRUTURA E PRUMO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important; top: 1rem; left: 1rem; width: 190px !important; z-index: 1001;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 220px !important; }

    .scroll-stage { height: 75vh; overflow-y: auto; border-top: 1px solid #eee; padding-top: 15px; }
    .stButton button { width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & TRADUÇÃO ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def traduzir(texto, destino):
    mapa_idiomas = {
        "Português": "pt", "Español": "es", "English": "en", "Deutsch": "de", 
        "Nederlands": "nl", "Français": "fr", "Italiano": "it", "Català": "ca", 
        "Ελληνικά": "el", "Türkçe": "tr", "العربية": "ar", "ע Hebrew": "he", "हिन्दी": "hi"
    }
    sigla = mapa_idiomas.get(destino, "en")
    try:
        return GoogleTranslator(source='auto', target=sigla).translate(texto)
    except:
        return texto

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    st.write("### controles")
    # Botões de Arte, Som e Vídeo (Habilitados)
    ic1, ic2, ic3 = st.columns(3)
    btn_som = ic1.button("🔈", key="talk_btn", help="Som (TTS)")
    btn_arte = ic2.button("🎨", key="arts_btn", help="Arte (Imagem)")
    btn_video = ic3.button("🎬", key="video_btn", help="Vídeo")
    
    st.divider()
    
    livro_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sel_l")
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
        st.selectbox("temas", temas, key="sel_t")
    
    lang_sel = st.selectbox("idioma", IDIOMAS, key="sel_i")

with c2:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Navegação
    cp = st.columns(pesos)
    for i, p in enumerate(paginas):
        cp[i].button(p.lower() if p != "yPoemas" else p, key=f"btn_{i}", 
                     on_click=nav_to, args=(p, False))

    cs = st.columns(pesos)
    for i, p in enumerate(paginas):
        cs[i].button("★", key=f"star_{i}", on_click=nav_to, args=(p, True))

    st.divider()

    # --- 5. RENDERIZAÇÃO: PÁGINA DEMO ---
    st.markdown('<div class="scroll-stage">', unsafe_allow_html=True)
    p_cur, h_cur = st.session_state.page, st.session_state.show_help

    if p_cur == "demo":
        st.subheader("Módulo de Demonstração")
        texto_base = """A Máquina de Fazer Poesia processa o tempo em versos. 
        Cada permutação é um universo que nasce e morre em silêncio."""
        
        if lang_sel != "Português":
            with st.spinner(f"Traduzindo para {lang_sel}..."):
                texto_exibicao = traduzir(texto_base, lang_sel)
        else:
            texto_exibicao = texto_base
            
        st.markdown(f"### {lang_sel}")
        st.write(texto_exibicao)
        
        if btn_som: st.toast("Preparando áudio...")
        if btn_arte: st.toast("Gerando representação visual...")
        if btn_video: st.toast("Iniciando renderização de vídeo...")

    elif h_cur:
        st.write(f"Documentação para {p_cur.upper()}")
    else:
        st.write(f"Página {p_cur.lower()} ativa.")
        
    st.markdown('</div>', unsafe_allow_html=True)
