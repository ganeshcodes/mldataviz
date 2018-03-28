from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
import plotly
#plotly.tools.set_credentials_file(username='ganeshcodes', api_key='9QIJefjnbz6Y0arQD7ww')
#import plotly.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go
#py.sign_in('ganeshcodes', '9QIJefjnbz6Y0arQD7ww')

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
    # Get inputs from form
    s =  request.form['start']
    e = request.form['end']
    # construct query
    q = "select avg(sat_avg) as average,state from Education where unitid between "+s+" and "+e+" group by state limit 10"
    # execute and get results
    cursor = mysql.connect().cursor()
    cursor.execute(q)
    results = cursor.fetchall()
    # prepare the data to plot
    labels = []
    values = []
    for i in range(len(results)):
        if results[i][0]:
            labels.append(results[i][1])
            values.append(int(results[i][0]))
    # plot pie chart
    trace = go.Pie(labels=labels, values=values)
    data = [trace]
    output = plot(data,output_type='div',show_link=False, image_height=600, image_width=600)
    return output
    #return json.dumps({'status':'OK','data':resp})

@app.route('/countrylinechart')
def countrylinechart():
    # construct query
    q = "select count(*) as count,CountryCode from Starbucks group by CountryCode limit 10"
    # execute and get results
    cursor = mysql.connect().cursor()
    cursor.execute(q)
    results = cursor.fetchall()
    # prepare the data to plot
    countrycode = []
    count = []
    for i in range(len(results)):
        countrycode.append(results[i][1])
        values.append(int(results[i][0]))

    # plot line chart
    trace0 = go.Scatter(
        x = countrycode,
        y = count,
        name = 'Number of stores',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
    )
    data = [trace0]
    output = plot(data,output_type='div',show_link=False, image_height=600, image_width=600)
    return output

@app.route('/piechartdemo')
def piechartdemo():
    labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
    values = [4500,2500,1053,500]

    #output = plot([go.Scatter(x=[1, 2, 3], y=[3, 2, 6])], output_type='div')

    trace = go.Pie(labels=labels, values=values)
    data = [trace]
    output = plot(data,output_type='div',show_link=False, image_height=600, image_width=600)
    return output

    #layout = go.Layout(title='Pie chart demo', width=800, height=640)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)