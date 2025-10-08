from itertools import combinations, product
import time

class Materia:
    def __init__(self, id: int, cupos: int, estudiantes: list):
        self.id = id
        self.cupos = cupos
        self.estudiantes = estudiantes
    
    def __repr__(self):
        return f"Materia(id={self.id}, cupos={self.cupos}, estudiantes={self.estudiantes})"

def encontrarMateria(estudiante: list, codigoMateria: str) -> bool:
    """
    Verifica si un estudiante quiere 
    matricular una materia

    Args
    - estudiante (list): estudiante a verificar
    - codigoMateria (str): codigo de la materia a verificar

    Return
    - True si el estudiante quiere ver la materia, False en caso contrario (bool)
    """

    for idMateria, prioridad in estudiante[1]:
        if idMateria == codigoMateria: 
            return True
    
    return False

def getEstudiantesByMateria(estudiantes: list, materias: list) -> None:
    """
    Crea una materia y añade a cada estudiante que quiere ver la materia
    Cada materia tiene una copia del estudiante que quiere ver la materia

    Args
    - estudiantes (list): lista de estudiantes
    - materias (list): lista de materias

    Return
    - None (void)
    """

    global ObjectMaterias
    
    for id, cupos in materias: # 3
        lista_estudiantes = list()
        materia = Materia(id, cupos, lista_estudiantes)
        for estudiante in estudiantes: # 5
            if encontrarMateria(estudiante, id):
                materia.estudiantes.append(estudiante)
        ObjectMaterias.append(materia)
    
def combinacionesEstudiantesByMateria(materia) -> list:
    """
    Genera todas las combinaciones posibles de los estudiantes aspirantes a una materia,
    pero solo retorna aquellas combinaciones cuya cantidad de estudiantes no supera el número de cupos disponibles.
    """
    lista = []
    for r in range(1, len(materia.estudiantes) + 1):
        for combinacion in combinations(materia.estudiantes, r):
            if len(combinacion) <= materia.cupos:
                nueva_materia = Materia(materia.id, materia.cupos, list(combinacion))
                lista.append(nueva_materia)
    return lista

def calcularGamma(num_materias_solicitadas: int) -> int:
    """
    Cantidad maxima de prioridad que pueden 
    tener en conjunto el total de materias 
    de un estudiante

    Args
    - num_materias_solicitadas (int): cantidad de materias que quiere matricular un estudiante

    Return
    - cantidad maxima de prioridad que puede usar un estudiante (int)
    """
    return 3 * num_materias_solicitadas - 1

def sumatoriaPrioridades(estudiante: list) -> int:
    """Suma las prioridades de las materias de un estudiante"""
    return sum(prioridad for _, prioridad in estudiante[1])

def sumatoriaPrioridadesMateriasNoMatriculadasPorUnEstudiante(ma: list[Materia], ms: list[tuple]) -> int:
    """
    Suma las prioridades de las materias 
    que el estudiante no pudo matricular

    Args
    - ma (list): lista de materias que pudo matricular el estudiante
    - ms (list): lista de materias que queria matricular el estudiante

    Return
    - valor de la sumatoria de las prioridades (int)
    """
    total = 0
    ids_matriculadas = {materia.id for materia in ma}
    
    for codigo, prioridad in ms:
        if codigo not in ids_matriculadas:
            total += prioridad    
    return total

def medirInsatisfaccionEstudiante(ma: list[Materia], ms: list[tuple]) -> float:
    """
    Mide la insatisfaccion de un estudiante

    Args
    - ma (list): lista de materias que pudo matricular el estudiante
    - ms (list): lista de materias que queria matricular el estudiante

    Return
    - (float) valor de la insatisfacción del estudiante
    """
    primer_operando: float = 1 - (len(ma)/len(ms))
    segundo_operando: float = sumatoriaPrioridadesMateriasNoMatriculadasPorUnEstudiante(ma, ms) / calcularGamma(len(ms))

    #print("Primer operando: ", 1, " - ", (len(ma)/len(ms)), " = ", primer_operando)
    #print("Segundo operando: ", sumatoriaPrioridadesMateriasNoMatriculadasPorUnEstudiante(ma, ms), " / ", calcularGamma(len(ms)), " = ", segundo_operando)
    #print("Insatisfacción del estudiante: ", primer_operando, " * ", segundo_operando, " = ", primer_operando * segundo_operando)
    return primer_operando * segundo_operando

def obtenerMateriasMatriculadas(estudiante: list, materias: list[Materia]) -> list[Materia]:
    """
    Obtiene de la combinacion las materias que 
    pudo matricular un estudiante

    Args
    - estudiante (list): estudiante a verificar
    - materias (list): lista de materias con sus cupos y estudiantes matriculados de la combinacion

    Return
    - lista de materias que pudo matricular el estudiante (list)
    """
    lista = list()
    for materia in materias:
        if estudiante in materia.estudiantes:
            lista.append(materia)
    
    #print("-----")
    #print("Materias matriculadas por el estudiante ", estudiante[0], " en la combinacion: ")
    #print(lista)
    #print(f"Materias que quiere matricular el estudiante: {estudiante[1]}")
    return lista

def medirInsatisfaccionGeneral(materias: list[Materia], estudiantes: list[list]) -> float:
    """
    Mide la insatisfaccion general de todos los estudiantes
    
    Args
    - materias (list): lista de materias con sus cupos
    - estudiantes (list): lista de todos los estudiantes
    
    Return
    - (float) valor de la insatisfacción general
    """
    total: int = 0
    for estudiante in estudiantes:
        ma = obtenerMateriasMatriculadas(estudiante, materias)
        ms: list[tuple] = estudiante[1]
        total += medirInsatisfaccionEstudiante(ma, ms)

    #print("Insatisfacción general: ", total/len(estudiantes))
    return total/len(estudiantes)

def encontrarSolucion(listaCombinacionesMateriasAceptadas: list[list[Materia]], estudiantes: list[list]) -> tuple:
    """
    Encuentra la mejor combinación de estudiantes para todas las materias
    que minimiza la insatisfacción general.

    Args
    - listaCombinacionesMateriasAceptadas: lista de listas de combinaciones por materia
    - estudiantes: lista de todos los estudiantes

    Returns
    - mejor_combinacion: lista con la mejor combinación de materias
    - menor_insatisfaccion: valor mínimo de insatisfacción general
    """

    mejor_combinacion = None 
    menor_insatisfaccion = 1.0

    # Generar todas las combinaciones posibles: una por materia
    for combinacion in product(*listaCombinacionesMateriasAceptadas):
        # combinacion es una tupla con una opción por materia

        # Calcular insatisfacción general para esta combinación
        #print("\n--- Nueva Combinación ---")
        #print(len(combinacion))
        #print(combinacion)
        #print("\n\n")
        insatisfaccion = medirInsatisfaccionGeneral(list(combinacion), estudiantes)

        # Verificar si es la mejor hasta ahora
        if insatisfaccion < menor_insatisfaccion:
            menor_insatisfaccion = insatisfaccion
            mejor_combinacion = combinacion

    #print("\n\n------")
    #print(f"Mejor combinación: {mejor_combinacion}, \nInsatisfacción: {menor_insatisfaccion}")
    return mejor_combinacion, menor_insatisfaccion

def rocFB(materias: list[Materia], estudiantes: list) -> tuple:
    """
    Función principal que resuelve el problema de optimización
    de asignación de estudiantes a materias.
    
    Args
    - materias (list): lista de materias con sus cupos
    - estudiantes (list): lista de estudiantes con las materias que quieren ver
    
    Return
    - mejor_combinacion (list): lista con la mejor combinación de materias
    - menor_insatisfaccion (float): valor mínimo de insatisfacción general
    """

    # se añade a la lista "ObjectMaterias" objetos creados de las materias, 
    # cada objeto tiene una copia de los estudiantes que quieren ver la materia
    getEstudiantesByMateria(estudiantes, materias)

    ListaDeListaDeSoluciones = list()

    # para cada materia, se generan todas las combinaciones posibles de estudiantes
    for materia in ObjectMaterias:
        # todas las combinaciones que cumplen el criterio de cupos de una materia
        lista = combinacionesEstudiantesByMateria(materia)
        ListaDeListaDeSoluciones.append(lista)

    asignaciones = {e_id: [] for e_id, _ in estudiantes}
    mejor_combinacion, menor_insatisfaccion = encontrarSolucion(ListaDeListaDeSoluciones, estudiantes)
    
    # Llenar el diccionario de asignaciones por estudiante
    for materia in mejor_combinacion:
        for estudiante in materia.estudiantes:
            asignaciones[estudiante[0]].append(materia.id)

    # # se encuentra la mejor combinacion de estudiantes para todas las materias
    return asignaciones, menor_insatisfaccion

# Archivo de texto
materias = [
            ("M1", 3), 
            ("M2", 4), 
            ("M3", 2)
            ]
ms = [
        [("M1", 5), ("M2", 2), ("M3", 1)],
        [("M1", 4), ("M2", 1), ("M3", 3)],
        [("M1", 3), ("M2", 2)],
        [("M1", 2), ("M2", 3)],
        [("M1", 3), ("M2", 2), ("M3", 3)]
      ]
estudiantes = [
                ("e1", ms[0]), 
                ("e2", ms[1]), 
                ("e3", ms[2]), 
                ("e4", ms[3]), 
                ("e5", ms[4])
             ]

# Almacena las materias con todos los estudiantes que la quieren ver.
ObjectMaterias = []

if __name__ == "__main__":
    start_time = time.time()
    mejor_combinacion, menor_insatisfaccion = rocFB(materias, estudiantes)
    end_time = time.time()
    print(f"\nTiempo de ejecución: {end_time - start_time} segundos")
    print(f"Mejor combinación: {mejor_combinacion}, \nInsatisfacción: {menor_insatisfaccion}")
