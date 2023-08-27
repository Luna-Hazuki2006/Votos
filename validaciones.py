from db import votantes, candidatos

def agregar_votante(votante): 
    lista = votantes.find({'estatus': 'A'})
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
    return True