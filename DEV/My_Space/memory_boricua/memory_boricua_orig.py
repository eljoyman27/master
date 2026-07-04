import tkinter as tk
from functools import partial
import random

# ==========================
# CONFIGURACIÓN DEL JUEGO
# ==========================

# Figuras culturales puertorriqueñas (puedes cambiar nombres o emojis)
FIGURAS = [
    ("Coquí", "🐸"),
    ("Vejigante", "🎭"),
    ("Mofongo", "🍽️"),
    ("El Morro", "🏰"),
    ("Flamboyán", "🌺"),
    ("Güiro", "🥁"),
    ("Cuatro", "🎸"),
    ("Parranda", "🎶"),
    ("Piragua", "🍧"),
    ("Sol Taíno", "☀️"),
]

# Duplicamos para formar las parejas
PAIRS = FIGURAS * 2       # 20 cartas (10 pares)
random.shuffle(PAIRS)

TOTAL_CARDS = len(PAIRS)
COLS = 5                  # número de columnas en el tablero
ROWS = TOTAL_CARDS // COLS  # filas calculadas

# ==========================
# CLASE DEL JUEGO
# ==========================

class MemoryGamePR:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Memoria • Cultura de Puerto Rico")

        # Variables de estado
        self.buttons = []
        self.values = PAIRS[:]   # copia de la lista mezclada
        self.first_idx = None
        self.second_idx = None
        self.lock = False        # para evitar clicks mientras se compara
        self.tries = 0
        self.found_pairs = 0
        self.total_pairs = len(FIGURAS)

        # ---- Sección de status (intentos, pares) ----
        status_frame = tk.Frame(root)
        status_frame.pack(pady=8)

        self.tries_var = tk.StringVar(value="Intentos: 0")
        self.found_var = tk.StringVar(value=f"Pares encontrados: 0 / {self.total_pairs}")

        tk.Label(status_frame, textvariable=self.tries_var,
                 font=("Helvetica", 11)).grid(row=0, column=0, padx=10)
        tk.Label(status_frame, textvariable=self.found_var,
                 font=("Helvetica", 11)).grid(row=0, column=1, padx=10)

        # ---- Tablero de cartas ----
        self.board_frame = tk.Frame(root, padx=10, pady=10, bg="#f2f2f2")
        self.board_frame.pack()

        self.create_board()

        # ---- Botón de reinicio ----
        reset_frame = tk.Frame(root)
        reset_frame.pack(pady=8)

        tk.Button(reset_frame, text="Reiniciar juego",
                  command=self.reset_game,
                  font=("Helvetica", 10)).pack()

    # ==========================
    # CREAR TABLERO
    # ==========================
    def create_board(self):
        self.buttons.clear()
        idx = 0
        for r in range(ROWS):
            for c in range(COLS):
                # cada botón representa una carta
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    width=14,
                    height=4,
                    bg="#e6e6e6",
                    activebackground="#d9d9d9",
                    font=("Helvetica", 11),
                    command=partial(self.flip_card, idx)
                )
                btn.grid(row=r, column=c, padx=6, pady=6)
                self.buttons.append(btn)
                idx += 1

    # ==========================
    # ACCIONES DEL JUEGO
    # ==========================
    def show_label(self, title, icon):
        """Texto que se verá al voltear la carta."""
        return f"{icon} {title}"

    def flip_card(self, idx):
        """Maneja el clic sobre una carta."""
        if self.lock:
            return

        btn = self.buttons[idx]

        # Carta ya deshabilitada (par encontrado)
        if btn["state"] == "disabled":
            return

        # Si ya está volteada (tiene texto), no hacer nada
        if btn["text"] != "":
            return

        title, icon = self.values[idx]
        btn.config(text=self.show_label(title, icon), bg="white")

        if self.first_idx is None:
            # Primera carta seleccionada
            self.first_idx = idx
        else:
            # Segunda carta seleccionada
            self.second_idx = idx
            self.lock = True
            # Esperar un momento para mostrar las dos y luego evaluar
            self.root.after(600, self.check_match)

    def check_match(self):
        """Verifica si las dos cartas seleccionadas forman un par."""
        i = self.first_idx
        j = self.second_idx

        title1, icon1 = self.values[i]
        title2, icon2 = self.values[j]

        self.tries += 1
        self.tries_var.set(f"Intentos: {self.tries}")

        if title1 == title2 and icon1 == icon2:
            # Es un par correcto
            self.buttons[i].config(state="disabled", bg="#d5f5e3")
            self.buttons[j].config(state="disabled", bg="#d5f5e3")
            self.found_pairs += 1
            self.found_var.set(f"Pares encontrados: {self.found_pairs} / {self.total_pairs}")
            if self.found_pairs == self.total_pairs:
                self.tries_var.set(f"¡Ganaste! Intentos totales: {self.tries}")
        else:
            # No son iguales, las volteamos nuevamente
            self.buttons[i].config(text="", bg="#e6e6e6")
            self.buttons[j].config(text="", bg="#e6e6e6")

        # Reset selección
        self.first_idx = None
        self.second_idx = None
        self.lock = False

    # ==========================
    # REINICIAR JUEGO
    # ==========================
    def reset_game(self):
        """Reinicia el tablero con las cartas mezcladas nuevamente."""
        random.shuffle(self.values)
        self.first_idx = None
        self.second_idx = None
        self.lock = False
        self.tries = 0
        self.found_pairs = 0
        self.tries_var.set("Intentos: 0")
        self.found_var.set(f"Pares encontrados: 0 / {self.total_pairs}")

        for b in self.buttons:
            b.config(text="", state="normal", bg="#e6e6e6")


# ==========================
# PUNTO DE ENTRADA
# ==========================

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryGamePR(root)
    root.mainloop()
