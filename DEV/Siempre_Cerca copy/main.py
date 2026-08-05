import tkinter as tk

from services.greetings import (
    obtener_saludo,
    obtener_fecha_actual,
    obtener_hora_actual,
)

app = tk.Tk()
app.title("Siempre Cerca")
app.geometry("1000x700")
app.configure(background="#F4F1EA")

nombre_usuarios = "Papi y Mami"

# --- Labels principales ---
welcome_label = tk.Label(
    app,
    text="",
    font=("Arial", 30),
    foreground="#243447",
    background="#F4F1EA",
    justify="center"
)
welcome_label.pack(expand=True)

time_label = tk.Label(
    app,
    text="",
    font=("Arial", 24),
    foreground="#243447",
    background="#F4F1EA"
)
time_label.pack()

# --- Función de actualización ---
def actualizar_pantalla():
    saludo = obtener_saludo()
    fecha_actual = obtener_fecha_actual()
    hora_actual = obtener_hora_actual()

    mensaje_bienvenida = (
        f"{saludo},\n\n"
        f"{nombre_usuarios}\n\n"
        f"Hoy es {fecha_actual}\n\n"
        "Bienvenidos a Siempre Cerca"
    )

    welcome_label.config(text=mensaje_bienvenida)
    time_label.config(text=hora_actual)

    # Actualiza saludo/fecha cada 60 segundos
    app.after(60000, actualizar_pantalla)

def actualizar_hora():
    hora_actual = obtener_hora_actual()
    time_label.config(text=hora_actual)
    app.after(1000, actualizar_hora)

# --- Inicialización ---
actualizar_pantalla()
actualizar_hora()

app.mainloop()

