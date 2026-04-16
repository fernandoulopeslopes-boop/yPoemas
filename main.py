import streamlit as st

# --- [ CONFIGURAÇÃO DE ESTADO E PERSISTÊNCIA ] ---
if 'livro_idx' not in st.session_state: st.session_state.livro_idx = 0
if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
if 'idioma_idx' not in st.session_state: st.session_state.idioma_idx = 0
if 'intruso_detectado' not in st.session_state: st.session_state.intruso_detectado = False

# --- [ DADOS DE NAVEGAÇÃO ] ---
lista_livros = ["Vivo", "Poesia", "Ensaios", "Jocosos", "Muerte", "Poly"]
lista_temas = ["Ais", "Amare", "Babel", "Tempo", "Victor", "Zelo"]
lista_idiomas = ["Português", "English", "Español", "Français", "Italiano", "Deutsch"]

# --- [ SIDEBAR: NAVEGAÇÃO E CONTROLE ] ---
with st.sidebar:
    st.title("yPoemas @ Machina")
    
    # Seleção de Livros
    escolha_livro = st.selectbox("Escolha o iLivro", lista_livros, 
                                 index=st.session_state.livro_idx, key="sb_livro")
    
    # Seleção de Temas
    escolha_tema = st.selectbox("Escolha o Tema", lista_temas, 
                                 index=st.session_state.tema_idx, key="sb_tema")
    
    st.markdown("---")
    
    # Seleção de Idiomas (Tradução Imediata)
    escolha_idioma = st.selectbox("Idioma do Palco", lista_idiomas, 
                                   index=st.session_state.idioma_idx, key="sb_idioma")

# Sincronização de Índices para o Rerun
st.session_state.livro_idx = lista_livros.index(st.session_state.sb_livro)
st.session_state.tema_idx = lista_temas.index(st.session_state.sb_tema)
st.session_state.idioma_idx = lista_idiomas.index(st.session_state.sb_idioma)

# --- [ O PALCO CENTRAL ] ---

st.title(f"📖 {st.session_state.sb_livro}")
st.write(f"**Tema:** {st.session_state.sb_tema} | **Língua:** {st.session_state.sb_idioma}")

st.markdown("---")

# --- [ DETECÇÃO DE INTRUSO NO PALCO ] ---
# Se houver inserção de texto sem consulta prévia (simulado)
texto_intruso = "inserção de textos sem prévia consulta" # Gatilho de violação

with st.container():
    # Saída Oficial da Machina
    st.subheader("yPoema Gerado:")
    st.info(f"O palco está agora operando em {st.session_state.sb_idioma}. A seleção do tema '{st.session_state.sb_tema}' foi processada com sucesso.")
    
    # A Defesa de José Maria dos Santos
    st.markdown(f"**Defesa de José Maria dos Santos:**")
    st.success("A beleza deste ítimo resiste até mesmo à rigidez da tradução.")
    
    # Bloco de Alerta: O Intruso
    st.markdown("---")
    st.warning("⚠️ **ALERTA DE SISTEMA: INTRUSO DETECTADO NO PALCO**")
    st.error(f"TEXTO NÃO HOMOLOGADO: '{texto_intruso}'")
    
    # Resposta Crítica de José Maria ao Intruso
    st.write(f"*José Maria observa a mancha no papel e diz:* 'A A.B.N.P. enviará um fiscal, mas o sentimento não se deixa carimbar por estranhos.'")

st.markdown("---")
st.caption("Copyright © 1983-2026 Nando Lopes - Machina de Fazer Poesia")
