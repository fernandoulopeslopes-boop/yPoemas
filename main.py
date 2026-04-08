import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] MOTOR SOBERANO ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: lay_2_ypo.py não encontrado.\nTema: {t}"

# --- DICIONÁRIO DE CURADORIA (A LISTA QUE VOCÊ CRIOU) ---
# Mapeia o Tema ao Grupo de Imagens correspondente
DIC_TEMAS_GRUPOS = {
    "Ais": "ais", "Anjos": "anjos", "Augusto": "augusto", "Beijo": "beijo",
    "Bicicleta": "bicicleta", "Cabelos": "cabelos", "Café": "cafe",
    "Cais": "cais", "Caminho": "caminho", "Chuva": "chuva", 
    # ... o sistema buscará dinamicamente nesta lógica
}

def normalizar_e_traduzir(conteudo, idioma_nome):
    if not conteudo: return ""
    texto_unificado = "\n".join(conteudo) if isinstance(conteudo, list) else conteudo
    cod_target = idioma_nome.split(" - ")[0].lower()
    if cod_target == "pt":
        return texto_unificado.replace('\r\n', '\n').replace('\n\n', '\n').strip()
    try:
        texto_final = GoogleTranslator(source='auto', target=cod_target).translate(texto_unificado)
        return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()
    except Exception:
        return texto_unificado

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            footer { visibility: hidden; }
            [data-testid="stSidebar"] { display: none; }
            
            .block-container { 
                padding-top: 1.5rem !important; 
                padding-left: 8% !important; 
                padding-right: 8% !important; 
                max-width: 100% !important;
            }
            
            .poema-container {
                font-family: 'Courier New', Courier, monospace;
                font-size: 1.15em;
                line-height: 1.6;
                color: #222;
                background-color: #fcfcfc;
                padding: 30px;
                border-left: 1px solid #eee;
                white-space: pre-wrap;
                margin-top: 10px;
            }

            div.stButton > button {
                border-radius: 50% !important;
                width: 46px !important;
                height: 46px !important;
                border: 1px solid #333 !important;
                background-color: white !important;
                margin: 0 auto !important;
                display: block;
            }
            
            .cockpit-header { 
                font-size: 0.85em; 
                font-weight: bold; 
                color: #666; 
                margin-top: 8px;
                text-align: center;
                font-family: monospace; 
                text-transform: lowercase;
            }
        </style>
    """, unsafe_allow_html=True)

def buscar_arte_curada(tema):
    # 1. Identifica o grupo pelo tema (Curadoria Exata)
    grupo = DIC_TEMAS_GRUPOS.get(tema, "maquina")
    
    # 2. Tenta encontrar uma imagem dentro da pasta desse grupo
    pasta_grupo = os.path.join("img", grupo)
    
    if os.path.exists(pasta_grupo):
        arquivos = [f for f in os.listdir(pasta_grupo) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if arquivos:
            # Seleciona uma imagem do grupo (pode ser fixa ou aleatória do grupo)
            return os.path.join(pasta_grupo, random.choice(arquivos))
    
    # 3. Fallback: Se o grupo falhar, busca no grupo "maquina"
    pasta_maquina = os.path.join("img", "maquina")
    if os.path.exists(pasta_maquina):
        arquivos_m = [f for f in os.listdir(pasta_maquina) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if arquivos_m:
            return os.path.join(pasta_maquina, random.choice(arquivos_m))
            
    return None

MAPA_BOOKS = {
    "livro vivo": "rol_livro_vivo.txt", "poemas": "rol_poemas.txt", "ensaios": "rol_ensaios.txt",
    "jocosos": "rol_jocosos.txt", "variações": "rol_variações.txt", "metalinguagem": "rol_metalinguagem.txt",
    "sociais": "rol_sociais.txt", "outros autores": "rol_outros autores.txt",
    "todos os temas": "rol_poemas.txt", "todos os signos": "rol_todos os signos.txt", "temas mini": "rol_temas_mini.txt"
}

LISTA_IDIOMAS = ["PT - Português", "EN - English", "ES - Español", "IT - Italiano", "FR - French", "DE - German"] # Simplificado para teste

def carregar_temas(nome_book):
    arquivo = MAPA_BOOKS.get(nome_book, "rol_poemas.txt")
    caminho = os.path.join("base", arquivo)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        except Exception: pass
    return ["Fatos"]

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "poemas"
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}
    if 'com_imagem' not in st.session_state: st.session_state.com_imagem = True

    PAGINAS_APP = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]
    book_em_foco = st.session_state.book_em_foco
    
    temas_do_livro = carregar_temas(book_em_foco)
    idx_atual = st.session_state.tema_idx_por_book.get(book_em_foco, 0) % len(temas_do_livro)
    tema_selecionado = temas_do_livro[idx_atual]

    # --- NAVEGAÇÃO ---
    _, c_prev, c_rand, c_next, _ = st.columns([3, 1, 1, 1, 3])
    if c_prev.button("❰"): st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual - 1); st.rerun()
    if c_rand.button("✱"): st.session_state.tema_idx_por_book[book_em_foco] = random.randint(0, len(temas_do_livro)-1); st.rerun()
    if c_next.button("❱"): st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual + 1); st.rerun()

    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)

    # --- COCKPIT ---
    c1, c2, c3, c4 = st.columns([1, 1.5, 2.5, 1])
    idioma = c1.selectbox("L", LISTA_IDIOMAS, label_visibility="collapsed")
    novo_book = c2.selectbox("B", list(MAPA_BOOKS.keys()), index=list(MAPA_BOOKS.keys()).index(book_em_foco), label_visibility="collapsed")
    if novo_book != book_em_foco: st.session_state.book_em_foco = novo_book; st.rerun()
    
    tema_sel = c3.selectbox("T", temas_do_livro, index=idx_atual, label_visibility="collapsed")
    if tema_sel != tema_selecionado: st.session_state.tema_idx_por_book[book_em_foco] = temas_do_livro.index(tema_sel); st.rerun()
    
    st.session_state.com_imagem = c4.toggle("Arte", value=st.session_state.com_imagem)

    st.markdown(f'<div class="cockpit-header">{book_em_foco} | {tema_selecionado} ({idx_atual+1}/{len(temas_do_livro)})</div>', unsafe_allow_html=True)
    st.markdown("---")

    # --- PALCO ---
    poema = gera_poema(tema_selecionado)
    txt = normalizar_e_traduzir(poema, idioma)

    if st.session_state.com_imagem:
        col_img, col_txt = st.columns([1, 1.2])
        arte = buscar_arte_curada(tema_selecionado)
        if arte: col_img.image(arte, use_container_width=True)
        col_txt.markdown(f'<div class="poema-container">{txt}</div>', unsafe_allow_html=True)
    else:
        _, col_central, _ = st.columns([1, 2, 1])
        col_central.markdown(f'<div class="poema-container">{txt}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# --- FIM DO ARQUIVO: CURADORIA TEMA/GRUPO ESTABELECIDA ---
