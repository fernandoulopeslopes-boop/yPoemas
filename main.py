import streamlit as st
import os
import random
from deep_translator import GoogleTranslator

# --- 1. BOOT & ESTADO (PTC) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception: 
    def gera_poema(t, p=""): return ["A precisão dança conforme o instinto.", "O labirinto aguarda."]

for key, val in {
    'page': 'demo', 'show_help': False, 'idx_tema': 0, 
    'temas_atuais': [], 'som': False, 'arte': False, 'video': False
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. CSS: REFINO ESTÉTICO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main .block-container { max-width: 95%; padding-top: 1rem !important; }
    
    .typo-title {
        font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold;
        text-decoration: underline; text-align: left; margin-bottom: 20px; color: #333;
    }
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.32rem; 
        line-height: 1.35; color: #1a1a1a; margin-bottom: 8px;
    }

    hr { margin: 1.5rem 0 !important; border: 0; border-top: 1px solid #ddd !important; }

    .st-key-nav_p button, .st-key-nav_a button, .st-key-nav_r button, .st-key-nav_n button {
        border-radius: 50% !important; width: 48px !important; height: 48px !important;
        background-color: #f8f9fa !important; border: 1px solid #e0e0e0 !important;
    }

    .md-container { 
        font-family: 'Georgia', serif; line-height: 1.65; color: #222; 
        font-size: 1.15rem; padding-bottom: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE BUSCA "CASSA-EXTENSÃO" ---
def busca_documento_agnostico(nome_pagina):
    pasta = "md_files"
    if not os.path.exists(pasta): return None
    
    arquivos = os.listdir(pasta)
    
    # Lista de possíveis nomes para a página atual
    alvos = []
    if nome_pagina.lower() == "sobre":
        alvos.append("info_about")
        alvos.append("about_sobre")
    else:
        alvos.append(f"about_{nome_pagina}")

    # Varre a pasta buscando match de nome (ignorando caixa e extensão)
    for f in arquivos:
        nome_base = os.path.splitext(f)[0].lower()
        if nome_base in alvos:
            with open(os.path.join(pasta, f), "r", encoding="utf-8") as file:
                return file.read()
                
    return None

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    m_cols = st.columns(3)
    if m_cols[0].button("🔊", key="m_s"): st.toast("Som: Ativo")
    if m_cols[1].button("🎨", key="m_a"): st.toast("Arte: Ativa")
    if m_cols[2].button("🎬", key="m_v"): st.toast("Vídeo: Ativo")
    st.divider()
    
    if os.path.exists("base"):
        files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
        acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}
        lista_l = list(acervo.keys())
        ini_l = "Livro Vivo" if "Livro Vivo" in lista_l else (lista_l[0] if lista_l else "-")
        sel_l = st.selectbox("Livros", lista_l, index=lista_l.index(ini_l) if ini_l in lista_l else 0)
        
        with open(os.path.join("base", acervo[sel_l]), "r", encoding="utf-8") as f:
            st.session_state.temas_atuais = [line.strip() for line in f if line.strip()]
        
        tot = len(st.session_state.temas_atuais)
        idx = st.session_state.idx_tema % tot if tot > 0 else 0
        st.selectbox("Temas", st.session_state.temas_atuais, index=idx)
    
    st.selectbox("Idioma", ["Português", "English", "Español", "Latin"], key="l_sel")

with c2:
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"btn_{p}"): st.session_state.page = p
    with t_cols[3]:
        if st.button("?", key="h_btn"): st.session_state.show_help = not st.session_state.show_help
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"btn_{p}"): st.session_state.page = p

    st.write("") 
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    if n_cols[1].button("❮", key="nav_p"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="nav_a"): st.toast("Semente guardada")
    if n_cols[3].button("✱", key="nav_r"): st.session_state.idx_tema = random.randint(0, 100)
    if n_cols[4].button("❯", key="nav_n"): st.session_state.idx_tema += 1
    st.divider()

    if st.session_state.show_help:
        st.info("A precisão agora dança conforme o instinto.")
    elif st.session_state.page == "demo" and 'temas_atuais' in st.session_state:
        tema = st.session_state.temas_atuais[st.session_state.idx_tema % len(st.session_state.temas_atuais)]
        st.markdown(f'<div class="typo-title">{tema.upper()}</div>', unsafe_allow_html=True)
        for v in gera_poema(tema, ""):
            st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
    else:
        conteudo = busca_documento_agnostico(st.session_state.page)
        if conteudo:
            st.markdown('<div class="md-container">', unsafe_allow_html=True)
            st.markdown(conteudo)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"O arquivo para '{st.session_state.page}' ainda não foi colhido no labirinto de /md_files.")
