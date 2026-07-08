# contrato_CIA.md

## Contrato das Análises da Machina

Este documento registra as regras acordadas para a camada de análises da Machina/yPoemas.

## Princípio geral

```text
motor poético não analisa
rotina de análise não renderiza
palco não interpreta
leitor decide
```

A análise é uma leitura possível, não uma sentença final sobre o yPoema.

## Vozes

```text
CIA = Centro Imaginativo Aplicado
OLA = Onda Leitora Analítica
```

A CIA é a leitura principal da Machina.

A OLA é visitante convidada: visita, escuta, oferece e recua.

A CIA não corrige a OLA.  
A OLA não corrige a CIA.  
O leitor decide.

## Contrato técnico comum

```python
MAX_ANALISE_CHARS = 900

def gerar_analise_cia(tipo, tema, ypoema_texto):
    ...
    return analise_texto

def gerar_analise_ola(tipo, tema, ypoema_texto):
    ...
    return analise_texto
```

Cada rotina recebe:

```text
tipo
tema
ypoema_texto limpo
```

Cada rotina devolve:

```text
texto simples
curto
sem HTML
sem markdown pesado
sem alterar o yPoema original
```

Cada rotina deve:

```text
gerar apenas conteúdo textual
não renderizar
não mexer em st.session_state
não chamar Streamlit
não misturar análise com visual
```

## Fluxo da análise

```text
yPoema gerado
→ texto limpo
→ rotina de análise
→ texto simples
→ render_analise_palco()
→ leitor decide
```

## Renderização

A função de renderização deve apenas mostrar o texto recebido.

```python
render_analise_palco(texto)
```

Ela não deve interpretar, reescrever nem decidir o conteúdo da análise.

## Estado atual

A implementação inicial está no `ypo_tools.py`, para testes locais na Off Sina.

O destino final, depois de validado, é o `ypo_seguro.py`, no site público.

## Regra de migração

```text
testar no tools
validar leitura e ergonomia
migrar para o seguro público
sem levar ferramentas locais para o site
```

## Regra final

```text
A Machina oferece.
A CIA sugere.
A OLA contrapõe com elegância.
O leitor decide.
```
