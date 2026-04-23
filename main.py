import streamlit as st
import os
import lay_2_ypo as coração  # O motor combinatório

# --- Configurações de UI ---
st.set_page_config(layout="wide", page_title="Machina de Fazer Poesia")

# CSS: Foco na limpeza e na largura fixa de 300px
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { width: 300px; max-width: 300px; }
        .stButton button { 
            width: 100%; 
            border-radius: 20px; 
            height: 3em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .poema-container { 
            font-family: 'Georgia', serif; 
            line-height: 1.8; 
            font-size: 1.3rem; 
            padding: 20px;
            background-color: transparent;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def carregar_ativos():
    try:
        with open("./base/ativos.txt", "r", encoding="utf-8") as f:
            return [line.split(":")[0].strip() for line in f if line.strip() and not line.startswith("#")]
    except:
        return ["Machina"]

def main():
    temas = carregar_ativos()

    # --- Sidebar (O Painel de Controle Silencioso) ---
    with st.sidebar:
        st.title("a Máquina")
        # Descoberta pura: apenas o seletor, sem rótulos.
        tema = st.selectbox(" ", options=temas, index=0, label_visibility="collapsed")
        
        st.divider()
        st.write(f"🧬 {tema}")
        
        # Protocolo invisível
        with st.expander(" ", expanded=False):
            st.write("ptc: go")

    # --- Cockpit Binário (Topo da Área Principal) ---
    col1, col2 = st.columns(2)
    with col1:
        btn_arte = st.button("Arte") # Ajustado conforme CPC
    with col2:
        btn_som = st.button("Som")

    st.divider()

    # --- Área de Impressão ---
    try:
        # A variação do poema surge aqui
        poema_gerado = coração.gera_poema(tema) 
        st.markdown(f'<div class="poema-container">{poema_gerado}</div>', unsafe_allow_html=True)
        
    except Exception:
        st.error(f"A engrenagem {tema} está em manutenção.")

    # --- Lógica de Exibição de Arte (O Próximo Passo) ---
    if btn_arte:
        # Aqui injetaremos o try/except para carregar {tema}.jpg ou Machina.jpg
        pass

if __name__ == "__main__":
    main()
