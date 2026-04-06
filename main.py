Você tem razão. Eu me distraí com a técnica e ignorei o conteúdo que você já havia consolidado. A sintonia quebrou porque eu substituí o seu **recheio real** (os 48 temas e os milhões de combinações que compõem a verdadeira Machina) por esse "placeholder" genérico de 3 linhas.

Para retomar o prumo, aqui está o `main.py` com a estrutura de layout corrigida (sem encavalamento), o motor de busca blindado, e o **espaço sagrado** para o seu dicionário completo. 

**Importante:** Como eu não tenho o texto integral de todos os seus 48 temas aqui nesta mensagem, deixei o bloco `DIC_TEMAS` aberto para você colar o seu conteúdo real do `ypo_old.py`.

```python
import streamlit as st
import random
import os
from pathlib import Path

# --- [ PROTOCOLO DE SEGURANÇA E DISPARO v1.8.2 ] ---
# Recomposição da Sintaxe e do Recheio Original.
# Foco: Estabilidade de layout e fidelidade ao conteúdo do usuário.

st.set_page_config(
    page_title="Machina yPoemas",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS: ESTABILIZAÇÃO DO PALCO (SEM ENCAVALAMENTO) ---
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-right: 5rem;
        padding-left: 5rem;
        max-width: 1000px;
    }
    section[data-testid="stSidebar"] {
        width: 350px !important;
        background-color: #f0f2f6;
    }
    .poesia-box {
        font-family: 'Courier New', Courier, monospace;
        font-size: 26px;
        line-height: 1.5;
        color: #2c3e50;
        padding: 50px;
        border-left: 8px solid #fffd01;
        background-color: #ffffff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-top: 20px;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE BUSCA: O BAÚ DE JACARANDÁ (OFF-MACHINA) ---
def load_off_content(file_target):
    path_off = Path(__file__).parent / "off_machina"
    if not path_off.exists():
        return "Erro: Pasta 'off_machina' não encontrada."

    def normalize(text):
        return text.lower().replace("ú", "u").replace("á", "a").replace("é", "e").strip()

    target_norm = normalize(file_target)
    
    try:
        for item in path_off.iterdir():
            if normalize(item.name) == target_norm:
                with open(item, "r", encoding="utf-8") as f:
                    return f.read()
    except Exception as e:
        return f"Erro de leitura: {e}"
    
    return f"O arquivo '{file_target}' não reside no baú."

# --- ESTRUTURA DE DADOS: O CORAÇÃO DA MACHINA (COLE SEUS 48 TEMAS AQUI) ---
# Substitua as linhas abaixo pelo conteúdo integral do seu dicionário original.
DIC_TEMAS = {
    "LINGUAFIADA": [
        "O Si grave ressoa...",
        "No baú de jacarandá",
        "A violinista espera."
    ],
    # Adicione aqui os demais temas (HONESTO, VIOLINO, etc.) do seu ypo_old.py
}

# --- SIDEBAR: NAVEGAÇÃO ---
with st.sidebar:
    st.title("Machina yPoemas")
    st.markdown("---")
    menu_choice = st.radio(
        "Navegação:",
        ["O Palco (Home)", "O Manual (About)"]
    )
    st.markdown("---")
    st.caption("v1.8.2 - Retorno à Essência")
    st.info("Status: Bolo Consolidado.")

# --- PÁGINA 1: O PALCO (HOME) ---
if menu_choice == "O Palco (Home)":
    st.title("A Machina Poética")
    st.write("---")
    
    tema_selecionado = st.selectbox("Selecione o Tema:", list(DIC_TEMAS.keys()))
    
    if st.button("Girar a Machina"):
        # Sorteio do Drope dentro do tema escolhido
        st.session_state.current_poem = random.choice(DIC_TEMAS[tema_selecionado])
    
    if "current_poem" in st.session_state:
        st.markdown(f'<div class="poesia-box">{st.session_state.current_poem}</div>', unsafe_allow_html=True)
    else:
        st.info("Escolha um tema e gire a Machina para revelar a poesia.")

# --- PÁGINA 2: O MANUAL (ABOUT) ---
elif menu_choice == "O Manual (About)":
    st.title("Sobre a Machina")
    aba1, aba2, aba3 = st.tabs(["Inventário", "Arquitetura", "Acessar o Baú"])
    
    with aba1:
        st.markdown("""
        ### **Linguafiada: O Inventário de Achados**
        * **O Baú de Jacarandá:** Repositório do raro.
        * **A Nota Si:** A sensível que atrai.
        * **A Violinista:** O som contínuo no labirinto.
        """)
        
    with aba2:
        st.subheader("Arquitetura do Labirinto")
        st.table([
            {"Círculo": "NÚCLEO", "Elemento": "Drope", "Função": "Átomo da poesia"},
            {"Círculo": "EXTERIOR", "Elemento": "Off-Machina", "Função": "Arquivos .Pip e .md"},
        ])
        
    with aba3:
        st.write("Consulta ao repositório off-machina.")
        query = st.text_input("Buscar no baú:", placeholder="ex: violino.Pip")
        if st.button("Abrir"):
            resultado = load_off_content(query)
            st.code(resultado, language="text")

# --- FIM DO ARQUIVO ---
```
