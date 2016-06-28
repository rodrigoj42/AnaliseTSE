from flask import *

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/item1')
def item1():
    return render_template('item.html')

@app.route('/item2')
def item2():
    return render_template('item.html')

@app.route('/item3')
def item3():
    return render_template('item.html')
if __name__ == '__main__':
    app.run('0.0.0.0')
