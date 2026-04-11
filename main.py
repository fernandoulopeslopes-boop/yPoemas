import streamlit as st
import os
import time

# --- CONFIGURAÇÃO E CSS (Pente-fino no topo e botões) ---
st.set_page_config(page_title="a Máquina de Fazer Poesia", page_icon="ツ")

st.markdown("""
    <style>
    /* Remove espaço no topo */
    .block-container { padding-top: 0rem; }
    header { visibility: hidden; }
    
    /* Botões Circulares de Navegação */
    div.stButton > button {
        border-radius: 50%;
        width: 50px;
        height: 50px;
        padding: 0px;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #ccc;
        background-color: #f0f2f6;
    }
    
    /* Hover e Seleção */
    div.stButton > button:hover {
        border-color: #000;
        background-color: #e0e2e6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ESTADO DE NAVEGAÇÃO ---
if "page" not in st.session_state:
    st.session_state.page = "Demo"

# --- SIDEBAR (Limpa e Funcional) ---
with st.sidebar:
    st.title("ツ Machina")
    
    # Ponto 3: Dropdown de Idiomas
    idiomas = ["Português", "English", "Español", "Français", "Italiano", "Deutsch"]
    st.selectbox("Idioma", idiomas, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Ponto 4: Navegação por Ícones Circulares { + < * > ? }
    cols = st.columns(5)
    if cols[0].button("+"): st.session_state.page = "Demo"
    if cols[1].button("<"): st.session_state.page = "yPoemas"
    if cols[2].button("*"): st.session_state.page = "Eureka"
    if cols[3].button(">"): st.session_state.page = "Off-Machina"
    if cols[4].button("?"): st.session_state.page = "About"

    st.markdown("---")
    
    # Talk e Arte (Mantendo a simetria)
    c1, c2 = st.columns(2)
    c1.button("Talk")
    c2.button("Arte")

# --- EXECUÇÃO SILENCIOSA (Sem mensagens de "Rodar...") ---
pagina = st.session_state.page

# Aqui a Machina apenas opera. 
# Se for Demo ou yPoemas, o motor é chamado direto se o Modo Auto estiver ON
# ou se o usuário interagir com o centro da tela.

try:
    from lay_2_ypo import gera_poema
    
    # Exemplo de renderização (Indolor) respeitando o layout
    if pagina == "Demo":
        # Chamada direta ao motor sem avisos
        versos = gera_poema("Restos", "") 
        
        st.markdown("<br>", unsafe_allow_html=True)
        for verso in versos:
            if verso == "":
                st.write("")
            else:
                st.subheader(verso)
        st.markdown("---")

except Exception as e:
    # Silencioso ou apenas log técnico se necessário
    pass
