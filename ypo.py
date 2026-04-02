# 1. FUNÇÕES DE COMANDO (Devem vir antes da renderização)
def nav_prev(max_idx):
    if st.session_state.take <= 0:
        st.session_state.take = max_idx
    else:
        st.session_state.take -= 1

def nav_next(max_idx):
    if st.session_state.take >= max_idx:
        st.session_state.take = 0
    else:
        st.session_state.take += 1

def nav_rand(max_idx):
    st.session_state.take = random.randint(0, max_idx)

# 2. O PALCO (Dentro da sua função page_ypoemas)
def page_ypoemas():
    # Carrega os temas do ROL
    path = f'./base/rol_{st.session_state.book}.txt'
    temas = [line.strip() for line in open(path, 'r', encoding='utf-8') if line.strip()] if os.path.exists(path) else ["Fatos"]
    max_idx = len(temas) - 1

    # OS 3 BOTÕES (Agora com gatilhos reais)
    _, b_prev_col, b_rand_col, b_next_col, _ = st.columns([3, 1, 1, 1, 3])
    
    # O segredo é o 'on_click': ele executa a função ANTES de recarregar a tela
    b_prev_col.button("◀", on_click=nav_prev, args=(max_idx,))
    b_rand_col.button("✻", on_click=nav_rand, args=(max_idx,))
    b_next_col.button("▶", on_click=nav_next, args=(max_idx,))

    # O Selectbox agora APENAS MOSTRA onde a navegação está
    # Ele não pode mais ser o dono do 'take'
    st.selectbox(
        "↓ Lista de Temas", 
        range(len(temas)), 
        index=st.session_state.take, 
        format_func=lambda x: temas[x],
        key="sync_selector"
    )
    
    # Sincroniza se o usuário mudar no braço pelo Selectbox
    if st.session_state.sync_selector != st.session_state.take:
        st.session_state.take = st.session_state.sync_selector
        st.rerun()

    # RESULTADO NO PALCO
    tema_atual = temas[st.session_state.take]
    poema = gera_poema(tema_atual, "")
    
    st.divider()
    # Exibe o poema e a imagem (se houver)
    img_path = f"./images/machina/{tema_atual}.jpg"
    write_ypoema("<br>".join(poema), img_path if st.session_state.draw else None)
