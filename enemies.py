import tkinter as tk
from PIL import Image, ImageSequence, ImageTk
import numpy as np
import map
from player import load_gif

class MimicChest:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.current_frame = 0
        self.mimic_hp = 5
        self.mimic_alive = True
        self.mimic_moving = False
        self.animations = self.load_animations()
        self.current_animation = self.animations["move_down"]
        self.image = self.canvas.create_image(self.x, self.y, image=self.current_animation[0])
        self.update_animation()

    def load_animations(self):
        return {
            "move_down": load_gif("assets/mob_mimic_chest/move/move_down.gif"),
            "move_left": load_gif("assets/mob_mimic_chest/move/move_left.gif"),
            "move_right": load_gif("assets/mob_mimic_chest/move/move_right.gif"),
            "move_up": load_gif("assets/mob_mimic_chest/move/move_up.gif"),
            "damage_down": load_gif("assets/mob_mimic_chest/damage/damage_down.gif"),
            "damage_left": load_gif("assets/mob_mimic_chest/damage/damage_left.gif"),
            "damage_right": load_gif("assets/mob_mimic_chest/damage/damage_right.gif"),
            "damage_up": load_gif("assets/mob_mimic_chest/damage/damage_up.gif"),
        }

    def update_animation(self):
        if self.mimic_alive and self.mimic_moving:
            if self.current_frame >= len(self.current_animation):
                self.current_frame = 0
            self.canvas.itemconfig(self.image, image=self.current_animation[self.current_frame])
            self.current_frame += 1
            self.canvas.after(500, self.update_animation)

    def smooth_move(self, target_x, target_y, direction):
        current_x, current_y = self.canvas.coords(self.image)
        step_x = (target_x - current_x) / 50
        step_y = (target_y - current_y) / 50

        for i in range(10):
            self.canvas.after(i * 50, lambda i=i: self.canvas.move(self.image, step_x, step_y))

        if direction in self.animations:
            self.canvas.after(500, lambda: self.canvas.itemconfig(self.image, image=self.animations[direction][0]))

    def reverse_direction(self, direction):
        directions = {"up": "down", "down": "up", "left": "right", "right": "left"}
        return directions.get(direction, "down") 

    def take_damage(self, direction):
        if self.mimic_alive:
            self.mimic_hp -= 1
            if self.mimic_hp <= 0:
                self.mimic_alive = False
                self.canvas.delete(self.image)
            else:
                if f"damage_{direction}" in self.animations: 
                    self.current_animation = self.animations[f"damage_{direction}"]
                    self.current_frame = 0
                    self.update_damage_animation()

    def update_damage_animation(self):
        if self.mimic_alive and self.current_frame < len(self.current_animation):
            self.canvas.itemconfig(self.image, image=self.current_animation[self.current_frame])
            self.current_frame += 1
            self.canvas.after(100, self.update_damage_animation)
        else:
            self.current_frame = 0

            if "move_down" in self.animations:
                self.current_animation = self.animations["move_down"]
                self.update_animation()

    def is_valid_move(self, x, y):
        tile_x = (x - map.X_OFFSET) // map.TILE_SIZE
        tile_y = (y - map.Y_OFFSET) // map.TILE_SIZE
        if 0 <= tile_x < len(map.MAP[0]) and 0 <= tile_y < len(map.MAP):
            return map.MAP[tile_y][tile_x] == 1
        return False


class Boss:
    def __init__(self, canvas, x, y, player):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.player = player
        self.boss_images = {
            "move": {
                "down": self.load_gif("assets/boss/move/boss_move_down.gif"),
                "left": self.load_gif("assets/boss/move/boss_move_left.gif"),
                "right": self.load_gif("assets/boss/move/boss_move_right.gif"),
                "up": self.load_gif("assets/boss/move/boss_move_up.gif"),
            },
            "attack": {
                "down": self.load_gif("assets/boss/attack/boss_attack_down.gif"),
                "left": self.load_gif("assets/boss/attack/boss_attack_left.gif"),
                "right": self.load_gif("assets/boss/attack/boss_attack_right.gif"),
                "up": self.load_gif("assets/boss/attack/boss_attack_up.gif"),
            },
            "damage": {
                "down": self.load_gif("assets/boss/damage/boss_damage_down.gif"),
                "left": self.load_gif("assets/boss/damage/boss_damage_left.gif"),
                "right": self.load_gif("assets/boss/damage/boss_damage_right.gif"),
                "up": self.load_gif("assets/boss/damage/boss_damage_up.gif"),
            },
            "death": self.load_gif("assets/boss/death/boss_death.gif")
        }
        self.image = self.canvas.create_image(x, y, image=self.boss_images["move"]["down"][0], state=tk.HIDDEN)
        self.is_visible = False
        self.is_moving = False
        self.boss_alive = True
        self.boss_hp = 100
        self.direction = "down"
        self.animation_speed = 150  # Intervalo de atualização da animação em ms (ajustado para ser mais lento)
        self.animation_index = 0
        self.movement_speed = self.animation_speed  # Utilize o mesmo intervalo para movimentos e animações
        self.step_size = 2  # Tamanho do passo em pixels
        self.attack_cooldown = 1000  # Intervalo de tempo entre ataques em ms
        self.can_attack = True
        self.after_id = None
        self.animation_id = None
        self.movement_id = None  # Adicionei este atributo para controlar a movimentação

    def load_gif(self, gif_path):
        return [tk.PhotoImage(file=gif_path, format=f'gif -index {i}') for i in range(4)]

    def reveal(self):
        self.is_visible = True
        self.canvas.itemconfig(self.image, state=tk.NORMAL)

    def start_movement(self):
        if self.is_visible and not self.is_moving:
            self.is_moving = True
            self.animate()  # Iniciar animação contínua
            self.move_towards_player()

    def move_towards_player(self):
        if not self.is_visible or not self.is_moving:
            return

        player_coords = self.canvas.coords(self.player.image)
        if self.is_near_player(player_coords) and self.can_attack:
            self.attack()
        else:
            direction = self.get_direction(player_coords)
            self.update_position(direction)
            self.movement_id = self.canvas.after(self.movement_speed, self.move_towards_player)

    def update_position(self, direction):
        target_x, target_y = self.x, self.y
        if direction == "left":
            target_x -= self.step_size
        elif direction == "right":
            target_x += self.step_size
        elif direction == "up":
            target_y -= self.step_size
        elif direction == "down":
            target_y += self.step_size

        self.x, self.y = target_x, target_y
        self.canvas.coords(self.image, self.x, self.y)
        self.direction = direction

    def get_direction(self, player_coords):
        player_x, player_y = player_coords
        if abs(self.x - player_x) > abs(self.y - player_y):
            return "left" if self.x > player_x else "right"
        else:
            return "up" if self.y > player_y else "down"

    def animate(self):
        frames = self.boss_images["move"][self.direction]
        self.canvas.itemconfig(self.image, image=frames[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(frames)
        self.animation_id = self.canvas.after(self.animation_speed, self.animate)

    def attack(self):
        if not self.is_visible or not self.can_attack:
            return

        self.can_attack = False  # Desabilita a capacidade de atacar até que o cooldown termine

        # Parar a animação e movimento atual
        if self.movement_id:
            self.canvas.after_cancel(self.movement_id)
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)

        frames = self.boss_images["attack"][self.direction]
        self.canvas.itemconfig(self.image, image=frames[0])
        self.canvas.after(self.animation_speed, self.update_attack_animation, frames, 1)

        # Simula o dano no jogador
        self.player.receive_damage(10)

    def update_attack_animation(self, frames, frame_index):
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.canvas.after(self.animation_speed, self.update_attack_animation, frames, frame_index + 1)
        else:
            # Após o ataque, retomar a animação de movimento e continuar o movimento
            self.animate()
            self.move_towards_player()
            # Inicia o cooldown de ataque
            self.canvas.after(self.attack_cooldown, self.reset_attack)

    def reset_attack(self):
        self.can_attack = True

    def take_damage(self, direction):
        if self.boss_alive:
            self.boss_hp -= 10
            if self.boss_hp <= 0:
                self.die()
            else:
                frames = self.boss_images["damage"][direction]
                self.update_damage_animation(frames, 0)

    def update_damage_animation(self, frames, frame_index):
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.canvas.after(self.animation_speed, self.update_damage_animation, frames, frame_index + 1)
        else:
            # Após sofrer dano, retomar a animação de movimento e continuar o movimento
            self.animate()
            self.move_towards_player()

    def die(self):
        self.boss_alive = False
        frames = self.boss_images["death"]
        self.update_death_animation(frames, 0)

    def update_death_animation(self, frames, frame_index):
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.canvas.after(self.animation_speed, self.update_death_animation, frames, frame_index + 1)
        else:
            self.canvas.delete(self.image)

    def is_near_player(self, player_coords):
        player_x, player_y = player_coords
        return abs(self.x - player_x) < 20 and abs(self.y - player_y) < 20

