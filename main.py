import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL (Rigor Estático: Wide Layout) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide", # Essencial para controlar o palco fixo
    initial_sidebar_state="expanded", # Garante que ela nasça aberta
)

st.markdown("""
    <style>
    /* DESATIVAR HEADER PADRÃO (Oculta setas <<< de recolhimento) */
    [data-testid="stHeader"] { 
        display: none !important;
    }

    /* SIDEBAR: Fixa em 320px, sem controle de recolhimento */
    [data-testid="stSidebar"] { 
        min-width: 320px !important; 
        max-width: 320px !important; 
        background-color: #fafafa;
    }

    /* 2. DINÂMICA DO PALCO: Centralizado dinamicamente em relação à sidebar fixa */
    .main .block-container {
        max-width: 800px !important; /* Limite de leitura pactuado */
        margin: 0 auto !important;   /* Centraliza no espaço disponível */
        padding-top: 1rem !important;
        transition: all 0.3s ease;    /* Suaviza a expansão */
    }

    /* 3. BOTÕES: Black Negrito Profundo, 32px */
    div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000000 !important;   /* BLACK PROFUNDO */
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        min-width: 32px !important;
        border: 2px solid #000000 !important; /* Borda Black reforça o negrito */
        font-size: 20px !important; /* Visibilidade radical */
        font-weight: 900 !important; /* NEGRITO PROFUNDO */
        padding: 0px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1;
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #000000 !important;
        color: #ffffff !important;
        border-color: #000000 !important;
    }

    /* 4. SELECTBOX: Largura 130px (Compacta) */
    div[data-testid="stSelectbox"] {
        width: 130px !important;
        margin: 0 !important;
    }
    label { display: none !important; }

    /* 5. RÉGUAS SINCRONIZADAS (HR) */
    hr { 
        border: 0; 
        height: 1px; 
        background: #e0e0e0; 
        margin: 12px 0 !important; 
    }
    
    /* Títulos na sidebar sem o símbolo ツ */
    .sidebar-title {
        text-align: center;
        color: #f06292;
        margin-top: -30px;
        font-weight: 900;
        font-size: 28px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR FIXA (Informações Importantes) ---
with st.sidebar:
    st.markdown("<h1 class='sidebar-title'>Machina</h1>", unsafe_allow_html=True)
    st.selectbox("Idioma", ["Português", "English", "Español", "Français"], key="lang_v35")
    st.markdown("---") # Linha divisória da sidebar
    
    col_s1, col_s2 = st.columns(2)
    col_s1.button("Talk", key="tk_v35", use_container_width=True)
    col_s2.button("Arte", key="art_v35", use_container_width=True)

# --- 3. BARRA DE COMANDO CENTRALIZADA (Botões Black ← Lista 50%) ---
# Usamos colunas para centralizar o conjunto de 1/3 dentro do palco de 800px
_, col_barra, _ = st.columns([1, 2, 1])

with col_barra:
    # A estrutura de colunas interna mantém o alinhamento horizontal
    # mas o conjunto todo é centralizado pelas colunas externas
    c_btns, c_lista = st.columns([1.6, 0.8])
    
    with c_btns:
        n1, n2, n3, n4, n5 = st.columns(5)
        # Sinais gráficos em Black Negrito Profundo
        n1.button("＋", key="v35_1") 
        n2.button("＜", key="v35_2")
        n3.button("＊", key="v35_3")
        n4.button("＞", key="v35_4")
        n5.button("？", key="v35_5")

    with c_lista:
        try:
            arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Tema", arquivos, key="main_palco_v35")
        except:
            st.write("Erro /data")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. RENDERIZAÇÃO DO CONTEÚDO (Centralizado dinamicamente) ---
# Esta área (Palco) começa a partir daqui e está dinamicamente centralizada
st.markdown("""
<div style='text-align: center; color: #b0bec5; font-family: Georgia; margin-top: 50px;'>
    v.33.5 Integral: Sidebar Fixa. Palco centralizado no espaço restante.<br>
    Botões em Black Negrito Profundo e sem símbolos externos.
</div>
""", unsafe_allow_html=True)
