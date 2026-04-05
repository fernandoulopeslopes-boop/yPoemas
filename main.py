import streamlit as st
import os
import re
import time
import random
import base64
import socket

# 1. CONFIGURAÇÃO (OBRIGATÓRIO SER O PRIMEIRO COMANDO ST)
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# 2. AJUSTE DE LAYOUT: SEPARAÇÃO E PALCO CENTRADO
st.markdown(
    """
    <style>
    /* Separa a sidebar do conteúdo principal */
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }
    /* Centraliza o palco e evita o encavalamento */
    .main .block-container {
        max-width: 850px;
        padding-left: 3.5rem;
        padding-right: 3.5rem;
        margin: auto;
    }
    /* Oculta menus padrão */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. IMPORTS DE DEPENDÊNCIAS
from extra_streamlit_components import TabBar as stx
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        pass
    try:
        from gtts import gTTS
    except ImportError:
        pass

# Endereço IP
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# [O RESTANTE DO SEU CÓDIGO ORIGINAL - FUNÇÕES E CHAMADA DA PÁGINA - SEGUE ABAIXO]
