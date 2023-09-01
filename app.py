from flask import Flask, render_template, request, flash
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from db import candidatos, votantes
from validaciones import agregar_votante, agregar_candidato, verificar_usuario
from pprint import pprint
# korean queen tokyo walmart 2 DRIP > TOKYO , rope SKYPE _ 4 & korean XBOX
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'kqtw2D>T,rS_4&kX'

@app.route('/')
def iniciar():
    with open('datos_importantes', 'w+') as datos:
        datos.write('Votantes:\n')
        for esto in votantes.find({'estatus': 'A'}): 
            datos.write(esto['cedula'])
            datos.write('\n')
            datos.write(generate_password_hash(esto['clave']))
            datos.write('\n')
        datos.write('Candidatos:\n')
        for esto in candidatos.find({'estatus': 'A'}): 
            datos.write(esto['cedula'])
            datos.write('\n')
            datos.write(generate_password_hash(esto['clave']))
            datos.write('\n')
    return render_template('/principio/index.html')

@app.route('/candidatos', methods=['GET'])
def listar_candidatos(): 
    lista = candidatos.find({'estatus': 'A'})
    return render_template('/candidatos/index.html', lista=lista)

@app.route('/registro', methods=['GET', 'POST'])
def registrar_usuario(): 
    if request.method == 'POST':
        forma = request.form
        if forma['contraseña'] == forma['repetida']: 
            nuevo_usuario = {
                'cedula': forma['cedula'], 
                'nombre': forma['nombre'], 
                'apellido': forma['apellido'], 
                'clave': generate_password_hash(forma['contraseña']), 
                'correo': forma['correo'], 
                'estatus': 'A'
            }
            if forma['tipo'] == 'votante': 
                if agregar_votante(nuevo_usuario): 
                    id = votantes.insert_one(nuevo_usuario).inserted_id
                    if id: 
                        flash('Se ha registrado como votante éxitosamente')
                    else: 
                        flash('Ha sucedido un error al registrarse')
                else: 
                    flash('La cédula que ha registrado ya existe')
            elif forma['tipo'] == 'candidato': 
                if agregar_candidato(nuevo_usuario): 
                    id = candidatos.insert_one(nuevo_usuario).inserted_id
                    if id: 
                        flash('Se ha registrado como candidato éxitosamente')
                    else: 
                        flash('Ha sucedido un error al registrarse')
                else: 
                    flash('La cédula que ha registrado ya existe')
            pprint(nuevo_usuario)
            pprint(forma['tipo'])
        else: 
            flash('Las contraseñas no son iguales')
    return render_template('/registro/index.html')

@app.route('/inicio', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST': 
        forma = request.form
        
    return render_template('/inicio/index.html')

@app.route('/resultados', methods=['GET'])
def mostrar_resultados(): 
    return render_template('/resultados/index.html')

@app.route('/votantes', methods=['GET'])
def listar_votantes(): 
    lista = votantes.find({'estatus': 'A'})
    return render_template('/votantes/index.html', lista=lista)

if __name__ == '__main__':
    app.run(debug=True)