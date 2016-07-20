from os import system, listdir, path

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
<<<<<<< Updated upstream
=======
    #i.replace(" ","\\ ")
>>>>>>> Stashed changes
    dados_path += "_" + i
  return dados_path + "/" 

def usuario_seleciona_de_variavel(disponiveis ,s):
    print "\nPor favor escolha um %s:" % s
    for i in range(len(disponiveis)):
        if "." in disponiveis[i]:
            disponiveis[i] = disponiveis[i][:disponiveis[i].index(".")]
<<<<<<< Updated upstream
=======
            if disponiveis[i][-1] == '\n': disponiveis[i] = disponiveis[i][:-1]
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
def gerar_variavel(arquivo, call, selecoes):
    print "ENTROU!!!!!!!!!!!!!!!!!!",arquivo
    if path.exists(arquivo) == False:
        selecao = colocar_espacos(selecoes)
        print "SELECAO",selecao
        print "CAHAMADA!!!!!!!!!!!!!!!!!!!!!!!___+++++++",call+selecao
=======
def gerar_variavel(arquivo, call, sel):
    print arquivo
    if path.exists(arquivo) == False:
        selecao = colocar_espacos(sel)
        print call + selecao 
>>>>>>> Stashed changes
        system(call + selecao)
    try:
        csv = open(arquivo)
    except:
        csv = []
    disponiveis = []
    for line in csv:
        disponiveis.append(line)
    return disponiveis


# 1
perfil_path = "./spark/perfil/"
bweb_path = "./spark/bweb/"

bweb_path, ano_selecionado    = usuario_seleciona_de_pasta(bweb_path, "ano")
bweb_path, estado_selecionado = usuario_seleciona_de_pasta(bweb_path, "estado")
bweb_path, turno_selecionado  = usuario_seleciona_de_pasta(bweb_path, "turno")

selecoes = [ano_selecionado, estado_selecionado, turno_selecionado]
<<<<<<< Updated upstream
=======
selecoes_submit = [ano_selecionado, estado_selecionado, turno_selecionado]
>>>>>>> Stashed changes

# 2
arquivo = gerar_path("cargosDisponiveis", selecoes) + "part-00000"

<<<<<<< Updated upstream
cargosDisponiveis = gerar_variavel(arquivo, "spark-submit modulo1/cargosdisponiveis.jar")
print arquivo
print cargosDisponiveis
=======
cargosDisponiveis = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo1/cargosdisponiveis.jar", selecoes)
>>>>>>> Stashed changes


# 3a
cargo_selecionado = usuario_seleciona_de_variavel(cargosDisponiveis, "cargo")
selecoes.append(cargo_selecionado)
<<<<<<< Updated upstream
print cargo_selecionado

arquivo = gerar_path("candidatosDisponiveis", selecoes) + "part-00000"
print arquivo
candidatosDisponiveis = gerar_variavel(arquivo, "spark-submit modulo2a/candidatosdisponiveis.jar")
=======
selecoes_submit.append("\"" + cargo_selecionado + "\"")

# 3b
arquivo = gerar_path("porcentagemCandidatos", selecoes) + "part-00000"
gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo2b/porcentagemcandidatos.jar", selecoes_submit)

arquivo = gerar_path("candidatosDisponiveis", selecoes) + "part-00000"
candidatosDisponiveis = gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo2a/candidatosdisponiveis.jar", selecoes_submit)
>>>>>>> Stashed changes


candidato_selecionado = usuario_seleciona_de_variavel(candidatosDisponiveis, "candidato")
selecoes.append(candidato_selecionado)
<<<<<<< Updated upstream

# 3b

arquivo = gerar_path("porcentagemCandidatos", selecoes) + "part-00000"
print arquivo
gerar_variavel(arquivo, "spark-submit modulo2b/porcentagemcandidatos.jar")

# 4

=======
selecoes_submit.append("\"" + candidato_selecionado + "\"")



# 4
>>>>>>> Stashed changes
indicadores = { "Estado civil":  8,
                "Faixa etaria": 10, 
                "Escolaridade": 12,
                       "Sexo" : 14}

valores = {  8 : {"SOLTEIRO":1 ,"CASADO":3,"VIUVO":5,"SEPARADO JUDICIALMENTE":7,"DIVORCIADO":9},
            10 : {"INVALIDA":-3, "16 ANOS":1, "17 ANOS":2, "18 A 20 ANOS":3, "21 A 24 ANOS":4, "25 A 34 ANOS":5, "35 A 44 ANOS":6, "45 A 59 ANOS":7, "60 A 69 ANOS":8, "70 A 79 ANOS":9, "SUPERIOR A 79 ANOS":10},
            12 : {"NAO INFORMADO":0, "ANALFABETO":1, "LE E ESCREVE":2, "ENSINO FUNDAMENTAL INCOMPLETO":3, "ENSINO FUNDAMENTAL COMPLETO":4, "ENSINO MEDIO INCOMPLETO":5, "SUPERIOR INCOMPLETO":7, "SUPERIOR COMPLETO":8},
            14 : {"NAO INFORMADO":0, "MASCULINO":2 , "FEMININO":4}}

print "Por favor escolha o indicador "
indicadores_keys = indicadores.keys()
for i in range(len(indicadores_keys)):
    print i, 
    print '- ' + indicadores_keys[i]
indicador_selecionado = indicadores[indicadores_keys[input("Selecione um numero ")]]
selecoes.append(str(indicador_selecionado))
<<<<<<< Updated upstream
=======
selecoes_submit.append(str(indicador_selecionado))
>>>>>>> Stashed changes

print "Por favor escolha o valor " 
valores_keys = valores[indicador_selecionado].keys()
for i in range(len(valores_keys)):
    print i, 
    print '- ' + valores_keys[i]
valor_selecionado = valores[indicador_selecionado][valores_keys[input("Selecione um numero ")]]
selecoes.append(str(valor_selecionado))
<<<<<<< Updated upstream

print "SELECOES FORA DO MOD 3 ", selecoes
arquivo = gerar_path("analiseIndicador", selecoes) + "part-00000"
gerar_variavel(arquivo, "spark-submit modulo3/analiseindicador.jar")
system("python web/graficos.py " + arquivo)

# Apresentacao 2
selecoes = [ano_selecionado, estado_selecionado, turno_selecionado, cargo_selecionado]
arquivo = gerar_path("dadosInconsistentes", selecoes)
print arquivo
gerar_variavel(arquivo, "spark-submit modulo5/dadosinconsistentes.jar")

# Apresentacao 3
selecoes.append(candidato_selecionado)
arquivo = gerar_path("analiseGeral", selecoes)
gerar_variavel(arquivo, "spark-submit modulo4/analisegeral.jar")
=======
selecoes_submit.append(str(valor_selecionado))

arquivo = gerar_path("analiseIndicador", selecoes) + "part-00000"
gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo3/analiseindicador.jar", selecoes_submit)
system("python web/graficos.py " + "\"" + arquivo + "\"")

# Apresentacao 2

selecoes = [ano_selecionado, estado_selecionado, turno_selecionado]
selecoes_submit = selecoes_submit[:-3]
arquivo = gerar_path("dadosInconsistentes", selecoes)

if path.exists(arquivo) == False:
    selecao = colocar_espacos(selecoes_submit)
    call = "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo5/dadosinconsistentes.jar"
    system(call + selecao)
# try:
#     csv = open(arquivo)
# except:
#     csv = []
# disponiveis = []
# for line in csv:
#     disponiveis.append(line)

# Apresentacao 3
selecoes.append(cargo_selecionado)
selecoes.append(candidato_selecionado)
selecoes_submit.append("\"" + candidato_selecionado + "\"")
arquivo = gerar_path("analiseGeral", selecoes)
gerar_variavel(arquivo, "/Users/Damasceno/Desktop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit  modulo4/analisegeral.jar", selecoes_submit)
>>>>>>> Stashed changes
