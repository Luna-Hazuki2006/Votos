from flask import Flask, render_template
from db import candidatos, votantes
# korean queen tokyo walmart 2 DRIP > TOKYO , rope SKYPE _ 4 & korean XBOX
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'kqtw2D>T,rS_4&kX'

@app.route('/')
def iniciar():
    return render_template('/principio/index.html')

@app.route('/candidatos', methods=['GET'])
def listar_candidatos(): 
    return render_template('/candidatos/index.html')

@app.route('/registro', methods=['GET'])
def registrar_usuario(): 
    return render_template('/registro/index.html')

@app.route('/inicio', methods=['GET'])
def iniciar_sesion():
    return render_template('/inicio/index.html')

@app.route('/resultados', methods=['GET'])
def mostrar_resultados(): 
    return render_template('/resultados/index.html')

@app.route('/votantes', methods=['GET'])
def listar_votantes():
    return render_template('/votantes/index.html')

if __name__ == '__main__':
    app.run(debug=True)