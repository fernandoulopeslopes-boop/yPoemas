# =============================================================================
# lay_tools.py — puxadinho autorizado do motor histórico lay_2_ypo.py
# =============================================================================
# Modernizações de proteção/persistência ficam aqui para preservar legível e
# reconhecível a arquitetura do motor.
# =============================================================================

import datetime
import os


def linha_fim(linha):
    texto = str(linha)
    if texto.endswith("\r\n"):
        return "\r\n"
    if texto.endswith("\n"):
        return "\n"
    if texto.endswith("\r"):
        return "\r"
    return ""


def comando_espacamento_compacto(linha):
    """Reconhece |$|, |$$|, ...; devolve a quantidade de $ ou 0."""
    corpo = str(linha).rstrip("\r\n")
    partes = corpo.split("|")
    if (
        len(partes) == 3
        and partes[0] == ""
        and partes[2] == ""
        and partes[1]
        and set(partes[1]) == {"$"}
    ):
        return len(partes[1])
    return 0


def tabs_payload(array_itimos, tabs_pendente=0):
    itens = list(array_itimos)
    tabs = 0
    if itens and itens[0] and set(itens[0]) == {"$"}:
        tabs = len(itens[0])
        itens = itens[1:]
    if tabs == 0 and tabs_pendente:
        tabs = int(tabs_pendente)
    return itens, tabs


def indice_konstante(itimos_atual, total_itimos):
    if int(total_itimos) <= 0:
        return 0
    return max(1, min(int(itimos_atual), int(total_itimos))) - 1


def linha_com_itimos_atual(linha_original, itimos_atual):
    """Preserva a linha inteira e altera somente o campo histórico itimos_atual."""
    fim = linha_fim(linha_original)
    corpo = str(linha_original).rstrip("\r\n")
    campos = corpo.split("|")
    if len(campos) < 9 or campos[0] != "" or campos[-1] != "":
        raise RuntimeError("persistência bloqueada: registro .ypo inválido")
    campos[6] = str(int(itimos_atual))
    return "|".join(campos) + fim


def abre_ypo_preservando_newline(path):
    with open(path, encoding="utf-8", newline="") as arquivo:
        return list(arquivo)


def validar_estrutura_ypo(linhas):
    """
    Regra estrutural:
      HEADER = tudo antes do primeiro registro BODY;
      BODY   = somente linhas que começam e terminam com |;
      <EOF>  = fecha o BODY;
      FINAIS = tudo após <EOF>.
    """
    if not linhas:
        raise RuntimeError("estrutura .ypo inválida: arquivo vazio")

    viu_body = False
    viu_eof = False
    qtd_eof = 0

    for numero, linha in enumerate(linhas, start=1):
        corpo = str(linha).rstrip("\r\n")

        if corpo == "<EOF>":
            qtd_eof += 1
            if qtd_eof > 1:
                raise RuntimeError("estrutura .ypo inválida: <EOF> duplicado")
            if not viu_body:
                raise RuntimeError("estrutura .ypo inválida: <EOF> antes do BODY")
            viu_eof = True
            continue

        if viu_eof:
            continue

        if corpo.startswith("|"):
            viu_body = True
            if not corpo.endswith("|"):
                raise RuntimeError(
                    f"estrutura .ypo inválida: BODY sem pipe final na linha {numero}"
                )
            continue

        if viu_body:
            raise RuntimeError(
                f"estrutura .ypo inválida: invasão entre BODY e <EOF> na linha {numero}"
            )

    if not viu_body:
        raise RuntimeError("estrutura .ypo inválida: BODY ausente")
    if not viu_eof:
        raise RuntimeError("estrutura .ypo inválida: <EOF> ausente")


def _eh_updated(linha):
    return str(linha).lstrip("\r\n").strip().lower().startswith("updated em:")


def _eh_build_by(linha):
    texto = str(linha).strip().lower()
    return texto.startswith("build_by") or texto.startswith("build by")


def _newline_referencia(linhas):
    for linha in linhas:
        fim = linha_fim(linha)
        if fim:
            return fim
    return "\n"


def aplicar_updated_em(linhas, agora=None):
    """
    Atualiza as duas assinaturas técnicas autorizadas no FINAIS:
      - build_by lay_2_ypo: dd/mm/aaaa - hh:mm
      - updated em: dd/mm/aaaa - hh:mm

    Todo o restante do rodapé, inclusive território autoral, permanece intocado.
    """
    validar_estrutura_ypo(linhas)
    agora = agora or datetime.datetime.now()
    newline = _newline_referencia(linhas)
    carimbo = agora.strftime("%d/%m/%Y - %H:%M")
    build_assinatura = f"build_by lay_2_ypo: {carimbo}"
    updated_assinatura = f"updated em: {carimbo}"

    eof_idx = next(
        i for i, linha in enumerate(linhas)
        if str(linha).rstrip("\r\n") == "<EOF>"
    )

    antes = list(linhas[: eof_idx + 1])
    finais = list(linhas[eof_idx + 1 :])
    novos_finais = []

    build_pos = None
    updated_pos = None

    for linha in finais:
        fim = linha_fim(linha) or newline

        if _eh_build_by(linha):
            if build_pos is None:
                build_pos = len(novos_finais)
                novos_finais.append(build_assinatura + fim)
            # Assinaturas build_by duplicadas são território técnico;
            # mantém-se uma única assinatura canônica.
            continue

        if _eh_updated(linha):
            if updated_pos is None:
                updated_pos = len(novos_finais)
                novos_finais.append(updated_assinatura + fim)
            # Mesmo princípio: uma única assinatura updated em.
            continue

        novos_finais.append(linha)

    if build_pos is None:
        # Sem build_by anterior: cria logo no início do FINAIS,
        # sem alterar nenhum conteúdo autoral existente.
        novos_finais.insert(0, build_assinatura + newline)
        build_pos = 0
        if updated_pos is not None:
            updated_pos += 1

    if updated_pos is None:
        # Posição canônica: imediatamente após build_by.
        novos_finais.insert(build_pos + 1, updated_assinatura + newline)

    return antes + novos_finais


def _sem_assinaturas_tecnicas(linhas):
    return [
        linha for linha in linhas
        if not _eh_updated(linha) and not _eh_build_by(linha)
    ]


def validar_persistencia(original_linhas, novas_linhas):
    """
    CAE estrutural da escrita:
      - HEADER permanece idêntico;
      - BODY mantém estrutura/conteúdo e só pode mudar o campo 6;
      - no FINAIS, somente build_by e updated em podem mudar;
      - todo o restante do rodapé permanece byte a byte e na mesma ordem.
    """
    validar_estrutura_ypo(original_linhas)
    validar_estrutura_ypo(novas_linhas)

    def blocos(linhas):
        eof_idx = next(
            i for i, linha in enumerate(linhas)
            if str(linha).rstrip("\r\n") == "<EOF>"
        )
        pre = linhas[:eof_idx]
        fim = linhas[eof_idx:]
        primeiro_body = next(i for i, linha in enumerate(pre) if str(linha).startswith("|"))
        return pre[:primeiro_body], pre[primeiro_body:], fim

    oh, ob, of = blocos(original_linhas)
    nh, nb, nf = blocos(novas_linhas)

    if oh != nh:
        raise RuntimeError("persistência bloqueada: HEADER mudou")

    if len(ob) != len(nb):
        raise RuntimeError("persistência bloqueada: quantidade de linhas do BODY mudou")

    for numero, (antes, depois) in enumerate(zip(ob, nb), start=1):
        if antes == depois:
            continue

        if linha_fim(antes) != linha_fim(depois):
            raise RuntimeError(f"persistência bloqueada: newline mudou no BODY {numero}")

        a = str(antes).rstrip("\r\n")
        b = str(depois).rstrip("\r\n")
        af = a.split("|")
        bf = b.split("|")

        # Comandos compactos e linhas especiais devem permanecer byte a byte.
        if comando_espacamento_compacto(antes):
            raise RuntimeError(f"persistência bloqueada: comando compacto mudou no BODY {numero}")

        if len(af) != len(bf) or len(af) < 9:
            raise RuntimeError(f"persistência bloqueada: estrutura mudou no BODY {numero}")

        for idx, (x, y) in enumerate(zip(af, bf)):
            if idx == 6:
                continue
            if x != y:
                raise RuntimeError(
                    f"persistência bloqueada: campo {idx} mudou no BODY {numero}"
                )

    # Removendo somente as duas assinaturas técnicas autorizadas,
    # o restante do FINAIS deve ser rigorosamente idêntico.
    if _sem_assinaturas_tecnicas(of) != _sem_assinaturas_tecnicas(nf):
        raise RuntimeError(
            "persistência bloqueada: FINAIS mudaram além de build_by/updated em"
        )

    builds_novos = [linha for linha in nf if _eh_build_by(linha)]
    if len(builds_novos) != 1:
        raise RuntimeError(
            "persistência bloqueada: build_by deve existir uma única vez"
        )
    if not str(builds_novos[0]).strip().casefold().startswith(
        "build_by lay_2_ypo:"
    ):
        raise RuntimeError(
            "persistência bloqueada: assinatura build_by fora do formato canônico"
        )

    updated_novos = [linha for linha in nf if _eh_updated(linha)]
    if len(updated_novos) != 1:
        raise RuntimeError(
            "persistência bloqueada: updated em deve existir uma única vez"
        )


def gravar_ypo_certificado(path, original_linhas, linhas_com_body_atualizado, agora=None):
    """Staging + validação semântica + escrita atômica + conferência byte a byte."""
    candidato = aplicar_updated_em(linhas_com_body_atualizado, agora=agora)
    validar_persistencia(original_linhas, candidato)

    novo_bytes = "".join(candidato).encode("utf-8")
    tmp_path = str(path) + ".lay.tmp"

    try:
        with open(tmp_path, "wb") as arquivo:
            arquivo.write(novo_bytes)

        if open(tmp_path, "rb").read() != novo_bytes:
            raise RuntimeError("persistência bloqueada: staging não confere byte a byte")

        os.replace(tmp_path, path)

        if open(path, "rb").read() != novo_bytes:
            raise RuntimeError("persistência bloqueada: .ypo gravado não confere byte a byte")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return candidato
