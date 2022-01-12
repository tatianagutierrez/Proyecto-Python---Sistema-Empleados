from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL

app= Flask(__name__)

mysql= MySQL()

# para que se conecte a sql usamos el host 'localhost'
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
    # DB: data base
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('empleados/index.html')

if __name__== '__main__':
    app.run(debug=True)

