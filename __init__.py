from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
import plotly
#plotly.tools.set_credentials_file(username='ganeshcodes', api_key='9QIJefjnbz6Y0arQD7ww')
#import plotly.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go
#py.sign_in('ganeshcodes', '9QIJefjnbz6Y0arQD7ww')

#kmeans imports
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

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
    q = "select StateName, TotalPop, Voted from StateVotingClean limit 10"
    # execute and get results
    cursor = mysql.connect().cursor()
    cursor.execute(q)
    results = cursor.fetchall()
    # prepare the data to plot
    states = []
    totalpop = []
    voted = []
    for i in range(len(results)):
        states.append(results[i][0])
        totalpop.append(int(results[i][1]))
        voted.append(int(results[i][2]))

    print(states,totalpop,voted)

    # plot line chart
    trace0 = go.Scatter(
        x = states,
        y = totalpop,
        name = 'Total population',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
    )
    trace1 = go.Scatter(
        x = states,
        y = voted,
        name = 'Voted',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4)
    )
    data = [trace0,trace1]
    output = plot(data,output_type='div',show_link=False, image_height=600, image_width=600)
    return output

@app.route('/countrybarchart')
def countrybarchart():
    # construct query
    q = "select StateName, TotalPop, Voted from StateVotingClean limit 10"
    # execute and get results
    cursor = mysql.connect().cursor()
    cursor.execute(q)
    results = cursor.fetchall()
    # prepare the data to plot
    states = []
    totalpop = []
    voted = []
    for i in range(len(results)):
        states.append(results[i][0])
        totalpop.append(int(results[i][1]))
        voted.append(int(results[i][2]))

    print("printing states")
    print(states)

    # plot bar chart
    trace0 = go.Bar(
        x = states,
        y = totalpop,
        name = 'Total population',
    )
    trace1 = go.Bar(
        x = states,
        y = voted,
        name = 'Voted',
    )
    data = [trace0,trace1]
    output = plot(data,output_type='div',show_link=False, image_height=600, image_width=600)
    return output

@app.route('/kmeansdemo')
def kmeansdemo():
    df = pd.read_csv('csv/Students.csv',sep=';')
    #Make a copy of DF
    df_tr = df

    #Transsform the timeOfDay to dummies
    df_tr = pd.get_dummies(df_tr, columns=['timeOfDay'])

    #Standardize
    clmns = ["GivenName","Surname","StreetAddress","City","State","StateFull","ZipCode","EmailAddress","Username","Password","TelephoneNumber","MothersMaiden","Birthday","Age","CCNumber","CVV2","NationalID","BloodType","Kilograms","Centimeters","Latitude","Longitude"]
    df_tr_std = stats.zscore(df_tr[clmns])

    #Cluster the data
    kmeans = KMeans(n_clusters=2, random_state=0).fit(df_tr_std)
    labels = kmeans.labels_

    #Glue back to originaal data
    df_tr['clusters'] = labels

    #Add the column into our list
    clmns.extend(['clusters'])

    #Lets analyze the clusters
    print(df_tr[clmns].groupby(['clusters']).mean())

    snsplot = sns.lmplot('Kilograms', 'Centimeters', 
           data=df_tr, 
           fit_reg=False, 
           hue="clusters",  
           scatter_kws={"marker": "D", 
                        "s": 100})
    '''plt.title('Clusters Wattage vs Duration')
    plt.xlabel('Wattage')
    plt.ylabel('Duration')'''

    snsplot.savefig("output.png")
    return "kmeans plot generated!"



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