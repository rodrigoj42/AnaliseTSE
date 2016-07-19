from os import system, listdir, path

def ignorar_lixo_em(l):
    for i in l: 
        if i[0] == ".": l.remove(i)
    return l

def colocar_espacos(l):
    s = ""
    for i in l:
        s += i + " "
    return s

def gerar_path(s,l):
  dados_path = "../spark/dados/" + s
  for i in l:
    dados_path += "_" + i
  return dados_path + "/" 

def usuario_seleciona(path, s):
    disponiveis = ignorar_lixo_em(listdir(path))
    print path
    print "\nPor favor selecione um %s:" % s
    for i in range(len(disponiveis)):
        if "." in disponiveis[i]:
            disponiveis[i] = disponiveis[i][:disponiveis[i].index(".")]
        print i + 1,
        print "- " + disponiveis[i]
    selecionado = disponiveis[input("Selecione um numero: ")-1]
    path += selecionado + "/"
    print path
    return (path, selecionado)

# 1
perfil_path = "../spark/perfil/"
bweb_path = "../spark/bweb/"

bweb_path, ano_selecionado    = usuario_seleciona(bweb_path, "ano")
bweb_path, estado_selecionado = usuario_seleciona(bweb_path, "estado")
bweb_path, turno_selecionado  = usuario_seleciona(bweb_path, "turno")

selecoes = [ano_selecionado, estado_selecionado, turno_selecionado]

# 2
arquivo = gerar_path("cargosDisponiveis", selecoes) + "part-00000"

if path.exists(arquivo) == False:
    selecao = colocar_espacos(selecoes)
    system("spark-submit ../modulo1/cargosdisponiveis.jar " + selecao)

csv = open(arquivo)
cargosDisponiveis = [] 
for line in csv: 
    cargosDisponiveis += line


