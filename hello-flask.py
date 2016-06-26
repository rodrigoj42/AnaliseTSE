from flask import *
app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
def show_the_login_form():
    return send_from_directory('index.html')
def do_the_login():
    return 'Login realizado'


if __name__ == '__main__':
    app.run('0.0.0.0')
