import customtkinter as ctk
import tkinter as tk
from estructuras import ListaEnlazada, Pila, Tarea 

# 1. Configuración de apariencia de CustomTkinter
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
   
    def __init__(self):
        super().__init__()
      
        
        # --- Inicializar Estructuras de Datos Manuales ---
        self.lista_tareas = ListaEnlazada()      # Tareas Pendientes
        self.lista_completadas = ListaEnlazada() # NUEVA: Tareas Completadas
        self.pila_undo = Pila()                  # Historial de eliminaciones
        
        self.crear_layout()
        # --- Configuración de la Ventana Principal ---
        self.title("Gestor de Tareas Pendientes (Estructuras de Datos)")
        self.geometry("800x600")
        
        # Configurar la cuadrícula principal para que la columna 1 (Main Frame) se expanda
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Inicializar Estructuras de Datos Manuales ---
        self.lista_tareas = ListaEnlazada() # Almacena todas las tareas (Lista Enlazada)
        self.pila_undo = Pila()             # Almacena tareas eliminadas para "Deshacer" (Pila)
        
        # --- Construir la Interfaz Gráfica ---
        self.crear_layout()
        
    def crear_layout(self):
        """
        Define y posiciona todos los Frames y Widgets. 
        Este método garantiza que los contenedores se creen primero.
        """
        
        # ----------------------------------------------------
        # A. FRAME LATERAL (SIDEBAR) - Entrada de Datos
        # ----------------------------------------------------
        # ESTE ES EL PRIMER FRAME CREADO: self.sidebar_frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="NUEVA TAREA", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))

        # Widget de Entrada (Título)
        self.title_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Título de la Tarea")
        self.title_entry.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")

        # Botón para Agregar (llama al método de Inserción de la Lista Enlazada)
        self.add_button = ctk.CTkButton(self.sidebar_frame, text="➕ AGREGAR", command=self.agregar_tarea)
        self.add_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Botón para Deshacer (llama al método Pop de la Pila)
        self.undo_button = ctk.CTkButton(self.sidebar_frame, text="↩️ DESHACER", command=self.deshacer_accion, fg_color="#3B5998")
        self.undo_button.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="ew")
        
        # ----------------------------------------------------
        # B. FRAME PRINCIPAL (MAIN) - Visualización de Tareas
        # ----------------------------------------------------
        # Usamos un ScrollableFrame para la lista de tareas
        self.main_scroll_frame = ctk.CTkScrollableFrame(self, label_text="Tareas Pendientes", corner_radius=0)
        self.main_scroll_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_scroll_frame.grid_columnconfigure(0, weight=1)

        # Inicializa la vista de tareas
        self.actualizar_vista_tareas()

    # ----------------------------------------------------
    # --- MÉTODOS DE LÓGICA (Conexión con Estructuras) ---
    # ----------------------------------------------------
    
    def agregar_tarea(self):
        """
        Función de Inserción. Obtiene datos de la GUI y llama a: 
        ListaEnlazada.insertar_al_final().
        """
        titulo = self.title_entry.get().strip()
        if titulo:
            # Creamos el objeto Tarea
            nueva_tarea = Tarea(titulo=titulo, descripcion="Pendiente")
            
            # 1. OPERACIÓN DE INSERCIÓN MANUAL
            self.lista_tareas.insertar_al_final(nueva_tarea)
            
            # Limpiar la entrada y actualizar la interfaz
            self.title_entry.delete(0, 'end')
            self.actualizar_vista_tareas()
        
    def deshacer_accion(self):
        """
        Función Deshacer. Llama a: Pila.pop() y luego ListaEnlazada.insertar_al_final().
        """
        # 1. OPERACIÓN POP DE LA PILA
        tarea_revertida = self.pila_undo.pop() 
        
        if tarea_revertida:
            # 2. OPERACIÓN DE INSERCIÓN MANUAL (Revertir)
            self.lista_tareas.insertar_al_final(tarea_revertida)
            self.actualizar_vista_tareas()
        else:
            print("No hay acciones para deshacer.") # Podrías mostrar un mensaje de error en la GUI
            
    def eliminar_tarea_gui(self, titulo):
        """
        Función de Eliminación. Llama a: ListaEnlazada.eliminar_por_titulo() 
        y luego Pila.push().
        """
        # 1. OPERACIÓN DE ELIMINACIÓN MANUAL
        tarea_eliminada = self.lista_tareas.eliminar_por_titulo(titulo)
        
        if tarea_eliminada:
            # 2. OPERACIÓN PUSH DE LA PILA (Guardar para Undo)
            self.pila_undo.push(tarea_eliminada)
            self.actualizar_vista_tareas()
            
    def actualizar_vista_tareas(self):
        """
        Función de Recorrido/Visualización. Llama a: ListaEnlazada.recorrer() 
        y actualiza dinámicamente el ScrollableFrame.
        """
        
        # 1. Limpiar la vista anterior
        for widget in self.main_scroll_frame.winfo_children():
            widget.destroy()

        # 2. OPERACIÓN DE RECORRIDO MANUAL
        tareas = self.lista_tareas.recorrer()
        
        if not tareas:
            ctk.CTkLabel(self.main_scroll_frame, text="¡Todo listo! No hay tareas pendientes.").pack(padx=20, pady=20)
            return

        # 3. Dibuja cada tarea como un elemento dinámico
        for i, tarea in enumerate(tareas):
            # Frame para cada fila de tarea para agrupar Label y Botones
            tarea_frame = ctk.CTkFrame(self.main_scroll_frame, corner_radius=5)
            tarea_frame.pack(fill="x", padx=10, pady=5)

            # Etiqueta para el título de la tarea (Visualización)
            tarea_label = ctk.CTkLabel(tarea_frame, text=str(tarea), anchor="w")
            tarea_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            # Botón de eliminación
            delete_button = ctk.CTkButton(
                tarea_frame, 
                text="❌", 
                width=30, 
                command=lambda t=tarea.titulo: self.eliminar_tarea_gui(t)
            )
            delete_button.pack(side="right", padx=5, pady=5)
            
            # Botón de Búsqueda (ejemplo conceptual, puedes expandirlo)
            search_button = ctk.CTkButton(
                tarea_frame, 
                text="🔍", 
                width=30, 
                command=lambda t=tarea.titulo: print(f"Buscando: {self.lista_tareas.buscar_por_titulo(t)}") # Llama a la Búsqueda
            )
            search_button.pack(side="right", padx=5, pady=5)
        
# Inicia la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()