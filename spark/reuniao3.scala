import org.apache.spark.mllib.stat.Statistics
import org.apache.spark.mllib.linalg._

// OBS: MARCADOS COM '*' PRECISAM DE INTERVENÇÃO 

// ==================
// INÍCIO DO MÓDULO 1
// ==================

// #1 SELECIONAR OS ARQUIVOS NECESSÁRIOS *
// =====================================

// CONTAGEM DOS VOTOS
val votos = sc.textFile("file:/Users/damasceno/Desktop/bweb/*.txt").filter(e => e.length > 0).map(e => e.split("\";\""))

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

// PERFIL DOS ELEITORES
val eleitores = sc.textFile("file:/Users/damasceno/Desktop/perfil_eleitor/*.txt").filter(e => e.length > 0).map(e => e.split("\";\"")) 

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

// #2 LEVANTAR OS CARGOS DISPONÍVEIS
// =================================
val cargosDisponiveis = votos.map(e => e(6)).distinct()

//export csv

// ===============
// FIM DO MÓDULO 1
// ===============


// ==================
// INÍCIO DO MÓDULO 2
// ==================

// #3 SELECIONAR O CARGO SOLICITADO *
// ================================

// numero de votos que um candidato teve em dada seção (zona.seção)
val votosCandidato = votos.filter(e => e(6) == "PRESIDENTE").map(e => ((e(7) + "." + e(8), e(22)), e(23).toInt)).reduceByKey((a,b) => a+b)
val votosCandidatoMapeada = votosCandidato.map(e => (e._1._1,(e._1._2, e._2)))

// total do número de votos por seção (somando os candidatos)
val numVotosPorSecao = votosCandidato.map(e => (e._1._1, e._2)).reduceByKey((a,b) => a+b)

// votos por candidato/total de votos
val votosPorcentagem = votosCandidatoMapeada.join(numVotosPorSecao).map(e => (e._1, e._2._1._1, e._2._1._2.toDouble*100/e._2._2))

// #4 LEVANTAR CANDIDATOS DISPONÍVEIS *
// ==================================

val candidatosDisponiveis = votos.filter(e => e(6) == "PRESIDENTE").map(e => e(22)).distinct()

//export csv

// ===============
// FIM DO MÓDULO 2
// ===============


// ==================
// INÍCIO DO MÓDULO 3
// ==================

// #5 LEVANTAR DADOS DO ELEITORADO
// ===============================

// eleitores cadastrados em cada secao (diferente de numero de votos por secao)
val eleitoresSecao = eleitores.map(e => (e(6) + "." + e(7), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)

// identificadores presentes no arquivo de perfil de eleitores
val estadoCivil  = eleitores.map(e => ((e(6) + "." + e(7), e(9) ), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)
val faixaEtaria  = eleitores.map(e => ((e(6) + "." + e(7), e(11)), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)
val escolaridade = eleitores.map(e => ((e(6) + "." + e(7), e(13)), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)
val sexo         = eleitores.map(e => ((e(6) + "." + e(7), e(15)), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)

// #6 LEVANTAR AS COMBINAÇÕES
// ==========================

// combinando indicador com total de eleitores na seção
val estadoCivilCombinado  =  estadoCivil.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)
val faixaEtariaCombinado  =  faixaEtaria.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)
val escolaridadeCombinado = escolaridade.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)
val sexoCombinado         =         sexo.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)

// transformando números absolutos em relativos
val estadoCivilPorcentado  =  estadoCivilCombinado.map(e => (e._1, (e._2._1._1, e._2._1._2.toDouble*100/e._2._2)))
val faixaEtariaPorcentado  =  faixaEtariaCombinado.map(e => (e._1, (e._2._1._1, e._2._1._2.toDouble*100/e._2._2)))
val escolaridadePorcentado = escolaridadeCombinado.map(e => (e._1, (e._2._1._1, e._2._1._2.toDouble*100/e._2._2)))
val sexoPorcentado         =         sexoCombinado.map(e => (e._1, (e._2._1._1, e._2._1._2.toDouble*100/e._2._2)))

// #7 ANÁLISE ESTATÍSTICA
// ======================

// candidato mais votado na seção
// (seria bom normalizar isso aqui)
val votosMax = votosPorcentagem.map(e => (e._1, (e._2, e._3))).reduceByKey((a, b) => (if (a._2 > b._2) a else b))

// tipo de identificador mais comum em cada seção (se tem mais homens que mulheres, p.e.)
val estadoCivilMax  =  estadoCivilPorcentado.reduceByKey((a, b) => (if (a._2 > b._2) a else b))
val faixaEtariaMax  =  faixaEtariaPorcentado.reduceByKey((a, b) => (if (a._2 > b._2) a else b))
val escolaridadeMax = escolaridadePorcentado.reduceByKey((a, b) => (if (a._2 > b._2) a else b))
val sexoMax         =         sexoPorcentado.reduceByKey((a, b) => (if (a._2 > b._2) a else b))

// combinação de candidato mais votado com indicador mais comum 
val votosEstadoCivil  =  votosMax.join(estadoCivilMax).sortBy(e => e._2._2._2, false)
val votosFaixaEtaria  =  votosMax.join(faixaEtariaMax).sortBy(e => e._2._2._2, false)
val votosEscolaridade = votosMax.join(escolaridadeMax).sortBy(e => e._2._2._2, false)
val votosSexo         =         votosMax.join(sexoMax).sortBy(e => e._2._2._2, false)

// % de cada candidato combinada com distribuição demográfica (ambos por seção)
val estadoCivilRelacionado  = votosPorcentagem.map(e => (e._1, (e._2,e._3))).join(estadoCivilPorcentado)
val faixaEtariaRelacionado  = votosPorcentagem.map(e => (e._1, (e._2,e._3))).join(faixaEtariaPorcentado)
val escolaridadeRelacionado = votosPorcentagem.map(e => (e._1, (e._2,e._3))).join(escolaridadePorcentado)
val sexoRelacionado         = votosPorcentagem.map(e => (e._1, (e._2,e._3))).join(sexoPorcentado)

// #8 CORRELAÇÕES *
// ==============

// // filtragens para Marina (vai ter algum uso??)
// val estadoCivilRelacionadoMarina  =  estadoCivilRelacionado.filter(e => e._2._1._1 == "MARINA SILVA")
// val faixaEtariaRelacionadoMarina  =  faixaEtariaRelacionado.filter(e => e._2._1._1 == "MARINA SILVA")
// val escolaridadeRelacionadoMarina = escolaridadeRelacionado.filter(e => e._2._1._1 == "MARINA SILVA")
// val sexoRelacionadoMarina         =         sexoRelacionado.filter(e => e._2._1._1 == "MARINA SILVA")

// filtrando votos para Marina e identificador de % de homens na seção
val votosMarinaFemSorted = sexoRelacionado.filter(e => e._2._1._1 == "MARINA SILVA" && e._2._2._1 == "FEMININO").sortBy(e => e._1)
// obs: RDDs neste formato serão usadas para gráfico "estilo Brexit" 

// separando em RDDs ordenados para aplicar a correlação
val votosMarinaSortedPercent = votosMarinaFemSorted.map(e => e._2._1._2)
val votosFemSortedPercent = votosMarinaFemSorted.map(e => e._2._2._2)

// correlação entre votos da Marina e % de mulheres na seção
val correlacaoMarinaMasc: Double = Statistics.corr(votosMarinaSortedPercent, votosFemSortedPercent, "pearson")

// filtrando votos para Marina
val votosMarinaFESorted = faixaEtariaRelacionado.filter(e => e._2._1._1 == "MARINA SILVA").sortBy(e => e._1)
// separando em RDDs ordenados para aplicar a correlação
val votosMarinaSortedPercent = votosMarinaFESorted.map(e => e._2._1._2)
val votosFESortedPercent = votosMarinaFESorted.map(e => e._2._2._2)
// correlação entre votos da Marina e % de homens na seção
val correlacaoMarinaFE: Double = Statistics.corr(votosMarinaSortedPercent, votosFESortedPercent, "pearson")

// ===============
// FIM DO MÓDULO 3
// ===============


// ==================
// INÍCIO DO MÓDULO 4
// ==================

// DADOS INCONSISTENTES
// ====================

// copy & paste do arquivo antigo
//val teste = votosCandidatoMapeada.join(eleitoresPorSecao).map(e => (e._1, e._2._1._2.toFloat*100/e._2._2)).reduceByKey((a,b) => a+b)

// ===============
// FIM DO MÓDULO 4
// ===============


// ==================
// INÍCIO DO MÓDULO 5
// ==================

// #9 TIPO DE SEÇÃO EM QUE O CANDIDATO MELHOR PERFORMA *
// ===================================================

// distribuição demográfica
val eleitoresPerfil = eleitores.map(e=> (e(6) + "." + e(7),  (e(9), e(11), e(13), e(15), e(16).dropRight(1).toInt))).join(eleitoresSecao)
val perfilPorcentado = eleitoresPerfil.map(e=> (e._1, (e._2._1._1,e._2._1._2,e._2._1._3,e._2._1._4,e._2._1._5.toFloat*100/e._2._2.toFloat)))

// perfil com maior % (por seção)
val votosPerfilMax = perfilPorcentado.reduceByKey((a, b) => (if (a._5 > b._5) a else b))
// combinação de candidato mais votado com perfil mais comum
val maisVotadosPerfil = votosMax.join(votosPerfilMax)

// mágica (reduceByKey)
val qntdVotosPorPerfil = maisVotadosPerfil.map(e=> ((e._2._1._1, e._2._2._1, e._2._2._2,e._2._2._3,e._2._2._4),1)).reduceByKey((a,b)=> a+b)

// analise perfil por candidato
val marinaPorPerfil = qntdVotosPorPerfil.filter(e=> (e._1._1 =="MARINA SILVA")).sortBy(e=> e._2,false)
val dilmaPorPerfil = qntdVotosPorPerfil.filter(e=> (e._1._1 =="DILMA")).sortBy(e=> e._2,false)

// ===============
// FIM DO MÓDULO 5
// ===============


// Exportando CSV
val marinaCSV = votosMarinaFESorted.map(e => e._2._1._1+";"+e._2._1._2+";"+e._2._2._1+";"+e._2._2._2)
marinaCSV.repartition(1).saveAsTextFile("./export/marina") 

val marinaFemCSV = votosMarinaFemSorted.map(e => e._2._1._1+";"+e._2._1._2+";"+e._2._2._1+";"+e._2._2._2)
marinaFemCSV.repartition(1).saveAsTextFile("./export/marina/reuniao2")

// TESTES DE VALIDAÇÃO
// ===================

println()
println("Testes de Validação")
println()
println()
println("% votos para Marina Silva em dada seção e % de mulheres")
votosMarinaFemSorted.take(5).foreach(println)
println()
println("Correlação entre % de votos de Luciana e % de jovens usando MLlib")
//println(correlacaoLucianaFE)
println()
println()
println("% de votos de Marina e Distribuição Demográfica por Faixa Etária")
votosMarinaFESorted.take(5).foreach(println)
println()
println()
println("Tipo de seção em que Marina melhor performou")
marinaPorPerfil.take(10).foreach(println)


// ANALISE HISTORICA
// =================