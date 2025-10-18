import tkinter as tk
from tkinter import filedialog, messagebox, font

from solucion_voraz import rocV
from solucion_fb import rocFB
from solucion_dinamica import rocPD
from utils import leer_entrada, escribir_salida
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto ADA II - Repartición Óptima de Cupos")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.color_bg = "#2E2E2E"
        self.color_fg_purple = "#D0B0FF" 
        self.color_btn = "#3E3E3E"
        self.color_primary = "#4CAF50"
        self.font_title = font.Font(family="Helvetica", size=20, weight="bold")
        self.font_label = font.Font(family="Helvetica", size=11)
        self.font_button = font.Font(family="Helvetica", size=10, weight="bold")
        
        self.root.configure(bg=self.color_bg)

        lbl_title = tk.Label(root, text="Repartición Óptima de Cupos", 
                             font=self.font_title, bg=self.color_bg, fg=self.color_fg_purple)
        lbl_title.pack(pady=(30, 10))

        lbl_instructions = tk.Label(root, text="Seleccione el algoritmo para resolver el problema:", 
                                     font=self.font_label, bg=self.color_bg, fg=self.color_fg_purple)
        lbl_instructions.pack(pady=10)
        
        btn_frame = tk.Frame(root, bg=self.color_bg)
        btn_frame.pack(pady=20, padx=20, fill='x')

        btn_voraz = tk.Button(btn_frame, text="Solución Voraz", 
                              command=self.ejecutar_voraz, 
                              font=self.font_button, bg=self.color_primary, fg="white", 
                              relief=tk.FLAT, pady=10)
        btn_voraz.pack(fill='x', pady=5)

        btn_fb = tk.Button(btn_frame, text="Fuerza Bruta", 
                           command=self.ejecutar_fuerza_bruta, 
                           font=self.font_button, bg=self.color_btn, fg=self.color_fg_purple, 
                           relief=tk.FLAT, pady=10)
        btn_fb.pack(fill='x', pady=5)

        btn_pd = tk.Button(btn_frame, text="Programación Dinámica", 
                           command=self.ejecutar_dinamica, 
                           font=self.font_button, bg=self.color_btn, fg=self.color_fg_purple, 
                           relief=tk.FLAT, pady=10)
        btn_pd.pack(fill='x', pady=5)

    def ejecutar_voraz(self):
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
            
        messagebox.showinfo("Procesando", "Ejecutando el algoritmo voraz. Por favor, espere.")

        start: float = time.perf_counter()
        asignaciones, costo = rocV(materias, estudiantes)
        end: float = time.perf_counter()

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar archivo de salida",
            defaultextension=".txt",
            initialfile="salida_voraz.txt",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if not ruta_salida:
            return

        escribir_salida(ruta_salida, asignaciones, costo)
    
        print(f"V, Tiempo de ejecucion: {end - start}, insatisfaccion {costo}")
        messagebox.showinfo("Éxito", f"Solución guardada en '{ruta_salida}'")

    def ejecutar_fuerza_bruta(self):
        ruta_entrada = filedialog.askopenfilename(
            title="Seleccione el archivo de entrada",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if not ruta_entrada:
            return

        materias, estudiantes = leer_entrada(ruta_entrada)

        # Convertir materias_dict a lista de tuplas
        materias = [(id_materia, cupos) for id_materia, cupos in materias.items()]
        # Convertir estudiantes_dict a lista de tuplas
        estudiantes = [(id_estudiante, datos['solicitudes']) for id_estudiante, datos in estudiantes.items()]

        if materias is None or estudiantes is None:
            messagebox.showerror("Error de Lectura", "No se pudieron leer los datos del archivo.")
            return
            
        messagebox.showinfo("Procesando", "Ejecutando el algoritmo de fuerza bruta. Por favor, espere.")

        start: float = time.perf_counter()
        asignaciones, costo = rocFB(materias, estudiantes)
        end: float = time.perf_counter()

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar archivo de salida",
            defaultextension=".txt",
            initialfile="salida_fuerza_bruta.txt",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if not ruta_salida:
            return
        
        escribir_salida(ruta_salida, asignaciones, costo)

        print(f"FB, Tiempo de ejecucion: {end - start}, insatisfaccion {costo}")
        messagebox.showinfo("Éxito", f"Solución guardada en '{ruta_salida}'")


    def ejecutar_dinamica(self):
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
        messagebox.showinfo("Procesando", "Ejecutando el algoritmo dinamico. Por favor, espere.")

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar archivo de salida",
            defaultextension=".txt",
            initialfile="salida_dinamica.txt",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if not ruta_salida:
            return

        start: float = time.perf_counter()
        asignaciones, costo = rocPD(materias, estudiantes)
        end: float = time.perf_counter()

        escribir_salida(ruta_salida, asignaciones, costo)
        print(f"PD, Tiempo de ejecucion: {end - start}, insatisfaccion {costo}")
        messagebox.showinfo("Éxito", f"Solución guardada en '{ruta_salida}'")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()