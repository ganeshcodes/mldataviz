from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ganesh'
app.config['MYSQL_DATABASE_DB'] = 'clouddb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/hello/<user>')
def hello_name(user):
    return render_template('hello.html', name = user)

@app.route('/satavgpieform')
def satavgpieform():
    return render_template('satavgpieform.html')

@app.route('/satavgpiechart', methods=['POST'])
def satavgpiechart():
    s =  request.form['start'];
    e = request.form['end'];
    q = "select avg(sat_avg) as average,state from Education where unitid between "+s+" and "+e+" group by state limit 10";
    cursor = mysql.connect().cursor()
    cursor.execute(q);
    results = cursor.fetchall();
    print(results);
    return json.dumps({'status':'OK','data':results});

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)