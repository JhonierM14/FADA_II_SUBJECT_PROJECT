import sys

def calcular_gamma(num_solicitadas):
    return 3 * num_solicitadas - 1

def calcular_insatisfaccion(asignaciones, estudiantes):
    if not estudiantes:
        return 0.0
        
    insatisfaccion_total = 0.0
    num_estudiantes = len(estudiantes)

    for e_id, e_info in estudiantes.items():
        materias_solicitadas = e_info['solicitudes']
        materias_asignadas = asignaciones.get(e_id, [])
        num_solicitadas = len(materias_solicitadas)
        num_asignadas = len(materias_asignadas)
        
        if num_solicitadas == 0:
            continue

        frustracion_cantidad = 1.0 - (num_asignadas / num_solicitadas)

        prioridades_perdidas = 0
        set_asignadas = set(materias_asignadas)
        for mat_id, prioridad in materias_solicitadas:
            if mat_id not in set_asignadas:
                prioridades_perdidas += prioridad
        
        gamma = calcular_gamma(num_solicitadas)
        if gamma == 0:
            frustracion_importancia = 0.0 if prioridades_perdidas == 0 else 1.0
        else:
            frustracion_importancia = prioridades_perdidas / gamma
        
        f_j = frustracion_cantidad * frustracion_importancia
        insatisfaccion_total += f_j

    return insatisfaccion_total / num_estudiantes

def rocV(materias, estudiantes):
    peticiones = []
    for e_id, e_info in estudiantes.items():
        for mat_id, prioridad in e_info['solicitudes']:
            peticiones.append({'estudiante': e_id, 'materia': mat_id, 'prioridad': prioridad})

    peticiones.sort(key=lambda x: x['prioridad'], reverse=True)

    cupos_restantes = materias.copy()
    asignaciones = {e_id: [] for e_id in estudiantes}

    for peticion in peticiones:
        estudiante_id = peticion['estudiante']
        materia_id = peticion['materia']
        
        if materia_id in cupos_restantes:
            if cupos_restantes[materia_id] > 0:
                if materia_id not in asignaciones[estudiante_id]:
                    asignaciones[estudiante_id].append(materia_id)
                    cupos_restantes[materia_id] -= 1

    costo_final = calcular_insatisfaccion(asignaciones, estudiantes)
    return asignaciones, costo_final

