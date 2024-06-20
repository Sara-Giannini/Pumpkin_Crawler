import tkinter as tk
from PIL import Image, ImageTk
from map import load_individual_images, TILE_SIZE, adjust_image_position

class InteractionHandler:
    def __init__(self, game_canvas):
        self.game_canvas = game_canvas
        self.individual_images = load_individual_images()
        self.animation_frames = {}
        self.setup_animations()
        self.setup_initial_state()

    def setup_animations(self):
        for key, data in self.individual_images.items():
            if "animation_images" in data:
                self.animation_frames[key] = {
                    "images": data["animation_images"],
                    "frame": 0  # Inicializa o frame de animação para 0
                }

    def setup_initial_state(self):
        # Desenha todos os elementos iniciais (exceto a alavanca e a porta)
        for key, data in self.individual_images.items():
            if key not in ["lever_up", "lever_down", "door_2_closed", "door_2_open"]:
                image_file = data["file"]
                x, y, offset_x, offset_y = data["position"]
                adjusted_x = x * TILE_SIZE + offset_x
                adjusted_y = y * TILE_SIZE + offset_y
                image = tk.PhotoImage(file=image_file)
                self.game_canvas.create_image(adjusted_x, adjusted_y, image=image, anchor=tk.SW)
                self.individual_images[key]["image"] = image

        # Inicializa com a porta fechada e a alavanca para cima
        self.toggle_door("door_2_closed")
        self.toggle_lever("lever_up")

    def handle_interaction(self, event, player_x, player_y):
        canvas_x = event.x // TILE_SIZE
        canvas_y = event.y // TILE_SIZE

        for key, data in self.individual_images.items():
            if (canvas_x, canvas_y) == data["position"]:
                if "lever" in key:
                    self.toggle_lever(key)
                    break

    def toggle_lever(self, lever_key):
        lever_data = self.individual_images[lever_key]
        current_frame = self.animation_frames[lever_key]["frame"]

        # Atualiza o frame da animação da alavanca
        current_frame = (current_frame + 1) % len(lever_data["images"])
        self.animation_frames[lever_key]["frame"] = current_frame

        lever_image = self.animation_frames[lever_key]["images"][current_frame]
        x, y, offset_x, offset_y = lever_data["position"]
        adjusted_x = x * TILE_SIZE + offset_x
        adjusted_y = y * TILE_SIZE + offset_y
        self.game_canvas.create_image(adjusted_x, adjusted_y, image=lever_image, anchor=tk.SW)

        # Verifica se a alavanca foi movida para baixo
        if lever_key == "lever_up" and not lever_data["locked"]:
            self.open_door()

    def toggle_door(self, door_key):
        door_data = self.individual_images[door_key]
        door_image_file = door_data["file"]
        x, y, offset_x, offset_y = door_data["position"]
        adjusted_x = x * TILE_SIZE + offset_x
        adjusted_y = y * TILE_SIZE + offset_y
        door_image = tk.PhotoImage(file=door_image_file)
        self.game_canvas.create_image(adjusted_x, adjusted_y, image=door_image, anchor=tk.SW)
        self.individual_images[door_key]["image"] = door_image

    def open_door(self):
        self.toggle_door("door_2_open")
        self.individual_images["door_2_closed"]["locked"] = False
        self.individual_images["lever_up"]["locked"] = False
        self.toggle_lever("lever_down")


