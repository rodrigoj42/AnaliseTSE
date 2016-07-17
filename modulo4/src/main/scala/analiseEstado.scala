import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

object candidatosDisponiveis {
  def main(args: Array[String]) {
    if (args.length != 4) {
      System.err.println("Uso: candidatosDisponiveis <ano> <estado> <turno> <cargo>")
      System.exit(1)
    }
    val sc = new SparkContext()

    val caminhoBweb = "file:/Users/Damasceno/Documents/AnaliseTSE/spark/bweb/" + args(0) + "/" + args(1) + "/" + args(2) + ".txt"

    val votos = sc.textFile(caminhoBweb).filter(e => e.length > 0).map(e => e.split("\";\""))

    // DADOS INCONSISTENTES
    // ====================

    // total do número de votos por seção (somando os candidatos) ---> val numVotosPorSecao
    // eleitores cadastrados em cada secao (diferente de numero de votos por secao) ---> val eleitoresSecao

    val votosComparados = numVotosPorSecao.join(eleitoresSecao).map(e => (e._1, e._2._1, e._2._2, e._2._1.toFloat*100/e._2._2)).sortBy(e=> e._4,false)
    // formato: (zona.secao, numVotosPorSecao, eleitoresSecao, % de votos recebidos na seção)
    val secaoSemVoto = eleitoresSecao.leftOuterJoin(numVotosPorSecao).filter(e => e._2._2.isDefined == false).map(e => (e._1, e._2._1))
    // formato: (zona.secao, eleitoresSecao)

    // eleitores cadastrados em cada zona
    val eleitoresZona = eleitores.map(e => (e(6), e(16).dropRight(1).toInt)).reduceByKey((a,b) => a+b)
    // total do número de votos por zona (somando os candidatos)
    val numVotosPorZona = votos.filter(e => e(6) == "PRESIDENTE").map(e => (e(7), e(23).toInt)).reduceByKey((a,b) => a+b)

    val votosComparadosZona = numVotosPorZona.join(eleitoresZona).map(e => (e._1, e._2._1, e._2._2, e._2._1.toFloat*100/e._2._2)).sortBy(e=> e._4,false)
    val zonaSemVoto = eleitoresZona.leftOuterJoin(numVotosPorZona).filter(e => e._2._2.isDefined == false).map(e => (e._1, e._2._1))

    // eleitores cadastrados no estado
    val eleitoresEstado = eleitores.map(e => (e(16).dropRight(1).toInt)).sum.toInt
    // total do número de votos por estado (somando os candidatos)
    val numVotosPorEstado = votos.filter(e => e(6) == "PRESIDENTE").map(e => (e(23).toInt)).sum.toInt

    val votosComparadosEstado = numVotosPorEstado.toFloat*100/eleitoresEstado

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

  	//export csv
  	val caminhoCSV = "/Users/Damasceno/Documents/AnaliseTSE/spark/dados/candidatosDisponiveis_" + args(0) + "_" + args(1) + "_" + args(2) + "_" + args(3)
  	candidatosDisponiveis.repartition(1).saveAsTextFile(caminhoCSV)
    }
}