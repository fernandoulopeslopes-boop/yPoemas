import streamlit as st
import os
import lay_2_ypo as coração

# --- configurações de ui ---
st.set_page_config(layout="wide", page_title="machina de fazer poesia")

# css: estética lower case e sidebar de 300px
st.markdown(
    """
    <style>
        html, body, [class*="css"], .stButton button, p, div, span {
            text-transform: lowercase !important;
        }
        
        [data-testid="stSidebar"] { 
            width: 300px; 
            max-width: 300px; 
        }

        .stButton button { 
            width: 100%; 
            border-radius: 20px; 
            height: 3em;
            font-weight: normal;
            border: 1px solid #ddd;
            background-color: transparent;
        }

        .poema-container { 
            font-family: 'georgia', serif; 
            line-height: 1.8; 
            font-size: 1.3rem; 
            padding: 40px 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def carregar_idiomas_cpc():
    return ["português", "english", "español", "français", "italiano", "deutsch", "nederlands", "dansk"]

def carregar_ativos():
    try:
        with open("./base/ativos.txt", "r", encoding="utf-8") as f:
            return [line.split(":")[0].strip() for line in f if line.strip() and not line.startswith("#")]
    except:
        return ["machina"]

def main():
    lista_idiomas = carregar_idiomas_cpc()
    lista_temas = carregar_ativos()

    # --- sidebar (apenas o essencial para o leitor) ---
    with st.sidebar:
        st.markdown("### machina")
        
        # seletor de idiomas (topo)
        idioma = st.selectbox(" ", options=lista_idiomas, index=0, label_visibility="collapsed")
        
        st.divider()
        
        # --- área reservada ---
        # aqui entrarão: imagem_da_pagina, page_info e redes sociais
        st.empty() 

    # --- palco principal ---
    
    # seletor de temas (no palco por enquanto, até migrar totalmente)
    tema = st.selectbox(" ", options=lista_temas, index=0, label_visibility="collapsed")
    
    st.write(f"🧬 {tema}")

    # cockpit de sentidos
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
        poema_gerado = coração.gera_poema(tema) 
        st.markdown(f'<div class="poema-container">{poema_gerado.lower()}</div>', unsafe_allow_html=True)
    except Exception:
        st.write(f"a engrenagem {tema.lower()} está em manutenção.")

if __name__ == "__main__":
    main()
