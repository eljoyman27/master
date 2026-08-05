"""
verses.py

Responsabilidad:
Contiene y selecciona los textos bíblicos
que Siempre Cerca mostrará en la pantalla principal.

Este módulo no crea Labels ni interactúa con Tkinter.
Solo devuelve el contenido bíblico solicitado.
"""

from datetime import datetime


TEXTOS_BIBLICOS = [
    {
        "texto": "El Señor es mi pastor; nada me faltará.",
        "referencia": "Salmo 23:1",
    },
    {
        "texto": "Este es el día que hizo el Señor; nos gozaremos y alegraremos en él.",
        "referencia": "Salmo 118:24",
    },
    {
        "texto": "Todo lo puedo en Cristo que me fortalece.",
        "referencia": "Filipenses 4:13",
    },
    # {
    #     "texto": "...",
    #     "referencia": "Proverbios 4:7",
    #     "version": "PDT",
    # }
]


def obtener_texto_biblico():
    dia_del_ano = datetime.now().timetuple().tm_yday
    posicion = (dia_del_ano - 1) % len(TEXTOS_BIBLICOS)

    return TEXTOS_BIBLICOS[posicion]

texto_del_dia = obtener_texto_biblico()

print(texto_del_dia["texto"])
print(texto_del_dia["referencia"])

def obtener_mensaje_reflexion():
    momento_actual = datetime.now()
    hora = momento_actual.hour

    if hora < 12:
        return "Lee este texto lentamente y guárdalo en tu corazón."
    elif hora < 18:
        return "¿Qué parte del texto de hoy puedes recordar?"
    else:
        return "Piensa en cómo este texto acompañó tu día."