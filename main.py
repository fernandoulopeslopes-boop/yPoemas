import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DO HARDWARE (RETORNO AO RETRATO) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    # Desativamos a sidebar para que os controles fiquem no palco
    initial_sidebar_state="collapsed", 
)

# Estilização CSS para centralização total e estética do print
st.markdown("""
    <style>
    /* DESATIVAR ELEMENTOS NATIVOS */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }

    /* CENTRALIZAÇÃO E LARGURA MÁXIMA DO CONTEÚDO */
    .block-container {
        max-width: 900px !important;
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        margin: 0 auto !important;
    }

    /* BOTÕES CIRCULARES DE COMANDO (Preto Profundo) */
    .st-key-palco_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000 !important;
        border-radius: 50% !important;
        width: 38px !important;
        height: 38px !important;
        border: 2px solid #000 !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0px !important;
    }

    /* ESTILO DA NAVEGAÇÃO SUPERIOR */
    .st-key-nav_super div.stButton > button {
        border-radius: 20px;
        background-color: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.1);
        font-weight: 900;
        letter-spacing: 1px;
    }

    /* ESTILO DO CONTEÚDO DO POEMA (Georgia) */
    .poema-container {
        font-family: 'Georgia', serif;
        font-size: 16px;
        line-height: 1.6;
        color: #111;
        padding-top: 20px;
    }

    /* AJUSTES DE LABELS E DIVISORES */
    label { font-size: 12px !important; color: #555 !important; font-weight: 900 !important; }
    hr { border: 0; height: 1px; background: #ddd; margin: 15px 0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. NAVEGAÇÃO SUPERIOR ---
paginas = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(len(paginas))

# Mapeamento para garantir o DEMO correto
if "active_page" not in st.session_state:
    st.session_state.active_page = "Demo"

for i, pg in enumerate(paginas):
    # Botões estilizados no topo
    st.markdown("<div class='st-key-nav_super'>", unsafe_allow_html=True)
    if cols_nav[i].button(pg.upper(), key=f"nav_{pg}"):
        st.session_state.active_page = pg
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

current = st.session_state.active_page

# --- 3. ÁREA DE COMANDO (CENTRALIZADA COMO NO PRINT) ---
# Usamos colunas para emular a disposição do best_Screenshot.png
_, col_comando_central, _ = st.columns([0.2, 8.0, 0.2])

with col_comando_central:
    c_btns, c_idio, c_temas, c_som = st.columns([2.0, 1.0, 1.0, 0.8])
    
    # A. Botões Circulares (✚, ✻, ☐)
    with c_btns:
        st.markdown("<div class='st-key-palco_btns'>", unsafe_allow_html=True)
        n1, n2, n3 = st.columns(3)
        n1.button("＋", key="cmd_add") # Novo texto
        n2.button("✻", key="cmd_star") # Aleatório
        n3.button("☐", key="cmd_auto") # Automático
        st.markdown("</div>", unsafe_allow_html=True)

    # B. Seletor de Idioma (Texto simples)
    with c_idio:
        elite_langs = ["Português", "Español", "Italiano", "Français", "English", "Català"]
        st.selectbox("Idioma", elite_langs, key="sel_idio")

    # C. Seletor de Temas
    with c_temas:
        # Placeholder para o seletor de temas (emulado)
        st.selectbox("Temas", ["Amor", "Morte", "Tempo"], key="sel_temas")

    # D. Seletor de Som/Voz
    with c_som:
        # Placeholder para o seletor de voz
        st.selectbox("Som", ["Voz 1", "Silêncio"], key="sel_som")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. ÁREA DE EXIBIÇÃO DO RETRATO (Demo/MINI) ---
if current == "Demo":
    _, col_retrato, _ = st.columns([0.1, 9.8, 0.1])
    
    with col_retrato:
        # Layout lado a lado: Imagem e Texto como no print
        img_col, txt_col = st.columns([0.5, 1.0])
        
        with img_col:
            # Carrega a arte da mulher com chapéu (img_demo.jpg) na raiz
            if os.path.exists("img_demo.jpg"):
                st.image("img_demo.jpg", width='stretch')
        
        with txt_col:
            st.markdown("<div class='poema-container'>", unsafe_allow_html=True)
            # Placeholder para a poesia
            st.write("""
                **TÍTULO DO POEMA**

                No silêncio da máquina,
                os versos se compõem...
                O tempo de Proust se recupera,
                na sintaxe que os dados mantêm.

                ...
            """)
            st.markdown("</div>", unsafe_allow_html=True)
else:
    # Para as outras páginas, mantemos a leitura dos manuais
    def load_manual(file_name):
        paths = [os.path.join(os.path.dirname(__file__), "md_files"), os.path.dirname(__file__)]
        target = file_name.upper()
        for p in paths:
            full_path = os.path.join(p, file_name)
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    return f.read()
        return f"⚠️ {target} não localizado."
    
    st.markdown(load_manual(f"MANUAL_{current.upper()}.MD"))

# --- 5. FOOTER CENTRALIZADO ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size: 11px; font-weight: 900; letter-spacing: 1px; color: #666;'>
    INSTAGRAM • GITHUB • LINKEDIN
</div>
""", unsafe_allow_html=True)
