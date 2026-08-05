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

def obtener_fecha_actual():
    momento_actual = datetime.now()

    dias = [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo"
    ]

    meses = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre"
    ]

    dia_semana = dias[momento_actual.weekday()]
    dia = momento_actual.day
    mes = meses[momento_actual.month - 1]
    anio = momento_actual.year

    return f"{dia_semana}, {dia} de {mes} de {anio}"

def obtener_hora_actual():
    momento_actual = datetime.now()
    return momento_actual.strftime("%I:%M %p")
print(obtener_hora_actual())

