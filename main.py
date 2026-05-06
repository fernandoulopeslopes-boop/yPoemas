import os
import json
import streamlit as st
from deep_translator import GoogleTranslator

# ==============================================================================
# 1. CONFIGURAÇÕES DE INTERFACE & LAYOUT
# ==============================================================================
st.set_page_config(layout="wide")

# ==============================================================================
# 2. CARREGAMENTO DE DADOS FONTE (JSON ÚNICO)
# ==============================================================================
@st.cache_data
def carregar_dados_idiomas():
    with open("idiomas.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ==============================================================================
# 3. FUNÇÕES DE SUPORTE (MARKDOWN E IMAGEM)
# ==============================================================================
def ler_conteudo_md(nome_pagina):
    nome_arquivo = f"info_{nome_pagina}.MD"
    caminho_arquivo = os.path.join("md_files", nome_arquivo)
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return f.read()
    return f"*Aviso: Arquivo {nome_arquivo} não encontrado na pasta md_files.*"

def exibir_arte_pagina(nome_pagina):
    nome_imagem = f"img_{nome_pagina}.JPG"
    caminho_imagem = os.path.join("images", nome_imagem)
    if os.path.exists(caminho_imagem):
        st.image(caminho_imagem, use_container_width=True)
    else:
        st.caption(f"*Arte {nome_imagem} não encontrada na pasta \\images*")

# ==============================================================================
# 4. EXECUÇÃO PRINCIPAL (TRAVA DE SEGURANÇA DO STREAMLIT)
# ==============================================================================
if __name__ == "__main__":
    
    # Carregamento estruturado dos idiomas
    dicionario_idiomas = carregar_dados_idiomas()
    LISTA_NOMES = list(dicionario_idiomas.keys())

    # Inicialização do Estado Global
    if "idioma_selecionado" not in st.session_state:
        st.session_state.idioma_selecionado = LISTA_NOMES[0]

    if "contexto_atual" not in st.session_state:
        st.session_state.contexto_atual = None

    # Definição exata da página em foco
    nome_pagina_atual = "mini"

    # Mapeamento fixo dos links das redes sociais
    links_sociais = {
        "facebook": "#",
        "instagram": "#",
        "whatsapp": "https://wa.me/seu_numero",
        "email": "mailto:seu_email@dominio.com"
    }

    # Tradução do rótulo em tempo real
    idioma_atual_nome = st.session_state.idioma_selecionado
    sigla_destino = dicionario_idiomas[idioma_atual_nome]

    try:
        info_da_lista = GoogleTranslator(source="auto", target=sigla_destino).translate("idiomas disponíveis...")
    except Exception:
        info_da_lista = "idiomas disponíveis..."

    # --------------------------------------------------------------------------
    # RENDERIZAÇÃO DA SIDEBAR (300px controlados pelo CSS global)
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("<h3 style='text-align: center;'>Machina</h3>", unsafe_allow_html=True)
        
        # Dropdown dinâmico
        idioma_escolhido = st.selectbox(
            label=info_da_lista,
            options=LISTA_NOMES,
            index=LISTA_NOMES.index(st.session_state.idioma_selecionado),
            key="selector_idiomas_global"
        )
        
        # Alinhamento dos botões de comando nas extremidades
        col_esquerda, col_direita = st.columns(2)
        with col_esquerda:
            if st.button("arte", key="btn_arte_sidebar"):
                st.session_state.contexto_atual = "arte"
                st.rerun()
                
        with col_direita:
            st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
            if st.button("audio", key="btn_audio_sidebar"):
                st.session_state.contexto_atual = "audio"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()
        
        # Renderização do texto e da imagem correspondentes à página atual
        conteudo_md = ler_conteudo_md(nome_pagina_atual)
        st.markdown(conteudo_md)
        
        exibir_arte_pagina(nome_pagina_atual)

    # --------------------------------------------------------------------------
    # CORPO PRINCIPAL DA PÁGINA & RODAPÉ SOCIAL
    # --------------------------------------------------------------------------
    st.title(f"Página: {nome_pagina_atual.capitalize()}")
    
    # Injeção controlada do rodapé estrutural na página principal
    st.markdown(
        f'''
        <div style="text-align: center; margin-top: 100px; padding: 20px; border-top: 1px solid #333;">
            <a href="{links_sociais['facebook']}" target="_blank" style="margin: 0 15px; text-decoration: none;">
                <img src="app/static/btn_face.jpg" width="32" style="border-radius: 50%;">
            </a>
            <a href="{links_sociais['instagram']}" target="_blank" style="margin: 0 15px; text-decoration: none;">
                <img src="app/static/btn_insta.jpg" width="32" style="border-radius: 50%;">
            </a>
            <a href="{links_sociais['whatsapp']}" target="_blank" style="margin: 0 15px; text-decoration: none;">
                <img src="app/static/btn_zap.jpg" width="32" style="border-radius: 50%;">
            </a>
            <a href="{links_sociais['email']}" target="_blank" style="margin: 0 15px; text-decoration: none;">
                <img src="app/static/btn_mail.jpg" width="32" style="border-radius: 50%;">
            </a>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Processamento e atualização de estado se houver interação com o seletor
    if idioma_escolhido != st.session_state.idioma_selecionado:
        st.session_state.idioma_selecionado = idioma_escolhido
        st.rerun()
