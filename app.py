from flask import Flask, render_template, request, flash
from os import urandom
from datetime import datetime
from itsdangerous import TimestampSigner, URLSafeTimedSerializer, base64_decode
from werkzeug.security import generate_password_hash
from db import candidatos, votantes, votos, administrador
from validaciones import agregar_votante, agregar_candidato, verificar_usuario, verificar_administrador
from pprint import pprint
from localStoragePy import localStoragePy
import json
# korean queen tokyo walmart 2 DRIP > TOKYO , rope SKYPE _ 4 & korean XBOX
app = Flask(__name__, template_folder='templates')
# app.config['SECRET_KEY'] = 'kqtw2D>T,rS_4&kX'
app.config['SECRET_KEY'] = urandom(16).hex()
BaseToken = URLSafeTimedSerializer(app.config['SECRET_KEY'])
localStorage = localStoragePy('votas', 'json')

def generar_token(usuario):
    actual = datetime.utcnow()
    adicion = 6
    if (actual.minute + adicion) > 59: 
        minuto = (actual.minute + adicion) - 59
        hora = actual.hour + 1
        tiempo = datetime(actual.year, actual.month, actual.day, hora, minuto)
        print(tiempo)
        localStorage.setItem('token', json.dumps({'cedula': f'{usuario}', 'vencimiento': tiempo.strftime('%d/%m/%Y, %H:%M:%S')}))
    else: 
        tiempo = datetime(actual.year, actual.month, actual.day, actual.hour, (actual.minute + adicion))
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
        token = eval(token)
        print(token)
        print(token['vencimiento'])
        vencimiento = datetime.strptime(token['vencimiento'], '%d/%m/%Y, %H:%M:%S')
        print(token["cedula"])
        if datetime.utcnow() > vencimiento: 
            flash(f'''
Tu sesión se venció, ya que son las {datetime.utcnow()}, 
y tu fecha de vencimiento era a las {vencimiento}
''')
            localStorage.setItem('token', None)
            print('LO LOGRASTEEEEEEEEEEEEEE')
            flash('lo lograsteeeeee')
            print(token)
        else: 
            flash(f'''
Lograste iniciar sesión sin ningún problema
Tu sesión se terminará a las {vencimiento}
''')
    except Exception as e:
        print(e) 
        flash('No has iniciado sesión, asique solo eres un observador')

@app.route('/')
def iniciar():
    verificar()
    token = localStorage.getItem('token')
    token = eval(token)
    if token is None: 
        print('nada')
    print(token)
    return render_template('/principio/index.html', 
                           token=eval(token))

@app.route('/candidatos', methods=['GET'])
def listar_candidatos(): 
    verificar()
    token = localStorage.getItem('token')
    print(token)
    lista = candidatos.find({'estatus': 'A'})
    return render_template('/candidatos/index.html', lista=lista, 
                           token=eval(token))

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
                'voto': False, 
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
                           token=eval(token))

@app.route('/registrar_candidato', methods=['GET', 'POST'])
def registrar_candidato():
    token = localStorage.getItem('token')
    return render_template('/registro/candidato/index.html', 
                           token=eval(token))

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
            token = localStorage.getItem('token')
            return render_template('/principio/index.html', token=eval(token))
        elif verificar_administrador(cedula, clave): 
            print('//////////////////////////////')
            generar_token(cedula)
            token = localStorage.getItem('token')
            return render_template('/principio/index.html', token=eval(token))
        else:
            flash('Parece que te equivocaste de contraseña')
    return render_template('/inicio/index.html', 
                           token=eval(token))

@app.route('/resultados', methods=['GET'])
def mostrar_resultados(): 
    verificar()
    token = localStorage.getItem('token')
    return render_template('/resultados/index.html', 
                           token=eval(token))

@app.route('/votantes', methods=['GET'])
def listar_votantes(): 
    verificar()
    token = localStorage.getItem('token')
    lista = votantes.find({'estatus': 'A'})
    return render_template('/votantes/index.html', lista=lista, 
                           token=eval(token))

@app.route('/votar', methods=['GET', 'POST'])
def votar(): 
    verificar()
    token = localStorage.getItem('token')
    lista = candidatos.find({'estatus': 'A'})
    print(token)
    if token == None: 
        flash('disculpe, tiene iniciar sesión para votar')
        return render_template('/inicio/index.html', 
                               token=token)
    if request.method == 'POST': 
        forma = request.form
        candidato = forma['candidato']
        momento = datetime.utcnow()
        token = eval(token)
        cedula = token['cedula']
        votante = votantes.find_one({'cedula': cedula})
        if not votante['voto']:
            voto = {
                'candidato': candidato, 
                'momento': momento
            }
            id = votos.insert_one(voto).inserted_id
            if id:
                flash('Ha votado exitósamente')
                busqueda = {'cedula': cedula, 'estatus': 'A'}
                final = {'$set': {'voto': True}}
                votantes.update_one(busqueda, final)
                render_template('/principio/index.html', 
                                token=eval(token))
            else: 
                flash('Hubo un problema al votar')
        else: 
            flash('Usted ya ha votado')
    return render_template('/votacion/index.html', 
                           token=eval(token), lista=lista)

@app.route('/cerrado')
def cerrar(): 
    # if localStorage.getItem('token') is not None: 
    #     localStorage.removeItem('token')
    localStorage.setItem('token', None)
    token = localStorage.getItem('token')
    flash(token)
    return render_template('/principio/index.html', 
                           token=eval(token))

if __name__ == '__main__':
    app.run(debug=True)
