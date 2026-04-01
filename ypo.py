import streamlit as st
import os
import random
import streamlit.components.v1 as components

# 1. CONFIGURAÇÃO DE BASE
st.set_page_config(page_title="yPoemas", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        .stButton>button { width: 100%; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

try:
    from lay_2_ypo import gera_poema
except:
    def gera_poema(t, s=""): return ["Motor em manutenção..."]

# 2. A LENTE (HTML)
def write_ypoema(TITULO, TEXTO_RAW, URL_IMAGEM=None):
    if isinstance(TEXTO_RAW, list):
        linhas = [str(l).strip() for l in TEXTO_RAW if str(l).strip()]
        TEXTO_RAW = "\n".join(linhas)
    
    html = f"""
    <div style="display: flex; gap: 40px; font-family: 'Crimson Pro', serif;">
        <div style="flex: 2.5;">
            <h1 style="font-size: 40px; margin-bottom: 20px;">{TITULO}</h1>
            <div style="font-size: 30px; line-height: 1.25; white-space: pre-wrap;">{TEXTO_RAW}</div>
        </div>
        <div style="flex: 1.2; text-align: right;">
            {f'<img src="{URL_IMAGEM}" style="max-width:100%; border-radius:8px;">' if URL_IMAGEM else ""}
        </div>
    </div>
    """
    components.html(html, height=1200, scrolling=True)

# 3. LÓGICA DE DADOS
if "take" not in st.session_state:
    st.session_state.update({'tema': 'Fatos', 'take': 0, 'book': "livro vivo"})

def load_temas():
    path = os.path.join("base", f"rol_{st.session_state.book}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    return ["Fatos", "Tempo", "Anjos"]

# 4. A SALA (LAYOUT)
def page_ypoemas():
    lista = load_temas()
    idx = st.session_state.take % len(lista)
    st.session_state.tema = lista[idx]

    # --- 4.1 O FAROL: NAVEGAÇÃO DE TOPO (A VITRINE) ---
    v1, n1, n2, n3, n4, n_help, n_lista, v2 = st.columns([2, 0.4, 0.4, 0.4, 0.4, 0.5, 3.5, 2])
    
    with n1: 
        if st.button("✚", key="f_more", help="Gerar nova semente/variação"): st.rerun()
    with n2: 
        if st.button("◀", key="f_back", help="Tema Anterior"):
            st.session_state.take -= 1; st.rerun()
    with n3: 
        if st.button("✻", key="f_rand", help="Exploração Aleatória"):
            st.session_state.take = random.randint(0, 1000); st.rerun()
    with n4: 
        if st.button("▶", key="f_next", help="Próximo Tema"):
            st.session_state.take += 1; st.rerun()
            
    with n_help:
        with st.popover("?", help="Ajuda e Matriz Préfacil"):
            st.markdown("**Matriz: Préfacil**")
            st.caption("Navegação da Machina:")
            st.write("A vitrine à direita é o seu elo com os mundos inexploráveis.")

    with n_lista:
        escolha = st.selectbox("Vitrine", options=lista, index=idx, label_visibility="collapsed", 
                              key="f_sel", help="A Porta do Paraíso: Vitrine de Temas")
        if escolha != st.session_state.tema:
            st.session_state.take = lista.index(escolha); st.rerun()
    
    st.divider()

    # --- 4.2 CONTEÚDO (APENAS LOGO E POEMA) ---
    col_painel, col_palco = st.columns([1.2, 4])
    with col_painel:
        st.image("https://via.placeholder.com/200x100?text=MACHINA", use_column_width=True)
        st.write("---")
        st.info(f"Matriz: {st.session_state.tema}")

    with col_palco:
        poema = gera_poema(st.session_state.tema)
        url = "https://images.unsplash.com/photo-1454117096348-e4abbeae002c?w=500"
        write_ypoema(st.session_state.tema, poema, URL_IMAGEM=url)

# 5. O MOTOR: SIDEBAR COM VARIÁVEIS GLOBAIS
def main():
    with st.sidebar:
        st.title("yPoemas")
        menu = st.radio("Ambiente:", ["Exploração", "Sobre"])
        
        st.divider()
        st.subheader("🌐 Comunicação Global")
        st.selectbox("Idioma da Machina", ["Português", "English", "Español"], key="g_lang", help="Afeta todo o ecossistema")
        
        st.write("---")
        st.checkbox("🔊 Ativar Voz", key="g_voice", help="Leitura automática das obras")
        st.checkbox("🎬 Renderizar Vídeo", key="g_video", help="Interpretação visual cinemática")
        st.checkbox("🖼️ Galeria de Arte", key="g_draw", help="Exibir artes geradas por IA")
        st.button("📋 Info Geral", key="g_info", help="Dados técnicos da Machina")

    if menu == "Exploração": page_ypoemas()
    else: st.write("### Sobre o Micro-ambiente")

if __name__ == "__main__":
    main()
    
