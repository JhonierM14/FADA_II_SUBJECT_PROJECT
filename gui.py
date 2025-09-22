import tkinter as tk
from tkinter import filedialog, messagebox, font

from utils import leer_entrada, escribir_salida
from solucion_voraz import rocV
# from solucion_fb import rocFB
# from solucion_pd import rocPD

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto ADA II - Repartición Óptima de Cupos")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # Colores y fuentes
        self.color_bg = "#2E2E2E"
        self.color_fg_purple = "#D0B0FF"
        self.color_btn = "#3E3E3E"
        self.color_primary = "#4CAF50"
        self.font_title = font.Font(family="Helvetica", size=20, weight="bold")
        self.font_label = font.Font(family="Helvetica", size=11)
        self.font_button = font.Font(family="Helvetica", size=10, weight="bold")

        # Configurar fondo
        self.root.configure(bg=self.color_bg)

        # Cargar los elementos de la interfaz
        self.cargar_componentes()

    def cargar_componentes(self):
        """Agrega los elementos visuales (labels y botones) a la interfaz."""
        tk.Label(
            self.root,
            text="Repartición Óptima de Cupos",
            font=self.font_title,
            bg=self.color_bg,
            fg=self.color_fg_purple
        ).pack(pady=(30, 10))

        tk.Label(
            self.root,
            text="Seleccione el algoritmo para resolver el problema:",
            font=self.font_label,
            bg=self.color_bg,
            fg=self.color_fg_purple
        ).pack(pady=10)

        frame_botones = tk.Frame(self.root, bg=self.color_bg)
        frame_botones.pack(pady=20, padx=20, fill='x')

        # Botones de algoritmos
        self.crear_boton_algoritmo(frame_botones, "Solución Voraz", self.ejecutar_voraz, self.color_primary, "white")
        self.crear_boton_algoritmo(frame_botones, "Fuerza Bruta", self.ejecutar_fuerza_bruta, self.color_btn, self.color_fg_purple)
        self.crear_boton_algoritmo(frame_botones, "Programación Dinámica", self.ejecutar_dinamica, self.color_btn, self.color_fg_purple)

    def crear_boton_algoritmo(self, padre, texto, accion, color_bg, color_fg):
        """Crea un botón estilizado y lo agrega al frame de botones."""
        tk.Button(
            padre,
            text=texto,
            command=accion,
            font=self.font_button,
            bg=color_bg,
            fg=color_fg,
            relief=tk.FLAT,
            pady=10
        ).pack(fill='x', pady=5)

    def ejecutar_algoritmo(self, nombre_algoritmo, funcion_algoritmo, nombre_salida):
        """Lógica común para ejecutar un algoritmo: leer entrada, aplicar, guardar salida."""
        ruta_entrada = filedialog.askopenfilename(
            title="Seleccione el archivo de entrada",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if not ruta_entrada:
            return

        materias, estudiantes = leer_entrada(ruta_entrada)
        if materias is None or estudiantes is None:
            messagebox.showerror("Error de Lectura", "No se pudieron leer los datos del archivo.")
            return

        messagebox.showinfo("Procesando", f"Ejecutando el algoritmo {nombre_algoritmo}. Por favor, espere.")
        asignaciones, costo = funcion_algoritmo(materias, estudiantes)

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar archivo de salida",
            defaultextension=".txt",
            initialfile=f"salida_{nombre_salida}.txt",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if not ruta_salida:
            return

        escribir_salida(ruta_salida, asignaciones, costo)
        messagebox.showinfo("Éxito", f"Solución guardada en '{ruta_salida}'")

    def ejecutar_voraz(self):
        self.ejecutar_algoritmo("voraz", rocV, "voraz")

    def ejecutar_fuerza_bruta(self):
        messagebox.showinfo("Info", "Fuerza bruta aún no implementada.")
        # self.ejecutar_algoritmo("fuerza bruta", rocFB, "fuerza_bruta")

    def ejecutar_dinamica(self):
        messagebox.showinfo("Info", "Programación dinámica aún no implementada.")
        # self.ejecutar_algoritmo("programación dinámica", rocPD, "dinamica")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
