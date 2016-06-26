from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/AnaliseTSE/login')
def login():
    return '<html><head></head><body><h1>Testando as rotas</h1><h2>Essa &eacute; a an&aacute;lise do TSE</h2></body></html>'

@app.route('/nathaliaeyago')
def eu_te_amo():
    return 'Amor, eu te amo muito!!!!'

if __name__ == '__main__':
    app.run()
