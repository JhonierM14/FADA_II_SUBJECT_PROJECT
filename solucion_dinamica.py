def calcular_gamma(num_solicitadas):
    return 3 * num_solicitadas - 1

def insatisfaccion_estudiante(solicitudes, asignadas):
    """
    solicitudes: dict materia -> prioridad
    asignadas: dict materia -> prioridad (subconjunto de solicitudes)
    """
    if not solicitudes:
        return 0.0
    
    total_prioridad = sum(solicitudes.values())   # suma de todas las prioridades
    gamma_val = calcular_gamma(len(solicitudes))           # γ(|ms_j|)
    
    # Cantidad de materias asignadas
    num_asignadas = len(asignadas)
    num_solicitudes = len(solicitudes)
    
    # Prioridades NO satisfechas (las que el estudiante pidió pero no se le asignaron)
    insatisfechas = [p for mat, p in solicitudes.items() if mat not in asignadas]
    suma_insatisfechas = sum(insatisfechas)
    
    f_j = (1 - num_asignadas / num_solicitudes) * (suma_insatisfechas / gamma_val)
    return f_j

def insatisfaccion_global(estudiantes, asignaciones):
    """
    estudiantes: dict id_est -> {materia: prioridad}
    asignaciones: dict id_est -> lista de materias asignadas
    """
    f_vals = []
    for est, solicitudes in estudiantes.items():
        asignadas = {m: solicitudes[m] for m in asignaciones.get(est, []) if m in solicitudes}
        f_vals.append(insatisfaccion_estudiante(solicitudes, asignadas))
    return sum(f_vals) / len(f_vals)


def dinamica(materias, estudiantes):
    n = len(estudiantes)
    m = len(materias)
    total_cupos = sum(materias.values())

    # dp[i][c] = mínima insatisfacción considerando hasta el estudiante i con c cupos usados
    INF = float("inf")
    dp = [[INF] * (total_cupos+1) for _ in range(n+1)]
    dp[0][0] = 0

    estudiantes_list = list(estudiantes.items())

    for i, (id_est, solicitudes) in enumerate(estudiantes_list, start=1):
        for c in range(total_cupos+1):  # cupos usados
            # Opción 1: no asignar nada
            insa_none = insatisfaccion_estudiante(solicitudes, {})
            dp[i][c] = min(dp[i][c], dp[i-1][c] + insa_none)

            # Opción 2: asignar materias que pidió
            for materia, valor in solicitudes.items():
                if materia in materias:  # existe la materia
                    cupo = 1  # supongamos que cada asignación usa 1 cupo
                    if c >= cupo:
                        insa = insatisfaccion_estudiante(solicitudes, {materia: valor})
                        dp[i][c] = min(dp[i][c], dp[i-1][c-cupo] + insa)
    return dp


#print(dinamica(materias, estudiantes))

def knapsack(values, weights, W):
    n = len(values)
    dp = [[0] * (W+1) for _ in range(n+1)]

    for i in range(1, n+1):
        for w in range(1, W+1):
            if weights[i-1] <= w:  # puedo tomarlo
                print(weights[i-1], w)
                dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w-weights[i-1]])
                print(dp[i][w])
            else:  # no cabe
                dp[i][w] = dp[i-1][w]
    return dp

#print(knapsack([3,4,5,6], [2,3,4,5], 5))

from math import inf

def dinamica(materias, estudiantes):
    total_cupos = sum(materias.values())
    n = len(estudiantes)
    gamma_max = {}
    for id, info in estudiantes.items():
        gamma_max[id] = calcular_gamma(info['solicitudes'])
        info.pop('solicitudes')
    
    dp = [[inf] * (total_cupos+1) for _ in range(n+1)]
    choice = [[None] * (total_cupos+1) for _ in range(n+1)]
    
    dp[0][0] = 0
    estudiantes_list = list(estudiantes.items())
    
    for i in range(1, n+1):
        id_est, solicitudes = estudiantes_list[i-1]
        for j in range(total_cupos+1):
            max = 0
            # no asignar
            insa_sin = insatisfaccion_estudiante(solicitudes, {})
            if dp[i-1][j] < inf and dp[i-1][j] + insa_sin < dp[i][j]:
                dp[i][j] = dp[i-1][j] + insa_sin
                choice[i][j] = ("none", j)
            
            # asignar cada materia posible
            dadas ={}
            for materia, prioridad in solicitudes.items():

                if materia in materias and j+1 <= total_cupos and materias[materia] > 0 and max <=  gamma_max[id_est]:
                    dadas[materia] = prioridad
                    max += prioridad
                    continue

            insa_con = insatisfaccion_estudiante(solicitudes, dadas)
            if dp[i-1][j] < inf and dp[i-1][j] + insa_con < dp[i][j+1] and max <= gamma_max[id_est]:
                        dp[i][j+1] = dp[i-1][j] + insa_con
                        choice[i][j+1] = (materia, j)

    # Buscar la mejor insatisfacción
    mejor_j = min(range(total_cupos+1), key=lambda x: dp[n][x])
    mejor_valor = dp[n][mejor_j]
    
    # Reconstrucción hacia atrás
    asignaciones = {}
    cont_asig = {id_est: 0 for id_est in estudiantes} 
    print(cont_asig)

    i, j = n, mejor_j
    while i > 0 and j >= 0:
        decision = choice[i][j]
        id_est, solicitudes = estudiantes_list[i-1]
        if decision:
            materia, prev_j = decision
            if materia != "none":
                if cont_asig[id_est] < gamma_max[id_est] and materias[materia] > 0:
                    asignaciones.setdefault(id_est, []).append(materia)
                    cont_asig[id_est] += 1
                    materias[materia] -= 1
            j = prev_j
        i -= 1
    
    return mejor_valor, asignaciones

# ========================
# Ejemplo
materias = {
    "M1": 3,
    "M2": 4,
    "M3": 2
}

estudiantes = {
    "e1": {"solicitudes": 3,"M1": 4, "M2": 2, "M3": 1},
    "e2": {"solicitudes": 3,"M1": 4, "M2": 1, "M3": 3},
    "e3": {"solicitudes": 2,"M2": 3, "M3": 2},
    "e4": {"solicitudes": 2,"M1": 2, "M3": 3},
    "e5": {"solicitudes": 3,"M1": 3, "M2": 2, "M3": 3}
}

valor, asignaciones = dinamica(materias, estudiantes)
print("Insatisfacción mínima global =", valor)
print("Asignaciones óptimas =", asignaciones)
















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
    #print("Insatisfacción total: ", insatisfaccion_total)
    #print("Asignaciones: ", asignaciones)
    return asignaciones, insatisfaccion_total

#Funcion auxiliar que nos ayuda a encontrar a los estudiantes con menor insatisfacción al asignarles una materia, 
# segun los cupos de dicha materia
def menorInsatisfaccion(materia, ins, ins_anterior):
    cupos: int = materia[1]
    #Se hacen deepcopies para evitar modificar las listas originales, porque python manda todo con referencias (como en lp xd)
    ins_copy = copy.deepcopy(ins)
    ins_anterior_copy = copy.deepcopy(ins_anterior)

    #Se usa para verificar si la insatisfacción no cambió respecto a la materia anterior, 
    # ya que eso significa que el estudiante no queria matricular esta materia
    #por lo cual se le asigna una insatisfacción de inf, para que sea mayor a cualquier otra insatisfacción y no sea seleccionado.
    #Y lo mismo pero alreves para su insatisfacción en la materia anterior.
    for i in range(len(ins)):
        if ins_anterior is not None and ins[i][1] == ins_anterior[i][1]:
            ins_copy[i][1]=float('inf')
            ins_anterior_copy[i][1]=float('-inf')

    ins_copy.sort(key=lambda x: x[1])

    #Buscar elementos con insatisfacción repetida
    seen = set()
    duplicates = []

    for i in ins_copy:
        if i[1] in seen:
            duplicates.append(i)
            break
        else:
            seen.add(i[1])

    #En caso de que hayan insatisfacciones repetidas, se asignan los cupos a los estudiantes con mayor insatisfacción
    #de la materia anterior, ya que asi se minimiza la insatisfacción total.
    if duplicates and ins_anterior is not None: 
        ins_anterior_copy.sort(key=lambda x: x[1], reverse=True)
        matriculados = [i[0] for i in ins_anterior_copy[:cupos]]        
        for i in range(len(ins)):
            if ins[i][0] in matriculados:
                ins[i].append(1) #1 si fue matriculado
            else:
                ins[i].append(0) #0 si no fue matriculado
    else:
        #Si no hay insatisfacciones repetidas, se asignan los cupos a los estudiantes con menor insatisfacción en la materia actual.
        matriculados = ins_copy[:cupos]
        for i in range(len(ins)):
            if ins[i] in matriculados:
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
