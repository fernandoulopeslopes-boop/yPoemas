import streamlit as st
import os

# --- 0. MOTORES DA MACHINA (SUPORTE) ---
def load_md_file(filename):
    """
    Busca o arquivo no diretório ignorando diferenças de caixa (case-insensitive).
    O simples resolve a complexidade.
    """
    folder = "md_files"
    # Garante a extensão na busca caso não venha no filename
    search_name = filename if filename.upper().endswith(".MD") else f"{filename}.MD"
    
    if os.path.exists(folder):
        for arq in os.listdir(folder):
            if arq.upper() == search_name.upper():
                with open(os.path.join(folder, arq), "r", encoding="utf-8") as f:
                    return f.read()
    return f"<!-- {search_name} não encontrado -->"

def translate(texto):
    traducoes = {"sobre": "sobre", "idiomas disponíveis": "idiomas disponíveis"}
    return traducoes.get(texto.lower(), texto)

def load_info(tema):
    return f"METADADOS DA MATRIX: {tema.upper()}"

def write_ypoema(texto, imagem):
    st.divider()
    if os.path.exists(imagem):
        st.image(imagem, use_container_width=True)
    st.markdown(f"### {texto}")
    st.divider()

# --- 1. BOOTSTRAP ---
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "sobre"
if 'sub_sobre' not in st.session_state:
    st.session_state.sub_sobre = "ypoemas"
if 'tema' not in st.session_state:
    st.session_state.tema = "default"
if 'lang_idx' not in st.session_state:
    st.session_state.lang_idx = 3

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- 2. CENTRO DE CONTROLE (SIDEBAR) ---
def render_sidebar():
    with st.sidebar:
        st.selectbox("↓ " + translate("idiomas disponíveis"), 
                     ["português : pt", "espanhol : es", "italiano : it", "inglês : en"], 
                     index=st.session_state.lang_idx)
        st.divider()
        
        tag_foco = st.session_state.sub_sobre.upper().replace("-", "_")
        # Uso da lógica simplificada também para metadados e imagens
        st.markdown(load_md_file(f"INFO_{tag_foco}"))
        
        path_img = f"./images/IMG_{tag_foco}.JPG"
        if os.path.exists(path_img):
            st.image(path_img, use_container_width=True)

# --- 3. O FAROL (SOBRE) ---
def page_sobre():
    sobre_list = ["comments", "prefácio", "machina", "off-machina", "outros", "traduttore", "notes", "license"]
    
    sobrios = "↓  " + translate("sobre")
    try:
        curr_idx = sobre_list.index(st.session_state.sub_sobre.lower())
    except ValueError:
        curr_idx = 0

    _, col_menu, _ = st.columns([1, 2, 1])
    with col_menu:
        choice = st.selectbox(sobrios, sobre_list, index=curr_idx, key="opt_sobre").upper()
    
    st.session_state.sub_sobre = choice.lower()
    st.divider()

    _, col_texto, _ = st.columns([1, 5, 1])
    with col_texto:
        with st.expander("", True):
            if choice == "MACHINA":
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                write_ypoema(load_info(st.session_state.tema), f"./images/matrix/{st.session_state.tema.upper()}.JPG")
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            elif choice == "OFF-MACHINA":
                st.markdown(load_md_file("ABOUT_OFF_MACHINA.MD"))
            else:
                st.markdown(load_md_file(f"ABOUT_{choice}.MD"))

# --- 4. EXECUÇÃO ---
if __name__ == "__main__":
    render_sidebar()
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
