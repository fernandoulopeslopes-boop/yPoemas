import streamlit as st
import random
import os


# 1. ARQUITETURA DE HARDWARE VIRTUAL (Layout Fixo)
st.set_page_config(page_title="a Máquina de Fazer Poesia", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* SIDEBAR: Rigor de 320px */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    /* PALCO: Container de 800px para leitura poética */
    .main .block-container { max-width: 800px !important; padding-top: 2rem; }
    
    /* MENU SUPERIOR: Botões Rosa Circulares 65px */
    div.stButton > button {
        background-color: #ff4b4b; color: white; border-radius: 50% !important;
        width: 65px !important; height: 65px !important; border: none;
        font-weight: bold; font-size: 26px; transition: 0.2s;
        display: flex; align-items: center; justify-content: center;
        margin: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover { background-color: #d33; transform: scale(1.1); rotate: 5deg; }
    
    /* DROP-DOWNS: Estilo Minimalista (Collapsed) */
    .stSelectbox label { display: none; } 
    
    /* DIVISOR: O 'fio de navalha' em gradiente */
    hr { border: 0; height: 1px; background: linear-gradient(to right, transparent, #ff4b4b, transparent); margin: 2rem 0; }
    
    /* VERSOS: Fonte Serifada para o Palco */
    .stSubheader { font-family: 'Georgia', serif; font-weight: 300; text-align: center; color: #1a1a1a; padding: 0.6rem 0; line-height: 1.4; }
    </style>
""", unsafe_allow_html=True)

# 2. MOTOR DA MACHINA (Filtragem de Quatrilhões de Verbetes)
def motor_v30(tema):
    try:
        caminho = f"data/{tema}.ypo"
        if not os.path.exists(caminho): return [f"Palco {tema} não encontrado."]
        
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
        
        poema = []
        for l in linhas:
            t = l.strip()
            # O Algoritmo agora identifica o que é POESIA e o que é CÓDIGO/BUILD
            if (not t or t.startswith(("#", "*-", "<EOF>")) or 
                t == "F" or t.isdigit() or "_" in t):
                continue
            
            # Escolha aleatória nos ítimos separados por pipe
            poema.append(random.choice(t.split("|")) if "|" in t else t)
        return poema
    except Exception as e:
        return [f"Erro de processamento: {e}"]

# 3. SIDEBAR (Configurações e Menu de Ação)
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>ツ Machina</h1>", unsafe_allow_html=True)
    
    # Menu Idiomas (O topo da sidebar)
    st.selectbox("Idioma", ["Português", "English", "Español", "Français", "Italiano"], key="lang_sel")
    
    st.markdown("---")
    
    # Drop-down de Temas (Palcos)
    try:
        arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        tema_atual = st.selectbox("Tema", arquivos, index=0, key="tema_sel")
    except:
        st.error("Pasta /data não encontrada.")
    
    st.markdown("---")
    # Botões de Ação
    c1, c2 = st.columns(2)
    c1.button("Talk", key="tk_btn")
    c2.button("Arte", key="art_btn")
    st.button("Share", key="sh_btn", use_container_width=True)

# 4. NAVEGAÇÃO SUPERIOR (Centralizada no Palco)
nav = st.columns(5)
icones = ["+", "<", "*", ">", "?"]
for i, col in enumerate(nav):
    with col:
        st.button(icones[i], key=f"nav_{i}")

# 5. O PALCO (Apresentação Final)
st.markdown("<hr>", unsafe_allow_html=True)

# Execução do motor e renderização dos subheaders
versos_finais = motor_v30(st.session_state.get("tema_sel", "Mirante"))
for verso in versos_finais:
    st.subheader(verso)

st.markdown("<hr>", unsafe_allow_html=True)
