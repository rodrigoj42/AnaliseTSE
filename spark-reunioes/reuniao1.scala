// abre arquivo e tira linhas vazias
val dados = sc.textFile("file:/Volumes/My Passport/bweb/*.txt").filter(e => e.length > 0)
// split dos dados + filtragem para presidente
val dadosPresidente = dados.map(e => e.split("\";\"")).filter(e => e(6) == "PRESIDENTE") 
// mantendo apenas nome do candidato (22) e numero de votos naquela secao (23)
val votos = dadosPresidente.map(e => (e(22), e(23).toInt))
// somando as secoes
val votosContados = votos.reduceByKey((a,b) => a+b)
// transformando (candidato, voto) em (voto, candidato) 
val votosInvertidos = votosContados.map(v => (v._2 , v._1))
// ordenacao (possibilitada pela inversao)
val votosOrdenados = votosInvertidos.sortByKey(false) 
// somando os candidatos
val total = votosOrdenados.reduce((a,b) => (a._1 + b._1, "Total"))(0)._1
// dividindo o numero de votos pelo total
val votosPorcentados = votosOrdenados.map(e => (e._1.toFloat*100/total._1, e._2))
// calculando a porcentagem de votos em cada secao
val porSecao;
val totalSecao;
val porcentoSecao;
// comparando com a porcentagem geral (quao geral?)
val diff;

votosOrdenados.take(20).foreach(println)

//e(1)(0) seção 
//e(1)(1) n do votável 
//e(0) n do votos
