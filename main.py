import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] MOTOR SOBERANO ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: lay_2_ypo.py não encontrado.\nTema: {t}"

def normalizar_e_traduzir(conteudo, idioma):
    if not conteudo: return ""
    texto_unificado = "\n".join(conteudo) if isinstance(conteudo, list) else conteudo
    texto_final = texto_unificado
    if "Português" not in idioma:
        try:
            codigos = {"ES - Español": "es", "IT - Italiano": "it", "EN - English": "en"}
            target = codigos.get(idioma, 'en')
            texto_final = GoogleTranslator(source='auto', target=target).translate(texto_unificado)
        except Exception: pass
    return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            footer { visibility: hidden; }
            .block-container { padding-top: 0rem !important; }
            div.stButton > button {
                border-radius: 50% !important;
                width: 50px !important;
                height: 50px !important;
                border: 1px solid #333 !important;
                background-color: white !important;
                margin: 0 10px !important;
            }
            .book-header { font-size: 0.85em; font-weight: bold; color: #666; margin-bottom: 2px; font-family: monospace; }
            .page-info { font-size: 0
