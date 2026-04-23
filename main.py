import streamlit as st
import os

# --- Configurações de UI ---
st.set_page_config(layout="wide", page_title="Machina de Fazer Poesia")

# Mantendo o prumo dos 300px
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { width: 300px; max-width: 300px; }
        .stImage img { border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

def carregar_ativos():
    """Lê o mapa da colmeia para montar o seletor"""
    try:
        with open("./base/ativos.txt", "r", encoding="utf-8") as f:
            # Filtra linhas vazias e comentários (#)
            return [line.split(":")[0].strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return ["Machina"] # Fallback se o arquivo sumir

def main():
    # 1. Carregar a lista de temas
    temas = carregar_ativos()

    # --- Sidebar (O Painel de Controle Geral) ---
    with st.sidebar:
        st.title("a Máquina")
        st.subheader("Painel de Controle")
        
        # O Seletor Master
        tema_selecionado = st.selectbox(
            "Escolha o Tema",
            options=temas,
            index=0,
            help="Selecione a engrenagem para iniciar a combinatória."
        )
        
        # Espaço para o futuro Seletor de Idiomas (Google Translator)
        st.divider()
        st.write(f"🧬 **Tema Ativo:** {tema_selecionado}")
        
        # Mantendo o seu expander de engenharia (vazio por enquanto)
        with st.expander(" ", expanded=False):
            st.write("Protocolo: go")

    # --- Área Principal (Área de Impressão) ---
    st.header(f"Impressão: {tema_selecionado}")
    
    # Aqui é onde o lay_2_ypo entrará para 'imprimir' o poema
    st.info(f"Aguardando conexão com o coração (lay_2_ypo) para processar {tema_selecionado}...")

if __name__ == "__main__":
    main()
