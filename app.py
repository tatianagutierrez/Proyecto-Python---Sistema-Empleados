from flask import Flask
from flask import render_template, request
from flaskext.mysql import MySQL
from datetime import datetime

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

    # conectar a la base de datos
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Tatiana', 'tatiana@gmail.com', 'foto.jpg');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return render_template('empleados/index.html')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():

    nombre = request.form['txtNombre']
    correo = request.form['txtCorreo']
    foto = request.files['txtFoto']

    # Esta funcion me retorna el tiempo actualmente
    now = datetime.now()
    # Lo convierto al formato Anio, hora, mes, segundo
    tiempo = now.strftime('%Y%H%M%S')

    if foto.filename != '':
        # Agregarle el tiempo evita que las fotos no tengan el mismo nombre y se sobreescriban
        nuevoNombreFoto = tiempo + foto.filename
        foto.save("uploads/" + nuevoNombreFoto)

    # el %s va a ser remplazado por los datos que sean ingresados en orden
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"

    datos = (nombre, correo, foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('empleados/index.html')



if __name__== '__main__':
    app.run(debug=True)