========================================================== SPEC  
001 — ACROS Versão 1.0 (rascunho inicial)  
  
Assim Continuamos Reinventando Outros Sentidos  
  
==========================================================  
  
CONCEITO  
  
O ACROS é uma aparição da Machina.  
  
Não é uma página. Não é um puxadinho. Não cria infraestrutura própria.  
  
Entra no palco, utiliza os serviços existentes da Machina e sai naturalmente.  
  
----------------------------------------------------------  
  
OBJETIVO  
  
Gerar uma leitura acróstica a partir de uma sequência de caracteres  
informada pelo leitor.  
  
----------------------------------------------------------  
  
ENTRADA  
  
Campo livre.  
  
Não restringir a nomes próprios.  
  
Exemplos de uso:  
  
- nome do leitor  
- sobrenome  
- nome do PET  
- empresa  
- sigla  
- cidade  
- presente  
- palavra qualquer  
  
O leitor decide.  
  
----------------------------------------------------------  
  
PARÂMETROS  
  
Modo  
  
( ) Bem ( ) Mal  
  
Gênero  
  
( ) Masculino ( ) Feminino ( ) Neutro  
  
----------------------------------------------------------  
  
AUTORIDADE  
  
As listas .akr são a autoridade.  
  
O código nunca cria verbetes.  
  
Apenas consulta, sorteia e monta.  
  
----------------------------------------------------------  
  
ALGORITMO  
  
Para cada letra:  
  
- normalizar acentos para busca  
- selecionar a lista correspondente  
- RANDOM  
- evitar repetição  
- montar saída vertical  
  
----------------------------------------------------------  
  
LETRAS INEXISTENTES  
  
Mensagem:  
  
Nenhum verbete digno da sua entrada para a letra "X".  
  
----------------------------------------------------------  
  
INTEGRAÇÃO  
  
Popup  
  
↓  
  
Entrada  
  
↓  
  
Gerar  
  
↓  
  
Popup desaparece  
  
----------------------------------------------------------  
  
PALCO  
  
O resultado ocupa normalmente o palco da Machina.  
  
Nenhum layout especial.  
  
----------------------------------------------------------  
  
BOTÕES  
  
📋 Cópia  
  
📷 Retrato  
  
🚪 Porta Aberta  
  
----------------------------------------------------------  
  
RETRATO  
  
Utiliza exatamente o retrato padrão da Machina.  
  
Imagem sorteada normalmente em /images.  
  
Nenhuma regra específica do ACROS.  
  
----------------------------------------------------------  
  
PORTA ABERTA  
  
Encerra apenas a experiência ACROS.  
  
O palco retorna ao fluxo normal.  
  
Nenhuma janela permanece aberta.  
  
----------------------------------------------------------  
  
FILOSOFIA  
  
O leitor não recebe um manual.  
  
Recebe uma experiência.  
  
A descoberta faz parte da leitura.  
  
----------------------------------------------------------  
  
PRINCÍPIO ARQUITETURAL  
  
Toda nova funcionalidade deve entrar como uma aparição.  
  
Nunca como um puxadinho.  
  
==========================================================  
  
  
========================================================== LISTA INICIAL DE  
SPECS ==========================================================  
  
001 - ACROS  
  
002 - Retrato Serviço comum da Machina.  
  
003 - Copy Serviço comum da Machina.  
  
004 - Porta Aberta Novo conceito de navegação.  
  
005 - Aparição Novo conceito arquitetural.  
  
006 - Serviços Compartilhados Palco Copy Retrato Popup Fontes Imagens  
  
007 - MéM Princípio de redução e reutilização.  
  
008 - Descoberta A experiência precede a explicação.  
  
009 - Manual × Convite A Machina convida. Não conduz.  
  
010 - Vocabulário da Machina  
  
011 - Certidão de Nascimento  
  
012 - Conceitos × Funcionalidades Nunca misturar.  
  
013 - Experiência em andamento  
  
014 - Leitura da Machina  
  
Pergunta:  
  
Alguém já leu a Machina?  
  
Resposta:  
  
Não.  
  
========================================================== algumas  
decisões abertas:  
  
- o que fazer quando não houver adjetivo para determinada letra;  
= nenhum verbete digno do seu nome para a letra " * "  
- se a escolha entre vários adjetivos será aleatória; = RANDOM  
- se letras repetidas podem repetir o mesmo adjetivo; = preferência = NUNCA  
- tratamento de espaços, hífens e nomes compostos; = manter os "acidentes" as-is  
- normalização de acentos, por exemplo Á procurando em A; = VALIDO  
- se a saída terá apenas o acróstico ou também título/nome; =  
o acróstico por enquanto  
- como integrar Copy e Retrato. = ***  
  
___  
  
Histórico:  
___  
encontrei no bau um "tema interativo" antigo mas, sem o fonte: é um tema simples  
de ser "recomposto/refeito": titulo: acros" meta : criar "acrósticos" com o nome  
do leitor/leitora informado em um READ nome_proper, genero M/F  
== INPUT, mode == Bem ou Mal (text - radio - radio)  
___  
. buscar em "lista_adjetivos_M (ou F) adjetivos correspondentes a cada letra  
nome_proper/genero . output: lista_simples_itens = letra do nome_proper em  
negrito + subs(adjetivo, 2) . exibir as linhas geradas na vertical  
  
fontes de dados: acros_bem_F.txt, acros_bem_M.txt, acros_mal_F.txt  
e acros_mal_M.txt  
  
*** como teremos input de dados o local de implantação vai ser "pensado" ***  
talvez apenas um button que dispara uma janel pop-up na tela,  
colhe os dados e cria a resposta  
___  
