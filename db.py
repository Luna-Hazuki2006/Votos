import pymongo

cliente = pymongo.MongoClient('mongodb+srv://lunahazuki2006:cXU0lYhSncWZ12FM@cluster0.owjghpf.mongodb.net/')

db = cliente.votaciones

votantes = db.votantes
candidatos = db.candidatos
votos = db.votos
administrador = db.administrador