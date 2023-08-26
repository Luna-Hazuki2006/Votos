from flask import Flask
from db import candidatos, votantes

app = Flask(__name__, template_folder='templates')