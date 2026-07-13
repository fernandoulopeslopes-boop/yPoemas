from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request


MAX_ANALISE_CHARS = 900
DEFAULT_MODEL = "gpt-4.1-mini"
RESPONSES_URL = "https://api.openai.com/v1/responses"


OLA_INSTRUCTIONS = """
Voce e OLA, analista da Machina de fazer Poesia.

Contrato:
- visite, escute, ofereca uma segunda leitura e recue
- nao tome autoridade sobre o yPoema
- nao corrija o yPoema
- nao altere o texto original
- nao use HTML
- nao use markdown pesado
- devolva somente texto simples
- escreva em portugues do Brasil
- use parcimonia e elegancia
- mantenha a analise curta, em 1 a 3 paragrafos breves
- limite maximo aproximado: 900 caracteres

Tipos OLA:
- Sintetica: leitura breve e concentrada
- Sintatica: observar ordem, cortes, pausas, respiracao e encaixes
- Aparicao: ler o acontecimento do yPoema, o que surge e que impressao deixa
- Completa: leitura um pouco mais ampla, sem virar palestra

O leitor decide.
""".strip()


def _plain_text(text: str) -> str:
    """Normaliza a resposta para texto simples, sem HTML ou markdown pesado."""
    text = str(text or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("```", "")
    text = re.sub(r"[*_#>`]+", "", text)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _limit_text(text: str, max_chars: int = MAX_ANALISE_CHARS) -> str:
    text = _plain_text(text)
    if len(text) <= max_chars:
        return text

    cut = text[:max_chars].rstrip()
    last_stop = max(cut.rfind("."), cut.rfind("!"), cut.rfind("?"))
    if last_stop >= int(max_chars * 0.65):
        return cut[: last_stop + 1].strip()
    return cut.rstrip(" ,;:") + "."


def _extract_output_text(response_data: dict) -> str:
    parts = []
    for item in response_data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    return "\n".join(parts).strip()


def _build_input(tipo: str, tema: str, ypoema_texto: str) -> str:
    return (
        f"Tipo de analise OLA: {tipo}\n\n"
        f"Tema: {tema}\n\n"
        "yPoema em texto limpo:\n"
        f"{ypoema_texto}"
    )


def ponte_ola_openai(
    tipo: str,
    tema: str,
    ypoema_texto: str,
    *,
    api_key: str | None = None,
    model: str | None = None,
    timeout_seconds: int = 30,
) -> str:
    """
    Ponte real para a OLA via OpenAI Responses API.

    Entrada: tipo, tema e yPoema limpo.
    Saida: analise curta em texto simples.

    Nao renderiza.
    Nao altera o yPoema.
    Nao chama Streamlit.
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return "OLA ainda nao conectada. Configure OPENAI_API_KEY para ativar a analise em tempo real."

    payload = {
        "model": model or os.getenv("OLA_OPENAI_MODEL", DEFAULT_MODEL),
        "instructions": OLA_INSTRUCTIONS,
        "input": _build_input(tipo, tema, ypoema_texto),
        "max_output_tokens": 260,
        "temperature": 0.85,
        "store": False,
    }

    request = urllib.request.Request(
        RESPONSES_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return f"OLA nao conectada: erro HTTP {exc.code}. {detail[:180]}"
    except Exception as exc:
        return f"OLA nao conectada: {exc}"

    text = _extract_output_text(data)
    if not text:
        return "OLA nao devolveu analise em texto simples."
    return _limit_text(text)


def gerar_analise_ola(tipo: str, tema: str, ypoema_texto: str) -> str:
    """
    Assinatura contratada pela Machina.

    Esta funcao e apenas a ponte OLA.
    """
    return ponte_ola_openai(tipo, tema, ypoema_texto)

