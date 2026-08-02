import tkinter as tk
from services.greetings import obtener_saludo

app=tk.Tk()

app.title('Siempre Cerca')
app.geometry("1000x700")
app.configure(background="#F4F1EA")
#-------Base de prueba inicial ------------
welcome_label=tk.Label(
    app,
    text="Buenos días,\n\nPapi y Mami\n\nBienvenidos a Siempre Cerca",
    font=("Arial", 40),
    foreground="#243447",
    background="#F4F1EA",
    justify="center"
)

welcome_label.pack(expand=True)

app.mainloop()