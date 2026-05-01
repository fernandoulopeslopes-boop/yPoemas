import streamlit as st
import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import os

# --- MOTOR DE TRADUÇÃO E VOZ (Protocolo yPoemas) ---
def t(texto, sigla_destino="pt"):
    protecao = {
        "arte": {"pt": "arte", "es": "arte", "it": "arte", "fr": "art", "en": "art", "ca": "art", "gl": "arte"},
        "som": {"pt": "som", "es": "sonido", "it": "suono", "fr": "son", "en": "sound"},
        "idiomas disponíveis": {"pt": "idiomas disponíveis", "es": "idiomas disponibles", "it": "lingue disponibili", "en": "available languages"}
    }
    chave = texto.lower().strip()
    if chave in protecao and sigla_destino in protecao[chave]:
        return protecao[chave][sigla_destino]
    try:
        return GoogleTranslator(source='auto', target=sigla_destino).translate(texto).lower()
    except:
        return texto.lower()

def main():
    # 1. ESTADOS (A Identidade da Machina)
    if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = "mini"
    if 'sigla_atual' not in st.session_state: st.session_state.sigla_atual = "pt"

    # Nomes originais preservados
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    # 2. CSS DE ALTA ESPECIFICIDADE (Teste: 22px)
    st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{ width: 100vw !important; }}
            [data-testid="stSidebar"] {{ min-width: 300px !important; width: 300px !important; }}
            
            /* Reset de Botão */
            div.stButton > button {{
                border: none !important;
                background-color: transparent !important;
                box-shadow: none !important;
                padding: 0px !important;
                width: 100% !important;
            }}

            /* Fonte Base (18px) */
            div.stButton > button p {{
                font-size: 18px !important;
                color: #888888 !important;
                white-space: nowrap !important;
                letter-spacing: -0.3px !important; /* Micro-ajuste de compressão */
                transition: all 0.3s ease;
            }}

            /* FOCO TIPOGRÁFICO: REDUÇÃO PARA 22px */
            div.stButton > button:has(p:contains("{big_page_atual}")) p {{
                font-size: 22px !important; /* O teste de 22px */
                color: #ffffff !important;
                font-weight: bold !important;
                letter-spacing: -0.5px !important;
            }}

            div.stButton > button:hover p {{
                color: #ffffff !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    # 3. SIDEBAR (Control Center)
    with st.sidebar:
        # Texto conforme manual: "idiomas disponíveis"
        st.selectbox("idiomas disponíveis", ["Português", "Espanhol", "Inglês", "Italiano"])
        st.divider()
        c1, c2 = st.columns(2)
        with c1: st.button("🎨 arte") # Labels conforme protocolo
        with c2: st.button("🔊 som")
        
        st.divider()
        # Pensamento e Visão
        path_md = os.path.join(os.getcwd(), "md_files", f"info_{big_page_atual}.md")
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        
        st.divider()
        path_img = os.path.join(os.getcwd(), f"img_{big_page_atual}.JPG")
        if os.path.exists(path_img):
            st.image(path_img, use_column_width=True)

    # 4. PALCO: NAVEGAÇÃO PROPORCIONAL
    # Peso 1.4 para o foco (agora com 22px)
    cols = st.columns([1.4 if pg == big_page_atual else 1 for pg in paginas])
    
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # 5. ÁREA DE CONTEÚDO (Status da Machina)
    with st.container(border=True):
        status = "vida real" if big_page_atual in ["off-machina", "sobre"] else t("em construção", st.session_state.sigla_atual)
        st.info(f"{big_page_atual.upper()} — {status}")

if __name__ == "__main__":
    main()
