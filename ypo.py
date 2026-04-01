import streamlit as st
import os
import random
import streamlit.components.v1 as components

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO E CSS DE LARGURA
# ==========================================
st.set_page_config(page_title="yPoemas", layout="wide")

st.markdown("""
    <style>
        /* Sidebar controlada ~20-25% */
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 300px;
        }
        .block-container { 
            padding-top: 1rem; 
            padding-left: 3rem; 
            padding-right: 3rem; 
        }
        .stButton>button { width: 100%; border-radius: 4px; height: 3em; }
    </style>
""", unsafe_allow_html=True)

try:
    from lay_2_ypo import gera_poema
except:
    def gera_poema(t, s="", l="Português"): return ["Motor em manutenção..."]

# ==========================================
# 2º ANDAR: A LENTE (HTML/CSS)
# ==========================================
def write_ypoema(TITULO, TEXTO_RAW, URL_IMAGEM=None):
    if isinstance(TEXTO_RAW, list):
        linhas = [str(l).strip() for l in TEXTO_RAW if str(l).strip()]
        TEXTO_RAW = "\n".join(linhas)
    
    html = f"""
    <div style="display: flex; gap: 40px; font-family: 'Crimson Pro', serif;">
        <div style="flex: 2.5;">
            <h1 style="font-size: 40px; margin-bottom: 20px; color: #000;">{TITULO}</h1>
            <div style="font-size: 30px; line-height: 1.25; white-space: pre-wrap; color: #222;">{TEXTO_RAW}</div>
        </div>
        <div style="flex: 1.2; text-align: right;">
            {f'<img src="{URL_IMAGEM}" style="max-width:100%; border-radius:8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">' if URL_IMAGEM else ""}
        </div>
    </div>
    """
    components.html(html, height=1200, scrolling=True)

# ==========================================
# 3º ANDAR: UTILITÁRIOS E ESTADO
# ==========================================
if "take" not in st.session_state:
    st.session_state.update({'tema': 'Fatos', 'take': 0, 'book': "livro vivo", 'sala': 'Exploração'})

def load_temas():
    path = os.path.join("base", f"rol_{st.session_state.book}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    return ["Fatos", "Tempo", "Anjos"]

# ==========================================
# 4º ANDAR: A SALA (EXPLORAÇÃO)
# ==========================================
def page_ypoemas():
    lista = load_temas()
    idx = st.session_state.take % len(lista)
    st.session_state.tema = lista[idx]

    # --- 4.1 O FAROL (NAVEGAÇÃO TOP) ---
    v1, n1, n2, n3, n4, n_help, n_lista, v2 = st.columns([1.5, 0.4, 0.4, 0.4, 0.4, 0.5, 3.5, 1.5])
    
    with n1: 
        if st.button("✚", key="f_more"): 
            st.session_state.take = random.randint(0, 99999); st.rerun()
    with n2: 
        if st.button("◀", key="f_back"):
            st.session_state.take -= 1; st.rerun()
    with n3: 
        if st.button("✻", key="f_rand"):
            st.session_state.take = random.randint(0, 99999); st.rerun()
    with n4: 
        if st.button("▶", key="f_next"):
            st.session_state.take += 1; st.rerun()
            
    with n_help:
        with st.popover("?"):
            st.markdown("**Matriz: Préfacil**")
            st.caption("A vitrine à direita é o elo com os mundos inexploráveis.")

    with n_lista:
        escolha = st.selectbox("Vitrine", options=lista, index=idx, label_visibility="collapsed", key="f_sel")
        if escolha != st.session_state.tema:
            st.session_state.take = lista.index(escolha); st.rerun()
    
    st.divider()

    # --- 4.2 ÁREA DA OBRA ---
    c_logo, c_obra = st.columns([1, 4])
    with c_logo:
        st.image("https://via.placeholder.com/200x100?text=MACHINA", use_column_width=True)
        st.write("---")
        st.info(f"Matriz: {st.session_state.tema}")

    with c_obra:
        # Passando TEMA, SEMENTE (take) e IDIOMA (da sidebar)
        poema = gera_poema(st.session_state.tema, str(st.session_state.take), st.session_state.g_lang)
        url_teste = "https://images.unsplash.com/photo-1454117096348-e4abbeae002c?w=500"
        write_ypoema(st.session_state.tema, poema, URL_IMAGEM=url_teste)

# ==========================================
# 5º ANDAR: O MOTOR (MENU TOP + SIDEBAR)
# ==========================================
def main():
    mapa_artes = {
        "Exploração": "img_ypoemas.jpg",
        "Sobre": "img_about.jpg",
        "Biblioteca": "img_books.jpg",
        "Eureka": "img_eureka.jpg",
        "Mini-Mundos": "img_mini.jpg",
        "Off-Machina": "img_off-marchina.jpg",
        "Poly-Gens": "img_poly.jpg"
    }

    # 5.1 MENU DE PÁGINAS (TOPO)
    salas = list(mapa_artes.keys())
    cols_menu = st.columns(len(salas))
    for i, nome_sala in enumerate(salas):
        if cols_menu[i].button(nome_sala, key=f"btn_{nome_sala}"):
            st.session_state.sala = nome_sala
            st.rerun()
    st.write("---")

    # 5.2 SIDEBAR PURIFICADA
    with st.sidebar:
        st.title("yPoemas")
        
        img_path = mapa_artes.get(st.session_state.sala)
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)
        
        st.write("---")
        st.subheader("🌐 Variáveis Globais")
        # Seletor de Idioma de volta, afetando a semente da tradução
        st.selectbox("Idioma da Obra", ["Português", "English", "Español"], key="g_lang")
        
        st.write("")
        st.checkbox("🔊 Voz", key="g_voice")
        st.checkbox("🎬 Vídeo", key="g_video")
        st.checkbox("🖼️ Galeria", key="g_draw")
        st.button("📋 Info", key="g_info")

    # 5.3 GATILHO
    if st.session_state.sala == "Exploração":
        page_ypoemas()
    else:
        st.write(f"### Bem-vindo ao portal {st.session_state.sala}")
        st.caption("Ambiente em calibração poética.")

if __name__ == "__main__":
    main()
    
