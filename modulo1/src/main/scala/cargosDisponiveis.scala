import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

object cargosDisponiveis {
  def main(args: Array[String]) {
    if (args.length != 3) {
      System.err.println("Uso: cargosDisponiveis <ano> <estado> <turno>")
      System.exit(1)
    }
    val sc = new SparkContext()

    val caminhoBweb = "./spark/bweb/" + args(0) + "/" + args(1) + "/" + args(2) + ".txt"

    val votos = sc.textFile(caminhoBweb).filter(e => e.length > 0).map(e => e.split("\";\""))

    val cargosDisponiveis = votos.map(e => e(6)).distinct()
    //export csv
    val caminhoCSV = "./spark/dados/cargosDisponiveis_" + args(0) + "_" + args(1) + "_" + args(2)
    cargosDisponiveis.repartition(1).saveAsTextFile(caminhoCSV)

  }
}