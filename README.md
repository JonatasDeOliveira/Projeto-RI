# Domínio Problemas de Programação
### Recuperação da Informação

### Autores e Responsabilidades
- Douglas Soares Lins | dsl@cin.ufpe.br (Extração)
- Jonatas de Oliveira Clementino | joc@cin.ufpe.br (Classificador)
- Valdemiro Rosa Vieira Santos | vrvs@cin.ufpe.br (Crawling)

### Tarefas
#### Localizar Páginas Relevantes
1. Encontrar manualmente	10	sites	no	domínio
2. Implementar	2	estratégias: <br />
– Baseline:	busca em largura <br />
– Heurística
3. Comparar estatégias:	<br />
– Harvest	ratio:	(número	de	páginas relevantes coletadas)/(total	de	
páginas visitadas)	<br />
– Mostrar tabela	com	resultados <br />

• Importante:	<br />
– Evitar sobrecarregar	o	site	<br />
– Respeitar	o	robots.txt <br />
– Detectar	o	conteúdo	da	página	com	o	campo	Content-Type	

#### Detectar Páginas	com	Instâncias
1. Rotular exemplos positivos	e	negativos	(10	positivos	e	10	
negativos por	site)	
2. Criar	o	conjunto	de	features	(ex.:	bag	of	words)	usando	feature	
selection	(ex.	frequência ou	information	gain)	
3. Treinar	o	classificador	com	uma ferramenta	de	ML	(ex.:	scikitlearn,
weka etc) <br />
– Métodos:	Naïve	bayes,	Decision	tree	(J48),	SVM	(SMO),	Logitic	
regression	(logistic),	Multilayer	perceptron
4. Comparar estratégias:	<br />
– Accuracy,	precision	e	recall	<br />
– Tempo	de	treinamento <br />
– Mostrar tabela	com	os resultados

#### Extrair Instâncias	com	seus Valores	e	Atributos
1. Criar	um	wrapper	para cada	site	<br />
– Criação	do	conjunto rotulado
2. Implementar uma solução que funcione para todos os	sites	<br />
– Ex:	detectores	de	tipos	do	domínio
3. Comparar estratégias:	<br />
– Accuracy,	precision	e	recall	<br />
– Mostrar tabela	com	os resultados


### Curso
Universidade Federal de Pernambuco <br />
Centro de Informática <br />
Gradução em Ciência da Computação <br />
