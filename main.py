import streamlit as st
import random
import os

# --- CONTADOR INTERNO ---
my_tries = 13

# --- CABEÇALHO DE SINCRONIA ---
st.error(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")
st.warning("MODO DE EMERGÊNCIA: CSS REDUZIDO AO MÍNIMO PARA RESTAURAR CLIQUES.")

try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"MOTOR ERROR: {e}")
    def gera_poema(t, s): return "OFFLINE"

# --- CONFIGURAÇÃO E CSS MÍNIMO ---
st.set_page_config(page_title=f"yPoemas #{my_tries}", layout="wide")

st.markdown(f"""
    <style>
    /* Apenas o fundo, sem mexer na camada de botões */
    .stApp {{
        background-color: #000000 !important;
        color: #00ff00 !important;
    }}
    /* Texto verde para visibilidade */
    p, label, span, div {{
        color: #00ff00 !important;
        font-family: monospace !important;
    }}
    /* Esconder o que não interessa */
    header, footer, .stDeployButton {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DA SESSÃO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- ESTRUTURA DE TESTE ---

# 1. Operadores Superiores
c_nav = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with c_nav[i]:
        # Botão padrão (sem CSS customizado)
        if st.button(op, key=f"op_{op}_{my_tries}"):
            if op == "*":
                st.session_state.seed_eureka = str(random.randint(1000, 9999))
                if st.session_state.last_tema:
                    res = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                    st.session_state.output = "\n".join(res) if isinstance(res, list) else res
                st.rerun()

st.markdown("---")

# 2. Palco e Variáveis
c_main, c_vars = st.columns([5, 1])

with c_main:
    # Input padrão
    tema = st.text_input("ARQUIVO", value=st.session_state.last_tema, placeholder="ex: Fatos.ypo", key=f"in_{my_tries}")
    
    if st.button("PROCESSAR AGORA", key=f"proc_{my_tries}"):
        if tema:
            st.session_state.last_tema = tema.strip()
            try:
                res = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            except Exception as e:
                st.session_state.output = f"ERRO: {e}"
            st.rerun()

    # Terminal padrão
    st.text_area("SAÍDA", value=st.session_state.output, height=500, key=f"text_{my_tries}")

with c_vars:
    # Variáveis padrão
    for v in range(1, 11):
        if st.button(f"v{v}", key=f"vbtn_{v}_{my_tries}"):
            st.session_state.seed_eureka = str(v)
            if st.session_state.last_tema:
                res = gera_poema(st.session_state.last_tema, str(v))
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

st.markdown("---")
st.caption(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")
