---
## Descripción de los Archivos del Proyecto

### El proyecto está compuesto por los siguientes archivos y carpetas:

main_ui.py: Contiene la interfaz gráfica del programa desarrollada con Tkinter. Desde este archivo se ejecuta la aplicación principal, permitiendo seleccionar el archivo de entrada y el algoritmo a utilizar (Fuerza Bruta, Voraz o Programación Dinámica).

solucion_fb.py: Implementa el algoritmo de fuerza bruta. Este método evalúa todas las combinaciones posibles para encontrar la solución óptima, aunque presenta un alto costo computacional y es viable solo para instancias pequeñas.

solucion_voraz.py: Contiene el algoritmo voraz, que toma decisiones locales rápidas priorizando las opciones de menor costo en cada paso. No garantiza siempre la solución óptima, pero logra tiempos de ejecución muy reducidos.

solucion_dinamica.py: Implementa la programación dinámica, aprovechando la subestructura óptima y el solapamiento de subproblemas para reducir el espacio de búsqueda y obtener soluciones óptimas o casi óptimas en un tiempo razonable.

utils.py: Incluye funciones auxiliares para la lectura y escritura de archivos de texto, procesamiento de datos de entrada y salida, y otras utilidades comunes a los tres algoritmos.

Pruebas/: Carpeta que contiene los archivos de entrada (.txt) utilizados para probar el funcionamiento de los algoritmos en distintos escenarios.

Salidas/: Carpeta donde se guardan los resultados generados por cada algoritmo, incluyendo las asignaciones y los niveles de insatisfacción obtenidos.

## ⚙️ ¿Cómo Ejecutar la Aplicación?

Para ejecutar el programa, sigue estos sencillos pasos.

### Prerrequisitos del Sistema

Antes de instalar y ejecutar el proyecto, asegúrate de tener las siguientes dependencias del sistema:

-   **Python 3.x**
-   **Tcl/Tk:** Esta librería es necesaria para la interfaz gráfica.
    -   En **macOS**, puedes instalarla usando Homebrew:
        ```bash
        brew install tcl-tk
        ```
    -   En distribuciones de Linux basadas en Debian (como Ubuntu), puedes instalarla con:
        ```bash
        sudo apt-get install python3-tk
        ```

### Ejecución

1.  **Clona o descarga** este repositorio en tu máquina local.

2.  **Abre una terminal** o línea de comandos y navega hasta la carpeta raíz del proyecto.

3.  **Ejecuta la interfaz de usuario** con el siguiente comando:
    ```bash
    python main_ui.py
    ```


---

## 📋 Formato de Archivos

### Archivo de Entrada

El archivo de entrada debe ser un `.txt` con la siguiente estructura:
1.  Número de materias (`k`).
2.  `k` líneas con `codigo_materia,cupo`.
3.  Número de estudiantes (`r`).
4.  `r` bloques, donde cada bloque consiste en:
    -   Una línea con `codigo_estudiante,num_solicitudes`.
    -   `num_solicitudes` líneas con `codigo_materia,prioridad`.

### Archivo de Salida

La aplicación generará un archivo `.txt` con la solución:
1.  La primera línea contiene el costo total de la solución (insatisfacción general).
2.  Luego, `r` bloques por cada estudiante, con la siguiente estructura:
    -   Una línea con `codigo_estudiante,num_materias_asignadas`.
    -   `num_materias_asignadas` líneas, cada una con el código de una materia asignada.
