import streamlit as st
import os

# --- 1. BOOTSTRAP (CPC) ---
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "mini"

if 'sub_sobre' not in st.session_state:
    st.session_state.sub_sobre = "ypoemas"

sb_state = "collapsed" if st.session_state.pagina_ativa == "sobre" else "expanded"

st.set_page_config(layout="wide", initial_sidebar_state=sb_state)

# --- 2. CENTRO DE CONTROLE (SIDEBAR) ---
def render_sidebar():
    with st.sidebar:
        # 1. idiomas
        idiomas = ["português : pt", "espanhol : es", "italiano : it", "francês : fr", "inglês : en", "catalão : ca"] + \
                  sorted(["alemão : de", "basco : eu", "córsico : co", "dinamarquês : da", "esperanto : eo", "finlandês : fi", 
                          "galego : gl", "galês : cy", "holandês : nl", "irlandês : ga", "latin : la", "norueguês : no", 
                          "polonês : pl", "romeno : ro", "sueco : sv"])
        st.selectbox("idiomas disponíveis", idiomas)
        st.divider()

        # 2. botões
        c1, c2 = st.columns(2)
        c1.button("arte", key="btn_arte", use_container_width=True)
        c2.button("audio", key="btn_audio", use_container_width=True)
        st.divider()

        # 3. info (dinâmico)
        tag = st.session_state.sub_sobre if st.session_state.pagina_ativa == "sobre" else st.session_state.pagina_ativa
        path_info = f"info_{tag.lower()}.md"
        if os.path.exists(path_info):
            with open(path_info, "r", encoding="utf-8") as f: 
                st.markdown(f.read().lower())
        st.divider()

        # 4. logo fixo
        if os.path.exists("img_logo.jpg"): 
            st.image("img_logo.jpg", use_container_width=True)
        st.divider()

        # 5. links
        s1, s2, s3 = st.columns(3)
        s1.markdown("[insta](#)"); s2.markdown("[git](#)"); s3.markdown("[mail](#)")

# --- 3. O FAROL (SOBRE) ---
def page_sobre():
    sobre_list = ["ypoemas", "machina", "off-machina", "comments", "prefácio", "outros", "imagens", "notes", "traduttore", "samizdát", "index", "bibliografia", "license"]
    
    _, col_menu, _ = st.columns([1, 2, 1])
    with col_menu:
        st.session_state.sub_sobre = st.selectbox(
            "↓ guia de navegação documental", 
            sobre_list, 
            index=sobre_list.index(st.session_state.sub_sobre)
        )

    st.divider()

    _, col_texto, _ = st.columns([1, 5, 1])
    with col_texto:
        path_about = f"about_{st.session_state.sub_sobre}.md"
        if os.path.exists(path_about):
            with open(path_about, "r", encoding="utf-8") as f: 
                st.markdown(f.read())
        else:
            st.info("os documentos da machina...")

# --- 4. EXECUÇÃO ---
if __name__ == "__main__":
    render_sidebar()
    
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    elif st.session_state.pagina_ativa == "mini":
        pass # reservado para o palco mini
