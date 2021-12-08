#Importamos el modulo flask para empezar a trabajar con el
import re
from flask import Flask,render_template,request, redirect, url_for
#debemos instalarlo con pip install flask_mysqldb antes de poder importarlos
from  flask_mysqldb import MySQL#importamos el modulo para trabajar con la base de datos 



app=Flask(__name__)
#HAcemos la configuracion del modulo para trabajar con la base de datos
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']= 'flaskcontacts'
#----------------------------------------------------------------------------------
mysql=MySQL(app)#pasamos la configuracion al servidor

#definismos las rutas dentro de nuestra aplicacion
@app.route("/")
def Index():
    Registros=list_contact()#asi obtenemos todos los registros desde la base de datos
    return render_template('index.html', datos=Registros)#asi pasamos los datos de la base de datos al html 

def list_contact():
    #Trabajamos con esta ruta para listar los datos del servidor y mostrarlos en el html
    cur=mysql.connection.cursor()#obtenemos de nuevo la conexion a la base de datos
    cur.execute(
        'SELECT * FROM contacts'
    )
    return cur.fetchall()#asi obtenemos todos los registros desde la base de datos
    

@app.route('/add_contact', methods=['POST'])#solicitud del metodo es en singular
def add_contact():
    if request.method=='POST':
        #Captamos los valores desde el html
        fullname=request.form['txt_fullname']
        phone=request.form['txt_phone']
        email=request.form['txt_email']
        #
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s, %s, %s)',(fullname,phone,email)) #pasamos la consulta al servidor
        mysql.connection.commit()
        
        return redirect(url_for("Index"))#lo redireccionamos a la vista principal

@app.route('/get_contact/<string>:id')
def get_contact(id):
    cur=mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM contacts WHERE Id='+id
    )
    Contacto=cur.fetchone()
    return render_template('Edite.html',Dato=Contacto)

@app.route('/delete_contact/<string:id>')#se debe de indicar en la ruta que estamos recibiendo desde el html un parametros
def delete_contact(id):

    cur=mysql.connection.cursor()
    cur.execute(
        'DELETE FROM contacts WHERE Id ='+id
    )
    #ejecutatmos la consulta
    mysql.connection.commit()
    return redirect(url_for('Index'))#lo que se redirecciona aqui no es el template sino la ruta 

#Validamos que se ejecute de primero este archivo
if __name__=='__main__':
    app.run(port=3000,debug=True)#inicamos un servidor

