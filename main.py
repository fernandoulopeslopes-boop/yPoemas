# --- 1. FUNDAÇÕES (DEPENDÊNCIAS LIMPAS) ---
import streamlit as st
import os
import random
from deep_translator import GoogleTranslator
# Removido matplotlib para otimizar o carregamento do palco

# ... (Gestão de estados e Navegação preservados)

# --- 2. PÁGINA PRINCIPAL (SEM MATPLOTLIB) ---
def view_ypoemas():
    """Renderização direta via CSS e Markdown para máxima performance"""
    nav_bar()
    control_bar()
    col_t, col_a = st.columns([1.2, 1])
    
    script = gera_poema(st.session_state.tema, st.session_state.seed)
    poema = "\n".join(script)
    
    # Tradução direta
    if st.session_state.lang != "pt":
        poema = GoogleTranslator(source="pt", target=st.session_state.lang).translate(poema)
    
    with col_t:
        # Uso de HTML puro para manter o esmero visual sem o peso do matplotlib
        st.markdown(f"<p class='logo-text'>{poema.replace('\n', '<br>')}</p>", unsafe_allow_html=True)
    
    with col_a:
        if st.session_state.draw == 'Y':
            st.write("🖼️ *Interface de Arte ativa.*")
