import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

object dadosInconsistentes {
  def main(args: Array[String]) {
    if (args.length != 4) {
      System.err.println("Uso: dadosInconsistentes <ano> <estado> <turno> <cargo>")
      System.exit(1)
    }
    val sc = new SparkContext()

    val caminhoBweb = "file:/home/yago/UFRJ/BigData/AnaliseTSE/spark/bweb/" + args(0) + "/" + args(1) + "/" + args(2) + ".txt"
    val caminhoPerfil = "file:/home/yago/UFRJ/BigData/AnaliseTSE/spark/perfil/" + args(0) + "/" + args(1) + ".txt"

    //val caminhoBweb = "file:/Users/Damasceno/Documents/AnaliseTSE/spark/bweb/" + args(0) + "/" + args(1) + "/" + args(2) + ".txt"
    //val caminhoPerfil = "file:/Users/Damasceno/Documents/AnaliseTSE/spark/perfil/" + args(0) + "/" + args(1) + ".txt"

    val votos = sc.textFile(caminhoBweb).filter(e => e.length > 0).map(e => e.split("\";\""))
    val eleitores = sc.textFile(caminhoPerfil).filter(e => e.length > 0).map(e => e.split("\";\""))

    // numero de votos que um candidato teve em dada seção (zona.seção)
    val votosCandidato = votos.filter(e => e(6) == args(3)).map(e => ((e(7) + "." + e(8), e(22)), e(23).toInt)).reduceByKey((a,b) => a+b)

    // total do número de votos por seção (somando os candidatos)
    val numVotosPorSecao = votosCandidato.map(e => (e._1._1, e._2)).reduceByKey((a,b) => a+b)

    // eleitores cadastrados em cada secao (diferente de numero de votos por secao)
    val eleitoresSecao = eleitores.map(e => (e(6) + "." + e(7), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)

    // DADOS INCONSISTENTES
    // ====================

    // total do número de votos por seção (somando os candidatos) ---> val numVotosPorSecao
    // eleitores cadastrados em cada secao (diferente de numero de votos por secao) ---> val eleitoresSecao

    val votosComparadosSecao = numVotosPorSecao.join(eleitoresSecao).map(e => (e._1, e._2._1, e._2._2, e._2._1.toFloat*100/e._2._2)).sortBy(e=> e._4,false)
    // formato: (zona.secao, numVotosPorSecao, eleitoresSecao, % de votos recebidos na seção)
    val votosComparadosSecaoCSV = votosComparadosSecao.map(e => (e._1.split("\\.")(0) + ";" + e._1.split("\\.")(1) + ";" + e._2 + ";" + e._3 + ";" + e._4))
    val secaoSemVoto = eleitoresSecao.leftOuterJoin(numVotosPorSecao).filter(e => e._2._2.isDefined == false).map(e => (e._1.split("\\."), e._2._1)).sortBy(e=> e._2,false)
    val secaoSemVotoCSV = secaoSemVoto.map(e => (e._1(0) + ";" + e._1(1) + ";" + e._2))
    // formato: (zona.secao, eleitoresSecao)

    // eleitores cadastrados em cada zona
    val eleitoresZona = eleitores.map(e => (e(6), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)
    // total do número de votos por zona (somando os candidatos)
    val numVotosPorZona = votos.filter(e => e(6) == args(3)).map(e => (e(7), e(23).toInt)).reduceByKey((a,b) => a+b)
    val votosComparadosZona = numVotosPorZona.join(eleitoresZona).map(e => (e._1, e._2._1, e._2._2, e._2._1.toFloat*100/e._2._2)).sortBy(e=> e._4,false)
    val votosComparadosZonaCSV = votosComparadosZona.map(e => (e._1 + ";" + e._2 + ";" + e._3 + ";" + e._4))
    //val zonaSemVoto = eleitoresZona.leftOuterJoin(numVotosPorZona).filter(e => e._2._2.isDefined == false).map(e => (e._1, e._2._1))

    // eleitores cadastrados no estado
    val eleitoresEstado = eleitores.map(e => (e(16).dropRight(1).toInt)).sum.toInt
    // total do número de votos por estado (somando os candidatos)
    val numVotosPorEstado = votos.filter(e => e(6) == args(3)).map(e => (e(23).toInt)).sum.toInt
    val votosComparadosEstado = sc.parallelize(Array(numVotosPorEstado.toString, eleitoresEstado.toString, (numVotosPorEstado.toFloat*100/eleitoresEstado).toString))

  	//export csv
  	val caminhoCSV = "/home/yago/UFRJ/BigData/AnaliseTSE/spark/dados/dadosInconsistentes_" + args(0) + "_" + args(1) + "_" + args(2) + "/"
    //val caminhoCSV = "/Users/Damasceno/Documents/AnaliseTSE/spark/dados/dadosInconsistentes_" + args(0) + "_" + args(1) + "_" + args(2) + "/"
  	votosComparadosSecaoCSV.repartition(1).saveAsTextFile(caminhoCSV + "votosComparadosSecao")
    secaoSemVotoCSV.repartition(1).saveAsTextFile(caminhoCSV + "secaoSemVoto")
    votosComparadosZonaCSV.repartition(1).saveAsTextFile(caminhoCSV + "votosComparadosZona")
    votosComparadosEstado.repartition(1).saveAsTextFile(caminhoCSV + "votosComparadosEstado")
    }
}