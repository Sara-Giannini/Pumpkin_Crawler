import tkinter as tk
from PIL import Image, ImageTk

class Player:
    def __init__(self, canvas, start_position=(0, 0)):
        self.canvas = canvas
        self.position = start_position
        self.image_file = "assets/player/player.png"  
        self.load_image()
        self.draw_player()

    def load_image(self):
        self.image = Image.open(self.image_file)
        self.image = ImageTk.PhotoImage(self.image)

    def draw_player(self):
        x, y = self.position
        self.player_id = self.canvas.create_image(
            x * 32, y * 32, image=self.image, anchor="nw", tags="player"
        )

    def move_player(self, dx, dy):
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy


        if 0 <= new_x < 32 and 0 <= new_y < 32: 
            self.position = (new_x, new_y)
            self.canvas.move(self.player_id, dx * 1, dy * 1)


