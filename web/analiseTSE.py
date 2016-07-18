#-*- coding: utf-8 -*-
from flask import *
from generateMap import *
import subprocess
from os import system

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()

ls = system_call('ls ../dados').split('\n')

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
    genMap()
    estados = ['RJ','SP','MG']
    dropdown=[generateDropdownList(ls),generateDropdownList(estados)]

    return render_template('index.html',dropdown=dropdown)

@app.route('/showResults')
def showResults():
    #l_args = args.split('&')
    return render_template('item.html')

@app.route('/item2')
def item2():
    return render_template('item.html')

@app.route('/item3')
def item3():
    return render_template('item.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port='5000')
