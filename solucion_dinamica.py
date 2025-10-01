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

def rocPD(materias, estudiantes):
    columnas=len(estudiantes)
    filas=len(materias)
    #Crear matriz de insatisfacciones
    matrix = [[None for _ in range(columnas)] for _ in range(filas)]
    
    asignaciones = [[None] for _ in range(columnas)]
    ins_finales = [None for _ in range(columnas)]

    # Llenar la matriz de insatisfacciones
    for i in range(filas):
        for j in range(columnas):
            matriculadas = []
            #Aqui se recorre la matriz hacia arriba para obtener las materias en las que ya fue matriculado el estudiante j
            for y in range(len(materias)):
                if y<i:
                    if matrix[y][j][2]==1:
                        matriculadas.append(materias[y])
            
            matriculadas.append(materias[i])
            matrix[i][j] = [estudiantes[j][0], calcular_insatisfaccion(matriculadas, estudiantes[j])]
        if i==0:
            menorInsatisfaccion(materias[i], matrix[i], None)
        else:
            menorInsatisfaccion(materias[i], matrix[i], matrix[i-1])

   #Se recorrre la matriz de izquierda a derecha, y abajo hacia arriba, para obtener la instatisfacción final de cada estudiante 
   # y mientras se van agregando las materias en las que fue matriculado.
    for j in range(columnas):
        i = filas - 1
        matriculadas = []
        while i >= 0:
            if matrix[i][j][2] == 1:                
                matriculadas.append(materias[i][0])
                if ins_finales[j] is None:
                    ins_finales[j] = matrix[i][j][1]
                i -= 1
            else:
                i -= 1
        asignaciones[j] = (estudiantes[j][0], matriculadas)

    insatisfaccion_total = sum(ins_finales) / columnas

    print("Insatisfacción total: ", insatisfaccion_total)
    #print("Asignaciones: ", asignaciones)
    return asignaciones, insatisfaccion_total

#Funcion auxiliar que nos ayuda a encontrar a los estudiantes con menor insatisfacción al asignarles una materia, 
# segun los cupos de dicha materia
def menorInsatisfaccion(materia, ins, ins_anterior):
    cupos: int = materia[1]
    #Se hacen deepcopies para evitar modificar las listas originales, porque python manda todo con referencias (como en lp xd)
    ins_copy = copy.deepcopy(ins)
    dif_ins = copy.deepcopy(ins_anterior)

    #Se calcula la diferencia de instatisfacción entre la materia actual y la anterior
    for i in range(len(ins)):
        if ins_anterior is not None:
            dif_ins[i][1]=ins_anterior[i][1]-ins[i][1]
            #Se usa para verificar si la insatisfacción no cambió respecto a la materia anterior, 
            # ya que eso significa que el estudiante no queria matricular esta materia
            #por lo cual se le asigna una insatisfacción de -inf, para que sea menor a cualquier otra insatisfacción y no sea seleccionado.
            if dif_ins[i][1] == 0:
                dif_ins[i][1]=float('-inf')

    #Buscar elementos con insatisfacción repetida
    """
    seen = set()
    duplicates = []

    for i in ins:
        if i[1] in seen:
            duplicates.append(i)
            break
        else:
            seen.add(i[1])

    print("duplicates: ", duplicates)
    """
    #print("ins: ", ins)
    #Luego de la primera materia, se busca asignar los cupos a los estudiantes en orden de mayor reduccion de insatisfacción
    #al agregarles la materia actual
    if ins_anterior is not None: 
        dif_ins.sort(key=lambda x: x[1], reverse=True)
        matriculados = [i[0] for i in dif_ins[:cupos]]        
        for i in range(len(ins)):
            if ins[i][0] in matriculados and ins[i][1] != 1:

                ins[i].append(1) #1 si fue matriculado
            else:
                ins[i].append(0) #0 si no fue matriculado
    else:
        #Se usa para la primera fila (materia), donde no hay insatisfacción anterior para comparar la diferencia
        ins_copy.sort(key=lambda x: x[1])
        matriculados = ins_copy[:cupos]        
        for i in range(len(ins)):
            if ins[i] in matriculados and ins[i][1] != 1:
                ins[i].append(1) #1 si fue matriculado
            else:
                ins[i].append(0) #0 si no fue matriculado
    

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
