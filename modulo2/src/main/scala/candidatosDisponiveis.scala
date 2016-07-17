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

	// #4 LEVANTAR CANDIDATOS DISPONÍVEIS *
	// ==================================

	val candidatosDisponiveis = votos.filter(e => e(6) == args(3)).map(e => e(22)).distinct()
	//export csv
	val caminhoCSV = "/Users/Damasceno/Documents/AnaliseTSE/spark/dados/candidatosDisponiveis_" + args(0) + "_" + args(1) + "_" + args(2) + "_" + args(3)
	candidatosDisponiveis.repartition(1).saveAsTextFile(caminhoCSV)
  }
}