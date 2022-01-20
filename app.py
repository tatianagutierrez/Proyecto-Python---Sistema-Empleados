from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app= Flask(__name__)

mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='' 
app.config['MYSQL_DATABASE_DB']='sistema' # DB: data base
mysql.init_app(app)

@app.route('/')
def index():

    # conectar a la base de datos
    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    
    empleados = cursor.fetchall() # trae todos los datos
    print(empleados)

    conn.commit()

    return render_template('empleados/index.html', empleados = empleados)

@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()

    # regresa a la pagina anterior
    return redirect('/')

@app.route('/edit/<int:id>')
def edit():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados = cursor.fetchall() # trae todos los datos
    conn.commit()

    return render_template('empleados/edit.html', empleados=empleados)

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