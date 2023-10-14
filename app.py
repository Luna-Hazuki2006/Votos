from flask import Flask, render_template, request, flash
from os import urandom
from datetime import datetime
from flask_login import LoginManager
from itsdangerous import TimestampSigner, URLSafeTimedSerializer, base64_decode
from werkzeug.security import generate_password_hash
from db import candidatos, votantes
from validaciones import agregar_votante, agregar_candidato, verificar_usuario
from pprint import pprint
from localStoragePy import localStoragePy
import json
import ast
# korean queen tokyo walmart 2 DRIP > TOKYO , rope SKYPE _ 4 & korean XBOX
app = Flask(__name__, template_folder='templates')
# app.config['SECRET_KEY'] = 'kqtw2D>T,rS_4&kX'
app.config['SECRET_KEY'] = urandom(16).hex()
BaseToken = URLSafeTimedSerializer(app.config['SECRET_KEY'])
localStorage = localStoragePy('votaciones', 'json')

def generar_token(usuario):
    actual = datetime.utcnow()
    if (actual.minute + 6) > 59: 
        minuto = (actual.minute + 6) - 59
        hora = actual.hour + 1
        tiempo = datetime(actual.year, actual.month, actual.day, hora, minuto)
        print(tiempo)
        localStorage.setItem('token', json.dumps({'cedula': f'{usuario}', 'vencimiento': tiempo.strftime('%d/%m/%Y, %H:%M:%S')}))
    else: 
        tiempo = datetime(actual.year, actual.month, actual.day, actual.hour, (actual.minute + 6))
        print(tiempo)
        localStorage.setItem('token', json.dumps({'cedula': f'{usuario}', 'vencimiento': tiempo.strftime('%d/%m/%Y, %H:%M:%S')}))
    print(localStorage.getItem('token'))

def verificar():
    try: 
        token = localStorage.getItem("token")
        if token is None: 
            return
        print('vencimiento: ')
        token = f'{token}'
        print(type(token))
        print(token)
        token = eval(token)
        print(token)
        print(token['vencimiento'])
        print(datetime.strptime(token['vencimiento'], '%d/%m/%Y, %H:%M:%S'))
        print(token["cedula"])
        if datetime.strptime(token['vencimiento'], '%d/%m/%Y, %H:%M:%S') > datetime.utcnow(): 
            localStorage.removeItem('token')
            print('LO LOGRASTEEEEEEEEEEEEEE')
            print(token)
        else: 
            print('aaaaaaaaaaaaaaaaaaaa')
            print('holaaaaaaaaaaaaa')
    except Exception as e:
        print(e) 
        flash('No has iniciado sesión, asique solo eres un observador')

@app.route('/')
def iniciar():
    verificar()
    token = localStorage.getItem('token')
    return render_template('/principio/index.html', 
                           token=token)

@app.route('/candidatos', methods=['GET'])
def listar_candidatos(): 
    verificar()
    token = localStorage.getItem('token')
    lista = candidatos.find({'estatus': 'A'})
    return render_template('/candidatos/index.html', lista=lista, 
                           token=token)

@app.route('/registro', methods=['GET', 'POST'])
def registrar_usuario(): 
    verificar()
    token = localStorage.getItem('token')
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
    return render_template('/registro/index.html', 
                           token=token)

@app.route('/inicio', methods=['GET', 'POST'])
def iniciar_sesion():
    verificar()
    token = localStorage.getItem('token')
    if request.method == 'POST': 
        forma = request.form
        cedula = forma['cedula']
        clave = forma['contraseña']
        if verificar_usuario(cedula, clave): 
            print('*******************')
            generar_token(cedula)
            return render_template('/principio/index.html', token=token)
        else: flash('Parece que te equivocaste de contraseña')
    return render_template('/inicio/index.html', 
                           token=token)

@app.route('/resultados', methods=['GET'])
def mostrar_resultados(): 
    verificar()
    token = localStorage.getItem('token')
    return render_template('/resultados/index.html', 
                           token=token)

@app.route('/votantes', methods=['GET'])
def listar_votantes(): 
    verificar()
    token = localStorage.getItem('token')
    lista = votantes.find({'estatus': 'A'})
    return render_template('/votantes/index.html', lista=lista, 
                           token=token)

@app.route('/votacion', methods=['POST, GET'])
def votar(): 
    verificar()
    token = localStorage.getItem('token')
    if token is None: 
        flash('disculpe, tiene iniciar sesión para votar')
        return render_template('/inicio/index.html', 
                               token)
    if request.method == 'POST': 
        forma = request.form
        candidato = forma['candidato']
        token = eval(token)
        usuario = token['cedula']
    return render_template('/votaciones/index.html', 
                           token=token)

@app.route('/cerrado')
def cerrar(): 
    if localStorage.getItem('token') is not None: 
        localStorage.removeItem('token')
    token = localStorage.getItem('token')
    return render_template('/principio/index.html', 
                           token=token)

if __name__ == '__main__':
    app.run(debug=True)
