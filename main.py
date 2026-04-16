import streamlit as st

# --- [ PROTOCOLO PTC: CONFIGURAÇÃO DE ESTADO ] ---
# Inicialização dos índices para garantir que a navegação seja persistente
if 'livro_idx' not in st.session_state: st.session_state.livro_idx = 0
if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
if 'idioma_idx' not in st.session_state: st.session_state.idioma_idx = 0

# --- [ DADOS DE NAVEGAÇÃO ] ---
# Estes dados devem vir do seu Catálogo e da lista de idiomas ocidentais
lista_livros = ["Vivo", "Poesia", "Ensaios", "Jocosos", "Muerte", "Poly"]
lista_temas = ["Ais", "Amare", "Babel", "Tempo", "Victor", "Zelo"] # Exemplo dinâmico
lista_idiomas = ["Português", "English", "Español", "Français", "Italiano", "Deutsch"]

# --- [ SIDEBAR: O CENTRO DE COMANDO ] ---
with st.sidebar:
    st.title("yPoemas @ Machina")
    st.subheader("Navegação Estruturada")

    # 1. Seleção de Livros
    # O index é alimentado pelo session_state para manter a posição
    escolha_livro = st.selectbox(
        "Escolha o iLivro",
        lista_livros,
        index=st.session_state.livro_idx,
        key="sb_livro"
    )

    # 2. Seleção de Temas
    # Atualização do index do tema para refletir a navegação no palco
    escolha_tema = st.selectbox(
        "Escolha o Tema",
        lista_temas,
        index=st.session_state.tema_idx,
        key="sb_tema"
    )

    st.markdown("---")
    
    # 3. Seleção de Idiomas (Tradução Imediata)
    # A troca aqui dispara a atualização dos componentes que consomem o idioma
    escolha_idioma = st.selectbox(
        "Idioma do Palco",
        lista_idiomas,
        index=st.session_state.idioma_idx,
        key="sb_idioma"
    )

# --- [ LÓGICA DE SINCRONIZAÇÃO ] ---
# Atualizamos os índices no state baseados na interação do usuário para o próximo rerun
st.session_state.livro_idx = lista_livros.index(st.session_state.sb_livro)
st.session_state.tema_idx = lista_temas.index(st.session_state.sb_tema)
st.session_state.idioma_idx = lista_idiomas.index(st.session_state.sb_idioma)

# --- [ O PALCO CENTRAL (ÁREA DE EXIBIÇÃO) ] ---

# Cabeçalho dinâmico que reage ao index selecionado
st.title(f"📖 {st.session_state.sb_livro}")
st.write(f"**Tema atual:** {st.session_state.sb_tema} | **Língua:** {st.session_state.sb_idioma}")

st.markdown("---")

# Espaço reservado para a saída da Machina
with st.container():
    # Aqui o código chamaria o gerador de yPoemas passando o idioma e o tema
    st.subheader("yPoema Gerado:")
    
    # Simulação de tradução e defesa de José Maria dos Santos
    st.info(f"O palco está agora operando em {st.session_state.sb_idioma}. "
            f"A seleção do tema '{st.session_state.sb_tema}' foi processada com sucesso.")
    
    st.markdown(f"**Defesa de José Maria dos Santos:**")
    st.write("A beleza deste ítimo resiste até mesmo à rigidez da tradução.")

st.markdown("---")
st.caption("Copyright © 1983-2022 Nando Lopes - Machina de Fazer Poesia")
