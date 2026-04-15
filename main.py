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

# Inicialização de Estados (Fidelidade)
for key, val in {
    'page': 'demo', 'show_help': False, 'idx_tema': 0, 
    'temas_atuais': [], 'som': False, 'arte': False, 'video': False
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. CSS: O NÓ DO SCROLL E AFIXAÇÃO DO MENU (CC: NO_EMPTY) ---
st.markdown("""
<style>
    /* 1. SCROLL INTEGRAL & MENU FIXO */
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    
    /* Força o container principal a não ter scroll interno, deixando para a página */
    .main .block-container { 
        max-width: 95%; 
        padding-top: 0.5rem !important; 
        padding-bottom: 5rem !important;
    }

    /* TÍTULO À ESQUERDA */
    .typo-title {
        font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold;
        text-decoration: underline; text-align: left; margin-bottom: 20px; color: #333;
    }
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.32rem; 
        line-height: 1.35; color: #1a1a1a; margin-bottom: 8px;
    }

    /* 5. ALINHAMENTO DE FIOS FINOS */
    hr { margin: 1.5rem 0 !important; border: 0; border-top: 1px solid #ddd !important; }

    /* BOTÕES DE PÁGINA */
    div.stButton > button { width: 100% !important; min-width: 95px; height: 40px !important; }

    /* 2. NAVEGAÇÃO REDONDA */
    .st-key-nav_p button, .st-key-nav_a button, .st-key-nav_r button, .st-key-nav_n button {
        border-radius: 50% !important;
        width: 50px !important; height: 50px !important;
        min-width: 50px !important;
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }

    /* HELP QUADRADO */
    .st-key-h_btn button { width: 40px !important; min-width: 40px !important; border-radius: 4px !important; }
    
    /* Ajuste de Markdown para os Docs */
    .md-container { font-family: 'Georgia', serif; line-height: 1.6; color: #222; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS, TRADUÇÃO E MOTOR DE DOCS ---
@st.cache_data
def traduzir(texto, lang_destino):
    mapeamento = {"Português": "pt", "English": "en", "Español": "es", "Deutsch": "de", "Français": "fr", "Italiano": "it", "Latin": "la"}
    if not texto or lang_destino == "Português": return texto
    try: return GoogleTranslator(source='auto', target=mapeamento.get(lang_destino, 'en')).translate(texto)
    except: return texto

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def carrega_markdown(nome_pagina):
    """Varre /md_files em busca de arquivos About_Pagina_*.md"""
    pasta = "md_files"
    if not os.path.exists(pasta): return None
    prefixo = f"About_{nome_pagina.capitalize()}"
    arquivos = [f for f in os.listdir(pasta) if f.startswith(prefixo) and f.endswith(".md")]
    if not arquivos: return None
    
    # Se houver múltiplos, pegamos o primeiro para o 'piloto'
    with open(os.path.join(pasta, arquivos[0]), "r", encoding="utf-8") as f:
        return f.read()

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # 6. MÍDIA FUNCIONAL (Ações de Estado)
    mc1, mc2, mc3 = st.columns(3)
    if mc1.button("🔊", key="m_s"): st.session_state.som = not st.session_state.som; st.toast(f"Som: {'On' if st.session_state.som else 'Off'}")
    if mc2.button("🎨", key="m_a"): st.session_state.arte = not st.session_state.arte; st.toast(f"Arte: {'On' if st.session_state.arte else 'Off'}")
    if mc3.button("🎬", key="m_v"): st.session_state.video = not st.session_state.video; st.toast(f"Vídeo: {'On' if st.session_state.video else 'Off'}")
    
    st.divider() # Fio alinhado
    
    lista_l = list(ACERVO.keys())
    ini_l = "Livro Vivo" if "Livro Vivo" in lista_l else (lista_l[0] if lista_l else "-")
    sel_l = st.selectbox("Livros", lista_l, index=lista_l.index(ini_l) if ini_l in lista_l else 0)
    
    if ACERVO:
        with open(os.path.join("base", ACERVO[sel_l]), "r", encoding="utf-8") as f:
            st.session_state.temas_atuais = [l.strip() for l in f if l.strip()]
    
    tot = len(st.session_state.temas_atuais)
    idx = st.session_state.idx_tema % tot if tot > 0 else 0
    st.selectbox("Temas", st.session_state.temas_atuais, index=idx, key="st_combo")
    idioma_alvo = st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français", "Italiano", "Latin"], key="l_sel")

with c2:
    # MENU SUPERIOR (Sticky-like via UI)
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"btn_{p}"): st.session_state.page = p; st.session_state.show_help = False
    with t_cols[3]:
        if st.button("?", key="h_btn"): st.session_state.show_help = not st.session_state.show_help
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"btn_{p}"): st.session_state.page = p; st.session_state.show_help = False

    # NAVEGAÇÃO REDONDA
    st.write("") 
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    if n_cols[1].button("❮", key="nav_p"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="nav_a"): st.toast("Semente guardada")
    if n_cols[3].button("✱", key="nav_r"): st.session_state.idx_tema = random.randint(0, tot-1) if tot > 0 else 0
    if n_cols[4].button("❯", key="nav_n"): st.session_state.idx_tema += 1
    
    st.divider() # Fio alinhado

    # PALCO (Com Injeção de Markdown e Scroll Global)
    container_palco = st.container()
    with container_palco:
        if st.session_state.show_help:
            st.markdown("### Ajuda da Machina\n*A precisão agora dança conforme o instinto.*")
            st.info("Navegue pelos temas com os botões redondos. O sistema agora lê a alma documental da pasta /md_files.")
        
        elif st.session_state.page == "demo" and tot > 0:
            tema = st.session_state.temas_atuais[st.session_state.idx_tema % tot]
            st.markdown(f'<div class="typo-title">{tema.upper()}</div>', unsafe_allow_html=True)
            for v in gera_poema(tema, ""):
                st.markdown(f'<div class="typo-verse">{traduzir(v, idioma_alvo)}</div>', unsafe_allow_html=True)
        
        else:
            # Tenta carregar o MD dinâmico baseado no nome da página
            conteudo_md = carrega_markdown(st.session_state.page)
            if conteudo_md:
                st.markdown(f'<div class="md-container">', unsafe_allow_html=True)
                st.markdown(conteudo_md)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"### {st.session_state.page.upper()}")
                st.info("Aguardando o arquivo About_" + st.session_state.page.capitalize() + "... na pasta /md_files.")
