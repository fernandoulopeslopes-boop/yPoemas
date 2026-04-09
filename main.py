import streamlit as st
import extra_streamlit_components as stx
import os
import random

# CRONOLOGIA ATIVA: X=10 (v1.5 - ESTABILIDADE FINAL DE RENDERIZAÇÃO E SINCRONIA)

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTO = True
except ImportError:
    HAS_AUTO = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- MOTOR ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: Motor não localizado.\nTema: {t}"

# --- DADOS ---
@st.cache_data
def carregar_temas_cached(arquivo_nome):
    caminho = os.path.join(BASE_DIR, "base", arquivo_nome)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        except: pass
    return ["Fatos"]

@st.cache_data
def load_images_list_cached():
    caminho = os.path.join(BASE_DIR, "base", "images.txt")
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return f.readlines()
        except: pass
    return []

def load_arts(nome_tema):
    path = "./images/machina/"
    path_list = load_images_list_cached()
    for line in path_list:
        if line.startswith(nome_tema):
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            if nome_tema == part_line[0]:
                path = "./images/" + part_line[2] + "/"
                break
    if not os.path.exists(path): return None
    arts_list = [f for f in os.listdir(path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    if not arts_list: return None
    if 'arts' not in st.session_state: st.session_state.arts = []
    image = random.choice(arts_list)
    intentos = 0
    while image in st.session_state.arts and intentos < 10:
        image = random.choice(arts_list)
        intentos += 1
    st.session_state.arts.append(image)
    if len(st.session_state.arts) > 36: del st.session_state.arts[0]
    return path + image

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 1rem !important; max-width: 100% !important; }
            div[data-testid="column"] { display: flex; justify-content: center; align-items: center; }
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; color: #555 !important;
            }
            div[data-testid="stSelectbox"] { width: fit-content !important; min-width: 250px !important; margin: 0 auto !important; }
            div[data-baseweb="select"] { border: none !important; background: transparent !important; font-family: serif !important; font-size: 1.4em !important; font-weight: bold !important; }
            .poema-box { 
                font-family: serif; 
                font-size: 1.6em; 
                line-height: 1.7; 
                color: #1a1a1a; 
                margin-top: 2rem; 
                padding: 10px;
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

MAPA_BOOKS = {
    "todos os temas": "rol_todos os temas.txt", "livro vivo": "rol_livro_vivo.txt", 
    "ensaios": "rol_ensaios.txt", "jocosos": "rol_jocosos.txt", "variações": "rol_variações.txt", 
    "metalinguagem": "rol_metalinguagem.txt", "sociais": "rol_sociais.txt", 
    "outros autores": "rol_outros autores.txt", "todos os signos": "rol_todos os signos.txt", 
    "temas mini": "rol_temas_mini.txt"
}

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # --- INICIALIZAÇÃO DE ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = 'todos os temas'
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}
    if 'com_imagem' not in st.session_state: st.session_state.com_imagem = True
    if 'show_config' not in st.session_state: st.session_state.show_config = False
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0
    if 'modo_auto' not in st.session_state: st.session_state.modo_auto = False
    if 'vel_auto' not in st.session_state: st.session_state.vel_auto = 15

    PAGINAS_APP = ["demo", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]

    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)
    if aba_clicada and aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada)
        st.rerun()

    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    lista_temas = carregar_temas_cached(MAPA_BOOKS.get(book_foco, "rol_todos os temas.txt"))
    
    if aba_atual == "demo" and st.session_state.modo_auto and HAS_AUTO:
        st_autorefresh(interval=st.session_state.vel_auto * 1000, key="auto_pilot")
        st.session_state.tema_idx_por_book[book_foco] += 1

    # Cálculo Soberano do Índice
    idx_tema = st.session_state.tema_idx_por_book.get(book_foco, 0) % len(lista_temas)
    tema_atual = lista_temas[idx_tema]

    # --- COCKPIT ---
    st.markdown("<br>", unsafe_allow_html=True)
    c_l, c_p, c_pr, c_ra, c_ne, c_he, c_cf, c_r = st.columns([3, 1, 1, 1, 1, 1, 1, 3])
    
    if c_p.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_pr.button("❰"): st.session_state.tema_idx_por_book[book_foco] = idx_tema - 1; st.rerun()
    if c_ra.button("✱"): st.session_state.tema_idx_por_book[book_foco] = random.randint(0, len(lista_temas)-1); st.rerun()
    if c_ne.button("❱"): st.session_state.tema_idx_por_book[book_foco] = idx_tema + 1; st.rerun()
    if c_he.button("?"): st.session_state.help_ativo = not st.session_state.get('help_ativo', False); st.rerun()
    if c_cf.button("@"): st.session_state.show_config = not st.session_state.show_config; st.rerun()

    # Sincronia do Selectbox: key baseada no índice para forçar refresh visual
    def troca_tema(): 
        st.session_state.tema_idx_por_book[book_foco] = lista_temas.index(st.session_state[f"sel_{book_foco}_{idx_tema}"])
    
    st.selectbox("Tema", lista_temas, index=idx_tema, key=f"sel_{book_foco}_{idx_tema}", on_change=troca_tema, label_visibility="collapsed")

    if st.session_state.show_config:
        with st.container(border=True):
            cfg_cols = st.columns(4)
            with cfg_cols[0]: st.selectbox("Idioma", ["PT - Português", "EN - English", "ES - Español"])
            with cfg_cols[1]: 
                def troca_book(): st.session_state.book_em_foco = st.session_state.sel_book
                st.selectbox("Livro", list(MAPA_BOOKS.keys()), index=list(MAPA_BOOKS.keys()).index(book_foco), key="sel_book", on_change=troca_book, disabled=(aba_atual=="demo"))
            with cfg_cols[2]: st.session_state.com_imagem = st.toggle("Artes", value=st.session_state.com_imagem)
            with cfg_cols[3]:
                if aba_atual == "demo":
                    st.session_state.modo_auto = st.toggle("Auto", value=st.session_state.modo_auto)
                    st.session_state.vel_auto = st.slider("Segundos", 5, 60, st.session_state.vel_auto)

    st.markdown("---")

    # --- PALCO CENTRAL (Formatação Garantida) ---
    if not st.session_state.get('help_ativo', False):
        try:
            res_bruto = gera_poema(tema_atual, str(st.session_state.seed_mutante))
            txt_raw = "".join(res_bruto) if isinstance(res_bruto, list) else str(res_bruto)
            
            # Conversão explícita para HTML breaks para evitar colapso de linha
            txt_poema = txt_raw.strip().replace("\n", "<br>")

            if st.session_state.com_imagem:
                col_i, col_t = st.columns([1, 2])
                with col_t: st.markdown(f'<div class="poema-box">{txt_poema}</div>', unsafe_allow_html=True)
                with col_i:
                    img_path = load_arts(tema_atual)
                    if img_path: st.image(img_path, use_container_width=True)
            else:
                st.markdown(f'<div class="poema-box" style="text-align:center;">{txt_poema}</div>', unsafe_allow_html=True)
        except: st.error("A Machina precisa de um ajuste técnico no motor.")

if __name__ == "__main__":
    main()
