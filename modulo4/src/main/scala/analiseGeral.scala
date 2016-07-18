import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

object analiseGeral {
  def main(args: Array[String]) {
    if (args.length != 5) {
      System.err.println("Uso: analiseGeral <ano> <estado> <turno> <cargo> <candidato>")
      System.exit(1)
    }
    val sc = new SparkContext()

    val caminhoBweb = "file:/home/yago/UFRJ/BigData/AnaliseTSE/spark/bweb/" + args(0) + "/" + args(1) + "/" + args(2) + ".txt"
    val caminhoPerfil = "file:/home/yago/UFRJ/BigData/AnaliseTSE/spark/perfil/" + args(0) + "/" + args(1) + ".txt"

    val votos = sc.textFile(caminhoBweb).filter(e => e.length > 0).map(e => e.split("\";\""))
    val eleitores = sc.textFile(caminhoPerfil).filter(e => e.length > 0).map(e => e.split("\";\""))

    // numero de votos que um candidato teve em dada seção (zona.seção)
    val votosCandidato = votos.filter(e => e(6) == args(3)).map(e => ((e(7) + "." + e(8), e(22)), e(23).toInt)).reduceByKey((a,b) => a+b)
    val votosCandidatoMapeada = votosCandidato.map(e => (e._1._1,(e._1._2, e._2)))

    // total do número de votos por seção (somando os candidatos)
    val numVotosPorSecao = votosCandidato.map(e => (e._1._1, e._2)).reduceByKey((a,b) => a+b)

    // votos por candidato/total de votos
    val votosPorcentagem = votosCandidatoMapeada.join(numVotosPorSecao).map(e => (e._1, e._2._1._1, e._2._1._2.toDouble*100/e._2._2))

    // eleitores cadastrados em cada secao (diferente de numero de votos por secao)
    val eleitoresSecao = eleitores.map(e => (e(6) + "." + e(7), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)

    // candidato mais votado na seção
    // (seria bom normalizar isso aqui)
    val votosMax = votosPorcentagem.map(e => (e._1, (e._2, e._3))).reduceByKey((a, b) => (if (a._2 > b._2) a else b))

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
    val candidatoPorPerfil = qntdVotosPorPerfil.filter(e=> (e._1._1 == args(4))).sortBy(e=> e._2,false).map(e => (e._1._1 + ";" + e._1._2 + ";" + e._1._3 + ";" + e._1._4 + ";" + e._1._5 + ";" + e._2))

  	//export csv
  	val caminhoCSV = "/home/yago/UFRJ/BigData/AnaliseTSE/spark/dados/analiseGeral_" + args(0) + "_" + args(1) + "_" + args(2) + "_" + args(3) + "_" + args(4)
  	candidatoPorPerfil.repartition(1).saveAsTextFile(caminhoCSV)
    }
}