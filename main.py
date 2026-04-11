# =================================================================
# 🧠 MOTOR LÉXICO DA MACHINA (lay_2_ypo.py) - LIMPEZA CIRÚRGICA
# =================================================================

import os
import io
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime

# --- REMOVIDO: extra_streamlit_components (causador de crash no Py 3.14)
# --- REMOVIDO: from lay_2_ypo import gera_poema (auto-importação eliminada)

### bof: settings

# ... (Mantenha suas configurações de st.set_page_config e estilos CSS aqui)

# --- CORREÇÃO DE CACHE (Protocolo de Segurança para Python Moderno) ---
# Substituindo o antigo @st.cache por st.cache_data

@st.cache_data(show_spinner=False)
def load_help_tips():
    help_list = []
    try:
        with open(os.path.join("./base/helpers.txt"), encoding="utf-8") as file:
            for line in file:
                help_list.append(line)
    except Exception:
        return ["Ajuda não disponível"]
    return help_list

@st.cache_data(show_spinner=False)
def load_temas(book):
    book_list = []
    try:
        with open(os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8") as file:
            for line in file:
                book_list.append(line.strip("\n"))
    except Exception:
        return ["Erro ao carregar temas"]
    return book_list

# =================================================================
# ⚙️ FUNÇÃO MESTRE: gera_poema
# =================================================================
# Esta função deve ser autossuficiente e NÃO importar a si mesma.

def gera_poema(tema, seed_manual=""):
    # Sua lógica de trilhões de combinações permanece intacta aqui.
    # Certifique-se de que todas as sub-funções chamadas aqui 
    # também estejam definidas neste arquivo.
    
    poema_gerado = [] 
    # ... (sua lógica original de construção do texto)
    
    return poema_gerado

# =================================================================
