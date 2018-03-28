from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/hello/<user>')
def hello_name(user):
   return render_template('hello.html', name = user)
   
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)