import tkinter as tk
from PIL import Image, ImageSequence, ImageTk
import map
from player import Player

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=1280, height=720, bg='black')
        self.canvas.pack()

        self.player_x = 25
        self.player_y = 8

        self.lever_state = "lever_up"
        self.gate_state = "gate_closed"
        self.lock_state = "lock"
        self.door_state = "door_closed"
        self.special_room_visible = False

        map.create_special_room(self.canvas, visibility="hidden")
        map.create_map(self.canvas)
        map.create_interactive_elements(self.canvas, self.lever_state, self.gate_state, self.lock_state, self.door_state)

        self.player = Player(self.canvas, self.player_x * map.TILE_SIZE + map.X_OFFSET, self.player_y * map.TILE_SIZE + map.Y_OFFSET)

        self.root.bind("<KeyPress>", self.handle_keypress)
        self.root.bind("<KeyRelease>", self.handle_keyrelease)
        self.canvas.bind("<Button-1>", self.on_click)

    def handle_keypress(self, event):
        if event.keysym == 'e':
            self.handle_interaction()

    def handle_keyrelease(self, event):
        pass

    def on_click(self, event):
        x, y = event.x, event.y
        tile_x = (x - map.X_OFFSET) // map.TILE_SIZE
        tile_y = (y - map.Y_OFFSET) // map.TILE_SIZE
        if self.is_valid_move(tile_x, tile_y):
            self.player.move_towards(tile_x * map.TILE_SIZE + map.X_OFFSET, tile_y * map.TILE_SIZE + map.Y_OFFSET)

    def handle_interaction(self):
        lever_info = map.interaction_element[self.lever_state]
        lever_x = lever_info["position"][0] * map.TILE_SIZE + lever_info["position"][2] + map.X_OFFSET
        lever_y = lever_info["position"][1] * map.TILE_SIZE + lever_info["position"][3] + map.Y_OFFSET

        lock_info = map.interaction_element[self.lock_state]
        lock_x = lock_info["position"][0] * map.TILE_SIZE + lock_info["position"][2] + map.X_OFFSET
        lock_y = lock_info["position"][1] * map.TILE_SIZE + lock_info["position"][3] + map.Y_OFFSET

        if self.is_near_player(lever_x, lever_y):
            self.toggle_lever()
        elif self.is_near_player(lock_x, lock_y):
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

    def is_valid_move(self, x, y):
        if 0 <= x < len(map.MAP[0]) and 0 <= y < len(map.MAP):
            return map.MAP[y][x] == 1
        return False

    def is_near_player(self, element_x, element_y, max_distance=64):
        player_px = self.player.x
        player_py = self.player.y
        distance = ((player_px - element_x) ** 2 + (player_py - element_y) ** 2) ** 0.5
        return distance <= max_distance

def load_gif(gif_path):
    imgs = []
    with Image.open(gif_path) as img:
        for frame in ImageSequence.Iterator(img):
            img_pil = frame.convert('RGB')
            img_tk = ImageTk.PhotoImage(img_pil)
            imgs.append(img_tk)
    return imgs

def start_game():
    window.destroy()
    game_root = tk.Tk()
    game = Game(game_root)
    game_root.mainloop()

def quit_game():
    print("Saindo...")
    window.destroy()

window = tk.Tk()
window.title("Menu Principal")
window.geometry("1920x1080")

imgs = load_gif("assets/menu/giff.gif")

canvas_gif = tk.Canvas(window, width=1920, height=1080)
canvas_gif.pack()

label_gif = tk.Label(canvas_gif, image=imgs[0])
label_gif.pack()

index_gif = 0
def update_gif():
    global index_gif, imgs
    index_gif = (index_gif + 1) % len(imgs)
    label_gif.config(image=imgs[index_gif])
    window.after(100, update_gif)

update_gif()

img_start = tk.PhotoImage(file="assets/menu/btn_start.png")
img_quit = tk.PhotoImage(file="assets/menu/btn_quit.png")

btn_start = tk.Button(window, image=img_start, command=start_game, borderwidth=0, highlightthickness=0)
btn_start.place(relx=0.5, rely=0.8, anchor="center", width=150, height=67)

btn_quit = tk.Button(window, image=img_quit, command=quit_game, borderwidth=0, highlightthickness=0)
btn_quit.place(relx=0.5, rely=0.9, anchor="center", width=150, height=67)

window.mainloop()

