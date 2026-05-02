import streamlit as st
import os

# --- CENTRO DE CONTROLE (SIDEBAR) ---
def render_sidebar():
    with st.sidebar:
        # 1. TRADUÇÃO DINÂMICA DO LABEL
        # Utiliza a função de tradução conforme o idioma selecionado
        label_idiomas = "↓ " + translate("idiomas disponíveis")
        
        idiomas_list = ["português : pt", "espanhol : es", "italiano : it", "francês : fr", "inglês : en", "catalão : ca"] + \
                       sorted(["alemão : de", "basco : eu", "córsico : co", "dinamarquês : da", "esperanto : eo", 
                               "finlandês : fi", "galego : gl", "galês : cy", "holandês : nl", "irlandês : ga", 
                               "latin : la", "norueguês : no", "polonês : pl", "romeno : ro", "sueco : sv"])
        
        st.selectbox(label_idiomas, idiomas_list, index=3, key="main_lang_selector")
        st.divider()

        # 2. INTERFACE DE AÇÃO
        c1, c2 = st.columns(2)
        if c1.button("arte", key="btn_arte", use_container_width=True):
            st.session_state.pagina_ativa = "mini"
            st.rerun()
        if c2.button("audio", key="btn_audio", use_container_width=True):
            pass 
        st.divider()

        # 3. CONTEÚDO DINÂMICO (PADRÃO PRO: UPPERCASE & DIRETÓRIOS)
        # Define a tag baseada na navegação atual (Palco ou Farol)
        tag_foco = st.session_state.sub_sobre if st.session_state.pagina_ativa == "sobre" else st.session_state.pagina_ativa
        tag_upper = tag_foco.upper()

        # Mapeamento \md_files\INFO_...MD
        path_info = os.path.join("md_files", f"INFO_{tag_upper}.MD")
        if os.path.exists(path_info):
            with open(path_info, "r", encoding="utf-8") as f:
                st.markdown(f.read().lower())
        
        # Mapeamento \images\IMG_...JPG
        path_img = os.path.join("images", f"IMG_{tag_upper}.JPG")
        if os.path.exists(path_img):
            st.image(path_img, use_container_width=True)
        st.divider()

        # 4. RODAPÉ SOCIAL
        s1, s2, s3 = st.columns(3)
        s1.markdown("[insta](#)")
        s2.markdown("[git](#)")
        s3.markdown("[mail](#)")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    render_sidebar()
    
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    elif st.session_state.pagina_ativa == "mini":
        # palco mini será integrado aqui
        pass
