import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=34 (MODO QUIET: Topo Zero, Eixo Central e Trindade Latina + English)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

DICI_LANG = {
    'Português': 'pt', 
    'English': 'en', 
    'Español': 'es', 
    'Français': 'fr', 
    'Italiano': 'it'
}

def aplicar_estetica_v34():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            .main .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top: -50px !important; 
            }
            
            .stApp { background-color: #ffffff; }

            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 5px 0 2px 0;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            .stButton > button { 
                border-radius: 50% !important; width: 38px !important; height: 38px !important; 
                border: 1px solid #eee !important; background: white !important; 
                margin-bottom: 2px !important;
            }

            div[data-testid="stSelectbox"] { 
                width: 180px !important; 
                margin: 0 auto !important;
            }

            .main-content { 
                margin-top: 110px; 
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                justify-content: flex-start;
