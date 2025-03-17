import pymongo
import os

cliente = pymongo.MongoClient(os.environ.get('URL'))

db = cliente.votaciones

votantes = db.votantes
candidatos = db.candidatos