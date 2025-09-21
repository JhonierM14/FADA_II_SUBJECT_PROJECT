---

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