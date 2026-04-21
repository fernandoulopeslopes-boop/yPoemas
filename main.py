import streamlit as st
import os
import json

# 1. SETUP & CSS (Palco Fluido e Sidebar Estrita)
st.set_page_config(page_title="a Machina de Fazer Poesia", layout="wide")

st.markdown("""
    <style>
        /* Sidebar fixa em 300px */
        [data-testid="stSidebar"] { min-width: 300px; max-width: 300px; }
        
        /* Força o palco a ocupar 100% da largura útil */
        section[data-testid="stMain"] { width: 100%; padding: 0rem; }
        
        /* Estilização de interface */
        .stMarkdown p { text-align: justify; font-size: 14px; }
        .stButton button { width: 100%; padding: 0px; font-size: 14px; height: 40px; }
    </style>
    """, unsafe_allow_html=True)

def main():
    # 2. GESTÃO DE ESTADOS
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "yPoemas"
    if 'idioma_sel' not in st.session_state: 
        st.session_state.idioma_sel = "pt"
    
    # Som e Arte apenas (pic removido)
    for sw in ['sw_som', 'sw_art']:
        if sw not in st.session_state: 
            st.session_state[sw] = False

    # 3. NAVEGAÇÃO SUPERIOR (Grafia Corrigida)
    t1, t2, t3, t4, t5, t6 = st.columns(6)
    btns = ["mini", "yPoemas", "eureka", "off-mach", "comments", "about"]
    for i, col in enumerate([t1, t2, t3, t4, t5, t6]):
        if col.button(btns[i]):
            st.session_state.pagina_ativa = btns[i]
            st.rerun()

    st.divider()

    # 4. SIDEBAR (SALA DE CONTROLE)
    with st.sidebar:
        # 4.1 Idiomas
        path_idiomas = os.path.join("ypo", "idiomas.json")
        dic_idiomas = {"Português": "pt"}
        if os.path.exists(path_idiomas):
            with open(path_idiomas, "r", encoding="utf-8") as f:
                try:
                    content = json.load(f)
                    if content: dic_idiomas = content
                except: pass
        
        sel_nome = st.selectbox("Idioma", list(dic_idiomas.keys()), label_visibility="collapsed")
        st.session_state.idioma_sel = dic_idiomas[sel_nome]

        # 4.2 Som e Arte
        st.write("")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                if st.button("som"): 
                    st.session_state.sw_som = not st.session_state.sw_som
                    st.rerun()
                if st.session_state.sw_som: st.caption("·on·")
            with c2:
                if st.button("art"): 
                    st.session_state.sw_art = not st.session_state.sw_art
                    st.rerun()
                if st.session_state.sw_art: st.caption("·on·")

        st.divider()

        # 4.3 & 4.4 Arte e INFO (Mapeamento Dinâmico)
        p_at = st.session_state.pagina_ativa
        
        # Mapeamento para arquivos físicos
        ref_file = p_at.upper() if p_at != "off-mach" else "OFF-MACHINA"
        img_name = f"img_{p_at.lower() if p_at != 'off-mach' else 'off-machina'}.jpg"
        
        path_img = os.path.join("ypo", img_name)
        path_info = os.path.join("md_files", f"INFO_{ref_file}.md")

        if os.path.exists(path_img):
            st.image(path_img, use_container_width=True)
        
        if os.path.exists(path_info):
            with open(path_info, "r", encoding="utf-8") as f:
                st.markdown(f.read())

        st.divider()

        # 4.5 Rodapé
        path_media = os.path.join("md_files", "INFO_MEDIA.md")
        if os.path.exists(path_media):
            with open(path_media, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        
        st.caption("Copyright © 1983-2026 Nando Lopes")

    # 5. PALCO
    col_main = st.container()
    with col_main:
        p = st.session_state.pagina_ativa
        if p == "mini":
            st.write("\n" * 5)
            st.markdown("<h1 style='text-align:center;'>Modo Mini</h1>", unsafe_allow_html=True)
        elif p == "yPoemas":
            st.title("yPoemas")
        elif p == "eureka":
            st.title("eureka")
        elif p == "off-mach":
            st.title("off-machina")
            if os.path.exists("off_machina"):
                arqs = sorted([f for f in os.listdir("off_machina") if f.endswith(".TXT")])
                for a in arqs:
                    with st.expander(a.replace(".TXT", "")):
                        with open(os.path.join("off_machina", a), "r", encoding="utf-8") as f:
                            st.text(f.read())
        elif p == "comments":
            st.title("comments")
        elif p == "about":
            st.title("about")

if __name__ == "__main__":
    main()
