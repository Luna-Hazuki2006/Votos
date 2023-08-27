from flask import Flask, render_template, request, flash
from db import candidatos, votantes
from validaciones import agregar_votante, agregar_candidato
from pprint import pprint
# korean queen tokyo walmart 2 DRIP > TOKYO , rope SKYPE _ 4 & korean XBOX
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'kqtw2D>T,rS_4&kX'

@app.route('/')
def iniciar():
    return render_template('/principio/index.html')

@app.route('/candidatos', methods=['GET'])
def listar_candidatos(): 
    return render_template('/candidatos/index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registrar_usuario(): 
    if request.method == 'POST':
        forma = request.form
        nuevo_votante = {
            'cedula': forma['cedula'], 
            'nombre': forma['nombre'], 
            'apellido': forma['apellido'], 
            'clave': forma['contraseña'], 
            'correo': forma['correo'], 
            'estatus': 'A'
        }
        pprint(nuevo_votante)
        if agregar_votante(nuevo_votante): 
            id = votantes.insert_one(nuevo_votante).inserted_id
            if id: 
                flash('Se ha registrado como votante éxitosamente')
            else: 
                flash('Ha sucedido un error al registrarse')
        else: 
            flash('La cédula que ha registrado ya existe')
    return render_template('/registro/index.html')

@app.route('/inicio', methods=['GET'])
def iniciar_sesion():
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