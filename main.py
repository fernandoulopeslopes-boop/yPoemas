import streamlit as st
import os
import re
import time
import random
import base64
import socket

# 1. ORDEM OBRIGATÓRIA PARA STREAMLIT
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# 2. SEPARAÇÃO DE LAYOUT
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
    </style>
    """,
    unsafe_allow_html=True,
)

from extra_streamlit_components import TabBar as stx
from datetime import datetime
from lay_2_ypo import gera_poema

# 3. TESTE DE RENDERIZAÇÃO IMEDIATA
st.write("Máquina de Poesia Ativa")

### bof: settings
# ... restante do seu código
