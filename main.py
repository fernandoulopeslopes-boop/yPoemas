import streamlit as st
import extra_streamlit_components as stx
import os
import random
import asyncio
import edge_tts

# --- CONFIGURAÇÃO E ESTADO INICIAL ---
def init_session():
    defaults = {
        "lang": "pt",
        "last_lang": "pt",
        "eureka": 0,
        "tema": "geral",
        "off_book": 0,
        "off_take": 0,
        "book": "livro vivo",
        "poly_take": 0,
        "poly_file": "poly.txt",
        "draw": True,
        "talk": False,
        "poly_name": "Português",
        "poly_lang": "pt"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# --- FUNÇÃO DE VOZ (EDGE-TTS) ---
def talk(text):
    """Gera e reproduz áudio usando vozes neurais do Edge."""
    async def speak():
        # Mapeamento básico de vozes por idioma (pode ser expandido)
        voices = {
            "pt": "pt-BR-AntonioNeural",
            "en": "en-US-GuyNeural",
            "es": "es-ES-AlvaroNeural",
            "fr": "fr-FR-HenriNeural",
            "it": "it-IT-DiegoNeural"
        }
        selected_voice = voices.get(st.session_state.lang, "pt-BR-AntonioNeural")
        
        # Limpa HTML básico para a leitura não soletrar as tags
        clean_text = text.replace("<br>", " ").replace("➪", "seta")
        
        communicate = edge_tts.Communicate(clean_text, selected_voice)
        output_path = "./temp/output.mp3"
        
        # Garante que a pasta temp existe
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
            
        await communicate.save(output_path)
        st.audio(output_path)

    if text:
        asyncio.run(speak())

# --- PÁGINAS DO SISTEMA ---

def page_eureka():
    help_tips = load_help(st.session_state.lang)
    help_rand, help_more = help_tips[1], help_tips[4]

    seed, more_col, rand_col, manu_col, occurrences = st.columns([2.5, 1.5, 1.5, 0.7, 4])

    with seed:
        find_what = st.text_input(label=translate("digite algo para buscar..."))

    btn_more = more_col.button("✚", help=help_more)
    btn_rand = rand_col.button("✻", help=help_rand)
    btn_manu = manu_col.button("?", help="help !!!")

    if btn_manu:
        st.subheader(load_md_file("MANUAL_EUREKA.md"))

    if len(find_what) < 3:
        st.warning(translate("digite pelo menos 3 letras..."))
        return

    seed_list = []
    soma_tema = []
    eureka_list = load_eureka(find_what)

    for line in eureka_list:
        this_line = line.strip("\n")
        palas, _, fonte = this_line.partition(" : ")
        if not palas or not fonte:
            continue
        seed_list.append(f"{palas} ➪ {fonte}")
        seed_tema = fonte[0:-5]
        if seed_tema not in soma_tema:
            soma_tema.append(seed_tema)

    if not btn_more and not btn_manu:
        st.session_state.eureka = 0

    if not seed_list:
        st.warning(translate(f'nenhuma ocorrência de "{find_what}" encontrada...'))
        return

    seed_list.sort()
    
    if btn_rand:
        st.session_state.eureka = random.randrange(0, len(seed_list))

    with occurrences:
        info_find = translate('ocorrência de "') if len(seed_list) == 1 else translate('ocorrências de "')
        label = f"↓ {len(seed_list)} {info_find}{find_what}"
        if len(soma_tema) > 1:
            label += f"\" em {len(soma_tema)} temas"

        opt_ocur = st.selectbox(
            label,
            range(len(seed_list)),
            index=st.session_state.eureka,
            format_func=lambda y: seed_list[y],
            key="sb_eureka"
        )
        st.session_state.eureka = opt_ocur

    this_seed = seed_list[st.session_state.eureka]
    _, _, nome_tema = this_seed.partition(" ➪ ")
    seed_tema = nome_tema[0:-5]
    st.session_state.tema = seed_tema

    if st.session_state.lang != st.session_state.last_lang:
        curr_ypoema = load_lypo()
    else:
        load_poema(seed_tema, this_seed)
        curr_ypoema = load_lypo()

    if st.session_state.lang != "pt":
        curr_ypoema = translate(curr_ypoema)
        curr_ypoema = curr_ypoema.replace('\r\n', '\n')

    with st.expander("", expanded=True):
        img = load_arts(seed_tema) if st.session_state.draw else None
        write_ypoema(curr_ypoema, img)
        update_readings(seed_tema)

    if st.session_state.talk:
        talk(curr_ypoema)

# [As demais funções de página: page_off_machina, page_polys, page_books, page_abouts permanecem as mesmas do segura.py anterior]

# --- MAPEAMENTO DE NAVEGAÇÃO ---

PAGES = {
    "1": {"func": page_mini, "img": "img_mini.jpg", "info": "INFO_MINI.md"},
    "2": {"func": page_ypoemas, "img": "img_ypoemas.jpg", "info": "INFO_YPOEMAS.md"},
    "3": {"func": page_eureka, "img": "img_eureka.jpg", "info": "INFO_EUREKA.md"},
    "4": {"func": page_off_machina, "img": "img_off-machina.jpg", "info": "INFO_OFF-MACHINA.md"},
    "5": {"func": page_books, "img": "img_books.jpg", "info": "INFO_BOOKS.md"},
    "6": {"func": page_polys, "img": "img_poly.jpg", "info": "INFO_POLY.md"},
    "7": {"func": page_abouts, "img": "img_about.jpg", "info": "INFO_ABOUT.md"},
}

def main():
    init_session()

    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id=1, title="mini", description=""),
            stx.TabBarItemData(id=2, title="yPoemas", description=""),
            stx.TabBarItemData(id=3, title="eureka", description=""),
            stx.TabBarItemData(id=4, title="off-machina", description=""),
            stx.TabBarItemData(id=5, title="books", description=""),
            stx.TabBarItemData(id=6, title="poly", description=""),
            stx.TabBarItemData(id=7, title="about", description=""),
        ],
        default=2,
    )

    pick_lang()
    draw_check_buttons()

    page_data = PAGES.get(str(chosen_id))
    if page_data:
        st.sidebar.info(load_md_file(page_data["info"]))
        with st.sidebar:
            st.image(page_data["img"])
        page_data["func"]()

    show_icons()

if __name__ == "__main__":
    main()
