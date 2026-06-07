import pandas as pd
import streamlit as st

st.set_page_config(page_title="Lista gráfica de ícones", layout="wide")

@st.cache_data
def load_icons():
    return pd.read_csv("lista_grafica_de_icones.csv")

df = load_icons()

st.title("Lista gráfica de ícones")
st.caption("Pré-visualização visual para ABA. Na Machina: usar raramente, discreto, só se agregar valor real.")

grupos = ["todos"] + sorted(df["grupo"].unique().tolist())
grupo = st.sidebar.selectbox("grupo", grupos)
busca = st.sidebar.text_input("buscar por nome", "")

view = df.copy()
if grupo != "todos":
    view = view[view["grupo"] == grupo]
if busca:
    view = view[view["nome"].str.contains(busca, case=False, na=False)]

st.write(f"{len(view)} itens")

cols = st.columns(6)
for i, row in enumerate(view.to_dict("records")):
    with cols[i % 6]:
        st.markdown(
            f"""
            <div style="border:1px solid #DDD;border-radius:12px;padding:12px;margin-bottom:10px;background:white;text-align:center;">
                <div style="font-size:34px;">{row['icone_streamlit']}</div>
                <div style="font-size:13px;"><code>{row['nome']}</code></div>
                <div style="font-size:11px;color:#777;"><code>{row['icone_streamlit']}</code></div>
                <div style="font-size:10px;color:#999;">{row['grupo']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
