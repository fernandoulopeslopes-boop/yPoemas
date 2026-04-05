import streamlit as st
import os
import re
import time
import random
import base64
import socket

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

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

### bof: settings
# ... segue o restante do código exatamente como está no seu Marco Zero
