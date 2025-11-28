# main.py

import customtkinter as ctk  # Biblioteca para interfaces modernas
import tkinter as tk         # Biblioteca estándar de Python para interfaces
from tkinter import messagebox  # Para mostrar mensajes de diálogo
from datetime import datetime, date  # Para manejar fechas y horas
# Importamos las clases de las estructuras de datos manuales
from estructuras import ListaEnlazada, Pila, Tarea 

# =============================================================================
# CONFIGURACIÓN INICIAL DE LA APLICACIÓN
# =============================================================================

# Configuración de apariencia de CustomTkinter
ctk.set_appearance_mode("Dark")  # Establece el tema oscuro para toda la app
ctk.set_default_color_theme("blue")  # Establece el tema de color azul

# =============================================================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# =============================================================================

class App(ctk.CTk):
    """
    Clase principal que representa la aplicación completa.
    Hereda de CTk (CustomTkinter) para crear la ventana principal.
    """
    
    def __init__(self):
        """
        Constructor de la clase App.
        Inicializa la ventana principal y todos los componentes.
        """
        super().__init__()  # Llama al constructor de la clase padre (CTk)

        # =====================================================================
        # CONFIGURACIÓN DE LA VENTANA PRINCIPAL
        # =====================================================================
        
        self.title("Gestor de Tareas Pendientes Ordenadas por Prioridad y Fecha")
        self.geometry("900x650")  # Ancho x Alto de la ventana
        
        # Configuración del sistema de grid para hacer la interfaz responsive
        # La columna 1 (área principal) se expandirá, la 0 (sidebar) mantiene tamaño fijo
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # =====================================================================
        # INICIALIZACIÓN DE ESTRUCTURAS DE DATOS MANUALES
        # =====================================================================
        
        # ListaEnlazada: Almacena las tareas ordenadas por prioridad
        self.lista_tareas = ListaEnlazada()
        
        # Pila: Guarda las tareas eliminadas para poder deshacer (patrón LIFO)
        self.pila_undo = Pila()
        
        # Crear todos los elementos visuales de la interfaz
        self.crear_layout()
        
    def crear_layout(self):
        
        """
        Construye y organiza todos los elementos visuales de la interfaz.
        Divide la pantalla en dos áreas principales: Sidebar y Área Principal.
        """
        
        # =====================================================================
        # A. FRAME LATERAL (SIDEBAR) - Zona de entrada de datos y controles
        # =====================================================================
        
        self.sidebar_frame = ctk.CTkFrame(self, width=160, corner_radius=0)
        # Posiciona el sidebar en la columna 0, que ocupa 4 filas y se expande verticalmente
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Configuración del grid interno del sidebar para que los botones no se amontonen
        # La fila 8 tiene weight=1 para empujar los elementos hacia arriba y dejar espacio abajo
        self.sidebar_frame.grid_rowconfigure(8, weight=1) 

        # Título de la sección de nueva tarea
        ctk.CTkLabel(self.sidebar_frame, text="NUEVA TAREA", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(
                    row=0, column=0, padx=20, pady=(20, 10))

        # =====================================================================
        # CAMPO DE ENTRADA PARA EL TÍTULO DE LA TAREA
        # =====================================================================
        
        self.title_entry = ctk.CTkEntry(self.sidebar_frame, 
                                       placeholder_text="Título de la Tarea")
        
        self.title_entry.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")

        # =====================================================================
        # SELECTOR DE PRIORIDAD
        # =====================================================================
        
        ctk.CTkLabel(self.sidebar_frame, text="Prioridad:").grid(
            row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.prioridades = ["Alta", "Media", "Baja"]  # Opciones de prioridad

        self.priority_combobox = ctk.CTkComboBox(

            self.sidebar_frame, 
            values=self.prioridades
        )

        self.priority_combobox.set("Media")  # Valor por defecto
        self.priority_combobox.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        # =====================================================================
        # SECCIÓN FECHA LÍMITE - Selector de fecha con día, mes y año
        # =====================================================================
        
        ctk.CTkLabel(self.sidebar_frame, text="Fecha Límite:", 
                    font=ctk.CTkFont(size=12)).grid(
                    row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        
        # Frame transparente para organizar los 3 combobox de fecha
        fecha_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        fecha_frame.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="ew")
        
        # Combobox para seleccionar el día (01-31)
        self.dia_combobox = ctk.CTkComboBox(

            fecha_frame, 
            values=[str(i).zfill(2) for i in range(1, 32)],  # zfill(2) para que sea "01", "02", etc.
            width=50
        )

        self.dia_combobox.set("01")  # Valor por defecto: día 1
        self.dia_combobox.pack(side="left", padx=(0, 5))
        
        # Combobox para seleccionar el mes (01-12)
        self.mes_combobox = ctk.CTkComboBox(

            fecha_frame, 
            values=[str(i).zfill(2) for i in range(1, 13)],
            width=50

        )

        # Valor por defecto: mes actual
        self.mes_combobox.set(datetime.now().strftime("%m"))
        self.mes_combobox.pack(side="left", padx=5)
        
        # Combobox para seleccionar el año (año actual + 2 años siguientes)
        año_actual = datetime.now().year
        self.año_combobox = ctk.CTkComboBox(

            fecha_frame, 
            values=[str(i) for i in range(año_actual, año_actual + 3)],
            width=60

        )

        self.año_combobox.set(str(año_actual))  # Valor por defecto: año actual
        self.año_combobox.pack(side="left", padx=(5, 0))

        # =====================================================================
        # BOTONES DE ACCIÓN PRINCIPALES
        # =====================================================================
        
        # Botón para agregar nueva tarea
        self.add_button = ctk.CTkButton(self.sidebar_frame, 
                                       text="➕ AGREGAR", 
                                       command=self.agregar_tarea)
        
        self.add_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # Botón para buscar tareas existentes
        self.search_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="🔍 BUSCAR", 
            command=self.buscar_tarea,
            fg_color="#8B9DC3"  # Color personalizado azul claro

        )

        self.search_button.grid(row=7, column=0, padx=20, pady=5, sticky="ew")

        # Botón para deshacer la última eliminación
        self.undo_button = ctk.CTkButton(self.sidebar_frame, 
                                        text="↩️ DESHACER", 
                                        command=self.deshacer_accion, 
                                        fg_color="#3B5998")  # Color azul oscuro
        
        self.undo_button.grid(row=8, column=0, padx=20, pady=(5, 10), sticky="ew")
        
        # =====================================================================
        # B. FRAME PRINCIPAL (MAIN) - Área de visualización de tareas
        # =====================================================================
        
        # Frame desplazable que contendrá todas las tareas organizadas por meses
        self.main_scroll_frame = ctk.CTkScrollableFrame(

            self, 
            label_text="Lista de Tareas por Mes", 
            corner_radius=0

        )

        self.main_scroll_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_scroll_frame.grid_columnconfigure(0, weight=1)

        # Mostrar las tareas en la interfaz
        self.actualizar_vista_tareas()
    
    def obtener_fecha_limite(self):

        """
        Obtiene la fecha seleccionada por el usuario y la valida.
        
        Returns:
            str or None: Fecha en formato "dd/mm/aaaa" si es válida, None si hay error
        """

        try:

            # Obtener valores de los combobox y convertirlos a enteros
            dia = int(self.dia_combobox.get())
            mes = int(self.mes_combobox.get())
            año = int(self.año_combobox.get())
            
            # Validar si la fecha es válida (esto lanza ValueError si no lo es)
            fecha_limite = date(año, mes, dia)
            
            # Verificar que la fecha no sea en el pasado
            hoy = date.today()
            if fecha_limite < hoy:

                messagebox.showwarning("Advertencia", "La fecha límite no puede ser en el pasado.")
                return None
                
            # Devolver fecha en formato string "dd/mm/aaaa"
            return fecha_limite.strftime("%d/%m/%Y")
            
        except ValueError:

            # Capturar errores de fecha inválida (ej: 30 de febrero)
            messagebox.showerror("Error", "Fecha límite inválida.")
            return None
        
    # =========================================================================
    # MÉTODOS DE LÓGICA DE NEGOCIO - Conexión con estructuras de datos
    # =========================================================================
    
    def agregar_tarea(self):

        """
        Crea una nueva tarea y la inserta en la lista enlazada de forma ordenada.
        Valida los datos de entrada antes de crear la tarea.
        """

        # Obtener datos del formulario
        titulo = self.title_entry.get().strip()  # strip() elimina espacios al inicio/final
        prioridad_seleccionada = self.priority_combobox.get()
        fecha_limite = self.obtener_fecha_limite()  # Puede devolver None si hay error
        
        # Validar que el título no esté vacío
        if not titulo:

            messagebox.showwarning("Advertencia", "Ingresa un título para la tarea.")

            return
            
        # Validar que la fecha sea válida
        if not fecha_limite:

            return  # No agregar tarea si la fecha es inválida

        # Crear nuevo objeto Tarea con todos los datos
        nueva_tarea = Tarea(

            titulo=titulo, 
            descripcion="Pendiente",
            prioridad=prioridad_seleccionada,
            fecha_limite=fecha_limite

        )

        # LLAMADA AL MÉTODO DE INSERCIÓN ORDENADA en la lista enlazada
        # La lista se mantiene automáticamente ordenada por prioridad
        self.lista_tareas.insertar_ordenado(nueva_tarea)
        
        # Limpiar el campo de título y actualizar la vista
        self.title_entry.delete(0, 'end')  # Borrar desde posición 0 hasta el final
        self.actualizar_vista_tareas()  # Refrescar la interfaz
        
    def deshacer_accion(self):

        """
        Recupera la última tarea eliminada usando la pila (patrón LIFO).
        Si la pila está vacía, muestra un mensaje informativo.
        """

        # LLAMADA A LA OPERACIÓN POP DE LA PILA - obtiene el último elemento eliminado
        tarea_revertida = self.pila_undo.pop() 
        
        if tarea_revertida:

            # Reinsertar la tarea en la lista enlazada (manteniendo el orden por prioridad)
            self.lista_tareas.insertar_ordenado(tarea_revertida)
            self.actualizar_vista_tareas()  # Refrescar la vista

        else:

            # La pila está vacía
            messagebox.showinfo("Información", "No hay acciones para deshacer.")
            
    def eliminar_tarea_gui(self, titulo):

        """
        Elimina una tarea de la lista y la guarda en la pila para posible deshacer.
        
        Args:

            titulo (str): Título de la tarea a eliminar

        """

        # LLAMADA A LA OPERACIÓN DE ELIMINACIÓN en la lista enlazada
        tarea_eliminada = self.lista_tareas.eliminar_por_titulo(titulo)
        
        if tarea_eliminada:

            # LLAMADA A LA OPERACIÓN PUSH DE LA PILA - guardar para deshacer
            self.pila_undo.push(tarea_eliminada)
            self.actualizar_vista_tareas()  # Refrescar la vista
            
    def toggle_estado_tarea(self, titulo):

        """
        Cambia el estado de una tarea entre completada y pendiente.
        
        Args:
            titulo (str): Título de la tarea a modificar
        """

        # LLAMADA A LA OPERACIÓN DE BÚSqueda en la lista enlazada
        tarea = self.lista_tareas.buscar_por_titulo(titulo)
        
        if tarea:

            # Alternar el estado de completada (True/False)
            tarea.completada = not tarea.completada
            self.actualizar_vista_tareas()  # Refrescar la vista

    # =========================================================================
    # MÉTODOS DE ORGANIZACIÓN Y VISUALIZACIÓN
    # =========================================================================

    def organizar_tareas_por_mes(self, tareas):

        """
        Agrupa las tareas por mes y año basándose en su fecha límite.
        
        Args:
            tareas (list): Lista de objetos Tarea a organizar
            
        Returns:
            dict: Diccionario donde las claves son los meses ("Enero 2024") 
                  y los valores son listas de tareas de ese mes
        """
        tareas_por_mes = {}  # Diccionario vacío para almacenar la organización
        
        for tarea in tareas:

            # Verificar si la tarea tiene fecha límite
            if hasattr(tarea, 'fecha_limite') and tarea.fecha_limite:

                try:
                    # Convertir fecha de string "dd/mm/aaaa" a objeto date
                    fecha = datetime.strptime(tarea.fecha_limite, "%d/%m/%Y").date()

                    # Formatear como "Mes Año" (ej: "Enero 2024")
                    mes_año = fecha.strftime("%B %Y")
                    
                    # Si el mes no existe en el diccionario, crear una lista vacía
                    if mes_año not in tareas_por_mes:
                        tareas_por_mes[mes_año] = []
                    
                    # Agregar la tarea a la lista de su mes correspondiente
                    tareas_por_mes[mes_año].append(tarea)
                    
                except ValueError:

                    # Si hay error en el formato de fecha, poner en "Sin Fecha"
                    if "Sin Fecha" not in tareas_por_mes:

                        tareas_por_mes["Sin Fecha"] = []

                    tareas_por_mes["Sin Fecha"].append(tarea)
            else:

                # Tareas sin fecha límite van a la sección "Sin Fecha"
                if "Sin Fecha" not in tareas_por_mes:

                    tareas_por_mes["Sin Fecha"] = []

                tareas_por_mes["Sin Fecha"].append(tarea)
        
        return tareas_por_mes

    def actualizar_vista_tareas(self):

        """
        Actualiza completamente la interfaz gráfica mostrando todas las tareas
        organizadas por meses en orden cronológico.
        """

        # Limpiar todos los widgets anteriores del área de tareas
        for widget in self.main_scroll_frame.winfo_children():

            widget.destroy()

        # LLAMADA A LA OPERACIÓN DE RECORRIDO MANUAL de la lista enlazada
        # Obtiene todas las tareas como una lista de Python
        tareas = self.lista_tareas.recorrer()
        
        # Si no hay tareas, mostrar mensaje de "todo listo"
        if not tareas:

            ctk.CTkLabel(self.main_scroll_frame, 
                        text="¡Todo listo! No hay tareas pendientes.").pack(
                        padx=20, pady=20)
            
            return

        # Organizar tareas por mes usando el método auxiliar
        tareas_por_mes = self.organizar_tareas_por_mes(tareas)
        
        # Ordenar los meses cronológicamente (de más antiguo a más reciente)
        meses_ordenados = self.ordenar_meses_cronologicamente(tareas_por_mes.keys())
        
        # Para cada mes, crear una sección visual con sus tareas
        for mes_año in meses_ordenados:

            tareas_del_mes = tareas_por_mes[mes_año]
            
            # Crear sección visual del mes
            seccion_mes = self.crear_seccion_mes(mes_año, tareas_del_mes)
            seccion_mes.pack(fill="x", padx=10, pady=15)

    def ordenar_meses_cronologicamente(self, meses):

        """
        Ordena una lista de meses en orden cronológico.
        
        Args:
            meses (list): Lista de strings en formato "Mes Año"
            
        Returns:
            list: Meses ordenados cronológicamente + "Sin Fecha" al final
        """

        meses_ordenados = []   # Para meses con fecha válida
        meses_sin_fecha = []   # Para la sección "Sin Fecha"
        
        # Separar meses con fecha de "Sin Fecha"
        for mes in meses:

            if mes == "Sin Fecha":

                meses_sin_fecha.append(mes)

            else:

                meses_ordenados.append(mes)
        
        # Ordenar meses con fecha convertiéndolos a objetos datetime para comparar
        meses_ordenados.sort(key=lambda x: datetime.strptime(x, "%B %Y"))
        
        # Agregar "Sin Fecha" al final de la lista ordenada
        return meses_ordenados + meses_sin_fecha

    def crear_seccion_mes(self, mes_año, tareas):

        """
        Crea una sección visual completa para un mes específico.
        
        Args:
            mes_año (str): Nombre del mes y año (ej: "Enero 2024")
            tareas (list): Lista de tareas pertenecientes a ese mes
            
        Returns:
            CTkFrame: Frame completo de la sección del mes
        """

        # Frame principal de la sección del mes (con bordes redondeados)
        seccion_frame = ctk.CTkFrame(self.main_scroll_frame, corner_radius=10)
        
        # =====================================================================
        # HEADER DEL MES - Barra superior con el nombre del mes
        # =====================================================================
        
        header_frame = ctk.CTkFrame(seccion_frame, corner_radius=8, fg_color="#2B2B2B")
        header_frame.pack(fill="x", padx=5, pady=(5, 0))  # Rellenar horizontalmente
        
        # Etiqueta con el nombre del mes en negrita y blanco
        mes_label = ctk.CTkLabel(

            header_frame, 
            text=mes_año,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"

        )

        mes_label.pack(padx=15, pady=8)
        
        # =====================================================================
        # CONTENIDO DEL MES - Área donde se muestran las tareas
        # =====================================================================
        
        contenido_frame = ctk.CTkFrame(seccion_frame, fg_color="transparent")
        contenido_frame.pack(fill="x", padx=5, pady=5)
        
        # Crear un widget para cada tarea del mes
        for tarea in tareas:

            self.crear_widget_tarea(contenido_frame, tarea)
        
        return seccion_frame  # Devolver la sección completa

    def crear_widget_tarea(self, parent, tarea):
        """
        Crea el widget visual para una tarea individual dentro de su mes.
        
        Args:
            parent (CTkFrame): Frame padre donde se insertará la tarea
            tarea (Tarea): Objeto tarea a mostrar
        """
        # =====================================================================
        # LÓGICA DE ESTILO SEGÚN ESTADO DE LA TAREA
        # =====================================================================
        
        if tarea.completada:

            # Tarea completada: texto gris y tachado
            text_color = "gray" 
            font_style = ctk.CTkFont(size=14, weight="normal", overstrike=1) 

        else:

            # Tarea pendiente: texto blanco azulado normal
            text_color = "#DCE4EE" 
            font_style = ctk.CTkFont(size=14, weight="normal")

        # Frame individual para cada tarea
        tarea_frame = ctk.CTkFrame(parent, corner_radius=5)
        tarea_frame.pack(fill="x", padx=5, pady=3)  # Rellenar horizontalmente
        
        # Frame interno para organizar mejor los elementos de la tarea
        contenido_frame = ctk.CTkFrame(tarea_frame, fg_color="transparent")
        contenido_frame.pack(fill="x", padx=10, pady=5)
        
        # =====================================================================
        # CHECKBOX - Para marcar tarea como completada/pendiente
        # =====================================================================
        
        check_box = ctk.CTkCheckBox(

            contenido_frame,
            text=tarea.titulo,  # Texto que se muestra junto al checkbox
            command=lambda t=tarea.titulo: self.toggle_estado_tarea(t),  # Comando al hacer clic
            variable=tk.BooleanVar(value=tarea.completada),  # Variable que refleja el estado
            onvalue=True,   # Valor cuando está marcado
            offvalue=False, # Valor cuando no está marcado
            text_color=text_color,  # Color del texto (gris si completada)
            font=font_style,        # Estilo de fuente (tachado si completada)
            checkbox_height=20,     # Tamaño personalizado del checkbox
            checkbox_width=20
        )

        check_box.pack(side="left", anchor="w")  # Alinear a la izquierda
        
        # =====================================================================
        # INFORMACIÓN ADICIONAL - Prioridad y fecha límite
        # =====================================================================
        
        info_frame = ctk.CTkFrame(contenido_frame, fg_color="transparent")
        info_frame.pack(side="left", padx=(15, 0), fill="x", expand=True)
        
        # Prioridad con color según la importancia
        color_prioridad = {

            "Alta": "red",     # Rojo para alta prioridad
            "Media": "orange", # Naranja para media prioridad
            "Baja": "green"    # Verde para baja prioridad

        }.get(tarea.prioridad, "white")  # Blanco por defecto si no coincide
        
        # Etiqueta de prioridad
        prioridad_label = ctk.CTkLabel(

            info_frame, 
            text=f"Prioridad: {tarea.prioridad}",
            font=ctk.CTkFont(size=12),
            text_color=color_prioridad  # Color dinámico según prioridad
        )

        prioridad_label.pack(anchor="w")  # Alinear a la izquierda
        
        # Fecha límite (solo si existe)
        if hasattr(tarea, 'fecha_limite') and tarea.fecha_limite:

            fecha_label = ctk.CTkLabel(

                info_frame, 
                text=f"Fecha: {tarea.fecha_limite}",
                font=ctk.CTkFont(size=11),
                text_color="lightblue"  # Azul claro para las fechas
            )

            fecha_label.pack(anchor="w")  # Alinear a la izquierda
        
        # =====================================================================
        # BOTÓN DE ELIMINACIÓN
        # =====================================================================
        
        delete_button = ctk.CTkButton(

            contenido_frame, 
            text="❌", 
            width=30,
            command=lambda t=tarea.titulo: self.eliminar_tarea_gui(t)  # Comando con parámetro
        )

        delete_button.pack(side="right", padx=(5, 0))  # Alinear a la derecha
    
    # =========================================================================
    # FUNCIÓN DE BÚSQUEDA
    # =========================================================================
    
    def buscar_tarea(self):
        """
        Busca una tarea por título y muestra el resultado en un mensaje.
        Toma el texto del campo de entrada como término de búsqueda.
        """
        # Obtener texto a buscar del campo de entrada
        titulo_buscado = self.title_entry.get().strip()
        
        # Validar que no esté vacío
        if not titulo_buscado:

            messagebox.showwarning("Advertencia", "Ingresa un título para buscar.")
            return
        
        # LLAMADA A LA OPERACIÓN DE BÚSQUEDA en la lista enlazada
        tarea_encontrada = self.lista_tareas.buscar_por_titulo(titulo_buscado)
        
        if tarea_encontrada:

            # Preparar información detallada de la tarea encontrada
            estado = "Completada" if tarea_encontrada.completada else "Pendiente"
            fecha = tarea_encontrada.fecha_limite if hasattr(tarea_encontrada, 'fecha_limite') else "No especificada"
            
            # Crear mensaje con toda la información
            mensaje = f"TAREA ENCONTRADA:\n\nTítulo: {tarea_encontrada.titulo}\nPrioridad: {tarea_encontrada.prioridad}\nFecha: {fecha}\nEstado: {estado}"
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Resultado de Búsqueda", mensaje)

        else:

            # Tarea no encontrada
            messagebox.showinfo("Resultado de Búsqueda", f"La tarea '{titulo_buscado}' no se encontró.")

# =============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# =============================================================================

if __name__ == "__main__":

    # Crear instancia de la aplicación y ejecutar el loop principal
    app = App()
    app.mainloop()  # Este método mantiene la aplicación corriendo