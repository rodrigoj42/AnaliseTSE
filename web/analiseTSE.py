#-*- coding: utf-8 -*-
from flask import *
from generateMap import *
import subprocess
from os import system, listdir, path

g_path = ""

def ignorar_lixo_em(l):
    for i in l: 
        if i[0] == ".": l.remove(i)
    return l

def colocar_espacos(l):
    s = " "
    for i in l: s += i + " "
    return s

def gerar_path(s,l):
  dados_path = "../spark/dados/" + s
  for i in l:
    dados_path += "_" + i
  return dados_path + "/" 

def usuario_seleciona_de_variavel(disponiveis ,s):
    print "\nPor favor escolha um %s:" % s
    for i in range(len(disponiveis)):
        if "." in disponiveis[i]:
            disponiveis[i] = disponiveis[i][:disponiveis[i].index(".")]
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

def gerar_variavel(selecoes, arquivo, call):
    print "ENTROU!!!!!!!!!!!!!!!!!!",arquivo
    if path.exists(arquivo) == False:
        selecao = colocar_espacos(selecoes)
        print "SELECAO",selecao
        system(call + selecao)
    try:
        csv = open(arquivo)
    except:
        csv = []
    disponiveis = []
    for line in csv:
        disponiveis.append(line)
    return disponiveis

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()

ls = system_call('ls ../spark/dados').split('\n')

ls[:] = ls[:len(ls)-1]

def generateDropdownList(l):
	s_return = ""
	for i in l:
		s_return += '<option value="'+i+'">'+i+'</option>\n'
	return s_return


app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
def home(imagem=None):

    imagem='<img src="/static/assets/img/part-00000.png">'

    return render_template('index.html',imagem=imagem)

@app.route('/results',methods=['POST'])
def results():
    selecoes = [request.form['ano'], request.form['estado'], request.form['turno']]
    arquivo = gerar_path("cargosDisponiveis", selecoes) + "part-00000"
    cargosDisponiveis = gerar_variavel(selecoes, arquivo, "spark-submit ../modulo1/cargosdisponiveis.jar")
    selecoes.append(request.form['cargo'])
    arquivo = gerar_path("candidatosDisponiveis", selecoes) + "part-00000"
    candidatosDisponiveis = gerar_variavel(selecoes, arquivo, "spark-submit ../modulo2a/candidatosdisponiveis.jar")
    selecoes.append(request.form['candidato'])
    arquivo = gerar_path("porcentagemCandidatos", selecoes) + "part-00000"
    gerar_variavel(selecoes, arquivo, "spark-submit ../modulo2b/porcentagemcandidatos.jar")
    selecoes.append(request.form['criterio'])
    selecoes.append(request.form['filtro'])
    arquivo = gerar_path("analiseIndicador", selecoes) + "part-00000"
    gerar_variavel(selecoes, arquivo, "spark-submit ../modulo3/analiseindicador.jar")
    system("python graficos.py " + arquivo)
    system("cp "+arquivo+".png static/assets/img/part-00000.png")
    return redirect('home#indicator')

@app.route('/item2')
def item2():
    return render_template('item.html')

@app.route('/item3')
def item3():
    return render_template('item.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port='5000')
