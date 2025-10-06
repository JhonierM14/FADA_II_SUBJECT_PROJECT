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
        
        if num_solicitadas == 0:
            continue

        frustracion_cantidad = 1.0 - (num_asignadas / num_solicitadas)

        prioridades_perdidas = 0
        set_asignadas = set(materias_asignadas)
        for mat_id, prioridad in materias_solicitadas:
            if mat_id not in set_asignadas:
                prioridades_perdidas += prioridad
        
        gamma = calcular_gamma(num_solicitadas)
        
        if gamma <= 0:
            frustracion_importancia = 0.0 if prioridades_perdidas == 0 else 1.0
        else:
            frustracion_importancia = prioridades_perdidas / gamma
        
        f_j = frustracion_cantidad * frustracion_importancia
        insatisfaccion_total += f_j

    return insatisfaccion_total / num_estudiantes


def rocV(materias: Materias, estudiantes: Estudiantes) -> Tuple[Asignaciones, float]:
    """
    Asigna materias a estudiantes basándose en un algoritmo voraz
    que prioriza las solicitudes con mayor prioridad (Estrategia 1).

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

    peticiones.sort(key=lambda x: x['prioridad'], reverse=True)

    cupos_restantes = materias.copy()
    asignaciones = {e_id: [] for e_id in estudiantes}

    for peticion in peticiones:
        estudiante_id = peticion['estudiante']
        materia_id = peticion['materia']
        
        if cupos_restantes.get(materia_id, 0) > 0:
            if materia_id not in asignaciones[estudiante_id]:
                asignaciones[estudiante_id].append(materia_id)
                cupos_restantes[materia_id] -= 1

    costo_final = calcular_insatisfaccion(asignaciones, estudiantes)
    return asignaciones, costo_final

# --- esto es otra alternativa para ir probando, pero no me ha dado buenos resultados ---
def rocV_alternativa_A(materias: Materias, estudiantes: Estudiantes) -> Tuple[Asignaciones, float]:
    """
    Asigna materias basándose en un algoritmo voraz que prioriza
    al estudiante más 'necesitado' primero (Estrategia 2).

    Args:
        materias: Diccionario con las materias disponibles y sus cupos.
        estudiantes: Diccionario con las solicitudes de cada estudiante.

    Returns:
        Una tupla conteniendo las asignaciones finales y el costo de insatisfacción.
    """
    # Paso 1: Calcular un "Puntaje de Necesidad" para cada estudiante
    lista_estudiantes_con_puntaje = []
    for e_id, e_info in estudiantes.items():
        # El puntaje se calcula como la suma de los cuadrados de las prioridades
        puntaje_necesidad = sum(prioridad ** 2 for _, prioridad in e_info['solicitudes'])
        
        lista_estudiantes_con_puntaje.append({
            'id': e_id,
            'puntaje': puntaje_necesidad,
            'solicitudes': e_info['solicitudes']
        })

    # Paso 2: Ordenar la lista de estudiantes por su puntaje (de mayor a menor)
    lista_estudiantes_con_puntaje.sort(key=lambda x: x['puntaje'], reverse=True)

    # Inicializar las estructuras de datos para el resultado
    cupos_restantes = materias.copy()
    asignaciones = {e_id: [] for e_id in estudiantes}

    # Paso 3: Procesar a cada estudiante en el orden de "necesidad"
    for estudiante_data in lista_estudiantes_con_puntaje:
        estudiante_id = estudiante_data['id']
        solicitudes_personales = estudiante_data['solicitudes']
        
        # Ordenar las solicitudes personales de este estudiante por su propia prioridad
        solicitudes_personales.sort(key=lambda x: x[1], reverse=True)
        
        # Intentar asignar cada materia solicitada por este estudiante
        for materia_id, _ in solicitudes_personales:
            if cupos_restantes.get(materia_id, 0) > 0:
                if materia_id not in asignaciones[estudiante_id]:
                    asignaciones[estudiante_id].append(materia_id)
                    cupos_restantes[materia_id] -= 1
    
    # Calcular el costo de la solución encontrada
    costo_final = calcular_insatisfaccion(asignaciones, estudiantes)
    return asignaciones, costo_final