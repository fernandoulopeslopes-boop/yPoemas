# MANUAL DE INSTRUÇÕES — DNA DA MACHINA  
  
**Projeto:** Machina / yPoemas **Base de autoridade:** `SPEC — BUILD_DNA ÚNICO`,  
                                                                 
06/08/2026 **Estado:** manual técnico-organizacional. Nenhum  
código de produção é alterado por este documento.  
  
---  
  
## 1. O QUE É O DNA  
  
O DNA é a **autoridade cadastral central da Machina**.  
  
Sua função é reunir e coordenar, em um único ponto lógico, as  
informações técnicas e cadastrais necessárias para que a Machina saiba:  
  
- quais temas existem;  
- em que ordem participam do ambiente;  
- a que livro pertencem;  
- qual banco temático/visual utilizam;  
- quais métricas podem ser calculadas;  
- quais derivados precisam ser criados, atualizados ou removidos;  
- quais relações cadastrais precisam ser preservadas.  
  
O DNA **não substitui o `.ypo`**.  
  
O `.ypo` permanece a autoridade autoral e estrutural do tema.  
  
---  
  
## 2. PRINCÍPIO FUNDAMENTAL  
  
A unidade conceitual do DNA é:  
  
```text  
um tema  
um registro no DNA  
uma operação coordenadora  
```  
  
Forma:  
  
```text  
BUILD_DNA(nome_do_tema, operacao)  
```  
  
Operações:  
  
```text  
BUILD  
UPDATE  
REMOVE  
RODAPE  
```  
  
O autor não precisa lembrar uma sequência de Builds independentes.  
  
O coordenador executa internamente os algoritmos necessários.  
  
---  
  
## 3. FRONTEIRA FUNDADORA  
  
A arquitetura deve respeitar a regra de trabalho da parceria:  
  
> **o autor não faz código; o assistente não faz poesia.**  
  
Em termos de sistema:  
  
- o código decide **como** ler, validar, calcular, combinar e apresentar;  
- os arquivos autorais e listas externas decidem **o que** pode  
ser lido, ouvido ou visto;  
- o DNA registra decisões autorais já tomadas, mas não as cria;  
- defaults técnicos podem impedir quebra quando existe padrão conhecido;  
- se um default tocar em autoria/curadoria, ele é provisório  
e exige TALK imediato.  
  
O DNA centraliza **autoridade cadastral**, não autoria.  
  
---  
  
## 4. O QUE O DNA É — E O QUE NÃO É  
  
### O DNA é  
  
- cadastro central;  
- índice de autoridade;  
- coordenador de operações;  
- fonte de derivados;  
- mapa técnico dos temas;  
- ponto de consistência do ambiente.  
  
### O DNA não é  
  
- novo formato poético;  
- substituto do `.ypo`;  
- superlista de conteúdo;  
- molde obrigatório para todos os temas;  
- mecanismo de uniformização estética;  
- lugar para esconder decisões autorais no código.  
  
A centralização deve reduzir dispersão sem engessar a Machina.  
  
---  
  
## 5. AUTORIDADES DO SISTEMA  
  
### 5.1 Autoridade autoral e estrutural  
  
```text  
/data/<tema>.ypo  
```  
  
O `.ypo` é a autoridade do tema.  
  
Regras:  
  
- o corpo não pode ser corrigido silenciosamente;  
- nenhuma operação do DNA reescreve matéria autoral;  
- qualquer gravação exige backup prévio;  
- falha estrutural bloqueia a operação;  
- divergência é informada, nunca “consertada” por inferência.  
  
### 5.2 Autoridade cadastral  
  
```text  
DNA  
```  
  
O DNA concentra as informações cadastrais antes espalhadas em listas auxiliares.  
  
### 5.3 Derivados  
  
Arquivos reconstruíveis a partir das autoridades não são autoridades primárias.  
  
Exemplos:  
  
- listas gerais;  
- listas por livro;  
- Matrix;  
- léxico;  
- INDEXY;  
- relatórios;  
- fichas técnicas.  
  
---  
  
## 6. UM REGISTRO POR TEMA  
  
Cada tema possui **um único registro** no DNA.  
  
Campos já considerados úteis no SPEC:  
  
```text  
tema  
ordem  
livro  
banco_tematico  
versos  
verbetes_no_texto  
verbetes_do_tema  
total_de_itimos  
qtd_de_variacoes  
qtd_cientifica  
```  
  
Campos eliminados por MéM:  
  
```text  
codigo  
ativo  
```  
  
Razões:  
  
- `tema` já é a chave natural;  
- código M0001/M0002 criaria identidade artificial desnecessária;  
- `ativo` mistura existência local, teste e publicação web;  
- a publicação web é definida pelo que efetivamente é levado ao ambiente web.  
  
---  
  
## 7. TRÊS CLASSES DE INFORMAÇÃO  
  
Para não misturar conceitos, cada dado deve pertencer a uma destas classes.  
  
### 7.1 Cadastro  
  
Decisão organizacional do ambiente.  
  
Exemplos:  
  
```text  
tema  
ordem  
livro  
banco_tematico  
```  
  
### 7.2 Derivado calculável  
  
Resultado obtido a partir de autoridades.  
  
Exemplos:  
  
```text  
versos  
verbetes_no_texto  
verbetes_do_tema  
total_de_itimos  
qtd_de_variacoes  
qtd_cientifica  
```  
  
Se puder ser calculado com segurança, não deve depender de digitação manual.  
  
### 7.3 INFO autoral  
  
Banco externo de matéria autoral ou semiautoral utilizado pela Machina.  
  
Pode ser:  
  
- específico de um tema;  
- compartilhado por vários temas;  
- historicamente originado em um tema e posteriormente transversal.  
  
INFO não é sinônimo de campo do DNA.  
  
O DNA pode registrar a existência e os consumidores da INFO,  
mas não precisa absorver seu conteúdo.  
  
---  
  
## 8. LIVRO  
  
Conceito canônico:  
  
```text  
nome_do_tema : livro  
```  
  
Exemplo:  
  
```text  
Manusgrito : metalinguagem  
```  
  
Livros válidos considerados no SPEC:  
  
```text  
todos os temas  
livro vivo  
poemas  
jocosos  
ensaios  
variações  
metalinguagem  
sociais  
outros autores  
signos_fem  
signos_mas  
todos os signos  
```  
  
Regra:  
  
> **Machina não é livro.**  
  
Livro é classificação editorial/cadastral.  
  
---  
  
## 9. BANCO TEMÁTICO / VISUAL  
  
Conceito:  
  
```text  
nome_do_tema : banco_tematico  
```  
  
Exemplo:  
  
```text  
Manusgrito : Machina  
```  
  
Regras:  
  
- `Machina` pode ser banco visual padrão quando isso estiver contratado;  
- a escolha específica do banco é decisão de curadoria;  
- o código pode impedir quebra, mas não escolhe silenciosamente  
o que o leitor verá;  
- o DNA registra a relação autoral já decidida.  
  
---  
  
## 10. AMBIENTE LOCAL E WEB  
  
O DNA não precisa dos campos:  
  
```text  
publicado  
ativo  
em_teste  
```  
  
### Local  
  
Um tema pode:  
  
- existir em `/data`;  
- entrar em `rol_todos os temas.txt`;  
- ser construído;  
- ser testado;  
- ser revisado;  
- existir no DNA local.  
  
### Web  
  
O tema é publicado quando é efetivamente levado ao ambiente web.  
  
A diferença local/web é operacional, não propriedade permanente do tema.  
  
---  
  
## 11. BUILD  
  
Entrada:  
  
```text  
BUILD_DNA(nome_do_tema, BUILD)  
```  
  
### Pré-condições  
  
- `.ypo` existe em `/data`;  
- nome válido;  
- estrutura válida;  
- quantidade declarada de ítimos igual à quantidade real da coluna  
7 até a última;  
- UTF-8 verificável;  
- nenhuma divergência estrutural ignorada.  
  
Divergência bloqueia a operação.  
  
Nenhuma correção silenciosa.  
  
### Obrigações  
  
1. validar o `.ypo`;  
2. criar um único registro completo no DNA;  
3. inserir o tema em `rol_todos os temas.txt` em ordem canônica;  
4. registrar livro;  
5. registrar banco temático;  
6. atualizar `lexico_pt.txt`;  
7. atualizar `verbetes.txt`;  
8. criar Matrix;  
9. incluir tema no INDEXY;  
10. verificar UTF-8;  
11. normalizar somente header e rodapé dentro do contrato;  
12. preservar integralmente o corpo do `.ypo`.  
  
---  
  
## 12. UPDATE  
  
Entrada:  
  
```text  
BUILD_DNA(nome_do_tema, UPDATE)  
```  
  
Obrigações:  
  
1. validar novamente o `.ypo`;  
2. recalcular o único registro do tema no DNA;  
3. substituir a contribuição do tema no léxico;  
4. recriar Matrix;  
5. recalcular participação no INDEXY;  
6. verificar UTF-8;  
7. atualizar header/rodapé;  
8. impedir duplicação de registros;  
9. não acrescentar dados novos sobre dados antigos;  
10. preservar integralmente o corpo.  
  
Princípio:  
  
> **UPDATE substitui o estado derivado; não empilha versões.**  
  
---  
  
## 13. REMOVE  
  
Entrada:  
  
```text  
BUILD_DNA(nome_do_tema, REMOVE)  
```  
  
Obrigações:  
  
1. remover o registro do DNA;  
2. remover Matrix;  
3. eliminar contribuição do léxico;  
4. eliminar participação no INDEXY;  
5. remover referências cadastrais derivadas;  
6. retirar o tema das listas derivadas correspondentes;  
7. preservar o `.ypo`, salvo ordem explícita em contrário.  
  
Regra:  
  
```text  
retirar do ambiente != excluir arquivo autoral  
```  
  
REMOVE cadastral não é DELETE autoral.  
  
---  
  
## 14. RODAPE  
  
Entrada:  
  
```text  
BUILD_DNA(nome_do_tema, RODAPE)  
```  
  
Header canônico:  
  
```text  
*-  
*- nome_do_tema.ypo  
*-  
```  
  
Observações especiais existentes devem ser preservadas quando contratadas.  
  
Exemplo:  
  
```text  
*- Obs: Manter |03|03| e |05|01| pareados.  
```  
  
### Corpo  
  
Tudo entre o header e `<EOF>` permanece sem alteração.  
  
### Rodapé  
  
Tudo depois de `<EOF>` é rodapé cadastral.  
  
Contrato:  
  
- contém dados cadastrais;  
- não interfere na engrenagem;  
- `build_by` é a última linha cadastral;  
- data e hora de `build_by` permanecem exatamente como estão;  
- qualquer texto posterior recebe prefixo `*- `;  
- nenhuma linha do corpo pode ser movida, corrigida ou regravada.  
  
---  
  
## 15. FUNÇÕES INTERNAS ABSORVIDAS  
  
Deixam de existir como Builds independentes para o autor:  
  
```text  
build_novo_tema  
build_update_tema  
build_remove_tema  
build_atualizar_rodape_ypo  
build_info  
build_ficha_lexica  
```  
  
Passam a ser coordenadas internamente pelo DNA.  
  
Algoritmos especializados internos:  
  
```text  
build_lexico  
build_matrix  
build_indexy  
build_utf8_temas  
```  
  
Princípio:  
  
> **especialização interna; operação externa única.**  
  
---  
  
## 16. INFO — DEFINIÇÃO  
  
INFO é uma unidade externa ao código usada pela Machina.  
  
Sua função é preservar:  
  
- controle autoral;  
- variedade;  
- reutilização;  
- independência do motor;  
- edição sem intervenção em Python.  
  
O DNA pode apontar para uma INFO.  
  
O conteúdo da INFO continua externo.  
  
---  
  
## 17. INFO LOCAL E INFO TRANSVERSAL  
  
### INFO local  
  
Pertence semanticamente a um tema ou módulo.  
  
### INFO transversal  
  
Pode ter surgido historicamente em um tema e ser usada por vários.  
  
Exemplo já reconhecido:  
  
```text  
cidade / país  
```  
  
Essa geografia nasceu historicamente em **Fatos**, mas também aparece em outros  
temas e compõe um **universo ficcional compartilhado da Machina**.  
  
Regra:  
  
> origem histórica não implica exclusividade de uso.  
  
---  
  
## 18. CENTRALIZAR INFO SEM ENGESSAR  
  
O erro seria criar uma tabela única obrigando todas as INFOs  
a obedecerem ao mesmo formato.  
  
Organização recomendada:  
  
### Nível 1 — índice de INFOs  
  
Cadastro leve:  
  
```text  
nome_da_info  
tipo  
origem_historica  
arquivo  
consumidores  
```  
  
### Nível 2 — conteúdo externo  
  
Cada INFO mantém o formato adequado ao conteúdo.  
  
Possibilidades:  
  
```text  
.txt  
.csv  
.json  
.akr  
ou formato legado já existente  
```  
  
Regra:  
  
> **centralizar endereço e autoridade; preservar diversidade de conteúdo.**  
  
Nenhum banco é convertido apenas para “ficar igual”.  
  
---  
  
## 19. LISTAS AUXILIARES CANDIDATAS À APOSENTADORIA  
  
Conforme o SPEC:  
  
```text  
ativos.txt  
images.txt  
rol_todos os temas.txt  
rol_<livro>.txt  
info.txt  
```  
  
Aposentadoria não significa exclusão imediata.  
  
Estratégia:  
  
1. DNA absorve o conceito;  
2. consumidores passam a ler o DNA;  
3. listas ainda necessárias passam a ser geradas como derivados;  
4. somente depois deixam a execução ativa;  
5. exclusão física depende de ausência comprovada de consumidores  
e decisão explícita.  
  
---  
  
## 20. MIGRAÇÃO SEM REGRESSÃO  
  
A transição deve ser progressiva.  
  
Nunca trocar ao mesmo tempo:  
  
- autoridade cadastral;  
- consumidores;  
- formato;  
- interface;  
- publicação.  
  
### Fase A — DNA em paralelo  
  
- construir DNA;  
- manter listas atuais;  
- comparar resultados.  
  
### Fase B — DNA gera derivados  
  
- listas continuam disponíveis;  
- deixam de ser editadas manualmente quando houver equivalência comprovada;  
- tornam-se reconstruíveis.  
  
### Fase C — consumidores migram  
  
- um consumidor por vez;  
- COMPARE antes/depois;  
- homologação funcional.  
  
### Fase D — aposentadoria  
  
- somente arquivos realmente redundantes deixam a execução;  
- backups e histórico preservados.  
  
---  
  
## 21. SEGURANÇA  
  
Regras obrigatórias:  
  
- backup antes de gravação;  
- validação antes de alterar cadastro;  
- falha estrutural preserva o DNA vigente;  
- nenhum `.ypo` é corrigido silenciosamente;  
- nenhum corpo de `.ypo` é alterado pelo DNA;  
- derivados podem ser reconstruídos;  
- BUILD não duplica tema;  
- UPDATE não empilha estado anterior;  
- REMOVE não apaga autoria por inferência;  
- nenhuma decisão autoral é criada pelo código.  
  
---  
  
## 22. INTEGRIDADE DO `.ypo`  
  
Regra estrutural:  
  
```text  
último registro terminado em |  
<EOF>  
```  
  
Nada pode ser inserido entre o último registro válido e `<EOF>`.  
  
O parser deve respeitar semânticas históricas legítimas.  
  
Casos estruturais válidos não podem ser “corrigidos” por heurística simplista.  
  
O código é zelador do `.ypo`, não dono.  
  
---  
  
## 23. DERIVADOS RECONSTRUÍVEIS  
  
Idealmente, tudo o que não contém decisão autoral deve poder ser reconstruído.  
  
Exemplos:  
  
- Matrix;  
- léxico;  
- INDEXY;  
- listas por livro;  
- lista geral de temas;  
- ficha lexical;  
- métricas;  
- relatórios técnicos.  
  
Reconstrução é proteção contra divergência e corrupção.  
  
---  
  
## 24. ORDEM  
  
O campo `ordem` existe porque ordem é conceito cadastral.  
  
A regra definitiva ainda precisa ser formalizada quando houver  
impacto real nos consumidores.  
  
Até lá:  
  
- não inventar uma nova regra;  
- preservar a ordem vigente quando semanticamente importante;  
- usar alfabética somente onde já estiver contratada.  
  
---  
  
## 25. UTF-8  
  
BUILD e UPDATE verificam UTF-8.  
  
Até homologação definitiva:  
  
- diagnóstico obrigatório;  
- correção automática apenas quando comprovadamente segura;  
- não regravar conteúdo autoral só para “normalizar” encoding;  
- falha deve ser informada objetivamente.  
  
---  
  
## 26. MATRIX  
  
Matrix é derivada.  
  
Regras:  
  
- BUILD cria;  
- UPDATE recria;  
- REMOVE elimina a Matrix correspondente;  
- exclusão da Matrix não afeta `.ypo`;  
- localização/nome físico seguem a implementação vigente até SPEC próprio.  
  
---  
  
## 27. INDEXY  
  
INDEXY é derivado global.  
  
Regras:  
  
- BUILD inclui;  
- UPDATE recalcula;  
- REMOVE elimina;  
- nenhum tema fantasma;  
- nenhuma duplicação de referências.  
  
---  
  
## 28. LÉXICO E VERBETES  
  
São derivados da matéria autoral, não autoria nova.  
  
O DNA coordena:  
  
- inclusão;  
- substituição no UPDATE;  
- remoção no REMOVE;  
- reconstrução global quando necessária.  
  
A métrica de verbetes deve seguir a definição canônica vigente.  
  
---  
  
## 29. DEFAULTS  
  
Default é ferramenta técnica.  
  
Não é autorização para curadoria.  
  
Admissível quando:  
  
- existe padrão conhecido;  
- impede quebra;  
- é identificável;  
- pode ser substituído.  
  
Se afetar o que o leitor:  
  
```text  
lê  
ouve  
vê  
```  
  
deve ser tratado como provisório e abrir TALK.  
  
---  
  
## 30. TALK  
  
TALK é obrigatório quando a operação exige decisão que não pertence ao código.  
  
Exemplos:  
  
- banco visual;  
- texto;  
- som;  
- escolha de imagem;  
- renomeação autoral;  
- ambiguidade poética;  
- exclusão de matéria autoral;  
- classificação editorial não técnica;  
- default que altere experiência de leitura, escuta ou visão.  
  
Não é necessário TALK para mecanismo puramente técnico já contratado.  
  
---  
  
## 31. PROCEDIMENTO OPERACIONAL  
  
### CAC  
  
Checar:  
  
- base atual;  
- autoridade;  
- consumidor afetado;  
- contrato vigente.  
  
### MéM  
  
Mudar apenas o necessário.  
  
### FBF  
  
Executar a alteração completa no ponto contratado.  
  
### CAE  
  
Conferir:  
  
- sintaxe;  
- integridade;  
- ausência de regressão;  
- correspondência com SPEC;  
- derivados;  
- diferença antes/depois.  
  
### FECHA  
  
Quando houver alteração de produção:  
  
1. fazer o pedido exato;  
2. devolver arquivo corrigido;  
3. autor compara;  
4. homologação na Machina;  
5. aprovação.  
  
---  
  
## 32. NÃO-REGRESSÃO  
  
“Funcionar” não basta.  
  
Uma alteração aceitável:  
  
- resolve o ponto solicitado;  
- preserva o resto;  
- não desloca autoridade autoral;  
- não cria cadastro paralelo;  
- não cria nova obrigação manual;  
- não exige nova sequência técnica para o autor.  
  
---  
  
## 33. ORGANIZAÇÃO FÍSICA — PRINCÍPIO  
  
A organização física deve refletir função e autoridade sem reorganização  
estética gratuita.  
  
Conceitualmente:  
  
```text  
/data/  
    <temas>.ypo  
  
/data/acros/  
    <fontes ACROS>  
  
/base/  
    <cadastros ou derivados ainda necessários>  
  
DNA  
    autoridade cadastral  
  
INFOs  
    bancos externos específicos ou compartilhados  
  
DERIVADOS  
    Matrix  
    índices  
    léxicos  
    listas geradas  
```  
  
A localização física definitiva do DNA e do índice de INFOs precisa  
respeitar a estrutura real do projeto.  
  
---  
  
## 34. O QUE O DNA PODE GERAR  
  
Quando a migração estiver completa, o DNA deve poder produzir ou alimentar:  
  
- `rol_todos os temas`;  
- `rol_<livro>`;  
- relação tema → livro;  
- relação tema → banco temático;  
- cadastros usados pela interface;  
- relatórios técnicos;  
- validações;  
- rotinas BUILD/UPDATE/REMOVE;  
- coordenação de Matrix, léxico e INDEXY.  
  
A mesma informação não deve precisar ser mantida manualmente em vários lugares.  
  
---  
  
## 35. TESTE DE AUTORIDADE  
  
Para cada dado do ambiente, deve ser possível responder:  
  
```text  
quem é o dono desta informação?  
```  
  
Exemplos:  
  
```text  
texto / ítimos              → .ypo  
estrutura do tema           → .ypo  
livro do tema               → DNA  
banco visual do tema        → DNA, registrando decisão autoral  
métricas calculadas         → derivados do .ypo  
Matrix                      → derivado  
léxico                      → derivado global  
INDEXY                      → derivado global  
INFO autoral                → arquivo externo próprio  
lista de livros             → cadastro/derivado conforme implementação final  
```  
  
Se houver dois donos para o mesmo dado, existe risco de divergência.  
  
---  
  
## 36. CONTÍNUO DA ARQUITETURA  
  
A mesma ideia aparece em toda a Machina:  
  
```text  
.ypo  
↓  
bancos de ítimos  
↓  
listas auxiliares  
↓  
INFOs específicas  
↓  
INFOs transversais  
↓  
imagens / sons / recursos  
↓  
classificações  
↓  
listas de livros  
```  
  
O princípio permanece:  
  
> **matéria autoral fora do código; mecanismo dentro.**  
  
Isso permite ao autor exercer controle sem editar Python e ao  
código evoluir sem alterar a obra.  
  
---  
  
## 37. MANUAL DE USO — BUILD  
  
Fluxo humano ideal:  
  
```text  
1. o tema .ypo existe  
2. autor solicita BUILD  
3. BUILD_DNA valida  
4. se houver decisão autoral ausente → TALK  
5. se houver erro estrutural → aborta sem alteração  
6. se estiver válido → coordena derivados  
7. grava DNA  
8. produz COMPARE/relatório  
9. autor homologa  
```  
  
O BUILD nunca deve “adivinhar” uma decisão autoral para conseguir  
terminar silenciosamente.  
  
---  
  
## 38. MANUAL DE USO — UPDATE  
  
```text  
1. tema já existe no DNA  
2. .ypo foi alterado pelo autor  
3. UPDATE valida estado atual  
4. recalcula derivados  
5. substitui estado técnico anterior  
6. mantém uma única identidade cadastral  
7. preserva corpo  
8. apresenta resultado para homologação  
```  
  
---  
  
## 39. MANUAL DE USO — REMOVE  
  
```text  
1. tema existe no DNA  
2. REMOVE retira cadastro e derivados  
3. .ypo permanece intacto  
4. exclusão física exige ordem separada  
```  
  
Nunca confundir:  
  
```text  
não participar da Machina  
```  
  
com:  
  
```text  
deixar de existir como obra  
```  
  
---  
  
## 40. MANUAL DE USO — RODAPE  
  
RODAPE é operação limitada.  
  
Pode:  
  
- normalizar o cadastro pós-`<EOF>`;  
- preservar observações contratadas;  
- manter assinatura `build_by`.  
  
Não pode:  
  
- editar verso;  
- mover linha do corpo;  
- corrigir conteúdo;  
- inserir matéria entre último registro e `<EOF>`.  
  
---  
  
## 41. CRITÉRIO PARA NOVA INFO  
  
Antes de criar uma nova INFO, perguntar:  
  
1. é conteúdo ou mecanismo?  
2. pertence a um tema ou é transversal?  
3. já existe banco equivalente?  
4. precisa mesmo de novo arquivo?  
5. quem será autoridade?  
6. quais consumidores a utilizam?  
7. pode ser editada pelo autor sem tocar no código?  
  
Se a resposta indicar matéria autoral, deve permanecer fora do código.  
  
---  
  
## 42. CRITÉRIO PARA NOVO CAMPO NO DNA  
  
Um campo só entra no DNA quando:  
  
- representa cadastro necessário;  
- ou representa métrica técnica útil;  
- ou é necessário para reconstrução/coordenação;  
- e não duplica informação cuja autoridade já existe em outro lugar.  
  
Pergunta de MéM:  
  
> **se este campo for removido, perdemos informação real ou apenas  
conveniência?**  
  
Se for apenas conveniência, evitar.  
  
---  
  
## 43. CRITÉRIO PARA APOSENTAR UMA LISTA  
  
Uma lista só deixa de ser ativa quando:  
  
1. o DNA contém sua informação;  
2. existe forma de reconstruí-la;  
3. todos os consumidores foram identificados;  
4. consumidores migraram ou recebem derivado equivalente;  
5. COMPARE confirma equivalência;  
6. Machina foi homologada;  
7. backup existe.  
  
Antes disso, permanece.  
  
---  
  
## 44. PENDÊNCIAS DO SPEC — NÃO DECIDIDAS SILENCIOSAMENTE  
  
O SPEC deixou explicitamente em aberto:  
  
- formato exato da linha do DNA;  
- forma de informar livro e banco temático no BUILD;  
- regra definitiva de ordem;  
- consumidores ainda dependentes de `ativos.txt`, `images.txt` e `rol_*.txt`;  
- transição sem derrubar `ypo_mobile.py`;  
- destino físico das listas aposentadas;  
- regra exata de exclusão da Matrix;  
- UTF-8: diagnóstico versus correção segura;  
- homologação final do contrato de rodapé.  
  
Esses pontos não são “lacunas a preencher por criatividade”.  
  
São próximos pontos de implementação/TALK quando se tornarem necessários.  
  
---  
  
## 45. REGRA DE IMPLEMENTAÇÃO  
  
O Manual organiza o sistema.  
  
A implementação deve ocorrer por mini-SPECs FECHA.  
  
Nunca por uma grande refatoração única.  
  
Ordem segura:  
  
```text  
1. definir formato físico do DNA  
2. construir leitor/escritor do DNA  
3. gerar DNA inicial sem trocar consumidores  
4. comparar com cadastros vigentes  
5. migrar um consumidor por vez  
6. transformar listas redundantes em derivados  
7. retirar dependências antigas somente após homologação  
```  
  
---  
  
## 46. REGRA DE CONSISTÊNCIA  
  
Para qualquer tema, o sistema deve conseguir verificar:  
  
```text  
.ypo existe?  
registro DNA existe?  
livro existe?  
banco_tematico está resolvido?  
Matrix existe?  
léxico contém contribuição correta?  
INDEXY contém participação correta?  
listas derivadas conferem?  
```  
  
A verificação não deve modificar nada.  
  
Diagnóstico e correção são operações separadas.  
  
---  
  
## 47. REGRA DE RECUPERAÇÃO  
  
Se um derivado for corrompido:  
  
```text  
autoridade → reconstrução  
```  
  
Se o DNA for corrompido:  
  
```text  
backup vigente + autoridades autorais → recuperação controlada  
```  
  
Se um `.ypo` estiver estruturalmente inválido:  
  
```text  
bloquear operação  
não corrigir silenciosamente  
não contaminar outros temas  
```  
  
Erro em um tema não deve impedir operação independente em outro  
quando não houver dependência real.  
  
---  
  
## 48. REGRA DE VISIBILIDADE  
  
Toda operação coordenadora deve poder produzir um relatório mínimo:  
  
```text  
tema  
operação  
validações  
arquivos lidos  
derivados alterados  
cadastro antes  
cadastro depois  
warnings  
erros  
status  
```  
  
Isso permite CAE e evita mudanças invisíveis.  
  
---  
  
## 49. FILOSOFIA DO DNA  
  
O DNA não é uma tentativa de controlar a Machina.  
  
É uma tentativa de **saber onde cada coisa pertence**.  
  
A obra continua aberta, combinatória e capaz de exceção.  
  
O que se organiza é:  
  
- autoridade;  
- responsabilidade;  
- origem;  
- dependência;  
- reconstrução.  
  
Não o conteúdo.  
  
---  
  
## 50. RESUMO OPERACIONAL  
  
```text  
.ypo = autoridade autoral e estrutural  
  
DNA = autoridade cadastral  
  
INFO = matéria externa específica ou compartilhada  
  
DERIVADO = aquilo que pode ser reconstruído  
  
BUILD_DNA = coordenador  
  
TALK = fronteira quando técnica encontra autoria  
  
FECHA = forma segura de implementação  
```  
  
Regra de ouro:  
  
> **centralizar sem engessar; automatizar sem usurpar autoria;  
reconstruir sem tocar na obra.**  
  
---  
  
## 51. ESTADO DESTE MANUAL  
  
Este Manual consolida o `SPEC — BUILD_DNA ÚNICO` como documento operacional.  
  
Ele **não altera código de produção** e não declara resolvidas  
as pendências explicitamente deixadas em aberto pelo SPEC.  
  
Próxima etapa técnica, quando contratada:  
  
```text  
FORMATO FÍSICO DO DNA  
```  
  
Somente depois disso deve começar a implementação do primeiro  
mini-SPEC de código.  