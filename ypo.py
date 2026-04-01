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
        /* Domando a largura da Sidebar para ~20% */
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 320px;
        }
        /* Ajuste de respiro para a área de trabalho */
        .block-container { 
            padding-top: 1rem; 
            padding-left: 3rem; 
            padding-right: 3rem; 
        }
        .stButton>button { width: 100%; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

try:
    from lay_2_ypo import gera_poema
except:
    def gera_poema(t, s=""): return ["Motor em manutenção..."]

# ==========================================
# 2º ANDAR: A LENTE (HTML/CSS) - O PALCO DO POEMA
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
    st.session_state.update({'tema': 'Fatos', 'take': 0, 'book': "livro vivo"})

def load_temas():
    path = os.path.join("base", f"rol_{st.session_state.book}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    return ["Fatos", "Tempo", "Anjos"]

# ==========================================
# 4º ANDAR: A SALA (LAYOUT DA EXPLORAÇÃO)
# ==========================================
def page_ypoemas():
    lista = load_temas()
    idx = st.session_state.take % len(lista)
    st.session_state.tema = lista[idx]

    # --- 4.1 O FAROL: NAVEGAÇÃO DE TOPO (VITRINE) ---
    v1, n1, n2, n3, n4, n_help, n_lista, v2 = st.columns([1.5, 0.4, 0.4, 0.4, 0.4, 0.5, 3.5, 1.5])
    
    with n1: 
        if st.button("✚", key="f_more", help="Variação da Matriz"): 
            st.session_state.take = random.randint(0, 99999); st.rerun()
    with n2: 
        if st.button("◀", key="f_back", help="Tema Anterior"):
            st.session_state.take -= 1; st.rerun()
    with n3: 
        if st.button("✻", key="f_rand", help="Sorteio Aleatório"):
            st.session_state.take = random.randint(0, 99999); st.rerun()
    with n4: 
        if st.button("▶", key="f_next", help="Próximo Tema"):
            st.session_state.take += 1; st.rerun()
            
    with n_help:
        with st.popover("?", help="Guia e Préfacil"):
            st.markdown("**Matriz: Préfacil**")
            st.caption("A vitrine à direita é o elo com os mundos inexploráveis.")

    with n_lista:
        escolha = st.selectbox("Vitrine", options=lista, index=idx, label_visibility="collapsed", 
                              key="f_sel", help="Porta do Paraíso: Vitrine de Temas")
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
        # CORREÇÃO: Passando o tema e a semente (take) para o motor
        poema = gera_poema(st.session_state.tema, st.session_state.take)
        url_teste = "https://images.unsplash.com/photo-1454117096348-e4abbeae002c?w=500"
        write_ypoema(st.session_state.tema, poema, URL_IMAGEM=url_teste)

# ==========================================
# 5º ANDAR: O MOTOR (SIDEBAR GLOBAIS + ARTES)
# ==========================================
def main():
    with st.sidebar:
        st.title("yPoemas")
        
        mapa_artes = {
            "Exploração": "img_ypoemas.jpg",
            "Sobre": "img_about.jpg",
            "Biblioteca": "img_books.jpg",
            "Eureka": "img_eureka.jpg",
            "Mini-Mundos": "img_mini.jpg",
            "Off-Machina": "img_off-machina.jpg",
            "Poly-Gens": "img_poly.jpg"
        }
        
        sala = st.radio("Ambiente:", list(mapa_artes.keys()))
        
        st.write("---")
        img_path = mapa_artes.get(sala)
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)
        
        st.write("---")
        st.subheader("🌐 Variáveis Globais")
        st.selectbox("Idioma", ["Português", "English", "Español"], key="g_lang")
        st.checkbox("🔊 Voz", key="g_voice")
        st.checkbox("🎬 Vídeo", key="g_video")
        st.checkbox("🖼️ Galeria", key="g_draw")
        st.button("📋 Info", key="g_info")

    if sala == "Exploração":
        page_ypoemas()
    else:
        st.write(f"### Bem-vindo ao portal {sala}")
        st.caption("Ambiente em calibração poética.")

if __name__ == "__main__":
    main()
    
