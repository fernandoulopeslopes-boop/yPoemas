import streamlit as st
import os

# --- 0. MOTORES DA MACHINA (SUPORTE) ---
def translate(texto):
    traducoes = {
        "idiomas disponíveis": "idiomas disponíveis",
        "sobre": "sobre",
        "guia de navegação documental": "guia de navegação documental"
    }
    return traducoes.get(texto.lower(), texto)

def load_md_file(filename):
    """Carrega arquivos md respeitando a extensão informada."""
    path = os.path.join("md_files", filename)
    msgAlert(path)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"<!-- {filename} não encontrado -->"

def load_info(tema):
    return f"METADADOS DA MATRIX: {tema.upper()}"

def write_ypoema(texto, imagem):
    st.divider()
    if os.path.exists(imagem):
        st.image(imagem, use_container_width=True)
    st.markdown(f"### {texto}")
    st.divider()

# --- 1. BOOTSTRAP (CPC) ---
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "sobre"

if 'sub_sobre' not in st.session_state:
    st.session_state.sub_sobre = "ypoemas"

if 'tema' not in st.session_state:
    st.session_state.tema = "default"

if 'lang_idx' not in st.session_state:
    st.session_state.lang_idx = 3

sb_state = "collapsed" if st.session_state.pagina_ativa == "sobre" else "expanded"
st.set_page_config(layout="wide", initial_sidebar_state=sb_state)

# --- 2. CENTRO DE CONTROLE (SIDEBAR) ---
def render_sidebar():
    with st.sidebar:
        label_idiomas = "↓ " + translate("idiomas disponíveis")
        idiomas_list = ["português : pt", "espanhol : es", "italiano : it", "francês : fr", "inglês : en", "catalão : ca"] + \
                       sorted(["alemão : de", "basco : eu", "córsico : co", "dinamarquês : da", "esperanto : eo", 
                               "finlandês : fi", "galego : gl", "galês : cy", "holandês : nl", "irlandês : ga", 
                               "latin : la", "norueguês : no", "polonês : pl", "romeno : ro", "sueco : sv"])
        
        sel_lang = st.selectbox(label_idiomas, idiomas_list, index=st.session_state.lang_idx, key="main_lang_selector")
        st.session_state.lang_idx = idiomas_list.index(sel_lang)
        st.divider()

        c1, c2 = st.columns(2)
        if c1.button("arte", key="btn_arte", use_container_width=True):
            st.session_state.pagina_ativa = "mini"
            st.rerun()
        st.divider()

        tag_foco = st.session_state.sub_sobre if st.session_state.pagina_ativa == "sobre" else st.session_state.pagina_ativa
        tag_upper = tag_foco.upper()

        # Fallback para nomes com underscore no sistema de arquivos
        tag_file = tag_upper.replace("-", "_")
        path_info = os.path.join("md_files", f"INFO_{tag_file}.MD")
        if os.path.exists(path_info):
            with open(path_info, "r", encoding="utf-8") as f:
                st.markdown(f.read().lower())
        
        path_img = os.path.join("images", f"IMG_{tag_file}.JPG")
        if os.path.exists(path_img):
            st.image(path_img, use_container_width=True)
        st.divider()

        s1, s2, s3 = st.columns(3)
        with s1: st.markdown("[insta](#)")
        with s2: st.markdown("[git](#)")
        with s3: st.markdown("[mail](#)")

# --- 3. O FAROL (SOBRE) ---
def page_sobre():
    sobre_list = ["comments", "prefácio", "machina", "off-machina", "outros", "traduttore", "imagens", "samizdát", "notes", "index", "bibliografia", "license"]
    
    options = list(range(len(sobre_list)))
    sobrios = "↓  " + translate("sobre")
    
    try:
        curr_idx = sobre_list.index(st.session_state.sub_sobre.lower())
    except ValueError:
        curr_idx = 0

    _, col_menu, _ = st.columns([1, 2, 1])
    with col_menu:
        opt_sobre = st.selectbox(sobrios, options, format_func=lambda x: sobre_list[x], index=curr_idx, key="opt_sobre")

    choice = sobre_list[opt_sobre].upper()
    st.session_state.sub_sobre = choice.lower()
    st.divider()

    _, col_texto, _ = st.columns([1, 5, 1])
    with col_texto:
        with st.expander("", True):
            if choice == "MACHINA":
                st.markdown(load_md_file("ABOUT_MACHINA_A.md"))
                LOGO_TEXTO = load_info(st.session_state.tema)
                LOGO_IMAGE = f"./images/matrix/{st.session_state.tema.upper()}.JPG"
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                st.markdown(load_md_file("ABOUT_MACHINA_D.md"))
            elif choice == "NOTES":
                st.markdown(load_md_file("ABOUT_NOTES.md"))
            else:
                # Resolve hífens para underscores nos nomes de arquivos físicos
                file_name = choice.replace("-", "_")
                st.markdown(load_md_file(f"ABOUT_{file_name}.MD"))

# --- 4. EXECUÇÃO ---
if __name__ == "__main__":
    render_sidebar()
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    elif st.session_state.pagina_ativa == "mini":
        st.info("palco 'arte' em desenvolvimento...")
