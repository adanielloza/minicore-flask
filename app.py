from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session, flash
from flask_login import current_user
from flask_mysqldb import MySQL, MySQLdb  # pip install Flask-MySQLdb
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__, template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'udla1'
app.config['MYSQL_DB'] = 'minicore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/comisiones', methods=['POST'])
def mostrar_comisiones():
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT usuarios.nombre, usuarios.apellido, SUM(ventas.monto) AS total_ventas FROM ventas JOIN usuarios ON ventas.idusuario = usuarios.idusuarios WHERE ventas.fecha BETWEEN %s AND %s GROUP BY usuarios.nombre, usuarios.apellido", (fecha_inicio, fecha_fin))
    comision = cur.fetchall()
    cur.close()

    return render_template('comision.html', comision=comision)

@app.route('/buscar_comisiones', methods=['GET'])
def mostrar_formulario_busqueda():
    return render_template('formulario_busqueda.html')

if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
