r"""
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
yPoemas - PAI ORIGINAL (RESTAURAÇÃO DOS COMANDOS DE PALCO)
[BOTÕES DE AÇÃO E NAVEGAÇÃO INTEGRADOS - PTC]
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
"""
import streamlit as st
import os
from deep_translator import GoogleTranslator
# ... (outros imports preservados conforme o PAI)

# --- 🚀 ESTADO ---
if "initialized" not in st.session_state:
    st.session_state.page = 'yPoemas'
    st.session_state.lang = 'pt'
    st.session_state.tema = 'Fatos'
    st.session_state.seed = random.randint(0, 999999)
    st.session_state.initialized = True

# =================================================================
# 📱 FUNÇÕES DE NAVEGAÇÃO E COMANDO (O PALCO REAIS)
# =================================================================

def nav_bar():
    """Menu Superior de Páginas"""
    cols = st.columns([1.2, 1, 1, 1, 1, 1, 1])
    if cols[0].button("📜 yPoemas"): st.session_state.page = "yPoemas"
    if cols[1].button("🧩 Mini"): st.session_state.page = "Mini"
    if cols[2].button("💡 Eureka"): st.session_state.page = "Eureka"
    if cols[3].button("🌍 Poly"): st.session_state.page = "Poly"
    if cols[4].button("📚 Books"): st.session_state.page = "Books"
    if cols[5].button("❓ Ajuda"): st.session_state.page = "Help"
    if cols[6].button("ℹ️ Sobre"): st.session_state.page = "About"
    st.write("---")

def control_bar():
    """Botões de Ação da Machina (✚ ◀ ✻ ▶ ?)"""
    c = st.columns([1,1,1,1,1,1,1,1])
    if c[0].button("✚"): # Novo Poema
        st.session_state.seed = random.randint(0, 999999)
    if c[1].button("◀"): # Anterior
        st.session_state.seed -= 1
    if c[2].button("✻"): # Aleatório
        st.session_state.seed = random.randint(0, 999999)
    if c[3].button("▶"): # Próximo
        st.session_state.seed += 1
    st.write("")

# =================================================================
# 📱 PÁGINAS COM BOTÕES DE OPERAÇÃO
# =================================================================

def page_ypoemas():
    nav_bar()
    control_bar()
    st.write(f"⚫ {st.session_state.lang} | Tema: **{st.session_state.tema}** | Seed: {st.session_state.seed}")
    
    from lay_2_ypo import gera_poema
    script = gera_poema(st.session_state.tema, st.session_state.seed)
    txt = "\n".join(script)
    if st.session_state.lang != "pt":
        txt = GoogleTranslator(source="pt", target=st.session_state.lang).translate(txt)
    
    st.markdown(f"<p class='logo-text'>{txt.replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_mini():
    nav_bar()
    if st.button("⚡ GERAR NOVO MINI"):
        st.session_state.seed = random.randint(0, 999999)
    # Conteúdo funcional do Mini aqui...

def page_eureka():
    nav_bar()
    st.write("### 💡 EXPLORADOR EUREKA")
    c1, c2 = st.columns([3, 1])
    busca = c1.text_input("Digite o termo:")
    if c2.button("🔍 BUSCAR"):
        # Lógica de busca no lexico.pt aqui...
        pass

# ... (About, Help, Books seguem o mesmo padrão de nav_bar + comandos específicos)

# =================================================================
# 🏁 ROTEADOR
# =================================================================
if st.session_state.page == "yPoemas": page_ypoemas()
elif st.session_state.page == "Mini": page_mini()
elif st.session_state.page == "Eureka": page_eureka()
# ... (restante do roteador)
