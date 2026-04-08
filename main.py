import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] MOTOR SOBERANO ---
from lay_2_ypo import gera_poema

def normalizar_e_traduzir(conteudo, idioma):
    if not conteudo: return ""
    texto_unificado = "\n".join(conteudo) if isinstance(conteudo, list) else conteudo
    texto_final = texto_unificado
    if "Português" not in idioma:
        try:
            codigos = {"ES - Español": "es", "IT - Italiano": "it", "EN - English": "en"}
            target = codigos.get(idioma, 'en')
            texto_final = GoogleTranslator(source='auto', target=target).translate(texto_unificado)
        except Exception: pass
    return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            footer { visibility: hidden; }
            .block-container { padding-top: 0rem !important; }
            .sb-art-top { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
            div.stButton > button {
                border-radius: 50% !important;
                width: 50px !important;
                height: 50px !important;
                border: 1px solid #333 !important;
                background-color: white !important;
                margin: 0 10px !important;
            }
            .book-header { font-size: 0.85em; font-weight: bold; color: #666; margin-bottom: 2px; font-family: monospace; }
        </style>
    """, unsafe_allow_html=True)

# Mapeamento dos Livros REAIS presentes na pasta \base
MAPA_BOOKS = {
    "mini": "rol_temas_mini.txt",
    "ypoemas": "rol_poemas.txt",
    "eureka": "rol_livro_vivo.txt",
    "off-máquina": "rol_livro_vivo.txt",
    "books": "rol_variações.txt",
    "sociais": "rol_sociais.txt",
    "ensaios": "rol_ensaios.txt",
    "jocosos": "rol_jocosos.txt",
    "metalinguagem": "rol_metalinguagem.txt",
    "outros": "rol_outros autores.txt"
}

def carregar_temas_reais(aba):
    arquivo = MAPA_BOOKS.get(aba, "rol_poemas.txt")
    caminho = os.path.join("base", arquivo)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return ["Fatos"]

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    PAGINAS_APP = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 0
    if 'tema_idx_por_aba' not in st.session_state: st.session_state.tema_idx_por_aba = {p: 0 for p in PAGINAS_APP}
    if 'help_ativo' not in st.session_state: st.session_state.help_ativo = False

    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]
    temas_do_livro = carregar_temas_reais(aba_atual)
    
    idx_atual = st.session_state.tema_idx_por_aba[aba_atual] % len(temas_do_livro)
    tema_atual = temas_do_livro[idx_atual]

    # --- 1. CONTROLES NO TOP (ORDEM: + < * > ? ) ---
    cl, c_plus, c_prev, c_rand, c_next, c_help, cr = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    if c_plus.button("✚"):
        st.session_state.seed_eureka += 1
        st.session_state.help_ativo = False
        st.rerun()

    if c_prev.button("❰"):
        if aba_atual == "eureka": st.session_state.seed_eureka -= 1
        else: st.session_state.tema_idx_por_aba[aba_atual] = (idx_atual - 1) % len(temas_do_livro)
        st.session_state.help_ativo = False
        st.rerun()

    if c_rand.button("✱"):
        if aba_atual == "eureka": st.session_state.seed_eureka = random.randint(0, 999999)
        else: st.session_state.tema_idx_por_aba[aba_atual] = random.randint(0, len(temas_do_livro) - 1)
        st.session_state.help_ativo = False
        st.rerun()

    if c_next.button("❱"):
        if aba_atual == "eureka": st.session_state.seed_eureka += 1
        else: st.session_state.tema_idx_por_aba[aba_atual] = (idx_atual + 1) % len(temas_do_livro)
        st.session_state.help_ativo = False
        st.rerun()

    if c_help.button("?"):
        st.session_state.help_ativo = not st.session_state.help_ativo

    # --- 2. NAVEGAÇÃO DE PÁGINAS ---
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)

    # --- SIDEBAR (Cockpit da Machina) ---
    with st.sidebar:
        idioma = st.selectbox("L", ["PT - Português", "ES - Español", "IT - Italiano", "EN - English"], label_visibility="collapsed")
        sigla_idioma = idioma[:2].lower()
        
        # Ativos Visuais
        img_aba = "img_poly.jpg" if aba_atual == "comments" else f"img_{aba_atual}.jpg"
        if os.path.exists(img_aba): st.image(img_aba, use_container_width=True)
        
        # LINHA DE STATUS BIBLIOGRÁFICO (Conforme MANUAL_YPOEMAS)
        status_line = f"{sigla_idioma} ( {aba_atual} ) ( {idx_atual + 1} / {len(temas_do_livro)} )"
        st.markdown(f'<div class="book-header">{status_line}</div>', unsafe_allow_html=True)
        
        tema_sel = st.selectbox("Book", temas_do_livro, index=idx_atual, label_visibility="collapsed")
        if tema_sel != tema_atual:
            st.session_state.tema_idx_por_aba[aba_atual] = temas_do_livro.index(tema_sel)
            st.rerun()

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada)
        st.session_state.help_ativo = False
        st.rerun()

    st.markdown("---")
    
    # --- 3. PALCO CENTRAL (Manual ou Motor) ---
    if st.session_state.help_ativo:
        # Busca o Manual Oficial da Página
        nome_manual = f"MANUAL_{aba_atual.upper()}.md"
        path_manual = os.path.join("md_files", nome_manual)
        
        if os.path.exists(path_manual):
            with open(path_manual, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))
        else:
            st.warning(f"Manual {nome_manual} não localizado.")
            
    elif aba_atual in ["mini", "ypoemas", "eureka", "books"]:
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        poema_bruto = gera_poema(tema_atual, semente)
        st.text(normalizar_e_traduzir(poema_bruto, idioma))

if __name__ == "__main__":
    main()
