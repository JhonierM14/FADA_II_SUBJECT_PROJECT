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

def generar_combinaciones(materias_dict, cupos_usados, preferencias_estudiante, gamma_max_estudiante):
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

    # Generar todas las combinaciones de 1 a gamma_max materias
    for k in range(1, gamma_max_estudiante + 1):
        # Solo se considera las materias que el estudiante solicitó
        materias_solicitadas = [m for m in materias_list if m in preferencias_estudiante]
        
        for combo in combinations(materias_solicitadas, k):
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
                combinaciones.append((tuple(nuevos_cupos), materias_asignadas))
    return combinaciones

def dinamica(materias, estudiantes):
    """
    Algoritmo de programación dinámica para asignación óptima de materias
    Args:
        materias: dict {materia: cupos_disponibles}
        estudiantes: dict {id: {solicitudes: n, materia1: prioridad1, ...}}
    
    Returns:
        (insatisfaccion_minima, dict_asignaciones)
    """
    n = len(estudiantes)
    #print(f"Procesando {n} estudiantes")
    
    # Calcular gamma_max para cada estudiante
    gamma_max = {}
    estudiantes_procesados = {}
    for id_est, info in estudiantes.items():
        gamma_max[id_est] = calcular_gamma(info['solicitudes'])
        # Extraer solo las preferencias sin 'solicitudes'
        estudiantes_procesados[id_est] = {k: v for k, v in info.items() if k != 'solicitudes'}
    
    #print(f"Primeros 5 estudiantes procesados: {dict(list(estudiantes_procesados.items())[:5])}")
    
    # Guarda (num_estudiante, (cupos_usados_por_materia)) e insatisfacción acumulada mínima
    dp = {}
    choice = {}  # Para rastrear decisiones
    
    # Estado inicial de 0 estudiantes procesados, 0 cupos usados
    estado_inicial = (0, tuple([0] * len(materias)))
    dp[estado_inicial] = 0
    choice[estado_inicial] = None
    
    estudiantes_list = list(estudiantes_procesados.items())
    #print(f"Total de estudiantes en lista: {len(estudiantes_list)}")

    # procesar estudiante por estudiante
    for i in range(1, n + 1):
        id_est, preferencias = estudiantes_list[i - 1]
        #print(f"\nProcesando estudiante {i}/{n}: {id_est} con preferencias: {preferencias}")
        
        estados_nuevos = {}
        
        # Contar estados del nivel anterior
        estados_nivel_anterior = [(estado, insa) for estado, insa in dp.items() if estado[0] == i-1]
        #print(f"Estados disponibles del nivel anterior: {len(estados_nivel_anterior)}")
        
        if not estados_nivel_anterior:
            #print(f"¡ERROR! No hay estados del nivel anterior para procesar estudiante {i}")
            break
        
        # Iterar sobre todos los estados del nivel anterior
        for estado, insa_acum in dp.items():
            num_est, cupos_usados = estado

            # Solo procesar estados del nivel anterior
            if num_est != i - 1:
                continue
            
            #print(f"  Procesando estado: {estado} con insatisfacción acumulada: {insa_acum}")
            
            # Generar todas las combinaciones válidas de materias para cada estudiante
            combinaciones = generar_combinaciones(
                materias, cupos_usados, preferencias, gamma_max[id_est]
            )
            
            #print(f"  Combinaciones generadas: {len(combinaciones)}")
            if not combinaciones:
                #print(f"  ¡ADVERTENCIA! No se generaron combinaciones para {id_est}")
                # Agregar opción de no asignar nada
                nuevo_estado = (i, cupos_usados)
                insa_no_asignar = 1.0  # Insatisfacción máxima por no asignar nada
                nueva_insa_total = insa_acum + insa_no_asignar
                
                if nuevo_estado not in estados_nuevos or nueva_insa_total < estados_nuevos[nuevo_estado]:
                    estados_nuevos[nuevo_estado] = nueva_insa_total
                    choice[nuevo_estado] = (estado, {}, id_est)
                    #print(f"  Agregada opción de no asignar: insatisfacción = {nueva_insa_total}")
                continue
            
            # Ordenar por insatisfacción calculada para cada combinación
            combinaciones_con_insa = []
            for nuevos_cupos, materias_asignadas in combinaciones:
                insa = insatisfaccion_estudiante(preferencias, materias_asignadas)
                combinaciones_con_insa.append((nuevos_cupos, materias_asignadas, insa))
            
            #print(f"  Primera combinación: {combinaciones_con_insa[0] if combinaciones_con_insa else 'Ninguna'}")

            for nuevos_cupos, materias_asignadas, insa_estudiante in combinaciones_con_insa:
                nueva_insa_total = insa_acum + insa_estudiante
                nuevo_estado = (i, nuevos_cupos)
                
                # Actualizar si es mejor que lo que teníamos
                if nuevo_estado not in estados_nuevos or nueva_insa_total < estados_nuevos[nuevo_estado]:
                    estados_nuevos[nuevo_estado] = nueva_insa_total
                    choice[nuevo_estado] = (estado, materias_asignadas, id_est)

        # Agregar los nuevos estados al DP
        dp.update(estados_nuevos)
        #print(f"Estados generados para nivel {i}: {len(estados_nuevos)}")
        
        if not estados_nuevos:
            #print(f"¡ERROR! No se generaron nuevos estados en nivel {i}")
            break

        # Limitar a los primeros 10 estudiantes para debug
        if i >= 10:
            #print("Limitando debug a primeros 10 estudiantes...")
            break
    
    # Encontrar el mejor estado final
    if i >= 10:  # Si limitamos el debug
        estados_finales = [(estado, insa) for estado, insa in dp.items() if estado[0] == i]
    else:
        estados_finales = [(estado, insa) for estado, insa in dp.items() if estado[0] == n]
    
    #print(f"\nEstados finales encontrados: {len(estados_finales)}")
    
    if not estados_finales:
        #print("¡ERROR! No se encontraron estados finales")
        return inf, {}
    
    mejor_estado, mejor_insa = min(estados_finales, key=lambda x: x[1])
    mejor_insa_promedio = mejor_insa / n
    
    #print(f"Mejor estado: {mejor_estado}")
    #print(f"Mejor insatisfacción total: {mejor_insa}")
    
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
    
    return mejor_insa_promedio, asignaciones

# Ejemplo Prueba1 - 5 estudiantes (dataset mínimo para testing básico)
# ...existing code...

# Nuevo dataset - 20 estudiantes, 4 materias
# ...existing code...

# Nuevo dataset - 30 estudiantes, 4 materias (mejor distribución de cupos)
materias = {
    "1000": 4,   # materia 1000 con 4 cupos
    "1001": 7,   # materia 1001 con 7 cupos
    "1002": 15,  # materia 1002 con 15 cupos (¡muy popular!)
    "1003": 4    # materia 1003 con 4 cupos
}

estudiantes = {
    "100": {"solicitudes": 4, "1001": 5, "1000": 3, "1002": 1, "1003": 2},
    "101": {"solicitudes": 4, "1002": 3, "1001": 1, "1000": 2, "1003": 4},
    "102": {"solicitudes": 1, "1002": 2},
    "103": {"solicitudes": 2, "1002": 1, "1003": 2},
    "104": {"solicitudes": 4, "1001": 1, "1002": 3, "1000": 1, "1003": 2},
    "105": {"solicitudes": 2, "1001": 3, "1002": 1},
    "106": {"solicitudes": 3, "1000": 3, "1002": 4, "1003": 1},
    "107": {"solicitudes": 1, "1002": 2},
    "108": {"solicitudes": 1, "1001": 2},
    "109": {"solicitudes": 1, "1000": 1},
    "110": {"solicitudes": 1, "1003": 1},
    "111": {"solicitudes": 4, "1000": 2, "1001": 4, "1002": 3, "1003": 1},
    "112": {"solicitudes": 1, "1002": 1},
    "113": {"solicitudes": 2, "1000": 2, "1001": 1},
    "114": {"solicitudes": 3, "1000": 3, "1002": 4, "1003": 1},
    "115": {"solicitudes": 2, "1000": 3, "1001": 2},
    "116": {"solicitudes": 3, "1002": 5, "1001": 1, "1000": 1},
    "117": {"solicitudes": 4, "1001": 1, "1000": 5, "1002": 3, "1003": 1},
    "118": {"solicitudes": 4, "1002": 2, "1003": 1, "1001": 4, "1000": 3},
    "119": {"solicitudes": 4, "1000": 1, "1002": 1, "1003": 2, "1001": 4},
    "120": {"solicitudes": 3, "1000": 4, "1001": 1, "1003": 3},
    "121": {"solicitudes": 1, "1000": 1},
    "122": {"solicitudes": 4, "1000": 5, "1001": 2, "1002": 2, "1003": 1},
    "123": {"solicitudes": 2, "1001": 2, "1003": 2},
    "124": {"solicitudes": 1, "1001": 1},
    "125": {"solicitudes": 2, "1000": 2, "1001": 3},
    "126": {"solicitudes": 1, "1002": 1},
    "127": {"solicitudes": 2, "1001": 2, "1002": 2},
    "128": {"solicitudes": 4, "1001": 3, "1002": 3, "1003": 4, "1000": 1},
    "129": {"solicitudes": 3, "1003": 4, "1002": 3, "1000": 1}
}

valor, asignaciones = dinamica(materias, estudiantes)
print(f"\nMejor insatisfacción total: {valor}")
print("Asignaciones óptimas ", asignaciones)