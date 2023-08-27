from db import votantes, candidatos

def agregar_votante(votante): 
    lista = votantes.find({'estatus': 'A'})
    # [[getattr(o, a) for a in ['cedula']] for o in lista]
    if votante['cedula'] in (o['cedula'] for o in lista): 
        return False
    return True