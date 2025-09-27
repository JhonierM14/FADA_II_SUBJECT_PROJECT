from tkinter import filedialog
import sys


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
            print(materias, estudiantes)
        return materias, estudiantes
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'")
        return None, None
    except (ValueError, IndexError) as e:
        print(f"Error: El archivo de entrada no tiene el formato correcto. Detalles: {e}")
        return None, None

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
