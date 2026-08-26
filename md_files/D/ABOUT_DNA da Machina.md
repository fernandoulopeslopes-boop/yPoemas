DNA — Auditoria viva da Machina
___
---> Registro de nascimento

O DNA nasceu durante a revisão da família Builds, a partir de uma necessidade concreta: impedir que informações essenciais dos temas continuassem espalhadas entre funções, arquivos e cálculos diferentes.

A ideia inicial era simples: reunir, em uma única lista, a ficha completa de cada tema da Machina.

Em poucas horas de uso, porém, o DNA revelou uma função maior.

Ele passou de cadastro unificado a instrumento de observação, validação e evolução da arquitetura.

---> O que é o DNA

O DNA é uma ferramenta altamente especializada de auditoria permanente da Machina.

Seu objetivo é produzir um "raio-X" temporal e localizado das principais engrenagens do ambiente, registrando:

- qual função foi chamada;
- qual informação foi consultada ou produzida;
- qual fonte foi usada;
- qual tema estava envolvido;
- qual resultado foi obtido;
- onde surgiu uma divergência;
- onde existe duplicação de responsabilidade;
- onde aparece um elo ainda não mapeado.

O DNA não corrige automaticamente.

Ele observa, registra, compara e mostra diferenças.

A decisão continua humana.

---> Por que o nome DNA

O nome não é apenas metáfora.

Cada tema da Machina possui características próprias e permanentes. Essas características formam seu cromossomo.

O DNA registra essas características em uma única estrutura, com endereço conhecido e responsabilidade definida.

Como qualquer `.ypo`, o DNA é mutante.

Ele pode ganhar novos genes, refinar genes existentes ou abandonar campos que deixem de representar a realidade da obra.

Sua evolução não é exceção: é parte de sua natureza.

---> Princípio de autoridade

Cada informação deve ter:

- um único lugar de origem;
- um único responsável;
- um único endereço no DNA.

O objetivo é eliminar a procura dispersa por informações em arquivos, funções e listas diferentes.

Quando uma função precisar de uma característica permanente do tema, deverá consultar o DNA.

Quando surgir uma característica nova, cria-se o cromossomo correspondente e o DNA evolui.

---> Estrutura inicial

------> `DNA.TXT`

Contém uma linha por tema.

A primeira linha contém os nomes oficiais dos campos.

O tema é o índice natural de cada registro.

------> `dna_dic.txt`

Documenta cada campo do `DNA.TXT`.

A posição da linha no dicionário corresponde à posição da coluna no DNA.

Não há índice duplicado.

O mesmo endereço serve às duas listas.

------> `LOG.TXT`

Registra o comportamento observado durante o uso real da Machina.

O LOG é o caderno do laboratório.

Ele não contém opinião. Contém ocorrências.

---> Classificação dos resultados

O DNA deve distinguir pelo menos quatro naturezas de informação:

------> Característica do tema

Informação que pertence ao cromossomo do tema.

Exemplos:

- tema;
- gênero;
- imagem;
- versos;
- verbetes;
- ítimos;
- quantidade de variações.

------> Dependência global

Informação usada pelo ambiente, mas que não pertence a um tema específico.

Exemplos:

- catálogo ABOUT;
- léxico global;
- listas gerais de navegação.

------> Chamada operacional

Ação transitória do sistema.

Exemplos:

- leitura de uma lista;
- acesso servido por cache;
- geração de uma página;
- rerun do Streamlit.

------> Elo perdido

Informação necessária que ainda não possui lugar definido.

O elo perdido não é automaticamente um erro.

Ele pode ser:

- uma característica nova;
- uma dependência global ainda não classificada;
- uma duplicação;
- uma mutação legítima da Machina;
- uma inconsistência real.

---> A autoridade dos temas ativos

A lista de autoridade para o universo ativo é:

`base/ativos.txt`

Outras listas podem ter funções operacionais diferentes e não devem substituir essa autoridade.

Temas em estudo, geradores experimentais ou estruturas fora de circulação podem existir sem integrar o conjunto ativo.

---> Laboratório inicial

O DNA foi instalado primeiro apenas no `ypo_tools.py`.

Motivos:

- a página Tools é local;
- o ambiente de testes permanece isolado;
- não há impacto na versão pública;
- o volume de uso real gera amostragem suficiente;
- o LOG pode crescer sem interferir no leitor.

A primeira fase revelou:

- necessidade de distinguir chamada lógica de execução física;
- interferência do `st.cache_data` na observação;
- necessidade de monitorar chamadas originadas em `tools.py`;
- necessidade de separar campos do DNA de dependências globais;
- necessidade de registrar erros por ocorrência, e não apenas por resumo final.

---> Primeiro resultado histórico

O primeiro aparente erro do DNA foi uma diferença entre a quantidade de temas registrados e a quantidade de temas ativos.

A investigação mostrou que não havia perda.

Um novo tema havia saído dos estudos e entrado em testes reais.

O DNA não encontrou um defeito.

Encontrou uma evolução da Machina.

Esse episódio definiu um princípio central:

> O DNA não procura apenas erros.  
> O DNA procura diferenças.

Depois da diferença encontrada, decide-se se ela representa:

- evolução;
- mutação;
- redundância;
- inconsistência;
- ou erro de fato.

---> Relação entre obra e arquitetura

A obra nasceu primeiro.

Ela é quem dita a arquitetura de que precisa.

O DNA não foi criado para impor uma forma à Machina.

Foi criado porque a Machina revelou a necessidade de uma fonte única, auditável e evolutiva para suas informações essenciais.

O mesmo princípio valerá para o SPEC.

A arquitetura poderá ser redesenhada pela obra sempre que novas possibilidades técnicas, gráficas ou poéticas assim exigirem.

---> Papel do ABOUT_DNA

O ABOUT_DNA nasce junto com o objeto que descreve.

Ele é o primeiro ABOUT da Machina escrito em paralelo com a criação de seu próprio motivo.

O DNA orienta o ABOUT porque o uso real revela:

- o que pertence ao cromossomo;
- o que é global;
- o que é operacional;
- o que ainda não tem endereço;
- o que precisa ser preservado como decisão histórica.

Este documento existe para impedir que, no futuro, seja necessário garimpar longas conversas para responder:

> Para que mesmo fizemos isso?

A resposta é:

> Para dar à Machina uma auditoria viva, permanente, localizada e temporal de suas principais engrenagens, sem congelar a obra e sem retirar dela a autoridade sobre a própria arquitetura.

---> For the Records

O DNA já pertence à Machina.

Ele não é mais apenas uma experiência.

É parte da arquitetura viva da obra.
