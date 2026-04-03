import streamlit as st
import random
import time
import os

# --- bof: funções resgatadas (O Coração) ---

def load_temas(book):
    book_list = []
    path = os.path.join(".", "base", f"rol_{book}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.replace(" ", "")
                book_list.append(line.strip("\n"))
    return book_list

# --- eof: funções resgatadas ---

def page_mini():
    # 1. Carregamento e Segurança
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)

    if st.session_state.mini >= maxy_mini:
        st.session_state.mini = 0

    # 2. Interface de Comando [4, 1, 1, 1, 4]
    foo1, more_col, rand_col, auto_col, foo2 = st.columns([4, 1, 1, 1, 4])

    help_tips = load_help(st.session_state.lang) # Precisa estar no main ou importada
    
    rand_btn = rand_col.button("✻", help=help_tips[1])
    st.session_state.auto = auto_col.checkbox("auto", value=st.session_state.auto)

    if st.session_state.auto:
        st.session_state.talk = False
        st.session_state.vydo = False
        with st.sidebar:
            # Uso do translate() conforme seu original
            wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60, 10)

    # 3. Lógica do Sorteio
    if rand_btn:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]
    analise = say_number(st.session_state.tema)
    more_btn = more_col.button("✚", help=help_tips[4] + " • " + analise)

    if more_btn:
        st.session_state.rand = False

    # 4. Fluxo de Exibição (Manual ou Auto)
    lnew = True
    if st.session_state.vydo:
        lnew = False
        show_video("mini")
        update_readings("video_mini")
        st.session_state.vydo = False

    mini_place_holder = st.empty()
    st.write("") # Espaçador original

    if lnew or st.session_state.auto:
        # Loop para suportar o Modo Auto ou execução única Manual
        # No Streamlit, o 'while auto' precisa de cuidado para não travar a UI
        
        primeira_execucao = True
        while st.session_state.auto or primeira_execucao:
            if st.session_state.rand:
                st.session_state.mini = random.randrange(0, maxy_mini)
                st.session_state.tema = temas_list[st.session_state.mini]

            # Lógica de Tradução / Carga do Poema
            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()
            else:
                # Onde a máchina gera o verso
                load_poema(st.session_state.tema, "") 
                curr_ypoema = load_lypo()

            if st.session_state.lang != "pt":
                curr_ypoema = translate(curr_ypoema)
                # ... (lógica de gravação do TYPO_user omitida mas mantida)
            
            # Preparação Visual
            update_readings(st.session_state.tema)
            LOGO_TEXTO = curr_ypoema
            LOGO_IMAGE = load_arts(st.session_state.tema) if st.session_state.draw else None

            # Renderização no Palco
            with mini_place_holder.container():
                mini_place_holder.empty()
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

            if st.session_state.talk and not st.session_state.auto:
                talk(curr_ypoema)

            if not st.session_state.auto:
                break # Sai do loop se for manual
            
            # Contagem regressiva do Auto
            primeira_execucao = False
            secs = wait_time
            while secs >= 0 and st.session_state.auto:
                time.sleep(1)
                secs -= 1
            
            if st.session_state.auto:
                st.session_state.rand = True # Sorteia novo para o próximo ciclo
