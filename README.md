# AnaliseTSE


## Sobre
Com o volume de dados cada vez mais disponíveis surge o desafio de transformar todo o volume de dados em conhecimento para uma organização ou para a sociedade. Inspirado nesse contexto, este projeto elaborado para a plataforma Spark, usufrui do [repositório de dados eleitorais](http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais/), formado pelos dados brutos das eleições desde 1945, disponibilizado pelo TSE.

O projeto desenvolvido em Scala tem como objetivo, analisar os dados acerca das eleições, incluindo dados coletados das urnas eletrônicas e do perfil do eleitorado. Através de uma consulta do usuário serão apresentadas informações e a correlação encontrada para a seleção, além de um gráfico de relacionamento.

> *“The goal is to turn data into information, and information into insight.”* – Carly Fiorina

## Softwares empregados
1. [Spark](http://spark.apache.org/) com desenvolvimento em Scala
2. [sbt](http://www.scala-sbt.org/) como project build tool
3. [Python](https://www.python.org/) para criar a interatividade com o usuário

## Código
O código desenvolvido Scala está divido em módulos de acordo com as pastas apresentadas neste repositório. O fonte de cada módulo se encontra dentro da pasta referente ao módulo e subpasta `src/main/scala`. Qualquer modificação neste exige o uso do software [sbt](http://www.scala-sbt.org/) como project build tool e o novo arquivo gerado deve ser copiado para a pasta raíz do módulo com o mesmo nome do disponibilizado anteriormente.
## Requisitos
Para utilizar o software como disponibilizado

1. [Apache Spark](http://spark.apache.org/) com o comando comando `spark-submit` podendo ser invocado sem especificar o path completo. Caso tenha problemas verifique este post no [StackOverflow](http://stackoverflow.com/a/21369216)
2. [Python](https://www.python.org/) com as seguintes dependências `prettytable`, `statsmodels`, `pandas` e `patsy`.

## Uso
O projeto desenvolvido possui como base a formatação dos arquivos *.txt disponíveis referentes as eleições de 2014 e deve funcionar corretamente para qualquer eleição com a mesma formatação.

Os arquivos de dados necessários podem ser encontrados no [repositório de dados eleitorais](http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais/).

O perfil do eleitorado pode ser encontrado na opção `Eleitorado` e deve ser inserido na pasta `spark/perfil` de acordo com o modelo disponível.

Os boletins de urna podem ser encontrados em `Resultados > Boletim de Urna - Primeiro ou Segundo Turno` e devem ser inseridos na pasta `spark/bweb` de acordo com o modelo disponível.

Para abrir o programa simplesmente abra o terminal, vá até a pasta AnaliseTSE e execute:

```
python snafu.py
```