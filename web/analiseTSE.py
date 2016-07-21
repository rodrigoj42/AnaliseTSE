#-*- coding: utf-8 -*-
from flask import *
from generateMap import *
import subprocess
from os import system, listdir, path

seleci = []

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
        if ".txt" in disponiveis[i]:
            disponiveis[i] = disponiveis[i][:disponiveis[i].index(".txt")]
            #if disponiveis[i][-1] == '\n': disponiveis[i] = disponiveis[i][:-1]
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
    print arquivo
    print path.exists(arquivo)
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

def generateDropdownList(l):
	s_return = ""
	for i in l:
		s_return += '<option value="'+i+'">'+i+'</option>\n'
	return s_return

def generateURL(s,selec):
    for i in selec:
        s+=i+"_"
    s+="part-00000.png"
    return s

app = Flask(__name__)

@app.route('/')
def root():
    #system('rm static/assets/img/part-00000.png')
    return redirect(url_for('home'))

@app.route('/home')
def home(imagem=None):
    #global dados_gerados
    global seleci
    #if path.exists(generateURL("static/assets/img/",seleci)):
    imagem='<img src="'+generateURL("static/assets/img/",seleci)+'">'
    # s='<h4>Seleções: '
    # for i in seleci:
    #     s+=i+" "
    # label=s+'</h4>'

    return render_template('index.html',imagem=imagem)

@app.route('/results',methods=['POST'])
def results():
    global seleci
    selecoes = [request.form['ano'], request.form['estado'], request.form['turno'], request.form['cargo'].rstrip()]
    print "ENTROU=====================",selecoes
    selecoes_submit = [request.form['ano'], request.form['estado'], request.form['turno'], '"'+request.form['cargo'].rstrip()+'"']
    
    arquivo = gerar_path("porcentagemCandidatos", selecoes) + "part-00000"
    gerar_variavel(arquivo, "spark-submit ../modulo2b/porcentagemcandidatos.jar",selecoes_submit)
    
    selecoes = [request.form['ano'], 
                request.form['estado'], 
                request.form['turno'], 
                request.form['cargo'].rstrip(),
                request.form['candidato'].rstrip() , 
                request.form['criterio'],
                request.form['filtro']]
    selecoes_submit = [request.form['ano'], 
                       request.form['estado'], 
                       request.form['turno'], 
                       '"'+request.form['cargo'].rstrip()+'"',
                       '"'+request.form['candidato'].rstrip()+'"',
                       request.form['criterio'],
                       request.form['filtro']]

    arquivo = gerar_path("analiseIndicador", selecoes) + "part-00000"
    gerar_variavel(arquivo, "spark-submit ../modulo3/analiseindicador.jar",selecoes_submit)
    system("python graficos.py " + "\""+arquivo+"\"")
    s=""
    for i in range(len(selecoes[3].split())):
        s+=selecoes[3].split()[i]
    selecoes[3] = s
    s=""
    for i in range(len(selecoes[4].split())):
        s+=selecoes[4].split()[i]
    selecoes[4] = s
    seleci=selecoes
    s=""
    for i in range(len(arquivo.split())):
        if i != len(arquivo.split())-1:
            s+=arquivo.split()[i]+"\ "
        else:
            s+=arquivo.split()[i]

    arq_cp = s
    system("cp "+arq_cp+".png "+generateURL("static/assets/img/",seleci))
    print "ARQUIVO:::::::::::::::::::::::::::::::",arquivo
    print generateURL("static/assets/img/",seleci)
    print "GLOBAL",seleci
    #return "<html><script type=text/javascript>window.close()</script></html>"
    return redirect('home#indicator')

@app.route('/genDrop',methods=['POST'])
def genDrop():
    return "Recebi: "+request.form['name']+" :D"

@app.route('/getAno',methods=['POST'])
def getAno():
    print "ENTROU!!!!!!! GETANO"
    disponiveis = ignorar_lixo_em(listdir('../spark/bweb/'))
    s = ""
    for i in xrange(len(disponiveis)):
        if i != len(disponiveis)-1:
            s+=str(disponiveis[i])+";"
        else:
            s+=str(disponiveis[i])
    print s
    return s

@app.route('/getEstado',methods=['POST'])
def getEstado():
    print "ENTROU!!!!!!! GETESTADO"
    disponiveis = ignorar_lixo_em(listdir('../spark/bweb/'+request.form['ano']))
    s = ""
    for i in xrange(len(disponiveis)):
        if i != len(disponiveis)-1:
            s+=str(disponiveis[i])+";"
        else:
            s+=str(disponiveis[i])
    print s
    return s

@app.route('/getTurno',methods=['POST'])
def getTurno():
    print "ENTROU!!!!!!! GETTURNO"
    disponiveis = ignorar_lixo_em(listdir('../spark/bweb/'+request.form['ano']+'/'+request.form['estado']))
    s = ""
    for i in xrange(len(disponiveis)):
        if i != len(disponiveis)-1:
            s+=str(disponiveis[i].split('.')[0])+";"
        else:
            s+=str(disponiveis[i].split('.')[0])
    print s
    return s

@app.route('/getCargo',methods=['POST'])
def getCargo():
    selecoes = [request.form['ano'], request.form['estado'], request.form['turno']]
    arquivo = gerar_path("cargosDisponiveis", selecoes) + "part-00000"
    cargosDisponiveis = gerar_variavel(arquivo, "spark-submit ../modulo1/cargosdisponiveis.jar",selecoes)
    print cargosDisponiveis
    s = ""
    for i in xrange(len(cargosDisponiveis)):
        if i != len(cargosDisponiveis)-1:
            s+=str(cargosDisponiveis[i])+";"
        else:
            s+=str(cargosDisponiveis[i])
    print s
    return s

@app.route('/getCandidato',methods=['POST'])
def getCandidato():
    selecoes = [request.form['ano'], request.form['estado'], request.form['turno'], request.form['cargo'].rstrip('\n')]
    selecoes_submit = [request.form['ano'], request.form['estado'], request.form['turno'], '"'+request.form['cargo'].rstrip('\n')+'"']
    arquivo = gerar_path("candidatosDisponiveis", selecoes) + "part-00000"
    print arquivo
    candidatosDisponiveis = gerar_variavel(arquivo, "spark-submit ../modulo2a/candidatosdisponiveis.jar", selecoes)
    print candidatosDisponiveis
    s = ""
    for i in xrange(len(candidatosDisponiveis)):
        if i != len(candidatosDisponiveis)-1:
            s+=str(candidatosDisponiveis[i])+";"
        else:
            s+=str(candidatosDisponiveis[i])
    print "+++++++++++++++S=",s
    return s

@app.route('/getFiltro',methods=['POST'])
def getFiltro():
    valores = {  8 : {"SOLTEIRO":1 ,"CASADO":3,"VIUVO":5,"SEPARADO JUDICIALMENTE":7,"DIVORCIADO":9},
                10 : {"INVALIDA":-3, "16 ANOS":1, "17 ANOS":2, "18 A 20 ANOS":3, "21 A 24 ANOS":4, "25 A 34 ANOS":5, "35 A 44 ANOS":6, "45 A 59 ANOS":7, "60 A 69 ANOS":8, "70 A 79 ANOS":9, "SUPERIOR A 79 ANOS":10},
                12 : {"NAO INFORMADO":0, "ANALFABETO":1, "LE E ESCREVE":2, "ENSINO FUNDAMENTAL INCOMPLETO":3, "ENSINO FUNDAMENTAL COMPLETO":4, "ENSINO MEDIO INCOMPLETO":5, "SUPERIOR INCOMPLETO":7, "SUPERIOR COMPLETO":8},
                14 : {"NAO INFORMADO":0, "MASCULINO":2 , "FEMININO":4}}
    valores_keys = valores[int(request.form['criterio'])].keys()
    print valores_keys
    valores_values= valores[int(request.form['criterio'])].values()
    s="<option>Selecione</option>"
    for i in range(len(valores_keys)):
        s+="<option value='"+str(valores_values[i])+"'>"+valores_keys[i]+"</option>"
    return s

@app.route('/gerarGrafico',methods=['POST'])
def gerarGrafico():
    selecoes = [request.form['ano'], request.form['estado'], request.form['turno'], request.form['cargo'].rstrip('\n')]
    selecoes_submit = [request.form['ano'], request.form['estado'], request.form['turno'], '"'+request.form['cargo'].rstrip('\n')+'"']
    arquivo = gerar_path("porcentagemCandidatos", selecoes) + "part-00000"
    gerar_variavel(arquivo, "spark-submit ../modulo2b/porcentagemcandidatos.jar",selecoes_submit)
    
    selecoes = [request.form['ano'], 
                request.form['estado'], 
                request.form['turno'], 
                request.form['cargo'].rstrip('\n'),
                request.form['candidato'].rstrip('\n') , 
                request.form['criterio'],
                request.form['filtro']]
    selecoes_submit = [request.form['ano'], 
                       request.form['estado'], 
                       request.form['turno'], 
                       '"'+request.form['cargo'].rstrip('\n')+'"',
                       '"'+request.form['candidato'].rstrip('\n')+'"',
                       request.form['criterio'],
                       request.form['filtro']]
    arquivo = gerar_path("analiseIndicador", selecoes) + "part-00000"
    gerar_variavel(arquivo, "spark-submit ../modulo3/analiseindicador.jar",selecoes_submit)
    system("python graficos.py " + "\""+arquivo+"\"")
    print "PASSOU 111111111111111111111"
    system("mkdir -p static/assets/img/"+selecoes[0]+"_"+selecoes[1]+"_"+selecoes[2]+"_"+selecoes[3]+"_"+selecoes[4]+"_"+selecoes[5]+"_"+selecoes[6]+"/")
    print "PASSOU 22222222222222222222222"
    system("cp "+arquivo+".png static/assets/img/"+selecoes[0]+"_"+selecoes[1]+"_"+selecoes[2]+"_"+selecoes[3]+"_"+selecoes[4]+"_"+selecoes[5]+"_"+selecoes[6]+"/part-00000.png")
    print "PASSOU 333333333333333333"
    s = "static/assets/img/"+selecoes[0]+"_"+selecoes[1]+"_"+selecoes[2]+"_"+selecoes[3]+"_"+selecoes[4]+"_"+selecoes[5]+"_"+selecoes[6]+"/part-00000.png"
    print "S==============================",s
    return s

if __name__ == '__main__':
    app.run('0.0.0.0', port='5000')
