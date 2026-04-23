import streamlit as st
import os
import lay_2_ypo as coração  # O motor combinatório

# --- Configurações de UI ---
st.set_page_config(layout="wide", page_title="machina de fazer poesia")

# CSS: lower case total e limpeza da sidebar
st.markdown(
    """
    <style>
        /* Importante: forçando o lower case em elementos globais */
        html, body, [class*="css"], .stButton button, p {
            text-transform: lowercase;
        }
        
        [data-testid="stSidebar"] { 
            width: 300px; 
            max-width: 300px; 
        }
        
        /* Estilo dos botões no palco */
        .stButton button { 
            width: 100%; 
            border-radius: 20px; 
            height: 3em;
            font-weight: normal;
            border: 1px solid #ddd;
            background-color: transparent;
        }
        
        .poema-container { 
            font-family: 'Georgia', serif; 
            line-height: 1.8; 
            font-size: 1.3rem; 
            padding: 20px;
        }
        
        /* Remove ruídos visuais extras da sidebar */
        [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

def carregar_ativos():
    try:
        with open("./base/ativos.txt", "r", encoding="utf-8") as f:
            return [line.split(":")[0].strip() for line in f if line.strip() and not line.startswith("#")]
    except:
        return ["machina"]

def main():
    temas = carregar_ativos()

    # --- sidebar (painel de controle silencioso) ---
    with st.sidebar:
        st.markdown("### machina")
        
        # seletor sem labels, apenas a escolha
        tema = st.selectbox(" ", options=temas, index=0, label_visibility="collapsed")
        
        st.divider()
        st.write(f"🧬 {tema.lower()}")
        
        # protocolo invisível
        with st.expander(" ", expanded=False):
            st.write("ptc: go")

    # --- cockpit no palco (área principal) ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("arte"): 
            st.session_state.modo = "arte"
    with col2:
        if st.button("som"):
            st.session_state.modo = "som"

    st.divider()

    # --- área de impressão ---
    try:
        # impressão da variação poética
        poema_gerado = coração.gera_poema(tema) 
        st.markdown(f'<div class="poema-container">{poema_gerado.lower()}</div>', unsafe_allow_html=True)
        
    except Exception:
        st.write(f"a engrenagem {tema.lower()} está em manutenção.")

    # --- TODO: lógica de fallback para imagens ---
    # se não houver {tema}.jpg, carregar machina.jpg

if __name__ == "__main__":
    main()
