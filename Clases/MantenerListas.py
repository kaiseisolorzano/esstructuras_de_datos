# MantenerListas.py
# -----------------------------------------------------------------------------
# Mantener guardadas las listas creadas por el usuario y evitar que se pierdan
# al cerrar la app principal.
# -----------------------------------------------------------------------------

# Uso de json para guardar archivos en el almacenamiento local del dispositivo.
import json 
import os               # Utilidades del SO. -> Comprobación de archivos.
import tempfile

class MantenerListas:

    # =========================================================================
    # Constructor 
    # -----------------------------------------
    # valor por defecto: "datos_de_tareas.json"
    # =========================================================================
    def __init__(self, archivo="Clases/Tareas/datos_de_tareas.json"):
        self.archivo = archivo
    
    # -------------------------------------------------------------------------
    # Método privado para convertir los datos en archivos que se puedan guardar
    # en el JSON.
    # -------------------------------------------------------------------------
    def _serializar_lista(self, lista_tareas):
        datos = []                      # Lista vacía para después guardar los datos.
        nodo = getattr(lista_tareas, "cabeza", None)
        while nodo:
            tarea = nodo.tarea           # Tomar tarea del nodo actual.

            # Convertir la tarea en un diccionario JSON.
            datos.append({
                "titulo": tarea.titulo,
                "descripcion": getattr(tarea, "descripcion", None),
                "prioridad": getattr(tarea, "prioridad", None),
                "completada": bool(getattr(tarea, "completada", False)),
                "fecha_limite": getattr(tarea, "fecha_limite", None)
            })

            nodo = nodo.siguiente       # Siguiente nodo.
        return datos

    # -------------------------------------------------------
    # Método privado
    # --------------------------------------------------------
    def _serializar_pila(self, pila):
        datos = []
        items = getattr(pila, "items", [])
        for tarea in items:   # De la clase pila...
            # convertir las tareas a JSON.
            datos.append({
                "titulo": tarea.titulo,
                "descripcion": getattr(tarea, "descripcion", None),
                "prioridad": getattr(tarea, "prioridad", None),
                "completada": bool(getattr(tarea, "completada", False)),
                "fecha_limite": getattr(tarea, "fecha_limite", None)
            })
        return datos

    # ---------------------------------------------------------------
    # Método para convertir el archivo en JSON y guardarlo localmente
    # en el dispositivo.
    # ---------------------------------------------------------------
    def guardar(self, lista_tareas, pila_eliminados):
        # Construir diccionario.
        data = {
            "lista": self._serializar_lista(lista_tareas),
            "pila_eliminados": self._serializar_pila(pila_eliminados)
        }

        # Guardar en temp file.
        dirpath = os.path.dirname(os.path.abspath(self.archivo)) or "."
        fd, tmp_path = tempfile.mkstemp(dir=dirpath, prefix="tmp_tareas_", suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            # Reemplazar el archivo destino (os.replace es atómico en la mayoría de SO)
            os.replace(tmp_path, self.archivo)
        except Exception:
            # intentar borrar temporal si existe y ocurrió error
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
            raise

    # ---------------------------------------------------------------
    # Método para cargar desde JSON
    # ---------------------------------------------------------------
    def cargar(self, ClaseLista, ClaseTarea, ClasePila):
        # Si el archivo no existe...
        if not os.path.exists(self.archivo):
            # ...crear lista y pila vacia.
            return ClaseLista(), ClasePila()

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            # Si el archivo está corrupto o no se puede leer, devolver estructuras vacías
            return ClaseLista(), ClasePila()

        # Rehacer la lista.
        lista = ClaseLista()
        for item in data.get("lista", []):
            titulo = item.get("titulo")
            descripcion = item.get("descripcion", "Pendiente")
            prioridad = item.get("prioridad", "Media")
            fecha_limite = item.get("fecha_limite", None)
            tarea = ClaseTarea(titulo=titulo, descripcion=descripcion, prioridad=prioridad, fecha_limite=fecha_limite)
            # Restaurar completada si existe
            tarea.completada = bool(item.get("completada", False))
            # Insertar en la lista 
            lista.insertar_ordenado(tarea)

        # Rehacer la pila.
        pila = ClasePila()
        for item in data.get("pila_eliminados", []):
            titulo = item.get("titulo")
            descripcion = item.get("descripcion", "Pendiente")
            prioridad = item.get("prioridad", "Media")
            fecha_limite = item.get("fecha_limite", None)
            tarea = ClaseTarea(titulo=titulo, descripcion=descripcion, prioridad=prioridad, fecha_limite=fecha_limite)
            tarea.completada = bool(item.get("completada", False))
            pila.push(tarea)

        return lista, pila  # Regresar las listas reconstruidas.
