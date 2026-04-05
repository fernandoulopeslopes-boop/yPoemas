import streamlit as st
import os
import re
import time
import random
import base64
import socket

# 1. CONFIGURAÇÃO (OBRIGATÓRIO PRIMEIRO)
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# 2. SEPARAÇÃO E PALCO (CSS)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }
    .main .block-container {
        max-width: 850px;
        padding-left: 3.5rem;
        padding-right: 3.5rem;
        margin: auto;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. TRATAMENTO DO ERRO DE IMPORTAÇÃO (O QUE ESTÁ CAUSANDO A TELA BRANCA)
try:
    from extra_streamlit_components import TabBar as stx
    from datetime import datetime
    from lay_2_ypo import gera_poema
except KeyError as e:
    st.error(f"Arquivo ausente no repositório: {e}")
    st.stop()
except ImportError as e:
    st.error(f"Erro de dependência: {e}")
    st.stop()

### bof: settings
# ... o restante do seu código segue aqui
