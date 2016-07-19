#-*- coding: utf-8 -*-
from flask import *
from generateMap import *
import subprocess
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
def home(dropdown=None):

    dropdown=[generateDropdownList(['2014','2012','2010','2008','2006','2004','2002']),
              generateDropdownList(['AC','AL','AM','AP','BA','BR','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO','ZZ']),
              generateDropdownList(['1','2']),
              generateDropdownList(['PRESIDENTE','VEREADOR','DEPUTADO ESTADUAL','DEPUTADO FEDERAL','GOVERNADOR','PREFEITO','SENADOR'])]

    return render_template('index.html',dropdown=dropdown)

#@app.route('/_add_numbers')
#def add_numbers():
#    a = request.args.get('txt', 0, type=string)
#    return jsonify(result=a)

@app.route('/results',methods=['POST'])
def results():
    selecoes = [request.form['ano'], request.form['estado'], request.form['turno']]
    arquivo = gerar_path("cargosDisponiveis", selecoes) + "part-00000"
    print arquivo
    print path.exists(arquivo)
    if path.exists(arquivo) == False:
        selecao = colocar_espacos(selecoes)
        system("spark-submit ../modulo1/cargosdisponiveis.jar " + selecao)
    return redirect('home#indicator')

@app.route('/item2')
def item2():
    return render_template('item.html')

@app.route('/item3')
def item3():
    return render_template('item.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port='5000')
