# main.py

import customtkinter as ctk
import tkinter as tk
# Importamos las clases de las estructuras de datos manuales
from estructuras import ListaEnlazada, Pila, Tarea 

# Configuración de apariencia de CustomTkinter
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la Ventana Principal
        self.title("Gestor de Tareas Pendientes Ordenadas por Prioridad")
        self.geometry("800x600")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Inicializar Estructuras de Datos Manuales ---
        self.lista_tareas = ListaEnlazada()
        self.pila_undo = Pila()
        
        self.crear_layout()
        
    def crear_layout(self):
        """Define y posiciona todos los Frames y Widgets."""
        
        # A. FRAME LATERAL (SIDEBAR) - Entrada de Datos
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        # Aseguramos que haya espacio debajo de los widgets
        self.sidebar_frame.grid_rowconfigure(6, weight=1) 

        ctk.CTkLabel(self.sidebar_frame, text="NUEVA TAREA", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))

        # Widget de Entrada (Título)
        self.title_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Título de la Tarea")
        self.title_entry.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")

        # Etiqueta y ComboBox para la Prioridad
        ctk.CTkLabel(self.sidebar_frame, text="Prioridad:").grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.prioridades = ["Alta", "Media", "Baja"] 
        self.priority_combobox = ctk.CTkComboBox(
            self.sidebar_frame, 
            values=self.prioridades
        )
        self.priority_combobox.set("Media") # Valor por defecto
        self.priority_combobox.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Botón AGREGAR (Llama a la operación de Inserción Ordenada)
        self.add_button = ctk.CTkButton(self.sidebar_frame, text="➕ AGREGAR", command=self.agregar_tarea)
        self.add_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Botón DESHACER (Llama a la operación Pop de la Pila)
        self.undo_button = ctk.CTkButton(self.sidebar_frame, text="↩️ DESHACER", command=self.deshacer_accion, fg_color="#3B5998")
        self.undo_button.grid(row=5, column=0, padx=20, pady=(10, 5), sticky="ew")
        
        # B. FRAME PRINCIPAL (MAIN) - Visualización de Tareas
        self.main_scroll_frame = ctk.CTkScrollableFrame(self, label_text="Lista de Tareas", corner_radius=0)
        self.main_scroll_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_scroll_frame.grid_columnconfigure(0, weight=1)

        self.actualizar_vista_tareas()
        
    # --- MÉTODOS DE LÓGICA (Conexión con Estructuras) ---
    
    def agregar_tarea(self):
        """Función de Inserción: Llama a ListaEnlazada.insertar_ordenado()."""
        titulo = self.title_entry.get().strip()
        prioridad_seleccionada = self.priority_combobox.get()
        
        if titulo:
            nueva_tarea = Tarea(
                titulo=titulo, 
                descripcion="Pendiente",
                prioridad=prioridad_seleccionada
            )
            # LLAMADA AL MÉTODO DE INSERCIÓN ORDENADA
            self.lista_tareas.insertar_ordenado(nueva_tarea)
            self.title_entry.delete(0, 'end')
            self.actualizar_vista_tareas()
        
    def deshacer_accion(self):
        """Función Deshacer: Llama a Pila.pop() y luego ListaEnlazada.insertar_ordenado()."""
        # LLAMADA A LA OPERACIÓN POP DE LA PILA
        tarea_revertida = self.pila_undo.pop() 
        
        if tarea_revertida:
            # LLAMADA A LA OPERACIÓN DE INSERCIÓN ORDENADA
            self.lista_tareas.insertar_ordenado(tarea_revertida)
            self.actualizar_vista_tareas()
        else:
            # Notificación simple
            dialog = ctk.CTkMessagebox(title="Información", message="No hay acciones para deshacer.", icon="info")
            dialog.get()
            
    def eliminar_tarea_gui(self, titulo):
        """Función de Eliminación: Llama a ListaEnlazada.eliminar_por_titulo() y Pila.push()."""
        # LLAMADA A LA OPERACIÓN DE ELIMINACIÓN
        tarea_eliminada = self.lista_tareas.eliminar_por_titulo(titulo)
        
        if tarea_eliminada:
            # LLAMADA A LA OPERACIÓN PUSH DE LA PILA
            self.pila_undo.push(tarea_eliminada)
            self.actualizar_vista_tareas()
            
    def toggle_estado_tarea(self, titulo):
        """Busca la tarea por título y alterna su estado 'completada'."""
        # LLAMADA A LA OPERACIÓN DE BÚSQUEDA
        tarea = self.lista_tareas.buscar_por_titulo(titulo)
        
        if tarea:
            tarea.completada = not tarea.completada
            self.actualizar_vista_tareas()

    def actualizar_vista_tareas(self):
        """
        Función de Recorrido/Visualización. Dibuja los widgets.
        """
        
        for widget in self.main_scroll_frame.winfo_children():
            widget.destroy()

        # LLAMADA A LA OPERACIÓN DE RECORRIDO MANUAL
        tareas = self.lista_tareas.recorrer()
        
        if not tareas:
            ctk.CTkLabel(self.main_scroll_frame, text="¡Todo listo! No hay tareas pendientes.").pack(padx=20, pady=20)
            return

        for i, tarea in enumerate(tareas):
            
            # Lógica de Estilo para simular 'transparencia' y tachado
            if tarea.completada:
                text_color = "gray" 
                # overstrike=1 simula tachado
                font_style = ctk.CTkFont(size=14, weight="normal", overstrike=1) 
            else:
                # Color de texto fijo y normal
                text_color = "#DCE4EE" 
                font_style = ctk.CTkFont(size=14, weight="normal")

            tarea_frame = ctk.CTkFrame(self.main_scroll_frame, corner_radius=5)
            tarea_frame.pack(fill="x", padx=10, pady=5)
            
            # CheckBox (Conexión a toggle_estado_tarea)
            check_box = ctk.CTkCheckBox(
                tarea_frame,
                text=str(tarea),
                command=lambda t=tarea.titulo: self.toggle_estado_tarea(t),
                variable=tk.BooleanVar(value=tarea.completada), 
                onvalue=True, 
                offvalue=False,
                text_color=text_color, 
                font=font_style,
                checkbox_height=20, 
                checkbox_width=20
            )
            check_box.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            # Botón de Eliminación (Operación de Eliminación)
            delete_button = ctk.CTkButton(
                tarea_frame, 
                text="❌", 
                width=30, 
                command=lambda t=tarea.titulo: self.eliminar_tarea_gui(t)
            )
            delete_button.pack(side="right", padx=5, pady=5)
            
            # Botón de Búsqueda (Operación de Búsqueda)
            search_button = ctk.CTkButton(
                tarea_frame, 
                text="🔍", 
                width=30, 
                command=lambda t=tarea.titulo: self.mostrar_busqueda(t) 
            )
            search_button.pack(side="right", padx=5, pady=5)

    def mostrar_busqueda(self, titulo_buscado):
        """Muestra el resultado de la Búsqueda en una ventana de diálogo simple."""
        # LLAMADA A LA OPERACIÓN DE BÚSQUEDA
        tarea_encontrada = self.lista_tareas.buscar_por_titulo(titulo_buscado)
        
        if tarea_encontrada:
            estado = "Completada" if tarea_encontrada.completada else "Pendiente"
            mensaje = f"TAREA ENCONTRADA:\n\nTítulo: {tarea_encontrada.titulo}\nPrioridad: {tarea_encontrada.prioridad}\nEstado: {estado}"
            ctk.CTkMessagebox(title="Resultado de Búsqueda", message=mensaje, icon="check").get()
        else:
            ctk.CTkMessagebox(title="Resultado de Búsqueda", message=f"La tarea '{titulo_buscado}' no se encontró.", icon="cancel").get()
        
# Inicia la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()