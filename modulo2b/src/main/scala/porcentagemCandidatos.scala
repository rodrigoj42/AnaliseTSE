import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

object porcentagemCandidatos {
  def main(args: Array[String]) {
    if (args.length != 4) {
      System.err.println("Uso: candidatosDisponiveis <ano> <estado> <turno> <cargo>")
      System.exit(1)
    }
    val sc = new SparkContext()

    val caminhoBweb = "file:/home/yago/UFRJ/BigData/AnaliseTSE/spark/bweb/" + args(0) + "/" + args(1) + "/" + args(2) + ".txt"

    val votos = sc.textFile(caminhoBweb).filter(e => e.length > 0).map(e => e.split("\";\""))

    // CANDIDATOS DO CARGO E SEUS VOTOS
    // ================================

    // numero de votos que os candidatos do cargo selecionado tiveram
    val votosCandidatoCargo = votos.filter(e => e(6) == args(3)).map(e => (e(22), e(23).toInt)).reduceByKey((a,b) => a+b)
    // numero de votos totais para o cargo selecionado
    val votosCargo = votosCandidatoCargo.map(e => e._2).sum.toInt
    // numero de votos que os candidatos do cargo selecionado tiveram e a porcentagem dos votos
    val votosCandidatoQntd = votosCandidatoCargo.map(e => (e._1, e._2, e._2*100.toFloat/votosCargo)).sortBy(e => e._2, false)
    val votosCandidatoQntdCSV = votosCandidatoQntd.map(e => (e._1 + ";" + e._2 + ";" + e._3))

	  //export csv
	  val caminhoCSV = "/home/yago/UFRJ/BigData/AnaliseTSE/spark/dados/porcentagemCandidatos_" + args(0) + "_" + args(1) + "_" + args(2) + "_" + args(3)
	  votosCandidatoQntdCSV.repartition(1).saveAsTextFile(caminhoCSV)
  }
}