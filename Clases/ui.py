import customtkinter as ctk
import tkinter as tk # También importamos tkinter nativo para posibles animaciones o widgets básicos

# 1. Configuración de apariencia
ctk.set_appearance_mode("System")  # Puede ser "System", "Dark", o "Light"
ctk.set_default_color_theme("blue") # Elige un tema de color

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la Ventana Principal
        self.title("Gestor de Tareas Pendientes")
        self.geometry("800x600")
        
        # Opcional: Configurar la cuadrícula (grid) principal para la responsividad
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Inicializa las estructuras de datos
        # Esto lo harías después de crearlas en 'estructuras.py'
        # self.lista_tareas = ListaEnlazada()
        # self.pila_undo = Pila()
        
        # Llamar al método para construir la interfaz
        self.crear_layout()

    def crear_layout(self):
        # Aquí definiremos los Frames (paneles) y Widgets
        
        # Ejemplo de Frame lateral para la entrada de datos (Columna 0)
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Ejemplo de Frame principal para mostrar la lista de tareas (Columna 1)
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        # Asegúrate de que este frame también sea configurable
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # --- Agregar Widgets a los Frames aquí ---
        
# Inicia la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()