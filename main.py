import streamlit as st
import os
import json

# 1. SETUP & CSS (Palco Fluido, Sidebar Estrita 300px e Balanceamento)
st.set_page_config(page_title="a Machina de Fazer Poesia", layout="wide")

st.markdown("""
    <style>
        /* Expansão total do palco quando a sidebar recolhe */
        [data-testid="stSidebar"] { min-width: 300px; max-width: 300px; }
        section[data-testid="stMain"] { width: 100%; padding-left: 1rem; padding-right: 1rem; }
        
        /* Balanceamento e largura fixa para os botões de página */
        .stButton button { 
            width: 100%; 
            padding: 0px; 
            font-size: 14px; 
            height: 40px; 
            white-space: nowrap;
        }
        
        /* Ajuste fino da sidebar e links pessoais */
        .stMarkdown p { text-align: justify; font-size: 13px; line-height: 1.2; }
        .stCaption { font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

def main():
    # 2. GESTÃO DE ESTADOS
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "yPoemas"
    if 'idioma_sel' not in st.session_state: 
        st.session_state.idioma_sel = "pt"
    
    for sw in ['sw_som', 'sw_arte']:
        if sw not in st.session_state: 
            st.session_state[sw] = False

    # 3. NAVEGAÇÃO SUPERIOR (Botões Balanceados)
    cols = st.columns(6)
    btns = ["mini", "yPoemas", "eureka", "off-mach", "comments", "about"]
    for i, col in enumerate(cols):
        if col.button(btns[i], key=f"btn_{btns[i]}"):
            st.session_state.pagina_ativa = btns[i]
            st.rerun()

    st.divider()

    # 4. SIDEBAR (SALA DE CONTROLE)
    with st.sidebar:
        # 4.1 Idiomas (Carregamento completo do JSON)
        path_idiomas = os.path.join("ypo", "idiomas.json")
        dic_idiomas = {"Português": "pt"}
        if os.path.exists(path_idiomas):
            with open(path_idiomas, "r", encoding="utf-8") as f:
                try:
                    loaded = json.load(f)
                    if loaded: dic_idiomas = loaded
                except: pass
        
        sel_nome = st.selectbox("Idioma", list(dic_idiomas.keys()), label_visibility="collapsed")
        st.session_state.idioma_sel = dic_idiomas[sel_nome]

        # 4.2 Som e Arte (Botões balanceados e rótulo corrigido)
        st.write("")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                if st.button("som"): 
                    st.session_state.sw_som = not st.session_state.sw_som
                    st.rerun()
                if st.session_state.sw_som: st.caption("·on·")
            with c2:
                if st.button("arte"): 
                    st.session_state.sw_arte = not st.session_state.sw_arte
                    st.rerun()
                if st.session_state.sw_arte: st.caption("·on·")

        st.divider()

        # 4.3 & 4.4 Arte e INFO (Mapeamento de Caminho)
        p_at = st.session_state.pagina_ativa
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

        # 4.5 Rodapé e Copyright (Sem ícone)
        path_media = os.path.join("md_files", "INFO_MEDIA.md")
        if os.path.exists(path_media):
            with open(path_media, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        
        st.caption("Copyright 1983-2026 Nando Lopes")

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
