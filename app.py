from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session, flash
from flask_login import current_user
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import os

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text

def create_app():
    app = Flask(__name__, template_folder='template')

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
    #postgres://minicore_4f6e_user:LZTi4jnMA3mGMtW4Ns8e1U1fLbwJeYu4@dpg-coga6vo21fec73d64sp0-a.oregon-postgres.render.com/minicore_4f6e
    db = SQLAlchemy(app)

    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/comisiones', methods=['POST'])
    def mostrar_comisiones():
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

        connection_str = text("""
        SELECT usuarios.nombre, usuarios.apellido, SUM(ventas.monto) AS total_ventas FROM ventas JOIN usuarios ON 
            ventas.idusuario = usuarios.idusuarios 
        WHERE 
            ventas.fecha BETWEEN :start AND :end
        GROUP BY 
            usuarios.nombre, 
            usuarios.apellido;
        """)

        try:
            result = db.session.execute(connection_str, {"start": fecha_inicio, "end": fecha_fin})
            comision = result.fetchall()
        except Exception as e:
            print(e)
            comision = []

        return render_template('comision.html', comision=comision)



    @app.route('/buscar_comisiones', methods=['GET'])
    def mostrar_formulario_busqueda():
        return render_template('formulario_busqueda.html')

    
    app.secret_key = "pinchellave"  
    return app


if __name__ == '__main__':
        create_app().run(debug=True, host='0.0.0.0', port=5003, threaded=True)
        #app.run(debug=True, host='0.0.0.0', port=5003, threaded=True)

