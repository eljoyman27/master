import tkinter as tk
from functools import partial
import random
import os

from PIL import Image, ImageTk  # <- USAMOS PILLOW PARA REDIMENSIONAR

# ==========================
# CONFIGURACIÓN DE FIGURAS
# ==========================
# Título que verás en el juego + ruta a la imagen
FIGURAS = [



    ("Amapola",      "img/amapola.png"),
    ("Bandra",       "img/bandera.png"),
    ("Bomba",        "img/bomba.png"),
    ("Bongo",        "img/bongo.png"),
    ("Cafe_Colao",   "img/cafe_colao.png"),
    ("Cafe_Semilla", "img/semilla_cafe.png"),
    ("Cuatro",       "img/cuatro.png"),
    ("Coco",         "img/palma_de_coco.png"),
    ("Coquí",        "img/coqui.png"),
    ("Cotorra",      "img/cotorra.png"),
    ("Güiro",        "img/guiro.jpg"),
    ("Hamaca",       "img/hamaca.png"),
    ("Jibaro",       "img/jibaro.png"),
    ("Mapa",         "img/mapa.png"),
    ("Maracas",      "img/maracas.png"),
    ("Mavi",         "img/mavi.png"),
    ("Trompeta",     "img/trompeta.png"),
    ("Velero",       "img/velero.png"),
    # ("Vegigante",    "img/vegigante.png"),
]

# Tamaño objetivo de las imágenes en píxeles (puedes subirlo o bajarlo)
TARGET_SIZE = 150 # 180x180 px aprox


PAIRS_BASE = FIGURAS[:]   # copia
PAIRS = PAIRS_BASE * 2    # 20 cartas (10 pares)

COLS = 6
ROWS = len(PAIRS) // COLS  # 4 filas


class MemoryGamePR:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Memoria • Cultura de Puerto Rico")

        # Cargar imágenes redimensionadas
        self.images = self.load_images()

        # Lista de valores (cada carta: título + clave de imagen)
        self.values = [(title, title) for (title, path) in PAIRS_BASE] * 2
        random.shuffle(self.values)

        # Estado del juego
        self.buttons = []
        self.first_idx = None
        self.second_idx = None
        self.lock = False
        self.tries = 0
        self.found_pairs = 0
        self.total_pairs = len(PAIRS_BASE)

        # ---- Barra de estado ----
        status_frame = tk.Frame(root)
        status_frame.pack(pady=8)

        self.tries_var = tk.StringVar(value="Intentos: 0")
        self.found_var = tk.StringVar(
            value=f"Pares encontrados: 0 / {self.total_pairs}"
        )

        tk.Label(status_frame, textvariable=self.tries_var,
                 font=("Helvetica", 11)).grid(row=0, column=0, padx=10)
        tk.Label(status_frame, textvariable=self.found_var,
                 font=("Helvetica", 11)).grid(row=0, column=1, padx=10)

        # ---- Tablero ----
        self.board_frame = tk.Frame(root, padx=10, pady=10, bg="#f2f2f2")
        self.board_frame.pack()

        self.create_board()

        # ---- Botón Reiniciar ----
        reset_frame = tk.Frame(root)
        reset_frame.pack(pady=8)

        tk.Button(reset_frame, text="Reiniciar juego",
                  command=self.reset_game,
                  font=("Helvetica", 10)).pack()

    # ==========================
    # CARGA Y REDIMENSIÓN DE IMÁGENES
    # ==========================
    def load_images(self):
        """
        Carga y redimensiona todas las imágenes a TARGET_SIZE x TARGET_SIZE
        Devuelve un diccionario: { "Coquí": PhotoImage, ... }
        """
        images = {}
        for title, path in FIGURAS:
            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"No se encontró la imagen para '{title}': {path}"
                )
            # Abrimos la imagen con PIL
            pil_img = Image.open(path).convert("RGBA")

            # La redimensionamos manteniendo proporción
            pil_img.thumbnail((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)

            # Para centrarla en un lienzo cuadrado blanco/transparente
            canvas_size = (TARGET_SIZE, TARGET_SIZE)
            bg = Image.new("RGBA", canvas_size, (255, 255, 255, 0))
            x = (canvas_size[0] - pil_img.width) // 2
            y = (canvas_size[1] - pil_img.height) // 2
            bg.paste(pil_img, (x, y), pil_img)

            # Convertimos a PhotoImage de Tkinter
            tk_img = ImageTk.PhotoImage(bg)
            images[title] = tk_img

        return images

    # ==========================
    # CREAR TABLERO
    # ==========================
    def create_board(self):
        self.buttons.clear()
        idx = 0
        for r in range(ROWS):
            for c in range(COLS):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    bg="#e6e6e6",
                    activebackground="#d9d9d9",
                    relief="raised",
                    bd=2,
                    command=partial(self.flip_card, idx),

                    # width=8-,  # more horizontal space
                    # height=8  # more vertical space
                )
                # btn = tk.Button(
                #     self.board_frame,
                #     text="",          # sin texto, solo imagen
                #     bg="#e6e6e6",
                #     activebackground="#d9d9d9",
                #     relief="raised",
                #     bd=2,
                #     command=partial(self.flip_card, idx)
                # )
                # NOTA: no ponemos width/height, dejamos que la imagen marque el tamaño
                btn.grid(row=r, column=c, padx=8, pady=8)
                self.buttons.append(btn)
                idx += 1

    # ==========================
    # LÓGICA DEL JUEGO
    # ==========================
    def flip_card(self, idx):
        if self.lock:
            return

        btn = self.buttons[idx]

        # Ya encontrada (deshabilitada)
        if btn["state"] == "disabled":
            return

        # Ya volteada
        if getattr(btn, "image_shown", False):
            return

        title, key = self.values[idx]
        img = self.images[key]

        # Mostrar imagen
        btn.config(image=img, bg="white")
        btn.image = img            # mantener referencia
        btn.image_shown = True     # flag propio

        if self.first_idx is None:
            self.first_idx = idx
        else:
            self.second_idx = idx
            self.lock = True
            self.root.after(700, self.check_match)

    def check_match(self):
        i = self.first_idx
        j = self.second_idx

        title1, key1 = self.values[i]
        title2, key2 = self.values[j]

        self.tries += 1
        self.tries_var.set(f"Intentos: {self.tries}")

        if key1 == key2:
            # Par correcto
            for idx in (i, j):
                self.buttons[idx].config(state="disabled", bg="#d5f5e3")
            self.found_pairs += 1
            self.found_var.set(
                f"Pares encontrados: {self.found_pairs} / {self.total_pairs}"
            )
            if self.found_pairs == self.total_pairs:
                self.tries_var.set(
                    f"¡Ganaste! Intentos totales: {self.tries}"
                )
        else:
            # No coinciden, las ocultamos de nuevo
            for idx in (i, j):
                b = self.buttons[idx]
                b.config(image="", bg="#e6e6e6")
                b.image = None
                b.image_shown = False

        self.first_idx = None
        self.second_idx = None
        self.lock = False

    # ==========================
    # REINICIAR
    # ==========================
    def reset_game(self):
        random.shuffle(self.values)
        self.first_idx = None
        self.second_idx = None
        self.lock = False
        self.tries = 0
        self.found_pairs = 0
        self.tries_var.set("Intentos: 0")
        self.found_var.set(f"Pares encontrados: 0 / {self.total_pairs}")

        for b in self.buttons:
            b.config(text="", image="", state="normal", bg="#e6e6e6")
            b.image = None
            b.image_shown = False


# ==========================
# PUNTO DE ENTRADA
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")  # ancho x alto en píxeles
    app = MemoryGamePR(root)
    root.mainloop()


