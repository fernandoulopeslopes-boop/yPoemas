import streamlit as st

# 1. Deve ser a primeira linha
st.set_page_config(page_title="Teste Machina")

st.title("ツ Machina - Teste de Vida")
st.sidebar.write("Sidebar Ativa")

# Teste de importação
try:
    import lay_2_ypo
    st.success("Motor detectado com sucesso!")
except Exception as e:
    st.error(f"O erro está no arquivo do motor: {e}")

st.write("Se você está vendo isso, o problema é o loop de execução no motor.")
