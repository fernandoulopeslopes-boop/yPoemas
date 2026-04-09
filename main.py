import streamlit as st
import streamlit.components.v1 as components
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=46 (EXTIRPAÇÃO DO VÁCUO + ALINHAMENTO CIRÚRGICO + ST.IFRAME)
# REGRA_ZERO: Foco na hospitalidade imediata e precisão geométrica.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

DICI_LANG = {
    'Português': 'pt', 'Español': 'es', 'Italiano': 'it', 
    'Français': 'fr', 'English': 'en', 'Català': 'ca',
    'Deutsch': 'de', 'Galego': 'gl', 'Română': 'ro'
}

def aplicar_estetica_v46():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            /* EXTIRPAÇÃO DO BLOCO SUPERIOR */
            .main .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top: -125px !important; 
            }
            
            /* Neutralização de Gaps Nativos do Streamlit */
            [data-testid="stVerticalBlock"] > div { gap: 0rem !important; }
            [data-testid="stElementContainer"] { margin-bottom: -1.5rem !important; }

            /* COCKPIT FIXO */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: white; z-index: 999;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
                padding-bottom: 5px;
            }
            
            .stButton > button { 
                border-radius: 50% !important; width: 36px !important; height: 38px !important; 
                background: white !important; border: 1px solid #eee !important;
            }
            
            /* SELECTBOX: Geometria sob os botões 2 e 3 */
            div[data-testid="stSelectbox"] label { display: none !important; }
            div[data-testid="stSelectbox"] { margin-top: -8px !important; }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout
