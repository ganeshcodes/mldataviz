from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
import plotly
plotly.tools.set_credentials_file(username='ganeshcodes', api_key='9QIJefjnbz6Y0arQD7ww')
import plotly.plotly as py
import plotly.graph_objs as go

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
    resp = [['State', 'Average']]
    for i in range(len(results)):
        if results[i][0]:
            resp.append([results[i][1], float(results[i][0])])

    print(resp);
    return json.dumps({'status':'OK','data':resp});

@app.route('/piechartdemo')
def piechartdemo():
    labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
    values = [4500,2500,1053,500]
    trace = go.Pie(labels=labels, values=values)
    data = [trace]
    layout = go.Layout(title='Pie chart demo', width=800, height=640)
    fig = go.Figure(data=data, layout=layout)

    py.image.save_as(fig, filename='piechartdemo.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)