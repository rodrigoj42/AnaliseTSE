// CONTAGEM DOS VOTOS
// ==================
val votos = sc.textFile("file:/Users/rodrigoj42/Downloads/bweb/*.txt").filter(e => e.length > 0).map(e => e.split("\";\""))

//  Legenda Boletim Web
//  0: data
//  1: hora
//  2: pleito
//  3: eleicao
//  4: uf
//  5: cod pergunta
//  6: desc pergunta
//  7: n zona
//  8: n seçao
//  9: n local votaçao
// 10: n partido
// 11: nome partido
// 12: cod municipio
// 13: nome municipio
// 14: data BU recebido
// 15: qntd eleitores aptos
// 16: qntd eleitores faltosos
// 17: qntd comparecimento
// 18: cod tipo eleicao
// 19: cod tipo urna
// 20: desc tipo urna
// 21: n do votavel
// 22: nome votavel
// 23: qntd votos
// 24: cod tipo votavel
// 25: n de urna efetivada
// 26: cod carga urna 1 efetivada
// 27: cod carga urna 2 efetivada
// 28: data carga urna efetivada
// 29: cod flashcard
// 30: cargo pergunta secao

val votosPresidente = votos.filter(e => e(6) == "PRESIDENTE").map(e => ((e(7) + "." + e(8), e(22)), e(23).toInt)).reduceByKey((a,b) => a+b)
val votosPresidenteMapeada = votosPresidente.map(e => (e._1._1,(e._1._2, e._2)))
  
val numVotosPorSecao = votosPresidente.map(e => (e._1._1, e._2)).reduceByKey((a,b) => a+b)

val votosPorcentagem = votosPresidenteMapeada.join(numVotosPorSecao).map(e => (e._1, e._2._1._1, e._2._1._2.toFloat*100/e._2._2))



// PERFIL DOS ELEITORES   
// ====================
val eleitores = sc.textFile("file:/Users/rodrigoj42/Downloads/perfil_eleitor/*.txt").filter(e => e.length > 0).map(e => e.split("\";\"")) 

//  Legenda Perfil Eleitorado
//  0: data
//  1: hora
//  2: periodo
//  3: UF
//  4: codigo municipio
//  5: municipio
//  6: numero zona
//  7: numero secao
//  8: codigo estado civil
//  9: descricao estado civil
// 10: codigo faixa etaria
// 11: desc faixa etaria
// 12: cod grau escolaridade
// 13: desc grau escolaridade
// 14: cod sexo
// 15: desc sexo 
// 16: qtd eleitores no perfil

// eleitores cadastrados em cada secao (diferente de numero de votos por secao)
val eleitoresSecao = eleitores.map(e => (e(6) + "." + e(7), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)

// possibilidade 1 => 4 rdds, 1 para cada indicador, depois so fazer filter, mas combinar seria mais complicado eu acho
val estadoCivil  = eleitores.map(e => ((e(6) + "." + e(7), e(9) ), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)
val faixaEtaria  = eleitores.map(e => ((e(6) + "." + e(7), e(11)), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)
val escolaridade = eleitores.map(e => ((e(6) + "." + e(7), e(13)), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)
val sexo         = eleitores.map(e => ((e(6) + "." + e(7), e(15)), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)

val estadoCivilCombinado  =  estadoCivil.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)
val faixaEtariaCombinada  =  faixaEtaria.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)
val escolaridadeCombinada = escolaridade.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)
val sexoCombinado         =         sexo.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)

val estadoCivilPorcentado  =  estadoCivilCombinado.map(e => ((e._1, e._2._1._1), e._2._1._2.toFloat*100/e._2._2))
val faixaEtariaPorcentada  =  faixaEtariaCombinada.map(e => ((e._1, e._2._1._1), e._2._1._2.toFloat*100/e._2._2))
val escolaridadePorcentada = escolaridadeCombinada.map(e => ((e._1, e._2._1._1), e._2._1._2.toFloat*100/e._2._2))
val sexoPorcentado         =         sexoCombinado.map(e => ((e._1, e._2._1._1), e._2._1._2.toFloat*100/e._2._2))

// possibilidade 2 => 1 rdd geral, depois so fazer filter + reduce, talvez mais facil pra combinar
val geral = eleitores.map(e => (e(6) + "." + e(7),(e(9), e(11), e(13), e(15), e(16).dropRight(1).toInt)))
val homensPorSecao = geral.map(e => ((e._1, e._2._4),e._2._5)).filter(e => e._2._1 == "MASCULINO").reduceByKey((a,b) => a + b)



// TESTES
// ======
val teste = votosPorcentagem.filter(e => (e._1 == "10.150"))
val teste = votosPresidenteMapeada.join(eleitoresSecao).map(e => (e._1, e._2._1._2.toFloat*100/e._2._2)).reduceByKey((a,b) => a+b)



// ANALISE ESTATISTICA
// ===================



// ANALISE HISTORICA
// =================

