from flask import Flask, render_template, request, flash
from os import urandom
from datetime import date, datetime
from flask_login import LoginManager
from itsdangerous import TimestampSigner, URLSafeTimedSerializer, base64_decode
from werkzeug.security import generate_password_hash
from db import candidatos, votantes
from validaciones import agregar_votante, agregar_candidato, verificar_usuario
from pprint import pprint
# korean queen tokyo walmart 2 DRIP > TOKYO , rope SKYPE _ 4 & korean XBOX
app = Flask(__name__, template_folder='templates')
# app.config['SECRET_KEY'] = 'kqtw2D>T,rS_4&kX'
app.config['SECRET_KEY'] = urandom(16).hex()
BaseToken = URLSafeTimedSerializer(app.config['SECRET_KEY'])

Token_Usuario = {
    'token': None, 
    'tiempo': None
}

def generar_token(usuario):
    token = BaseToken.dumps({'cedula': f'{usuario}'}, salt='usuario')
    BaseToken.loads(token, salt='usuario')
    print(datetime.utcnow())
    Token_Usuario['token'] = token
    # header, body, something_else = token.split(b'.'.decode('utf-8'))
    actual = datetime.utcnow()
    luego = None
    if (actual.minute + 6) > 59: 
        minuto = (actual.minute + 6) - 59
        hora = actual.hour + 1
        Token_Usuario['tiempo'] = datetime(actual.year, actual.month, actual.day, hora, minuto)
    else: 
        Token_Usuario['tiempo'] = datetime(actual.year, actual.month, actual.day, actual.hour, actual.minute + 6)
    print(Token_Usuario)

def verificar():
    
    return True

@app.route('/')
def iniciar():
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
        cedula = forma['cedula']
        clave = forma['contraseña']
        if verificar_usuario(cedula, clave): 
            print('*******************')
            generar_token(cedula)
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