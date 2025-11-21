import tkinter as tk

# Crear la venta a mostrar.
# -----------------------------
ventana = tk.Tk()
ventana.title("My Tkinter App")

# Crear un label hola mundo
# --------------------------------------------*
label = tk.Label(ventana, text="!Hola mundo!")
label.pack()        # <----------------------- Mostrar en la ventana.

# ---------------------------------------------------------
# Método para usarlo en el botón de prueba.
# ---------------------------------------------------------
def un_click():
    label_prueba.pack()


# Boton de prueba que mostrará un label.
# --------------------------------------
boton_prueba = tk.Button(
    ventana,
    command=un_click,
    text="Haz clic aquí"
)

# Crear el label de prueba.
# ---------------------------------------------*
label_prueba = tk.Label(
    ventana,
    text="!Presionaste el botón de prueba XDDD"
)

# Mostrar botón de prueba en ventana.
boton_prueba.pack(pady=10, padx=20)

# Mostrar ventana.
# ----------------+
ventana.mainloop()