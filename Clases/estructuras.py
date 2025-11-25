# --- Clase Tarea (Base de Datos) ---

class Tarea:
    """Define la estructura de datos para cada tarea individual."""
    def __init__(self, titulo, descripcion, prioridad="Media"):
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.completada = False
        
    def __str__(self):
        estado = "✅" if self.completada else "❌"
        return f"{estado} [{self.prioridad.upper()}] {self.titulo}"

# ------------------------------------

# --- Estructura 1: Lista Enlazada Simple ---
# 

class Nodo:
    """Representa un nodo en la lista enlazada."""
    def __init__(self, tarea):
        self.tarea = tarea      # El objeto Tarea (el dato)
        self.siguiente = None   # Puntero al siguiente nodo

class ListaEnlazada:
    """Implementa las operaciones de la Lista Enlazada de forma manual."""
    def __init__(self):
        self.cabeza = None  # La cabeza (head) de la lista, inicio de la estructura

    # 1. Operación: Recorrido/Visualización
    def recorrer(self):
        """Recorre la lista e imprime o devuelve las tareas."""
        tareas = []
        actual = self.cabeza
        
        # Iteramos hasta que 'actual' sea None, lo que marca el final de la lista
        while actual:
            # Agrega el objeto Tarea completo
            tareas.append(actual.tarea)
            # Mover al siguiente nodo
            actual = actual.siguiente
            
        return tareas

    # 2. Operación: Inserción
    def insertar_al_final(self, tarea):
        """Inserta una nueva Tarea al final de la lista."""
        nuevo_nodo = Nodo(tarea)
        
        # Caso 1: La lista está vacía
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            return
            
        # Caso 2: La lista no está vacía
        actual = self.cabeza
        # Recorremos hasta encontrar el último nodo (aquel cuyo 'siguiente' es None)
        while actual.siguiente:
            actual = actual.siguiente
            
        # El último nodo ahora apunta al nuevo nodo
        actual.siguiente = nuevo_nodo
        
    # 3. Operación: Búsqueda
    def buscar_por_titulo(self, titulo_buscado):
        """Busca y devuelve el objeto Tarea por su título."""
        actual = self.cabeza
        
        while actual:
            if actual.tarea.titulo.lower() == titulo_buscado.lower():
                # Tarea encontrada
                return actual.tarea
            actual = actual.siguiente
            
        # Tarea no encontrada
        return None

    # 4. Operación: Eliminación
    def eliminar_por_titulo(self, titulo_a_eliminar):
        """Elimina el primer nodo que coincida con el título y devuelve la Tarea eliminada."""
        actual = self.cabeza
        anterior = None
        tarea_eliminada = None
        
        # Búsqueda del nodo a eliminar
        while actual:
            if actual.tarea.titulo.lower() == titulo_a_eliminar.lower():
                tarea_eliminada = actual.tarea
                break # Encontrado
            
            anterior = actual
            actual = actual.siguiente
        
        # Si el nodo 'actual' es None, la tarea no se encontró
        if actual is None:
            return None # Eliminación fallida

        # Caso 1: Eliminar la Cabeza (Head)
        if anterior is None:
            # La cabeza se mueve al siguiente nodo
            self.cabeza = actual.siguiente
        # Caso 2: Eliminar un nodo intermedio o final
        else:
            # El nodo anterior apunta ahora al que seguía al nodo eliminado
            anterior.siguiente = actual.siguiente
            
        # Devolvemos la Tarea que fue eliminada para el historial/Pila
        return tarea_eliminada

