import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

object CargosDisponiveis {
  def main(args: Array[String]) {
    if (args.length <> 3) {
      System.err.println("Uso: CargosDisponiveis <ano> <estado> <turno>")
      System.exit(1)
    }
    val sc = new SparkContext()

    val caminhoBweb = "file:../spark/dados/" + 

    val caminhoEleitor = "file:.."

    val votos = sc.textFile(caminhoBweb).filter(e => e.length > 0).map(e => e.split("\";\""))

    val eleitores = sc.textFile(caminhoEleitor).filter(e => e.length > 0).map(e => e.split("\";\"")) 

    val cargosDisponiveis = votos.map(e => e(6)).distinct()
    //export csv
    cargosDisponiveis.repartition(1).saveAsTextFile("../spark/dados/cargosDisponiveis")

  }
}

