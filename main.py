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

        self.player_img = ImageTk.PhotoImage(Image.open("assets/player/player.png"))
        self.player = self.canvas.create_image(
            self.player_x * map.TILE_SIZE + map.X_OFFSET,
            self.player_y * map.TILE_SIZE + map.Y_OFFSET,
            image=self.player_img, anchor="nw"
        )

        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<KeyPress>", self.handle_keypress)

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

    def handle_keypress(self, event):
        if event.keysym == "Up":
            self.player.move_player(0, -1)
        elif event.keysym == "Down":
            self.player.move_player(0, 1)
        elif event.keysym == "Left":
            self.player.move_player(-1, 0)
        elif event.keysym == "Right":
            self.player.move_player(1, 0)

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

    
    def handle_keypress(self, event):
        new_x, new_y = self.player_x, self.player_y

        if event.keysym == 'Up':
            new_y -= 1
        elif event.keysym == 'Down':
            new_y += 1
        elif event.keysym == 'Left':
            new_x -= 1
        elif event.keysym == 'Right':
            new_x += 1

        if self.is_valid_move(new_x, new_y):
            self.player_x, self.player_y = new_x, new_y
            self.canvas.coords(
                self.player,
                self.player_x * map.TILE_SIZE + map.X_OFFSET,
                self.player_y * map.TILE_SIZE + map.Y_OFFSET
            )



    def is_valid_move(self, x, y):
        # Verificar se a posição está dentro dos limites do mapa
        if 0 <= x < len(map.MAP[0]) and 0 <= y < len(map.MAP):
            # Verificar se a posição é uma tile válida
            return map.MAP[y][x] == 1
        return False



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
    if index_gif == len(imgs):
        index_gif = 0
    label_gif.configure(image=imgs[index_gif])
    index_gif += 1
    window.after(100, update_gif)

update_gif()

img_start = ImageTk.PhotoImage(file="assets/menu/btn_start.png")
img_quit = ImageTk.PhotoImage(file="assets/menu/btn_quit.png")

btn_start = tk.Button(window, image=img_start, command=start_game, borderwidth=0, highlightthickness=0)
btn_start.place(relx=0.5, rely=0.8, anchor="center", width=150, height=67)

btn_quit = tk.Button(window, image=img_quit, command=quit_game, borderwidth=0, highlightthickness=0)
btn_quit.place(relx=0.5, rely=0.9, anchor="center", width=150, height=67)

window.mainloop()

