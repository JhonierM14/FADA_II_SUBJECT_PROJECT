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

def leer_entrada(ruta_archivo):
    materias = {}
    estudiantes = {}
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = [line.strip() for line in f if line.strip()]
            
            k = int(lineas[0])
            puntero = 1
            for i in range(k):
                codigo, cupo = lineas[puntero].split(',')
                materias[codigo] = int(cupo)
                puntero += 1

            r = int(lineas[puntero])
            puntero += 1
            
            for _ in range(r):
                if puntero >= len(lineas): break
                e_id, num_solicitudes = lineas[puntero].split(',')
                num_solicitudes = int(num_solicitudes)
                puntero += 1
                
                solicitudes = []
                for _ in range(num_solicitudes):
                    mat_id, prioridad = lineas[puntero].split(',')
                    solicitudes.append((mat_id, int(prioridad)))
                    puntero += 1
                
                estudiantes[e_id] = {'solicitudes': solicitudes}
        return materias, estudiantes
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'")
        return None, None
    except (ValueError, IndexError) as e:
        print(f"Error: El archivo de entrada no tiene el formato correcto. Detalles: {e}")
        return None, None

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

def escribir_salida(ruta_archivo, asignaciones, costo):
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(f"{costo}\n")
            for e_id, materias_asignadas in asignaciones.items():
                num_asignadas = len(materias_asignadas)
                f.write(f"{e_id},{num_asignadas}\n")
                materias_asignadas.sort()
                for mat_id in materias_asignadas:
                    f.write(f"{mat_id}\n")
        print(f"Solución guardada en '{ruta_archivo}'")
    except Exception as e:
        print(f"Error al guardar el archivo de salida. Detalles: {e}")
