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
    for i in lista[:n]:
        splitted = i.split(';')
        if selecionado == splitted[0]:
            adicionado = True
        t.add_row(splitted)
    if adicionado == False and selecionado != None:
        for i in lista[n:]:
            splitted = i.split(';')
            if selecionado == splitted[0]:
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

# Apresentacao 2

selecoes = [ano_selecionado, estado_selecionado, turno_selecionado]
selecoes_submit = selecoes_submit[:-3]
arquivo = gerar_path("dadosInconsistentes", selecoes)

if path.exists(arquivo) == False:
    selecao = colocar_espacos(selecoes_submit)
    call = "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo5/dadosinconsistentes.jar"
    system(call + selecao)
try:
    csv = open(arquivo)
except:
    csv = []
dadosInconsistentes = []
for line in csv:
    dadosInconsistentes.append(line)

# Apresentacao 3
selecoes.append(cargo_selecionado)
selecoes.append(candidato_selecionado)
selecoes_submit.append("\"" + candidato_selecionado + "\"")
arquivo = gerar_path("analiseGeral", selecoes)
analiseGeral = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo4/analisegeral.jar", selecoes_submit)


# PRINTAR:
print tabelar(porcentagemCandidatos, ["Candidato", "Numero de Votos", "Porcentagem"], candidato_selecionado)
print tabelar(analiseIndicador, ["Candidato", "Porcentagem de Votos na Secao", "Valor do Indicador", "Porcentagem do Indicador na Secao"])
# falta correlacao 
print tabelar(analiseGeral, ["Candidato", "Estado Civil Prevalente na Secao", "Faixa Etaria", "Escolaridade", "Sexo", "Quantidade de Secoes Ganhadas pelo Candidato"])
# print tabelar(dadosInconsistentes, )


# porcentagemCandidatos, analiseIndicador, analiseGeral, dadosInconsistentes  
