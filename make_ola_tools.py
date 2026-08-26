import os
import streamlit as st

try:
    from ponte_ola_openai import gerar_analise_ola as _gerar_analise_ola_real
except Exception:
    _gerar_analise_ola_real = None


def _ler_texto_utf8(uploaded_file):
    """Lê o arquivo enviado como UTF-8 estrito."""
    raw = uploaded_file.getvalue()
    try:
        texto = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("O arquivo escolhido não é texto UTF-8.") from exc

    texto = texto.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not texto:
        raise ValueError("O arquivo escolhido está vazio.")
    return texto


def render_make_ola_tool():
    """Faz uma única chamada OLA, sempre para análise sintática."""
    st.markdown("### make_ola")

    uploaded = st.file_uploader(
        "Escolha um arquivo textual UTF-8",
        type=None,
        key="make_ola_upload",
    )

    if uploaded is None:
        st.info("Escolha um arquivo textual UTF-8.")
        return

    tema = os.path.splitext(os.path.basename(uploaded.name or "texto"))[0].strip()
    tema = tema or "texto"

    assinatura = (
        str(uploaded.name or ""),
        int(getattr(uploaded, "size", 0) or 0),
    )
    if st.session_state.get("make_ola_upload_signature") != assinatura:
        st.session_state["make_ola_upload_signature"] = assinatura
        st.session_state.pop("make_ola_result", None)
        st.session_state.pop("make_ola_result_name", None)

    st.caption("tema: " + tema)

    if st.button("análise sintática OLA", width="stretch", key="make_ola_run"):
        if _gerar_analise_ola_real is None:
            st.error(
                "OLA não conectada: ponte_ola_openai.py não foi encontrada "
                "ou não pôde ser importada."
            )
            return

        try:
            texto = _ler_texto_utf8(uploaded)

            with st.spinner("OLA — análise sintática..."):
                # Exatamente uma chamada OLA.
                resultado = _gerar_analise_ola_real(
                    "Sintática",
                    tema,
                    texto,
                )

            resultado = str(resultado or "").strip()
            if not resultado:
                raise RuntimeError("A OLA não devolveu texto.")

            st.session_state["make_ola_result"] = resultado
            st.session_state["make_ola_result_name"] = f"OLA_{tema}.txt"
            st.success("Análise sintática concluída.")
        except Exception as exc:
            st.error(f"make_ola falhou: {exc}")

    resultado = str(st.session_state.get("make_ola_result", "") or "")
    if resultado:
        nome_saida = str(
            st.session_state.get("make_ola_result_name", f"OLA_{tema}.txt")
        )

        st.text_area(
            "análise sintática OLA",
            value=resultado,
            height=420,
            key="make_ola_result_text",
        )

        st.download_button(
            "baixar " + nome_saida,
            data=resultado + "\n",
            file_name=nome_saida,
            mime="text/plain",
            width="stretch",
            key="make_ola_download",
        )
