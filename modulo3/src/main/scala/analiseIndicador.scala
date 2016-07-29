import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.mllib.stat.Statistics
import org.apache.spark.mllib.linalg._

object analiseIndicador {
  def main(args: Array[String]) {
    if (args.length != 7) {
      System.err.println("Uso: analiseIndicador <ano> <estado> <turno> <cargo> <candidato> <indicador> <valor>")
      System.exit(1)
    }
    val sc = new SparkContext()

    val caminhoBweb = "./spark/bweb/" + args(0) + "/" + args(1) + "/" + args(2) + ".txt"

    val caminhoEleitor = "./spark/perfil/" + args(0) + "/" + args(1) + ".txt"

    val votos = sc.textFile(caminhoBweb).filter(e => e.length > 0).map(e => e.split("\";\""))

    val eleitores = sc.textFile(caminhoEleitor).filter(e => e.length > 0).map(e => e.split("\";\""))

	// #3 SELECIONAR O CARGO SOLICITADO
	// ================================

	// numero de votos que um candidato teve em dada seção (zona.seção)
	val votosCandidato = votos.filter(e => e(6) == args(3)).map(e => ((e(7) + "." + e(8), e(22)), e(23).toInt)).reduceByKey((a,b) => a+b)
	val votosCandidatoMapeada = votosCandidato.map(e => (e._1._1,(e._1._2, e._2)))

	// total do número de votos por seção (somando os candidatos)
	val numVotosPorSecao = votosCandidato.map(e => (e._1._1, e._2)).reduceByKey((a,b) => a+b)

	// votos por candidato/total de votos
	val votosPorcentagem = votosCandidatoMapeada.join(numVotosPorSecao).map(e => (e._1, e._2._1._1, e._2._1._2.toDouble*100/e._2._2))

	// #5 LEVANTAR DADOS DO ELEITORADO
	// ===============================

	// eleitores cadastrados em cada secao (diferente de numero de votos por secao)
	val eleitoresSecao = eleitores.map(e => (e(6) + "." + e(7), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)

	// identificadores presentes no arquivo de perfil de eleitores
	// args(5) indicador, 8 = estadoCivil, 10 = faixaEtaria, 12 = escolaridade, 14 = sexo

	val indicador = eleitores.map(e => ((e(6) + "." + e(7), e(args(5).toInt)), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)

	// #6 LEVANTAR AS COMBINAÇÕES
	// ==========================

	// combinando indicador com total de eleitores na seção
	val indicadorCombinado = indicador.map(e => (e._1._1, (e._1._2, e._2))).join(eleitoresSecao)

	// transformando números absolutos em relativos
	val indicadorPorcentado = indicadorCombinado.map(e => (e._1, (e._2._1._1, e._2._1._2.toDouble*100/e._2._2)))

	// #7 ANÁLISE ESTATÍSTICA
	// ======================

	// candidato mais votado na seção
	// (seria bom normalizar isso aqui)
	val votosMax = votosPorcentagem.map(e => (e._1, (e._2, e._3))).reduceByKey((a, b) => (if (a._2 > b._2) a else b))

	// tipo de identificador mais comum em cada seção (se tem mais homens que mulheres, p.e.)
	val indicadorMax = indicadorPorcentado.reduceByKey((a, b) => (if (a._2 > b._2) a else b))

	// combinação de candidato mais votado com indicador mais comum 
	val votosIndicador = votosMax.join(indicadorMax).sortBy(e => e._2._2._2, false)

	// % de cada candidato combinada com distribuição demográfica (ambos por seção)
	val indicadorRelacionado = votosPorcentagem.map(e => (e._1, (e._2,e._3))).join(indicadorPorcentado)

	// #8 CORRELAÇÕES
	// ==============

	// filtrando votos para Marina e identificador de % de homens na seção
	val votosCandidatoValorSorted = indicadorRelacionado.filter(e => e._2._1._1 == args(4) && e._2._2._1 == args(6)).sortBy(e => e._1)
	// obs: RDDs neste formato serão usadas para gráfico "estilo Brexit" 

	// separando em RDDs ordenados para aplicar a correlação
	val votosCandidatoSortedPercent = votosCandidatoValorSorted.map(e => e._2._1._2)
	val votosValorSortedPercent = votosCandidatoValorSorted.map(e => e._2._2._2)

	// correlação entre votos da Marina e % de mulheres na seção
	val correlacaoCandidatoValor = sc.parallelize(Array(Statistics.corr(votosCandidatoSortedPercent, votosValorSortedPercent, "pearson").toString))

	// Exportando CSV
	val candidatoCSV = votosCandidatoValorSorted.map(e => e._2._1._1+";"+e._2._1._2+";"+e._2._2._1+";"+e._2._2._2)
	val caminho = "./spark/dados/analiseIndicador_" + args(0) + "_" + args(1) + "_" + args(2) + "_" + args(3) + "_" + args(4) + "_" + args(5) + "_" + args(6)
	candidatoCSV.repartition(1).saveAsTextFile(caminho)
	correlacaoCandidatoValor.repartition(1).saveAsTextFile(caminho + "_correlacao")

  }
}