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
        except: pass
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
            .book-header { font-size: 0.85em; font-weight: bold; color: #666; margin-bottom: 2px; }
        </style>
    """, unsafe_allow_html=True)

# Mapeamento estrito dos Books (rol_) para as Abas
MAPA_BOOKS = {
    "mini": "rol_temas_mini.txt",
    "ypoemas": "rol_poemas.txt",
    "eureka": "rol_livro_vivo.txt",
    "books": "rol_variações.txt"
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

    # --- CONTROLES NO TOP ( + < * > ? ) ---
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

    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)

    # --- SIDEBAR ---
    with st.sidebar:
        idioma = st.selectbox("L", ["PT - Português", "ES - Español", "IT - Italiano", "EN - English"], label_visibility="collapsed")
        
        ativos = {
            "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
            "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
            "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
            "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md"},
            "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
            "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md"},
            "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
        }.get(aba_atual)

        if os.path.exists(ativos["img"]): st.image(ativos["img"], use_container_width=True)
        
        # Cabeçalho do Book: NOME: PAGINA / TOTAL
        header_book = f"{aba_atual.upper()}: {idx_atual + 1} / {len(temas_do_livro)}"
        st.markdown(f'<div class="book-header">{header_book}</div>', unsafe_allow_html=True)
        
        tema_sel = st.selectbox("Book", temas_do_livro, index=idx_atual, label_visibility="collapsed")
        if tema_sel != tema_atual:
            st.session_state.tema_idx_por_aba[aba_atual] = temas_do_livro.index(tema_sel)
            st.rerun()

        # O Help (INFO/ABOUT) da página, respeitando o Oráculo
        path_md = os.path.join("md_files", ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada)
        st.session_state.help_ativo = False
        st.rerun()

    st.markdown("---")
    
    # --- PALCO ---
    if st.session_state.help_ativo:
        # Se o Help for acionado pelo '?', ele busca o HELP.md ou o INFO da aba
        path_help = os.path.join("md_files", f"HELP_{aba_atual.upper()}.md")
        if not os.path.exists(path_help): path_help = os.path.join("md_files", ativos["md"])
        
        if os.path.exists(path_help):
            with open(path_help, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))
    elif aba_atual in ["mini", "ypoemas", "eureka", "books"]:
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        poema_bruto = gera_poema(tema_atual, semente)
        st.text(normalizar_e_traduzir(poema_bruto, idioma))

if __name__ == "__main__":
    main()
