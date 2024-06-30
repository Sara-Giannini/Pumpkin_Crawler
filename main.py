import tkinter as tk
import map
from player import MimicChest, Player, load_gif
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=1280, height=720, bg='black')
        self.canvas.pack()

        self.player_x = 25
        self.player_y = 8
        self.lever_state = "lever_up"
        self.gate_state = "gate_closed"
        self.lock_state = "keyless_lock"
        self.door_state = "door_closed"
        self.boss_room_visible = False

        map.create_boss_room(self.canvas, visibility="hidden")
        map.create_map(self.canvas)
        map.create_interactions(self.canvas, self.lever_state, self.gate_state, self.lock_state, self.door_state)

        self.player = Player(self.canvas, self.player_x * map.TILE_SIZE + map.X_OFFSET, self.player_y * map.TILE_SIZE + map.Y_OFFSET)

        self.mimic_x = 6
        self.mimic_y = 17
        self.mimic = MimicChest(self.canvas, self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET)

        self.root.bind("<KeyPress>", self.handle_keypress)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.update_map_for_states()
        self.after_id_mimic = None
        self.key_anim_id = None

    def handle_keypress(self, event):
        if event.keysym == 'e':
            self.handle_interaction()
        else:
            self.player.handle_keypress(event)

    def on_click(self, event):
        x, y = event.x, event.y
        tile_x = (x - map.X_OFFSET) // map.TILE_SIZE
        tile_y = (y - map.Y_OFFSET) // map.TILE_SIZE
        if self.is_valid_move(tile_x, tile_y):
            self.player.move_towards(tile_x * map.TILE_SIZE + map.X_OFFSET, tile_y * map.TILE_SIZE + map.Y_OFFSET)

    def on_right_click(self, event):
        self.player.attack()
        if self.is_near_player(self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET):
            self.mimic.mimic_hp -= 1
            direction = self.get_direction(self.mimic_x, self.mimic_y, self.player_x, self.player_y)
            self.canvas.itemconfig(self.mimic.image, image=self.mimic.animations[f"damage_{direction}"][0])
            if self.mimic.mimic_hp <= 0 and self.mimic.mimic_alive:
                self.mimic.mimic_alive = False
                self.canvas.delete(self.mimic.image)
                self.key_image = load_gif("assets/keys/key_1.gif")
                self.key = self.canvas.create_image(self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET, image=self.key_image[0])
                self.animate_key()
                self.canvas.tag_raise(self.key)
            else:
                self.mimic.mimic_moving = True
                self.start_mimic_animation()

    def handle_interaction(self):
        lever_info = map.interactions[self.lever_state]
        lever_x = lever_info["position"][0] * map.TILE_SIZE + lever_info["position"][2] + map.X_OFFSET
        lever_y = lever_info["position"][1] * map.TILE_SIZE + lever_info["position"][3] + map.Y_OFFSET

        lock_info = map.interactions[self.lock_state]
        lock_x = lock_info["position"][0] * map.TILE_SIZE + lock_info["position"][2] + map.X_OFFSET
        lock_y = lock_info["position"][1] * map.TILE_SIZE + lock_info["position"][3] + map.Y_OFFSET

        if self.is_near_player(lever_x, lever_y):
            self.toggle_lever()
        elif self.is_near_player(lock_x, lock_y):
            if self.player_has_key:
                self.toggle_lock()
        elif self.is_near_player(self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET):
            self.mimic.mimic_moving = True
            self.start_mimic_animation()

        if self.key and self.is_near_player(self.canvas.coords(self.key)[0], self.canvas.coords(self.key)[1]):
            self.canvas.delete(self.key)
            self.key = None
            self.player_has_key = True

    def toggle_lever(self):
        self.lever_state = "lever_down" if self.lever_state == "lever_up" else "lever_up"
        self.gate_state = "gate_open" if self.gate_state == "gate_closed" else "gate_closed"

        map.update_lever_state(self.canvas, self.lever_state)
        map.update_gate_state(self.canvas, self.gate_state)

        self.update_map_for_states()

        if self.lever_state == "lever_down":
            self.show_boss_room()

    def toggle_lock(self):
        self.lock_state = "key_lock" if self.lock_state == "keyless_lock" else "keyless_lock"
        self.door_state = "door_open" if self.door_state == "door_closed" else "door_closed"

        map.update_lock_state(self.canvas, self.lock_state)
        map.update_door_state(self.canvas, self.door_state)

        self.update_map_for_states()

    def show_boss_room(self):
        if not self.boss_room_visible:
            self.boss_room_visible = True
            map.toggle_boss_room_visibility(self.canvas, visibility="normal")

    def update_map_for_states(self):
        gate_pos = map.interactions["gate_closed"]["position"]
        door_pos = map.interactions["door_closed"]["position"]

        gate_x, gate_y = gate_pos[0], gate_pos[1]
        door_x, door_y = door_pos[0], door_pos[1]

        map.MAP[gate_y][gate_x] = 0 if self.gate_state == "gate_closed" else 1
        map.MAP[door_y][door_x] = 0 if self.door_state == "door_closed" else 1

    def is_valid_move(self, x, y):
        if 0 <= x < len(map.MAP[0]) and 0 <= y < len(map.MAP):
            if map.MAP[y][x] == 1:
                return True
        return False

    def is_near_player(self, element_x, element_y, max_distance=64):
        player_px = self.player.x
        player_py = self.player.y
        distance = ((player_px - element_x) ** 2 + (player_py - element_y) ** 2) ** 0.5
        return distance <= max_distance

    def get_direction(self, from_x, from_y, to_x, to_y):
        if abs(from_x - to_x) > abs(from_y - to_y):
            return "left" if from_x > to_x else "right"
        else:
            return "up" if from_y > to_y else "down"

    def start_mimic_animation(self):
        if self.after_id_mimic:
            self.root.after_cancel(self.after_id_mimic)
        self.update_mimic_animation()

    def update_mimic_animation(self):
        if self.mimic.mimic_alive and self.mimic.mimic_moving:
            if self.mimic.current_frame >= len(self.mimic.current_animation):
                self.mimic.current_frame = 0

            direction = random.choice(["up", "down", "left", "right"])
            new_x, new_y = self.move_item(self.mimic.image, direction, self.mimic_x, self.mimic_y)

            if not self.is_valid_move(new_x, new_y):
                direction = self.reverse_direction(direction)
                new_x, new_y = self.move_item(self.mimic.image, direction, self.mimic_x, self.mimic_y)

            if self.is_valid_move(new_x, new_y):
                self.mimic_x, self.mimic_y = new_x, new_y
                self.mimic.current_animation = self.mimic.animations[direction]

                self.smooth_move(self.mimic.image, self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET, direction)
                self.mimic.current_frame += 1

            self.after_id_mimic = self.root.after(500, self.update_mimic_animation)

    def smooth_move(self, item, target_x, target_y, direction):
        current_x, current_y = self.canvas.coords(item)
        step_x = (target_x - current_x) / 50
        step_y = (target_y - current_y) / 50

        for i in range(10):
            self.root.after(i * 50, lambda i=i: self.canvas.move(item, step_x, step_y))
        self.root.after(500, lambda: self.canvas.itemconfig(item, image=self.mimic.animations[direction][0]))

    def reverse_direction(self, direction):
        directions = {"up": "down", "down": "up", "left": "right", "right": "left"}
        return directions[direction]

    def move_item(self, item, direction, x, y):
        if direction == "up":
            return x, y - 1
        elif direction == "down":
            return x, y + 1
        elif direction == "left":
            return x - 1, y
        elif direction == "right":
            return x + 1, y

    def animate_key(self):
        def update_key_animation(frame_index):
            self.canvas.itemconfig(self.key, image=self.key_image[frame_index])
            next_frame_index = (frame_index + 1) % len(self.key_image)
            self.key_anim_id = self.root.after(100, update_key_animation, next_frame_index)

        if self.key_image:
            update_key_animation(0)



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

