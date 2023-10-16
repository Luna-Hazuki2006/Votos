from db import votantes, candidatos, administrador
from werkzeug.security import check_password_hash

def agregar_votante(votante): 
    lista = votantes.find({'estatus': 'A'})
    for esto in lista:
        if esto['cedula'] == votante['cedula']: return False
    lista = candidatos.find({'estatus': 'A'})
    for esto in lista: 
        if esto['cedula'] == votante['cedula']: return False
    return True
    # [[getattr(o, a) for a in ['cedula']] for o in lista]
    # if votante['cedula'] in (o['cedula'] for o in lista): 
    #     return False
    # return True

def agregar_candidato(candidato): 
    lista = candidatos.find({'estatus': 'A'})
    for esto in lista:
        if esto['cedula'] == candidato['cedula']: return False
    lista = votantes.find({'estatus': 'A'})
    for esto in lista: 
        if esto['cedula'] == candidato['cedula']: return False
    return True

def verificar_usuario(cedula, clave):
    lista = votantes.find({'estatus': 'A'})
    for esto in lista: 
        if (esto['cedula'] == cedula and 
            check_password_hash(esto['clave'], clave)): 
            return True
    return False

def verificar_administrador(nombre, clave): 
    admin = administrador.find_one({'nombre': 'Administrador'})
    if (nombre != 'Administrador' or 
        check_password_hash(clave, admin['clave'])): 
        return False
    return True