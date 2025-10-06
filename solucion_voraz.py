from typing import List, Dict, Tuple, Any

# Define tipos para mayor claridad
Materias = Dict[str, int]  # {'materia_id': cupo}
Solicitud = Tuple[str, int]  # ('materia_id', prioridad)
EstudianteInfo = Dict[str, List[Solicitud]] # {'solicitudes': [('mat1', 5), ...]}
Estudiantes = Dict[str, EstudianteInfo] # {'estudiante_id': EstudianteInfo}
Asignaciones = Dict[str, List[str]] # {'estudiante_id': ['mat1', 'mat3']}

def calcular_gamma(num_solicitadas: int) -> int:
    """Calcula el factor de normalización gamma según la fórmula γ(X) = 3X - 1."""
    return 3 * num_solicitadas - 1

def calcular_insatisfaccion(asignaciones: Asignaciones, estudiantes: Estudiantes) -> float:
    """
    Calcula la insatisfacción general promedio basada en las asignaciones y las solicitudes.

    Args:
        asignaciones: Un diccionario con las materias asignadas a cada estudiante.
        estudiantes: Un diccionario con la información y solicitudes de cada estudiante.

    Returns:
        Un valor flotante entre 0 y 1 que representa la insatisfacción general.
    """
    if not estudiantes:
        return 0.0
        
    insatisfaccion_total = 0.0
    num_estudiantes = len(estudiantes)

    for e_id, e_info in estudiantes.items():
        materias_solicitadas = e_info['solicitudes']
        materias_asignadas = asignaciones.get(e_id, [])
        
        num_solicitadas = len(materias_solicitadas)
        num_asignadas = len(materias_asignadas)
        
        # Si un estudiante no solicitó nada, su insatisfacción es 0.
        if num_solicitadas == 0:
            continue

        # Primer término: Frustración por la cantidad de materias no asignadas.
        frustracion_cantidad = 1.0 - (num_asignadas / num_solicitadas)

        # Segundo término: Frustración por la importancia de las materias no asignadas.
        prioridades_perdidas = 0
        set_asignadas = set(materias_asignadas)
        for mat_id, prioridad in materias_solicitadas:
            if mat_id not in set_asignadas:
                prioridades_perdidas += prioridad
        
        gamma = calcular_gamma(num_solicitadas)
        
        # El denominador gamma no debería ser cero si num_solicitadas >= 1.
        # Pero esta comprobación es una buena práctica de programación defensiva.
        if gamma == 0:
            frustracion_importancia = 0.0 if prioridades_perdidas == 0 else 1.0
        else:
            frustracion_importancia = prioridades_perdidas / gamma
        
        # Insatisfacción individual (f_j) es el producto de ambas frustraciones.
        f_j = frustracion_cantidad * frustracion_importancia
        insatisfaccion_total += f_j

    # La insatisfacción general es el promedio de las individuales.
    return insatisfaccion_total / num_estudiantes

def rocV(materias: Materias, estudiantes: Estudiantes) -> Tuple[Asignaciones, float]:
    """
    Asigna materias a estudiantes basándose en un algoritmo voraz
    que prioriza las solicitudes con mayor prioridad.

    Args:
        materias: Diccionario con las materias disponibles y sus cupos.
        estudiantes: Diccionario con las solicitudes de cada estudiante.

    Returns:
        Una tupla conteniendo las asignaciones finales y el costo de insatisfacción.
    """
    peticiones = []
    for e_id, e_info in estudiantes.items():
        for mat_id, prioridad in e_info['solicitudes']:
            peticiones.append({'estudiante': e_id, 'materia': mat_id, 'prioridad': prioridad})

    # Ordenar todas las peticiones de todos los estudiantes de mayor a menor prioridad
    peticiones.sort(key=lambda x: x['prioridad'], reverse=True)

    cupos_restantes = materias.copy()
    asignaciones = {e_id: [] for e_id in estudiantes}

    for peticion in peticiones:
        estudiante_id = peticion['estudiante']
        materia_id = peticion['materia']
        
        # Verificar si hay cupo y si el estudiante no tiene ya esa materia
        if cupos_restantes.get(materia_id, 0) > 0:
            if materia_id not in asignaciones[estudiante_id]:
                asignaciones[estudiante_id].append(materia_id)
                cupos_restantes[materia_id] -= 1

    # Calcular el costo de la solución encontrada
    costo_final = calcular_insatisfaccion(asignaciones, estudiantes)
    return asignaciones, costo_final
