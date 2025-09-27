import sys
import copy

def calcular_gamma(num_solicitadas):
    return 3 * num_solicitadas - 1

def calcular_insatisfaccion(asignaciones, estudiantes):
    if not estudiantes:
        return 0.0
    insatisfaccion_total = 0.0
    num_estudiantes = len(estudiantes)

    

    for estudiante in estudiantes:
        materias_solicitadas = estudiante[1]
        #Remover materias no solicitadas:
        set_solicitadas = set(estudiantes[0][1])
        for materia in asignaciones:
            if materia[0] not in set_solicitadas:
                asignaciones.remove(materia)
        num_solicitadas = len(materias_solicitadas)
        num_asignadas = len(asignaciones)
        
        if num_solicitadas == 0:
            continue

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
        insatisfaccion_total += f_j

    return insatisfaccion_total / num_estudiantes

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

def rocPD(materias, estudiantes):
    '''
    if len(estudiantes) != r:
        raise ValueError("El número de estudiantes no coincide con 'r'")
    if len(materias) != k:
        raise ValueError("El número de materias no coincide con 'k'")
    '''  
    columnas=len(estudiantes)
    filas=len(materias)  
    matrix = [[None for _ in range(columnas)] for _ in range(filas)]

    for i in range(len(materias)):
        for j in range(len(estudiantes)):
            matriculadas = []
            for y in range(len(materias)):
                if y<i:
                    if matrix[y][j][2]==1:
                        matriculadas.append(materias[y])
            matriculadas.append(materias[i])
            matrix[i][j] = [estudiantes[j][0], calcular_insatisfaccion(matriculadas, [estudiantes[j]])]
        if i==0:
            menorInsatisfaccion(materias[i], matrix[i], None)
        else:
            menorInsatisfaccion(materias[i], matrix[i], matrix[i-1])
    #print(matrix)
    return matrix

def menorInsatisfaccion(materia, ins, ins_anterior):
    cupos: int = materia[1]
    ins_copy = copy.deepcopy(ins)
    ins_copy.sort(key=lambda x: x[1])

    matriculados = ins_copy[:cupos]
    for i in range(len(ins)):
        if ins[i] in matriculados:
            ins[i].append(1) #1 si fue matriculado
        else:
            ins[i].append(0) #0 si no fue matriculado
    print("Matriculados: ", ins)

def escribir_salidaPD(ruta_archivo, asignaciones, costo):
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
