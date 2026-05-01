import streamlit as st
import os

def main():
    # 1. ESTADOS E DEFINIÇÕES
    if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = "mini"
    
    # Lista de páginas conforme o protocolo
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    # 2. CÁLCULO MATEMÁTICO DE LARGURAS (Proporção por caractere)
    # Referência: 4 letras = 1.0
    pesos = []
    for pg in paginas:
        # Peso base: comprimento da palavra / 4
        peso_base = len(pg) / 4
        # Multiplicador de Foco: se for a página ativa (22px), ganha 20% extra de respiro
        if pg == big_page_atual:
            peso_base *= 1.2
        pesos.append(peso_base)

    # 3. CSS DE ALTA FIDELIDADE
    st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{ width: 100vw !important; }}
            [data-testid="stSidebar"] {{ min-width: 300px !important; width: 300px !important; }}
            
            div.stButton > button {{
                border: none !important;
                background-color: transparent !important;
                padding: 0px !important;
                width: 100% !important;
            }}

            div.stButton > button p {{
                font-size: 18px !important;
                color: #888888 !important;
                white-space: nowrap !important;
                letter-spacing: -0.2px !important;
                transition: all 0.3s ease;
            }}

            /* Foco Tipográfico (22px conforme teste bem-sucedido) */
            div.stButton > button:has(p:contains("{big_page_atual}")) p {{
                font-size: 22px !important;
                color: #ffffff !important;
                font-weight: bold !important;
            }}

            div.stButton > button:hover p {{ color: #ffffff !important; }}
        </style>
    """, unsafe_allow_html=True)

    # 4. SIDEBAR (CONTROL CENTER)
    with st.sidebar:
        st.selectbox("idiomas disponíveis", ["Português", "Espanhol", "Inglês"])
        st.divider()
        c1, c2 = st.columns(2)
        with c1: st.button("🎨 arte")
        with c2: st.button("🔊 som")
        
        # Inserção dinâmica de MD e JPG conforme o manual
        path_md = os.path.join(os.getcwd(), "md_files", f"info_{big_page_atual}.md")
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # 5. PALCO COM LÓGICA DE PROPORÇÃO MATEMÁTICA
    cols = st.columns(pesos)
    
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # 6. CONTAINER DE STATUS
    with st.container(border=True):
        st.info(f"{big_page_atual.upper()}")

if __name__ == "__main__":
    main()
