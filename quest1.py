import tkinter as tk
import map


class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=1280, height=720, bg='black')
        self.canvas.pack()

        self.lever_state = "lever_up"
        self.gate_state = "gate_closed"
        self.lock_state = "lock"
        self.door_state = "door_closed"
        self.special_room_visible = False

        map.create_special_room(self.canvas, visibility="hidden")
        map.create_map(self.canvas)
        map.create_interactive_elements(self.canvas, self.lever_state, self.gate_state, self.lock_state, self.door_state)

        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        x, y = event.x, event.y

        lever_info = map.interaction_element[self.lever_state]
        lever_x = lever_info["position"][0] * map.TILE_SIZE + lever_info["position"][2] + map.X_OFFSET
        lever_y = lever_info["position"][1] * map.TILE_SIZE + lever_info["position"][3] + map.Y_OFFSET

        lock_info = map.interaction_element[self.lock_state]
        lock_x = lock_info["position"][0] * map.TILE_SIZE + lock_info["position"][2] + map.X_OFFSET
        lock_y = lock_info["position"][1] * map.TILE_SIZE + lock_info["position"][3] + map.Y_OFFSET

        if lever_x <= x <= lever_x + map.TILE_SIZE and lever_y <= y <= lever_y + map.TILE_SIZE:
            self.toggle_lever()
        elif lock_x <= x <= lock_x + map.TILE_SIZE and lock_y <= y <= lock_y + map.TILE_SIZE:
            self.toggle_lock()

    def toggle_lever(self):
        self.lever_state = "lever_down" if self.lever_state == "lever_up" else "lever_up"
        self.gate_state = "gate_open" if self.gate_state == "gate_closed" else "gate_closed"

        map.update_lever_state(self.canvas, self.lever_state)
        map.update_gate_state(self.canvas, self.gate_state)

        if self.lever_state == "lever_down":
            self.show_special_room()

    def toggle_lock(self):
        self.lock_state = "lock_key" if self.lock_state == "lock" else "lock"
        self.door_state = "door_open" if self.door_state == "door_closed" else "door_closed"

        map.update_lock_state(self.canvas, self.lock_state)
        map.update_door_state(self.canvas, self.door_state)

    def show_special_room(self):
        if not self.special_room_visible:
            self.special_room_visible = True
            map.toggle_special_room_visibility(self.canvas, visibility="normal")

def start_game():
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

