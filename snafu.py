from os import system, listdir, path
from prettytable import PrettyTable 

def ignorar_lixo_em(l):
    for i in l: 
        if i[0] == ".": l.remove(i)
    return l

def colocar_espacos(l):
    s = " "
    for i in l: s += i + " "
    return s

def gerar_path(s,l):
  dados_path = "./spark/dados/" + s
  for i in l:
    dados_path += "_" + i
  return dados_path + "/" 

def usuario_seleciona_de_variavel(disponiveis ,s):
    print "\nPor favor escolha um %s:" % s
    for i in range(len(disponiveis)):
        if "." in disponiveis[i]:
            disponiveis[i] = disponiveis[i][:disponiveis[i].index(".")]
            if disponiveis[i][-1] == '\n': disponiveis[i] = disponiveis[i][:-1]
        print i + 1,    
        print "- " + disponiveis[i]
    selecionado = disponiveis[input("Selecione um numero: ")-1]
    if selecionado[-1] == '\n': selecionado = selecionado[:-1]
    return selecionado

def usuario_seleciona_de_pasta(path, s):
    disponiveis = ignorar_lixo_em(listdir(path))
    selecionado = usuario_seleciona_de_variavel(disponiveis, s)
    path += selecionado + "/"
    return (path, selecionado)

def gerar_variavel(arquivo, call, sel):
    #print arquivo
    if path.exists(arquivo) == False:
        selecao = colocar_espacos(sel)
        #print call + selecao 
        system(call + selecao)
    try:
        csv = open(arquivo)
    except:
        csv = []
    disponiveis = []
    for line in csv:
        disponiveis.append(line)
    return disponiveis

def tabelar(lista, titulo, selecionado=None, n=5):
    lista_splitted = []
    adicionado = False
    t = PrettyTable(titulo)
    k = 0
    for i in lista[:n]:
        k += 1
        splitted = i.split(';')
        if selecionado == splitted[0]:
            adicionado = True
        if selecionado != None: splitted.insert(0,k)
        t.add_row(splitted)
    if adicionado == False and selecionado != None:
        for i in lista[n:]:
            k += 1
            splitted = i.split(';')
            if selecionado == splitted[0]:
                if selecionado != None: splitted.insert(0,k)
                t.add_row(splitted)
    return t

# 1
perfil_path = "./spark/perfil/"
bweb_path = "./spark/bweb/"

bweb_path, ano_selecionado    = usuario_seleciona_de_pasta(bweb_path, "ano")
bweb_path, estado_selecionado = usuario_seleciona_de_pasta(bweb_path, "estado")
bweb_path, turno_selecionado  = usuario_seleciona_de_pasta(bweb_path, "turno")

selecoes = [ano_selecionado, estado_selecionado, turno_selecionado]
selecoes_submit = [ano_selecionado, estado_selecionado, turno_selecionado]

# 2
arquivo = gerar_path("cargosDisponiveis", selecoes) + "part-00000"

cargosDisponiveis = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo1/cargosdisponiveis.jar", selecoes)


# 3a
cargo_selecionado = usuario_seleciona_de_variavel(cargosDisponiveis, "cargo")
selecoes.append(cargo_selecionado)
selecoes_submit.append("\"" + cargo_selecionado + "\"")

# 3b
arquivo = gerar_path("porcentagemCandidatos", selecoes) + "part-00000"
porcentagemCandidatos = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo2b/porcentagemcandidatos.jar", selecoes_submit)

arquivo = gerar_path("candidatosDisponiveis", selecoes) + "part-00000"
candidatosDisponiveis = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo2a/candidatosdisponiveis.jar", selecoes_submit)


candidato_selecionado = usuario_seleciona_de_variavel(candidatosDisponiveis, "candidato")
selecoes.append(candidato_selecionado)
selecoes_submit.append("\"" + candidato_selecionado + "\"")


# 4
indicadores = { "Estado civil":  8,
                "Faixa etaria": 10, 
                "Escolaridade": 12,
                       "Sexo" : 14}

valores = {  8 : {"SOLTEIRO":1 ,"CASADO":3,"VIUVO":5,"SEPARADO JUDICIALMENTE":7,"DIVORCIADO":9},
            10 : {"INVALIDA":-3, "16 ANOS":1, "17 ANOS":2, "18 A 20 ANOS":3, "21 A 24 ANOS":4, "25 A 34 ANOS":5, "35 A 44 ANOS":6, "45 A 59 ANOS":7, "60 A 69 ANOS":8, "70 A 79 ANOS":9, "SUPERIOR A 79 ANOS":10},
            12 : {"NAO INFORMADO":0, "ANALFABETO":1, "LE E ESCREVE":2, "ENSINO FUNDAMENTAL INCOMPLETO":3, "ENSINO FUNDAMENTAL COMPLETO":4, "ENSINO MEDIO INCOMPLETO":5, "SUPERIOR INCOMPLETO":7, "SUPERIOR COMPLETO":8},
            14 : {"NAO INFORMADO":0, "MASCULINO":2 , "FEMININO":4}}

print "\nPor favor escolha um indicador: "
indicadores_keys = indicadores.keys()
for i in range(len(indicadores_keys)):
    print i+1, 
    print '- ' + indicadores_keys[i] + '\n' 
indicador_selecionado = indicadores[indicadores_keys[input("Selecione um numero: ")-1]]
selecoes.append(str(indicador_selecionado))
selecoes_submit.append(str(indicador_selecionado))

print "\nPor favor escolha um valor: " 
valores_keys = valores[indicador_selecionado].keys()
for i in range(len(valores_keys)):
    print i+1, 
    print '- ' + valores_keys[i] + '\n' 
valor_selecionado = valores[indicador_selecionado][valores_keys[input("Selecione um numero: ")-1]]
selecoes.append(str(valor_selecionado))
selecoes_submit.append(str(valor_selecionado))

arquivo = gerar_path("analiseIndicador", selecoes) + "part-00000"
analiseIndicador = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo3/analiseindicador.jar", selecoes_submit)
system("python web/graficos.py " + "\"" + arquivo + "\"")

selecoes.append("correlacao")
arquivo = gerar_path("analiseIndicador", selecoes) + "part-00000"
analiseIndicador_correlacao = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo3/analiseindicador.jar", selecoes_submit)

# Apresentacao 2

selecoes = [ano_selecionado, estado_selecionado, turno_selecionado]
selecoes_submit = selecoes_submit[:-3]
arquivo = gerar_path("dadosInconsistentes", selecoes)

if path.exists(arquivo) == False:
    selecao = colocar_espacos(selecoes_submit)
    call = "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo5/dadosinconsistentes.jar"
    system(call + selecao)

dadosInconsistentes = {}

for i in ["secaoSemVoto", "votosComparadosSecao", "votosComparadosZona", "votosComparadosEstado"]:
    try:
        csv = open(arquivo + i + "/part-00000")
    except:
        print "***** ERRO: nao abriu " + i + " dos dados inconsistentes *****"
        csv = []
    dadosInconsistentesTmp = []
    for line in csv:
        dadosInconsistentesTmp.append(line)
    dadosInconsistentes[i] = dadosInconsistentesTmp


# Apresentacao 3
selecoes.append(cargo_selecionado)
selecoes.append(candidato_selecionado)
selecoes_submit.append("\"" + candidato_selecionado + "\"")
arquivo = gerar_path("analiseGeral", selecoes)  + "part-00000"
analiseGeral = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo4/analisegeral.jar", selecoes_submit)


# Preparando dadosInconsistentes["votosComparadosEstado"] e nomeValorIndicador para printar
votosComparadosEstado = ""
for i in dadosInconsistentes["votosComparadosEstado"]:
    votosComparadosEstado += i.replace("\n",";")

dadosInconsistentes["votosComparadosEstado"] = [votosComparadosEstado[:-1] + '\n']

nomeValorIndicador = valores[indicador_selecionado].keys()[valores[indicador_selecionado].values().index(valor_selecionado)]


# PRINTAR:
print "\n\nVotos recebidos pelos candidatos para " + cargo_selecionado + " em " + estado_selecionado
print tabelar(porcentagemCandidatos, ["Posicao do Candidato", "Nome do Candidato", "Numero de Votos", "Porcentagem"], candidato_selecionado)

print "\n\nRelacao entre a Porcentagem de Votos do(a) Candidato(a) " + candidato_selecionado + " e a Porcentagem do Indicador " + nomeValorIndicador
print tabelar(analiseIndicador, ["Candidato", "Porcentagem de Votos na Secao", "Valor do Indicador", "Porcentagem do Indicador na Secao"])
print "obs: Esses dados sao utilizados para a plotagem do grafico\n"

print tabelar(analiseIndicador_correlacao, ["Correlacao entre a Porcentagem de Votos na Secao e a Porcentagem do Indicador na Secao"])

print "\n\nAnalise do Perfil das Secoes e a Quantidade de Secoes Ganhas pelo Candidato"
print tabelar(analiseGeral, ["Candidato", "Estado Civil", "Faixa Etaria", "Escolaridade", "Sexo", "Quantidade de Secoes Ganhas pelo Candidato"])

print "\n\nSecoes que nao apresentam dados de Votos Recebidos e o seu Numero de Eleitores Correspondente"
print tabelar(dadosInconsistentes["secaoSemVoto"], ["N Zona", "N Secao", "Numero de Eleitores na Secao"])

print "\n\nComparacao do numero de Votos Recebidos na Secao com o Numero de Eleitores cadastrados"
print tabelar(dadosInconsistentes["votosComparadosSecao"], ["N Zona", "N Secao", "Numero de Votos na Secao", "Numero de Eleitores na Secao", "Porcentagem de Votos Recebidos na Secao"])
print "obs: Existem situacoes onde o Numero de Votos Recebidos supera o Numero de Eleitores para a Secao"

print "\n\nComparacao do numero de Votos Recebidos na Zona Eleitoral com o Numero de Eleitores cadastrados"
print tabelar(dadosInconsistentes["votosComparadosZona"], ["N Zona", "Numero de Votos na Zona", "Numero de Eleitores na Zona", "Porcentagem de Votos Recebidos na Zona"])

print "\n\nComparacao do numero de Votos Recebidos no Estado " + estado_selecionado + " com o Numero de Eleitores para o mesmo"
print tabelar(dadosInconsistentes["votosComparadosEstado"], ["Numero de Votos no Estado", "Numero de Eleitores no Estado", "Porcentagem de Votos Recebidos no Estado"])

