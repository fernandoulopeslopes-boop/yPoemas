import streamlit as st
import os
import random

# =================================================================
# 1º SETOR: LENTE (SUSTENTAÇÃO VISUAL)
# =================================================================
def configurar_lente():
    st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="expanded")
    st.markdown(""" 
        <style> 
        [data-testid="stSidebar"] { min-width: 310px !important; max-width: 310px !important; }
        [data-testid="stAppViewBlockContainer"] { max-width: 900px !important; margin: 0 auto !important; }
        .poesia-viva {
            font-family: 'Georgia', serif !important;
            font-size: 32px !important; 
            line-height: 1.6 !important;
            white-space: pre-wrap;
            padding: 40px;
            background-color: #fdfdfd;
            border-radius: 8px;
            border: 1px solid #eee;
        }
        /* SCROLL HORIZONTAL DAS SALAS */
        div[data-testid="stHorizontalBlock"] {
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            display: flex !important;
            gap: 10px !important;
        }
        div[data-testid="stHorizontalBlock"] > div {
            min-width: 150px !important;
            flex: 0 0 auto !important;
        }
        .stButton>button { width: 100%; height: 3.5em; font-weight: 700; text-transform: uppercase; }
        </style> 
    """, unsafe_allow_html=True)

# =================================================================
# 2º SETOR: PAIOL (SUPRIMENTO E MEMÓRIA)
# =================================================================
def carregar_paiol():
    if 'take' not in st.session_state: st.session_state.take = random.randint(1000, 9999)
    if 'sala' not in st.session_state: st.session_state.sala = "yPoemas"
    
    try:
        from lay_2_ypo import gera_poema
        return gera_poema
    except Exception as e:
        st.error(f"Erro no Paiol: {e}")
        return lambda t, s: [f"Motor em ajuste... {s}"]

# CALLBACKS DE COMANDO
def cmd_mudar_take(valor):
    if valor == "random": st.session_state.take = random.randint(1000, 9999)
    else: st.session_state.take += valor

def cmd_mudar_sala(nova_sala):
    st.session_state.sala = nova_sala

# =================================================================
# 3º SETOR: MOTOR (A PROPULSÃO)
# =================================================================
def processar_motor(func_gera):
    def limpar_texto(bruto):
        if isinstance(bruto, dict): return "\n".join([str(v) for v in bruto.values()])
        if isinstance(bruto, list): return "\n".join([str(p) for p in bruto])
        return str(bruto)
    
    conteudo = func_gera("Fatos", str(st.session_state.take))
    return limpar_texto(conteudo)

# =================================================================
# 4º SETOR: SALAS (EXPOSIÇÃO MODULAR)
# =================================================================
MAPA_ARTES = {
    "mini": "img_mini.jpg", "yPoemas": "img_ypoemas.jpg", "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg", "books": "img_books.jpg", 
    "poly": "img_poly.jpg", "sobre": "img_about.jpg"
}

def exibir_palco(texto):
    if st.session_state.sala == "yPoemas":
        st.markdown(f'<div class="poesia-viva">{texto}</div>', unsafe_allow_html=True)
    else:
        st.subheader(f"SALA: {st.session_state.sala.upper()}")
        st.info("Fluxo de dados em processamento.")

# =================================================================
# 5º SETOR: FAROL (SINAL SENSORIAL)
# =================================================================
def disparar_farol():
    st.write("### 🧭 FAROL")
    c1, c2, c3, c4, c_id = st.columns([1, 1, 1, 1, 2])
    c1.button("✚", on_click=cmd_mudar_take, args=("random",))
    c2.button("◀", on_click=cmd_mudar_take, args=(-1,))
    c3.button("✻", on_click=cmd_mudar_take, args=("random",))
    c4.button("▶", on_click=cmd_mudar_take, args=(1,))
    c_id.code(f"ID ATIVO: {st.session_state.take}")
    
    st.write("---")
    salas = list(MAPA_ARTES.keys())
    cols = st.columns(len(salas))
    for i, s in enumerate(salas):
        cols[i].button(s.upper(), key=f"n_{s}", on_click=cmd_mudar_sala, args=(s,))

# =================================================================
# 6º SETOR: METAS (O ENVIO FINAL)
# =================================================================
def despacho_final():
    with st.sidebar:
        st.title("A Machina")
        st.selectbox("Idioma", ["Português", "English"], key="lang")
        st.divider()
        st.checkbox("🖼️ Arte", key="draw_machina")
        st.checkbox("🔊 Voz", key="talk_machina")
        st.divider()
        img = MAPA_ARTES.get(st.session_state.sala, "img_ypoemas.jpg")
        if os.path.exists(img): st.image(img, use_column_width=True)

# --- FUNÇÃO PRINCIPAL (O ARRANQUE) ---
def main():
    configurar_lente()
    gera_poema_func = carregar_paiol()
    disparar_farol()
    st.divider()
    texto_final = processar_motor(gera_poema_func)
    exibir_palco(texto_final)
    despacho_final()

if __name__ == "__main__":
    main()
  
