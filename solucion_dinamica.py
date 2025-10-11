from itertools import combinations
from math import inf

def calcular_gamma(num_solicitadas):
    return 3 * num_solicitadas - 1

def insatisfaccion_estudiante(solicitudes, asignadas):
    """
    solicitudes: dict materia -> prioridad
    asignadas: dict materia -> prioridad
    """
    if not solicitudes:
        return 0.0
    
    gamma_val = calcular_gamma(len(solicitudes))
    
    num_asignadas = len(asignadas)
    num_solicitudes = len(solicitudes)
    
    insatisfechas = [p for mat, p in solicitudes.items() if mat not in asignadas]
    suma_insatisfechas = sum(insatisfechas)
    
    f_j = (1 - num_asignadas / num_solicitudes) * (suma_insatisfechas / gamma_val)
    return f_j

def generar_combinaciones(materias_dict, cupos_usados, preferencias_estudiante):
    """
    Genera todas las combinaciones válidas de materias para un estudiante
    Args:
        materias_dict: dict {materia: cupos_totales}
        cupos_usados: tuple con cupos usados de cada materia
        preferencias_estudiante: dict {materia: prioridad}
        gamma_max_estudiante: máximo de materias que puede tomar
    
    Returns:
        Lista de tuplas (nuevos_cupos_usados, dict_materias_asignadas)
    """
    materias_list = list(materias_dict.keys())
    combinaciones = []
    materias_solicitadas = [m for m in materias_list if m in preferencias_estudiante]

    # Incluir la opción de no asignar nada (k=0)
    for k in range(len(materias_solicitadas) + 1):
        if k == 0:
            # No asignar ninguna materia
            insa = insatisfaccion_estudiante(preferencias_estudiante, {})
            combinaciones.append((cupos_usados, {}, insa))
        else:
            # Generar combinaciones de k materias
            for combo in combinations(materias_solicitadas, k):
                nuevos_cupos = list(cupos_usados)
                valido = True
                
                for materia in combo:
                    idx = materias_list.index(materia)
                    if nuevos_cupos[idx] + 1 > materias_dict[materia]:
                        valido = False
                        break
                    nuevos_cupos[idx] += 1
                
                if valido:
                    materias_asignadas = {m: preferencias_estudiante[m] for m in combo}
                    insa = insatisfaccion_estudiante(preferencias_estudiante, materias_asignadas)
                    combinaciones.append((tuple(nuevos_cupos), materias_asignadas, insa))

    return combinaciones

def rocPD(materias, estudiantes):
    """
    Algoritmo de programación dinámica para asignación óptima de materias
    Args:
        materias: dict {materia: cupos_disponibles}
        estudiantes: dict {id: {solicitudes: [(materia, prioridad), ...]}}
        verbose: bool para activar prints de debug
    
    Returns:
        (asignaciones, insatisfaccion_promedio)
    """
    n = len(estudiantes)
    
    # Procesar estudiantes
    estudiantes_procesados = {}
    for id_est, info in estudiantes.items():
        solicitudes = info["solicitudes"]
        solicitudes2 = {id_m: prioridad for id_m, prioridad in solicitudes}
        estudiantes_procesados[id_est] = solicitudes2

    # Inicializar DP
    dp = {}
    choice = {}
    estado_inicial = (0, tuple([0] * len(materias)))
    dp[estado_inicial] = 0
    choice[estado_inicial] = None
    
    estudiantes_list = list(estudiantes_procesados.items())

    # Procesar estudiante por estudiante
    for i in range(1, n + 1):
        id_est, preferencias = estudiantes_list[i - 1]
        # print(f"\nProcesando estudiante {i}/{n}: {id_est}")
        
        # Iterar sobre todos los estados del nivel anterior
        for estado, insa_acum in list(dp.items()):
            num_est, cupos_usados = estado
            
            # Solo procesar estados del nivel anterior
            if num_est != i - 1:
                continue
            
            # Generar todas las combinaciones válidas
            combinaciones_con_insa = generar_combinaciones(materias, cupos_usados, preferencias)
            # print(f"  Estados previos: {estado}, Combinaciones: {len(combinaciones_con_insa)}")
            
            for nuevos_cupos, materias_asignadas, insa_estudiante in combinaciones_con_insa:
                nueva_insa_total = insa_acum + insa_estudiante
                nuevo_estado = (i, nuevos_cupos)
                
                # Actualizar si es mejor
                if nuevo_estado not in dp or nueva_insa_total < dp[nuevo_estado]:
                    dp[nuevo_estado] = nueva_insa_total
                    choice[nuevo_estado] = (estado, materias_asignadas, id_est)
    
    # Encontrar el mejor estado final
    estados_finales = [(estado, insa) for estado, insa in dp.items() if estado[0] == n]
    
    if not estados_finales:
        return {}, inf
    
    mejor_estado, mejor_insa = min(estados_finales, key=lambda x: x[1])
    mejor_insa_promedio = mejor_insa / n
    
    print(f"\nEstado final óptimo: {mejor_estado}")

    # Reconstrucción de la solución
    asignaciones = {}
    estado_actual = mejor_estado
    
    while choice[estado_actual] is not None:
        estado_anterior, materias_asignadas, id_est = choice[estado_actual]
        asignaciones[id_est] = list(materias_asignadas.keys())
        estado_actual = estado_anterior
    
    return asignaciones, mejor_insa_promedio