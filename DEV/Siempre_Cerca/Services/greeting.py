# -------------------------------------------------------
# Función: obtener_saludo
#
# Propósito:
# Determinar el saludo apropiado según la hora del día.
#
# Devuelve:
# "Buenos días"
# "Buenas tardes"
# o
# "Buenas noches"
#
# Esta función no muestra información en pantalla.
# Solo decide cuál saludo corresponde.
# -------------------------------------------------------
from narwhals.functions import Then
from tensorflow.python.framework.test_util import disable_asan

"""
greetings.py

Responsabilidad:
Contiene las funciones relacionadas con los saludos
y mensajes de bienvenida de Siempre Cerca.

Este módulo no dibuja pantallas.
No crea Labels.
No interactúa con Tkinter.

Su única responsabilidad es generar la información
que otras partes del sistema mostrarán.
"""

from datetime import datetime

def obtener_saludo():
    momento_actual = datetime.now()
    hora = momento_actual.hour
    if hora < 12:
        return "Buenos dias"
    elif hora < 18:
        return "Buenas tardes"
    else:
        return "Buenas Noches"

#print(obtener_saludo())
