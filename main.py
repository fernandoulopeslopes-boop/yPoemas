import streamlit as st
import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import os

# --- MOTOR DE APOIO ---
def t(texto, sigla_destino="pt"):
    protecao = {
        "arte": {"pt": "arte", "es": "arte", "it": "arte", "fr": "art", "en": "art", "ca": "art", "gl": "arte"},
        "som": {"pt": "som", "es": "sonido", "it": "suono", "fr": "son", "en": "sound"},
        "idiomas disponíveis": {"pt": "idiomas disponíveis", "es": "idiomas disponibles", "it": "lingue disponíveis", "en": "available languages"}
    }
    chave = texto.lower().strip()
    if chave in protecao and sigla_destino in protecao[chave]:
        return protecao[chave][sigla_destino]
    try:
        return GoogleTranslator(source='auto', target=sigla_destino).translate(texto).lower()
    except:
        return texto.lower()

def main():
    # 1. ESTADOS
    if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = "mini"
    if 'sigla_atual' not in st.session_state: st.session_state.sigla_atual = "pt"

    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    # 2. CSS DE ALTA ESPECIFICIDADE
    # O segredo aqui é o uso de "data-testid" e seletores descendentes diretos
    st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{ width: 100vw !important; }}
            [data-testid="stSidebar"] {{ min-width: 300px !important; width: 300px !important; }}
            
            /* 1. RESET DE TODOS OS BOTÕES DA NAVEGAÇÃO */
            div.stButton > button {{
                border: none !important;
                background-color: transparent !important;
                box-shadow: none !important;
                padding: 0px !important;
                min-height: 40px !important;
            }}

            /* 2. TAMANHO PADRÃO (18px) - Para todas as páginas */
            div.stButton > button div[data-testid="stMarkdownContainer"] p {{
                font-size: 18px !important;
                color: #888888 !important;
                transition: all 0.3s ease;
            }}

            /* 3. FOCO DINÂMICO (24px) - Aplicado via identificação do texto */
            /* Este bloco força o aumento real da fonte na página ativa */
            div.stButton > button:has(p:contains("{big_page_atual}")) div[data-testid="stMarkdownContainer"] p {{
                font-size: 24px !important;
                color: #ffffff !important;
                font-weight: bold !important;
            }}

            /* 4. HOVER - Garante que não fique invisível */
            div.stButton > button:hover p {{
                color: #ffffff !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    # 3. SIDEBAR (CONTROL CENTER)
    # [Mantendo lógica de idiomas do resumo para consistência]
    mapa_linguas = {
        "Português": ("pt", "pt-BR-AntonioNeural"), "Espanhol": ("es", "es-ES-AlvaroNeural"),
        "Inglês": ("en", "en-US-GuyNeural"), "Latim": ("la", "it-IT-DiegoNeural")
    }
    
    with st.sidebar:
        # Texto do seletor conforme manual: "idiomas disponíveis"
        st.selectbox("idiomas disponíveis", list(mapa_linguas.keys()))
        
        st.divider()
        # Botões obrigatórios: "arte" e "som"
        c1, c2 = st.columns(2)
        with c1: st.button("🎨 arte")
        with c2: st.button("🔊 som")

    # 4. PALCO: NAVEGAÇÃO COM COLUNAS DINÂMICAS
    # Usamos larguras de coluna diferentes para dar espaço ao texto de 24px
    cols = st.columns([1.6 if pg == big_page_atual else 1 for pg in paginas])
    
    for i, pg in enumerate(paginas):
        with cols[i]:
            # O nome da página deve ser lowercase conforme plano de páginas
            if st.button(pg.lower(), key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # 5. ÁREA DE CONTEÚDO
    with st.container(border=True):
        st.write(f"Conteúdo da página: {big_page_atual}")

if __name__ == "__main__":
    main()
