import sys
import copy

def calcular_gamma(num_solicitadas):
    return 3 * num_solicitadas - 1

def calcular_insatisfaccion(asignaciones, estudiante):
    if not estudiante:
        return 0.0

    materias_solicitadas = estudiante[1]
    #Remover de asignaciones las materias que no fueron solicitadas:
    asignaciones = [a for a in asignaciones if a[0] in [m[0] for m in materias_solicitadas]]
    if not asignaciones:
        return 1.0
    
    num_solicitadas = len(materias_solicitadas)
    num_asignadas = len(asignaciones)
        
    if num_solicitadas == 0:
        return 0.0

    frustracion_cantidad = 1.0 - (num_asignadas / num_solicitadas)

    prioridades_perdidas = 0
    id_asignadas = [i[0] for i in asignaciones]

    for materia in materias_solicitadas:
        if materia[0] not in id_asignadas:
            prioridades_perdidas += materia[1]

    gamma = calcular_gamma(num_solicitadas)
        
    if gamma == 0:
        frustracion_importancia = 0.0 if prioridades_perdidas == 0 else 1.0
    else:
        frustracion_importancia = prioridades_perdidas / gamma
        
    if prioridades_perdidas==gamma:
        f_j = 1.0
    else:
        f_j = frustracion_cantidad * frustracion_importancia

    return f_j

def leer_entradaPD(ruta_archivo):
    materias = []
    estudiantes = []
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = [line.strip() for line in f if line.strip()]
            
            k = int(lineas[0])
            puntero = 1
            for i in range(k):
                codigo, cupo = lineas[puntero].split(',')
                materias.append((codigo, int(cupo)))
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

                estudiantes.append((e_id, solicitudes))
        return materias, estudiantes
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'")
        return None, None
    except (ValueError, IndexError) as e:
        print(f"Error: El archivo de entrada no tiene el formato correcto. Detalles: {e}")
        return None, None


def menorInsatisfaccion(materia, ins, ins_anterior, estudiantes_dict):
    """
    Args:
        materia: (nombre, cupos)
        ins: lista de [id_estudiante, insatisfaccion]
        ins_anterior: lista del nivel anterior
        estudiantes_dict: dict {id_estudiante: {materia: prioridad, ...}}
    """
    print("ins", ins)
    cupos = materia[1]
    nombre_materia = materia[0]
    
    ins_copy = copy.deepcopy(ins)
    dif_ins = copy.deepcopy(ins_anterior)

    if ins_anterior is not None:
        # Calcular reducción de insatisfacción
        for i in range(len(ins)):
            dif_ins[i][1] = ins_anterior[i][1] - ins[i][1]
            if dif_ins[i][1] == 0:
                dif_ins[i][1] = float('-inf')
        
        # Preparar candidatos con prioridad
        candidatos = []
        for item in dif_ins:
            id_est = item[0]
            reduccion = item[1]
            # Obtener prioridad de este estudiante en esta materia
            prioridad = estudiantes_dict.get(id_est, {}).get(nombre_materia, 0)
            
            candidatos.append({
                'id': id_est,
                'reduccion': reduccion,
                'prioridad': prioridad
            })
        
        # Ordenar: primero mayor reducción, luego mayor prioridad
        candidatos.sort(key=lambda x: (x['prioridad'], -x['reduccion']), reverse=True)
        matriculados = [c['id'] for c in candidatos[:cupos]]
        print("not none", candidatos)
        for i in range(len(ins)):
            if ins[i][0] in matriculados and ins[i][1] != 1:
                print("ins[i][0]", [i][0])
                ins[i].append(1)
            else:
                ins[i].append(0)
    
    else:
        # Primera materia: ordenar por menor insatisfacción, desempate por mayor prioridad
        candidatos = []
        for item in ins_copy:
            id_est = item[0]
            insatisfaccion = item[1]
            prioridad = estudiantes_dict.get(id_est, {}).get(nombre_materia, 0)
            
            candidatos.append({
                'id': id_est,
                'insatisfaccion': insatisfaccion,
                'prioridad': prioridad
            })
        
        # Ordenar: menor insatisfacción primero, mayor prioridad para desempate
        candidatos.sort(key=lambda x: (x['insatisfaccion'], -x['prioridad']))
        matriculados_ids = [c['id'] for c in candidatos[:cupos]]
        print("none", candidatos)

        for i in range(len(ins)):
            if ins[i][0] in matriculados_ids and ins[i][1] != 1:
                print("ins[i][0]", [i][0])
                ins[i].append(1)
            else:
                ins[i].append(0)
    
    # Retornar la insatisfacción total para esta configuración
    total_insatisfaccion = sum(item[1] for item in ins)
    return total_insatisfaccion


def rocPD(materias, estudiantes):
    columnas = len(estudiantes)
    filas = len(materias)
    
    matrix = [[None for _ in range(columnas)] for _ in range(filas)]
    asignaciones = [[None] for _ in range(columnas)]
    ins_finales = [None for _ in range(columnas)]

    # Crear diccionario de estudiantes para acceso rápido
    # Convertir de [(materia, prioridad), ...] a {materia: prioridad}
    estudiantes_dict = {}
    for est_id, solicitudes_lista in estudiantes:
        estudiantes_dict[est_id] = {materia: prioridad for materia, prioridad in solicitudes_lista}

    # Llenar la matriz
    for i in range(filas):
        for j in range(columnas):
            matriculadas = []
            for y in range(len(materias)):
                if y < i:
                    if matrix[y][j][2] == 1:
                        matriculadas.append(materias[y])
            
            matriculadas.append(materias[i])
            matrix[i][j] = [estudiantes[j][0], calcular_insatisfaccion(matriculadas, estudiantes[j])]
        
        # Pasar diccionario de estudiantes
        if i == 0:
            menorInsatisfaccion(materias[i], matrix[i], None, estudiantes_dict)
        else:
            menorInsatisfaccion(materias[i], matrix[i], matrix[i-1], estudiantes_dict)

    # Reconstrucción
    for j in range(columnas):
        i = filas - 1
        matriculadas = []
        insatisfaccion_estudiante = 0
        
        while i >= 0:
            if matrix[i][j][2] == 1:
                matriculadas.append(materias[i][0])
                insatisfaccion_estudiante = matrix[i][j][1]
                i -= 1
            else:
                i -= 1
        
        asignaciones[j] = (estudiantes[j][0], matriculadas)
        ins_finales[j] = insatisfaccion_estudiante

    # Verificar que no hay valores None
    ins_finales = [x if x is not None else 0 for x in ins_finales]
    insatisfaccion_total = sum(ins_finales) / columnas
    return asignaciones, insatisfaccion_total
    
def escribir_salidaPD(ruta_archivo, asignaciones, costo):
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(f"{costo}\n")
            for i in range(len(asignaciones)):
                e_id, materias_asignadas = asignaciones[i]
                print("Estudiante:", e_id, "Materias asignadas:", materias_asignadas)
                num_asignadas = len(materias_asignadas)
                f.write(f"{e_id},{num_asignadas}\n")
                materias_asignadas.sort()
                for i in range(len(materias_asignadas)):
                    mat_id = materias_asignadas[i]
                    f.write(f"{mat_id}\n")
        print(f"Solución guardada en '{ruta_archivo}'")
    except Exception as e:
        print(f"Error al guardar el archivo de salida. Detalles: {e}")
