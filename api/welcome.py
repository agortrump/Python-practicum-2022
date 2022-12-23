from flask import Flask, render_template

app = Flask(__name__, template_folder='template')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/welcome')
def welcome():
    return 'Welcome'


@app.route('/welcome/home')
def welcome_home():
    return 'Welcome Home'


@app.route('/welcome/back')
def welcome_back():
    return 'Welcome Back'


if __name__ == '__main__':
    app.run(debug=True)
