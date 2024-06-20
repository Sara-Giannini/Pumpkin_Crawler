import tkinter as tk
import map

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=1280, height=720)
        self.canvas.pack()

        self.lever_state = "lever_up"
        self.gate_state = "gate_closed"

        map.create_map(self.canvas)
        map.create_interactive_elements(self.canvas, self.lever_state, self.gate_state)

        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        # Coordenadas do clique
        x, y = event.x, event.y

        # Obtendo a posição dos itens
        lever_info = map.interaction_element[self.lever_state]
        gate_info = map.interaction_element[self.gate_state]

        lever_x = lever_info["position"][0] * map.TILE_SIZE + lever_info["position"][2] + map.X_OFFSET
        lever_y = lever_info["position"][1] * map.TILE_SIZE + lever_info["position"][3] + map.Y_OFFSET

        gate_x = gate_info["position"][0] * map.TILE_SIZE + gate_info["position"][2] + map.X_OFFSET
        gate_y = gate_info["position"][1] * map.TILE_SIZE + gate_info["position"][3] + map.Y_OFFSET

        # Verificando se o clique foi na alavanca
        if lever_x <= x <= lever_x + map.TILE_SIZE and lever_y <= y <= lever_y + map.TILE_SIZE:
            self.toggle_lever()

    def toggle_lever(self):
        self.lever_state = "lever_down" if self.lever_state == "lever_up" else "lever_up"
        self.gate_state = "gate_open" if self.gate_state == "gate_closed" else "gate_closed"

        map.update_lever_state(self.canvas, self.lever_state)
        map.update_gate_state(self.canvas, self.gate_state)

def start_game():
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

