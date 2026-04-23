import streamlit as st
import os
import time

# Motores de construção (certifique-se de que os arquivos .py existam no repo)
from build_lexico import gera_lexico, build_lexico
from build_matrix import gera_matrix, build_matrix
from build_info import gera_info

# --- Configurações de UI ---
st.set_page_config(layout="wide", page_title="Machina de Fazer Poesia")

# CSS para garantir os 300px da sidebar e estilo das imagens
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { width: 300px; max-width: 300px; }
        .stImage img { border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Engine de Sincronização ---
#def executar_update(tema=None):
#    """
#    Variação: 
#    - Se tema: build_one (específico).
#    - Sem tema: build_all (update geral via ativos.txt).
#    """
#    start_time = time.time()
#    
#    if tema:
#        nome_tema = tema.strip().capitalize()
#        # Build individual
#        build_lexico(nome_tema)
#        build_matrix(nome_tema)
#    else:
#        # Build global (Independente)
#        gera_lexico()
#        gera_matrix()
#    
#    # Ambos os caminhos convergem na atualização do info.txt
#    gera_info()
#    
#    # Limpeza cirúrgica do cache do Streamlit
#    st.cache_data.clear()
#    
#    return time.time() - start_time

def main():
    # --- Sidebar / Cockpit ---
    with st.sidebar:
        st.title("a Máquina")
        
        # [AQUI ENTRA O SEU CÓDIGO DE SELEÇÃO DE IDIOMAS/TEMAS]
        # Exemplo: st.segmented_control(...)
        
        st.divider()

        # --- Módulo Admin (O seu 'ptc' invisível) ---
        with st.expander(" ", expanded=False):
            # Protocolo de segurança "go"
            chave = st.text_input("Refino", type="password", label_visibility="collapsed")
            
            if chave == "go":
                st.markdown("#### ⚙️ Engine")
                
                # Input para definir o alvo do build
                target = st.text_input("ID Tema", placeholder="Vazio = Update Geral", key="adm_target")
                
                label_btn = f"Update {target.capitalize()}" if target else "Update Geral"
                
                if st.button(label_btn, use_container_width=True):
                    with st.status("Lipoaspirando...", expanded=True) as s:
                        try:
                            delta = executar_update(target if target else None)
                            s.update(label=f"Prumo ajustado! ({delta:.2f}s)", state="complete")
                            st.toast("Machina sincronizada.")
                        except Exception as e:
                            s.update(label="Falha na cirurgia", state="error")
                            st.error(f"Erro: {e}")

    # --- Área Principal (Onde a Poesia acontece) ---
    st.markdown("### Bem-vindo à Cobertura")
    # [AQUI ENTRA A EXIBIÇÃO DO POEMA E DAS ARTES]

# --- Fechamento Seguro ---
if __name__ == "__main__":
    main()
