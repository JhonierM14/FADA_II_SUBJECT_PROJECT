from itertools import combinations
from math import inf

def calcular_gamma(num_solicitadas):
    return 3 * num_solicitadas - 1

def insatisfaccion_estudiante(solicitudes, asignadas):
    """
    solicitudes:  materia -> prioridad
    asignadas:  materia -> prioridad
    """
    if not solicitudes:
        return 0.0
    
    gamma_val = calcular_gamma(len(solicitudes)) # γ(|ms_j|)
    
    # Cantidad de materias asignadas
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
    # Solo se considera las materias que el estudiante solicitó
    materias_solicitadas = [m for m in materias_list if m in preferencias_estudiante]

    # Generar todas las combinaciones de 1 a gamma_max materias
    for k in range(len(materias_solicitadas)):
        # Crear las posibles combinaciones de materias a matricular para el estudiante
        for combo in combinations(materias_solicitadas, k+1):
            # Verificar que hay cupos disponibles para esta combinación
            nuevos_cupos = list(cupos_usados)
            valido = True
            # Itera sobre cada materia de las combinaciones 
            for materia in combo:
                idx = materias_list.index(materia)
                # Verifica si cada materia tiene cupos disponibles
                if nuevos_cupos[idx] + 1 > materias_dict[materia]:
                    #print(f"nuevos_cupos[idx] + 1  {nuevos_cupos[idx]} materias_dict[materia] {materias_dict[materia]}")
                    valido = False
                    break
                nuevos_cupos[idx] += 1
            if valido:
                # Crear dict de materias asignadas con sus prioridades
                materias_asignadas = {m: preferencias_estudiante[m] for m in combo}
                insa = insatisfaccion_estudiante(preferencias_estudiante, materias_asignadas)
                combinaciones.append((tuple(nuevos_cupos), materias_asignadas, insa))
    return combinaciones

def rocPD(materias, estudiantes):
    """
    Algoritmo de programación dinámica para asignación óptima de materias
    Args:
        materias: dict {materia: cupos_disponibles}
        estudiantes: dict {id: {solicitudes: n, materia1: prioridad1, ...}}
    
    Returns:
        (insatisfaccion_minima, dict_asignaciones)
    """
    n = len(estudiantes)
    
    estudiantes_procesados = {}
    for id_est, info in estudiantes.items():
        # Extraer solo las preferencias sin 'solicitudes'
        solicitudes = info["solicitudes"]
        solicitudes2 = {}
        for i in range(len(solicitudes)):
            id_m = solicitudes[i][0]
            solicitudes2[id_m] = solicitudes[i][1]
        estudiantes_procesados[id_est] = solicitudes2
        #print("estudiantes_procesados: ", solicitudes2)

    # Guarda (num_estudiante, (cupos_usados_por_materia)) e insatisfacción acumulada mínima
    dp = {}
    choice = {}  # Para rastrear decisiones
    # Estado inicial de 0 estudiantes procesados, 0 cupos usados
    estado_inicial = (0, tuple([0] * len(materias)))
    dp[estado_inicial] = 0
    choice[estado_inicial] = None
    estudiantes_list = list(estudiantes_procesados.items())

    # procesar estudiante por estudiante
    for i in range(1, n + 1):
        id_est, preferencias = estudiantes_list[i - 1]
        #print(f"\nProcesando estudiante {i}/{n}: {id_est}")
        estados_nuevos = {}
        # Iterar sobre todos los estados del nivel anterior
        for estado, insa_acum in dp.items():
            num_est, cupos_usados = estado
            #print(f"cupos_usados {cupos_usados} estado: {estado}")
            # Solo procesar estados del nivel anterior
            if num_est != i - 1:
                continue
            # Generar todas las combinaciones válidas de materias para cada estudiante
            combinaciones_con_insa = generar_combinaciones(materias, cupos_usados, preferencias)
                
            #print(f"ID: {id_est} Combinaciones: {combinaciones_con_insa}")
            for nuevos_cupos, materias_asignadas, insa_estudiante in combinaciones_con_insa:
                #print(f"Estudiante {id_est} materias_asignadas  {materias_asignadas} insatisfacción {insa_estudiante}")
                nueva_insa_total = insa_acum + insa_estudiante
                nuevo_estado = (i, nuevos_cupos)
                # Actualizar si es mejor que lo que teníamos
                if nuevo_estado not in estados_nuevos or nueva_insa_total < estados_nuevos[nuevo_estado]:
                    #print(f"nuevo_estado {nuevo_estado} nueva_insa_total  {nueva_insa_total} estados_nuevos[nuevo_estado]")
                    estados_nuevos[nuevo_estado] = nueva_insa_total
                    choice[nuevo_estado] = (estado, materias_asignadas, id_est)
                    #print(f"Estados nuevos: {estados_nuevos}")
                    #print(f"choice[nuevo_estado] {choice[nuevo_estado]} estados_nuevos[nuevo_estado]  {estados_nuevos[nuevo_estado]}")
        # Agregar los nuevos estados al DP
        dp = {}
        dp.update(estados_nuevos)
        #print("DP:", dp)
        #print(f"Estados activos después de procesar {id_est}: {len([e for e in dp if e[0] == i])}")
    
    # Encontrar el mejor estado final
    estados_finales = [(estado, insa) for estado, insa in dp.items()]
    
    if not estados_finales:
        return inf, {}
    
    mejor_estado, mejor_insa = min(estados_finales, key=lambda x: x[1])
    mejor_insa_promedio = mejor_insa / n
    
    print(f"Estado final: {mejor_estado}")
    
    # Reconstrucción de la solución
    asignaciones = {}
    estado_actual = mejor_estado
    
    while choice[estado_actual] is not None:
        estado_anterior, materias_asignadas, id_est = choice[estado_actual]
        if materias_asignadas:
            asignaciones[id_est] = list(materias_asignadas.keys())
        else:
            asignaciones[id_est] = []
        estado_actual = estado_anterior
    
    return asignaciones, mejor_insa_promedio