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


materias = {
    "M1": 3,
    "M2": 4,
    "M3": 2
}

estudiantes = {
    "e1": {"solicitudes": 3,"M1": 5, "M2": 2, "M3": 1},
    "e2": {"solicitudes": 3,"M1": 4, "M2": 1, "M3": 3},
    "e3": {"solicitudes": 2,"M2": 3, "M3": 2},
    "e4": {"solicitudes": 2,"M1": 2, "M3": 3},
    "e5": {"solicitudes": 3,"M1": 3, "M2": 2, "M3": 3}
}

print(dinamica(materias, estudiantes))

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

def dinamicas(materias, estudiantes):
    total_cupos = sum(materias.values())
    n = len(estudiantes)
    
    # DP inicialización
    dp = [[inf] * (total_cupos+1) for _ in range(n+1)]
    dp[0][0] = 0  # nadie asignado, insatisfacción = 0
    
    estudiantes_list = list(estudiantes.items())
    
    # Recorremos estudiantes
    for i in range(1, n+1):
        id_est, solicitudes = estudiantes_list[i-1]
        
        for j in range(total_cupos+1):
            # Caso 1: no asignar nada
            insa_sin = insatisfaccion_estudiante(solicitudes, {})
            if dp[i-1][j] < inf:
                dp[i][j] = min(dp[i][j], dp[i-1][j] + insa_sin)
            
            # Caso 2: asignar una materia
            for materia, prioridad in solicitudes.items():
                if materia in materias and j+1 <= total_cupos and materias[materia] > 0:
                    insa_con = insatisfaccion_estudiante(solicitudes, {materia: prioridad})
                    if dp[i-1][j] < inf:
                        dp[i][j+1] = min(dp[i][j+1], dp[i-1][j] + insa_con)
    
    # Mejor solución global
    return min(dp[n])

# -----------------------------
# Ejemplo
materias = {"M1": 1, "M2": 1}
estudiantes = {
    "e1": {"M1": 1, "M2": 4},
    "e2": {"M1": 2, "M2": 3}
}

print("Insatisfacción mínima global =", dinamicas(materias, estudiantes))