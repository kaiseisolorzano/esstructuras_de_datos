# estructuras.py
# -----------------------------------------------------------------------------
# Archivo donde se encuentran las clases para las tareas/actividades que 
# generará el usuario.
# -----------------------------------------------------------------------------

# Mapa de prioridades para facilitar la comparación numérica:
# Mayor número = Mayor prioridad (se inserta primero)
PRIORIDAD_MAP = {
    "Alta": 3,
    "Media": 2,
    "Baja": 1
}

# --- Clase Tarea (Base de Datos) ---
class Tarea:
    def __init__(self, titulo, descripcion="Pendiente", prioridad="Media", fecha_limite=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.completada = False
        self.fecha_limite = fecha_limite  # Nuevo atributo
        
    def __str__(self):
        base = f"[{self.prioridad.upper()}] {self.titulo}"
        if self.fecha_limite:
            base += f" - {self.fecha_limite}"
        return base

# -------------------------------------------

# --- Estructura 1: Lista Enlazada Simple ---

# -------------------------------------------

class Nodo:
    """Representa un nodo en la lista enlazada."""
    
    def __init__(self, tarea):

        self.tarea = tarea      # El objeto Tarea (el dato)
        self.siguiente = None   # Puntero al siguiente nodo

class ListaEnlazada:
    """Implementa las operaciones de la Lista Enlazada de forma manual."""

    def __init__(self):

        self.cabeza = None  # La cabeza (head) de la lista

    def get_priority_value(self, tarea):

        """Función auxiliar para obtener el valor numérico de la prioridad."""

        return PRIORIDAD_MAP.get(tarea.prioridad, 0)
        
    # 1. Operación: Inserción Ordenada (Core del requerimiento)
    def insertar_ordenado(self, tarea):
        """
        Inserta una nueva Tarea manteniendo la lista ordenada de mayor a menor prioridad 
        (Alta a Baja). Si las prioridades son iguales, se inserta al final de ese bloque.
        """
        nuevo_nodo = Nodo(tarea)
        valor_nueva = self.get_priority_value(tarea)
        
        # Caso 1: La lista está vacía O la nueva tarea tiene mayor prioridad que la cabeza
        if self.cabeza is None or valor_nueva > self.get_priority_value(self.cabeza.tarea):

            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo

            return
            
# ------------------------------------
        
# Caso 2: Buscar la posición correcta

# ------------------------------------
        actual = self.cabeza
        
        # Recorremos mientras el siguiente nodo exista Y la prioridad del siguiente nodo 
        # sea MAYOR o IGUAL a la nueva tarea. Cuando es menor, encontramos el punto de inserción.
        while actual.siguiente and valor_nueva <= self.get_priority_value(actual.siguiente.tarea):
            actual = actual.siguiente
            
        # Insertar el nuevo nodo en la posición encontrada
        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo

    # ------------------------------------

    # 2. Operación: Recorrido/Visualización

    # ------------------------------------
    def recorrer(self):

        """Recorre la lista y devuelve las tareas en forma de lista de Python."""

        tareas = []
        actual = self.cabeza

        while actual:

            tareas.append(actual.tarea)
            actual = actual.siguiente

        return tareas

# ------------------------------------
    
#---- 3. Operación: Búsqueda---------

# ------------------------------------
    def buscar_por_titulo(self, titulo_buscado):

        """Busca y devuelve el objeto Tarea por su título."""

        actual = self.cabeza

        while actual:

            if actual.tarea.titulo.lower() == titulo_buscado.lower():

                return actual.tarea
            
            actual = actual.siguiente

        return None

# ------------------------------------

# -----4. Operación: Eliminación-----

# ------------------------------------
    def eliminar_por_titulo(self, titulo_a_eliminar):

        """Elimina el primer nodo que coincida con el título y devuelve la Tarea eliminada."""

        actual = self.cabeza
        anterior = None
        tarea_eliminada = None
        
        while actual:

            if actual.tarea.titulo.lower() == titulo_a_eliminar.lower():

                tarea_eliminada = actual.tarea

                break

            anterior = actual
            actual = actual.siguiente
        
        if actual is None:

            return None # Eliminación fallida

        if anterior is None:

            self.cabeza = actual.siguiente # Eliminar la Cabeza

        else:

            anterior.siguiente = actual.siguiente # Eliminar un nodo intermedio o final
            
        return tarea_eliminada

# ------------------------------------

# --- Estructura 2: Pila (Stack) -----

# ------------------------------------
class Pila:

    """Implementa la Pila (LIFO) manualmente con operaciones push/pop restringidas."""

    def __init__(self):

        self.items = [] 

    # Operación: Inserción (Push)
    def push(self, elemento):

        """Agrega un elemento al tope de la Pila."""

        self.items.append(elemento)

    # Operación: Eliminación (Pop)
    def pop(self):

        """Remueve y devuelve el elemento del tope de la Pila."""

        if not self.esta_vacia():

            return self.items.pop() 
        
        return None

# ------------------------------------

#---- Método auxiliar-----------------

# ------------------------------------
    def esta_vacia(self):

        """Verifica si la Pila está vacía."""

        return len(self.items) == 0