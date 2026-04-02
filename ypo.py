import os
import base64
import streamlit as st
import extra_streamlit_components as stx

# O MOTOR DE GERAÇÃO
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DA PÁGINA (Sempre o primeiro comando)
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# 2. INICIALIZAÇÃO DE ESTADOS
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'poly_lang' not in st.session_state: st.session_state.poly_lang = 'ca'
if 'tema' not in st.session_state: st.session_state.tema = 'Olhares'
if 'poema_atual' not in st.session_state: st.session_state.poema_atual = ""
if 'draw' not in st.session_state: st.session_state.draw = False
if 'talk' not in st.session_state: st.session_state.talk = False

# 3. CSS "DIRETO NO ALVO"
# Este bloco força a largura da sidebar e alinha os botões de idioma
st.markdown(
    '''
    <style>
    /* Força a largura da Sidebar em 310px */
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }
    
    /* Remove espaços inúteis no topo */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Estilização dos Botões de Idioma na Sidebar */
    /* Força os botões em colunas a não quebrarem linha e terem fonte menor */
    div[data-testid="stHorizontalBlock"] > div {
        padding: 0px !important;
        margin: 0px !important;
    }
    
    div[data-testid="stHorizontalBlock"] button {
        padding: 0px !important;
        height: 30px !important;
        min-width: 40px !important;
        font-size: 14px !important;
    }

    /* O Poema com a "cara" da Machina */
    .poem-box {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 600;
        font-size: 19px;
        color: #1a1a1a;
        line-height: 1.6;
        border-left: 6px solid #000;
        padding-left: 20px;
        margin-top: 30px;
        background-color: transparent;
    }
    
    .poem-img-float {
        float: right;
        width: 280px;
        border: 1.5px solid #000;
        margin-left: 20px;
        margin-bottom: 15px;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 4. FUNÇÕES DE EXIBIÇÃO
def render_poema(texto, img_path=None):
    texto_br = texto.replace('\n', '<br>')
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        html = f'''
        <div style="overflow: auto;">
            <img class="poem-img-float" src="data:image/png;base64,{img_data}">
            <div class="poem-box">{texto_br}</div>
        </div>
        '''
    else:
        html = f'<div class="poem-box">{texto_br}</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# 5. SIDEBAR E IDIOMAS
with st.sidebar:
    # Logo ou Título
    if os.path.exists('logo_ypo.png'):
        st.image('logo_ypo.png')
    else:
        st.markdown("## yPoemas")
    
    st.write("---")
    
    # Grid de Idiomas (6 colunas juntas)
    cols = st.columns(6)
    langs = ["pt", "es", "it", "fr", "en", "⚒️"]
    for i, l in enumerate(langs):
        if cols[i].button(l):
            st.session_state.lang = l if l != "⚒️" else st.session_state.poly_lang
            st.rerun()

    st.write(f"**Idioma:** `{st.session_state.lang}`")
    st.write("---")
    
    st.session_state.draw = st.checkbox("imagem", value=st.session_state.draw)
    st.session_state.talk = st.checkbox("áudio", value=st.session_state.talk)

# 6. NAVEGAÇÃO POR ABAS
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="1", title="mini", description=''),
    stx.TabBarItemData(id="2", title="yPoemas", description=''),
    stx.TabBarItemData(id="3", title="eureka", description=''),
    stx.TabBarItemData(id="4", title="off-machina", description=''),
    stx.TabBarItemData(id="5", title="books", description=''),
    stx.TabBarItemData(id="6", title="poly", description=''),
    stx.TabBarItemData(id="7", title="sobre", description=''),
], default="1")

# 7. ROTEAMENTO
if chosen_id == "1":
    # PÁGINA MINI
    st.write("") # Espaçador
    c_btn, c_spacer = st.columns([1, 5])
    
    if c_btn.button("✻", help="Girar a sorte"):
        try:
            # Chama o motor da lay_2_ypo (Capitalize para bater com arquivos Fatos.txt)
            tema_nome = st.session_state.tema.capitalize()
            res = gera_poema(tema_nome, "")
            st.session_state.poema_atual = "\n".join(res)
        except Exception as e:
            st.error(f"Erro no motor: {e}")

    if st.session_state.poema_atual:
        render_poema(st.session_state.poema_atual)
    else:
        st.info("Aguardando o toque da estrela (✻).")

else:
    st.warning(f"Aba {chosen_id} em construção.")
