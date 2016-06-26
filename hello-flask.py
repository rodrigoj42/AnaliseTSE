from flask import *
app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('home'))
@app.route('/home')
def home():
    return render_template('index.html')
    #return 'Main page'
if __name__ == '__main__':
    app.run('0.0.0.0')
