import customtkinter as ctk
from estructuras import ListaEnlazada, Pila, Tarea # Importa tus clases manuales

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- Configuración de la Ventana (omito para brevedad) ---
        self.title("Gestor de Tareas Pendientes")
        self.geometry("800x600")
        
        # --- 1. Inicializar las Estructuras de Datos ---
        self.lista_tareas = ListaEnlazada() # Almacena todas las tareas (Lista Enlazada)
        self.pila_undo = Pila()             # Almacena tareas eliminadas para "Deshacer" (Pila)
        
        # --- 2. Crear la Interfaz ---
        self.crear_layout()
        
    def crear_layout(self):
        # Configuración de frames y grid (usa el código que te proporcioné antes)
        
        # --- 3. Conectar la Entrada de Datos (Ejemplo de función) ---
        
        # Widgets para la entrada de datos (usando el sidebar_frame)
        self.title_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Título de la Tarea")
        self.title_entry.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")

        self.add_button = ctk.CTkButton(self.sidebar_frame, text="Agregar Tarea", command=self.agregar_tarea)
        self.add_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Widget para la función Deshacer
        self.undo_button = ctk.CTkButton(self.sidebar_frame, text="Deshacer (Undo)", command=self.deshacer_accion)
        self.undo_button.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="ew")
        
        # Mostrar la lista inicial de tareas
        self.actualizar_vista_tareas()
        
    # --- 4. Métodos que Usan las Estructuras de Datos ---
    
    def agregar_tarea(self):
        """Llama al método de Inserción de la Lista Enlazada."""
        titulo = self.title_entry.get()
        if titulo:
            # Crea un objeto Tarea con los datos de la interfaz
            nueva_tarea = Tarea(titulo=titulo, descripcion="Descripción pendiente")
            
            # Llama a la operación de Inserción de la estructura manual
            self.lista_tareas.insertar_al_final(nueva_tarea)
            
            # Limpiar la entrada y actualizar la interfaz
            self.title_entry.delete(0, 'end')
            self.actualizar_vista_tareas()
        
    def deshacer_accion(self):
        """Llama al método Pop de la Pila y Push en la Lista Enlazada (revertir eliminación)."""
        # Llama a la operación de Eliminación de la Pila
        tarea_revertida = self.pila_undo.pop() 
        
        if tarea_revertida:
            # Reinserta la tarea de vuelta a la Lista Enlazada
            self.lista_tareas.insertar_al_final(tarea_revertida)
            self.actualizar_vista_tareas()
        else:
            print("No hay acciones para deshacer.") # Se puede mostrar un mensaje en la GUI
            
    def eliminar_tarea_gui(self, titulo):
        """Llama al método de Eliminación de la Lista Enlazada y usa la Pila."""
        # Llama a la operación de Eliminación de la estructura manual
        tarea_eliminada = self.lista_tareas.eliminar_por_titulo(titulo)
        
        if tarea_eliminada:
            # Guarda la tarea eliminada en la Pila para poder deshacer la acción (Push)
            self.pila_undo.push(tarea_eliminada)
            self.actualizar_vista_tareas()
            
    def actualizar_vista_tareas(self):
        """Llama al método de Recorrido de la Lista Enlazada y actualiza la GUI."""
        
        # Eliminar cualquier vista anterior del frame principal para dibujar la nueva lista
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Llama a la operación de Recorrido de la estructura manual
        tareas = self.lista_tareas.recorrer()
        
        if not tareas:
            ctk.CTkLabel(self.main_frame, text="No hay tareas pendientes. ¡Añade una!").pack(padx=20, pady=20)
            return

        # Dibuja cada tarea en la GUI
        for i, tarea in enumerate(tareas):
            # Usar un Frame para cada fila de tarea para agrupar Label y Botón
            tarea_frame = ctk.CTkFrame(self.main_frame, corner_radius=5)
            tarea_frame.pack(fill="x", padx=10, pady=5)

            # Etiqueta para el título de la tarea (Recorrido/Visualización)
            tarea_label = ctk.CTkLabel(tarea_frame, text=str(tarea), anchor="w")
            tarea_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            # Botón de eliminación
            # Se usa una función lambda para pasar argumentos al comando (eliminación)
            delete_button = ctk.CTkButton(
                tarea_frame, 
                text="❌", 
                width=30, 
                command=lambda t=tarea.titulo: self.eliminar_tarea_gui(t)
            )
            delete_button.pack(side="right", padx=5, pady=5)
        
# Inicia la aplicación (debe ir al final del archivo)
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark") # Diseño moderno!
    app = App()
    app.mainloop()