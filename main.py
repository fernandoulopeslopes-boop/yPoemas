import streamlit as st
import os

# --- 1. BOOTSTRAP (CPC) ---
# Inicialização mandatória de todos os estados para evitar AttributeError
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "sobre"

if 'sub_sobre' not in st.session_state:
    st.session_state.sub_sobre = "ypoemas"

if 'tema' not in st.session_state:
    st.session_state.tema = "default" # ou o tema padrão da Machina

if 'lang_idx' not in st.session_state:
    st.session_state.lang_idx = 3 # francês : fr

# Configuração de layout baseada no estado
sb_state = "collapsed" if st.session_state.pagina_ativa == "sobre" else "expanded"
st.set_page_config(layout="wide", initial_sidebar_state=sb_state)

# --- 2. CENTRO DE CONTROLE (SIDEBAR) ---
def render_sidebar():
    with st.sidebar:
        # 1. IDIOMAS (TRADUÇÃO DINÂMICA)
        label_idiomas = "↓ " + translate("idiomas disponíveis")
        idiomas_list = ["português : pt", "espanhol : es", "italiano : it", "francês : fr", "inglês : en", "catalão : ca"] + \
                       sorted(["alemão : de", "basco : eu", "córsico : co", "dinamarquês : da", 
                               "esperanto : eo", "finlandês : fi", "galego : gl", "galês : cy", 
                               "holandês : nl", "irlandês : ga", "latin : la", "norueguês : no", 
                               "polonês : pl", "romeno : ro", "sueco : sv"])
        
        sel_lang = st.selectbox(label_idiomas, idiomas_list, index=st.session_state.lang_idx, key="main_lang_selector")
        st.session_state.lang_idx = idiomas_list.index(sel_lang)
        st.divider()

        # 2. NAVEGAÇÃO
        c1, c2 = st.columns(2)
        if c1.button("arte", key="btn_arte", use_container_width=True):
            st.session_state.pagina_ativa = "mini"
            st.rerun()
        if c2.button("audio", key="btn_audio", use_container_width=True):
            pass 
        st.divider()

        # 3. CONTEÚDO DINÂMICO (PADRÃO UPPER & MD_FILES)
        tag_foco = st.session_state.sub_sobre if st.session_state.pagina_ativa == "sobre" else st.session_state.pagina_ativa
        tag_upper = tag_foco.upper()

        # INFO em \md_files
        path_info = os.path.join("md_files", f"INFO_{tag_upper}.MD")
        if os.path.exists(path_info):
            with open(path_info, "r", encoding="utf-8") as f:
                st.markdown(f.read().lower())
        
        # IMG em \images
        path_img = os.path.join("images", f"IMG_{tag_upper}.JPG")
        if os.path.exists(path_img):
            st.image(path_img, use_container_width=True)
        st.divider()

        # 4. RODAPÉ SOCIAL
        s1, s2, s3 = st.columns(3)
        s1.markdown("[insta](#)"); s2.markdown("[git](#)"); s3.markdown("[mail](#)")

# --- 3. O FAROL (SOBRE) ---
def page_sobre():
    sobre_list = ["comments", "prefácio", "machina", "off-machina", "outros", "traduttore", "imagens", "samizdát", "notes", "index", "bibliografia", "license"]

    options = list(range(len(sobre_list)))
    sobrios = "↓  " + translate("sobre")
    
    # Busca o índice atual para manter a sincronia
    current_idx = sobre_list.index(st.session_state.sub_sobre.lower()) if st.session_state.sub_sobre.lower() in sobre_list else 0

    opt_sobre = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: sobre_list[x],
        index=current_idx,
        key="opt_sobre",
    )

    choice = sobre_list[opt_sobre].upper()
    st.session_state.sub_sobre = choice.lower()
    
    about_expander = st.expander("", True)
    with about_expander:
        if choice == "MACHINA":
            st.subheader(load_md_file("ABOUT_MACHINA_A.MD"))
            # Agora garantido pelo Bootstrap
            LOGO_TEXTO = load_info(st.session_state.tema)
            LOGO_IMAGE = "./images/matrix/" + st.session_state.tema + ".JPG"
            write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
            st.subheader(load_md_file("ABOUT_MACHINA_D.MD"))
        else:
            st.subheader(load_md_file("ABOUT_" + choice + ".MD"))

# --- 4. EXECUÇÃO (CPC) ---
if __name__ == "__main__":
    render_sidebar()
    
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    elif st.session_state.pagina_ativa == "mini":
        st.empty() # Palco mini aguardando integração
