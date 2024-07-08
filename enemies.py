import random
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import map
from player import load_gif


class MimicChest:
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.hp = self.max_hp = 150
        self.mimic_alive = True
        self.mimic_moving = False
        self.animations = self.load_animations()
        self.current_animation = self.animations["move_down"]
        self.current_frame = 0
        self.image = self.canvas.create_image(self.x, self.y, image=self.current_animation[0], anchor='nw')
        self.after_id_mimic = None
        self.health_bar = self.canvas.create_rectangle(self.x, self.y - 10, self.x + 50, self.y - 5, fill='orange')
        self.canvas.itemconfig(self.health_bar, state='hidden')
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

    def move(self):
        if self.mimic_alive:
            direction = np.random.choice(["up", "down", "left", "right"])
            move_offset = {"up": (0, -10), "down": (0, 10), "left": (-10, 0), "right": (10, 0)}
            dx, dy = move_offset[direction]
            self.update_position(self.x + dx, self.y + dy)

    def start_mimic_animation(self):
        """Inicia a animação do baú mímico."""
        try:
            if self.after_id_mimic:
                self.root.after_cancel(self.after_id_mimic)
            self.update_animation()
        except Exception as e:
            print(f"Erro ao iniciar animação do baú mímico: {e}")

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
            self.canvas.after(i * 50, self.update_health_bar)  # Atualiza a barra durante o movimento

        if direction in self.animations:
            self.canvas.after(500, lambda: self.canvas.itemconfig(self.image, image=self.animations[direction][0]))

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.canvas.coords(self.image, self.x, self.y)
        self.update_health_bar()

    def is_valid_move(self, x, y):
        tile_x = (x - map.X_OFFSET) // map.TILE_SIZE
        tile_y = (y - map.Y_OFFSET) // map.TILE_SIZE
        if 0 <= tile_x < len(map.MAP[0]) and 0 <= tile_y < len(map.MAP):
            return map.MAP[tile_y][tile_x] == 1
        return False

    def take_damage(self, direction):
        if self.mimic_alive:
            self.hp -= 10
            print(f"Mimic Chest recebeu dano. HP restante: {self.hp}")
            if self.hp < self.max_hp:
                self.canvas.itemconfig(self.health_bar, state='normal')
            self.update_health_bar()
            if self.hp <= 0:
                self.die()
            else:
                if f"damage_{direction}" in self.animations:
                    self.current_animation = self.animations[f"damage_{direction}"]
                    self.current_frame = 0
                    self.update_damage_animation()

    def update_health_bar(self):
        health_ratio = max(self.hp / self.max_hp, 0)
        self.canvas.coords(self.health_bar, self.x, self.y - 10, self.x + health_ratio * 50, self.y - 5)

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

    def die(self):
        self.mimic_alive = False
        self.canvas.delete(self.image)
        self.canvas.delete(self.health_bar)
        print("Mimic Chest foi derrotado")
        self.drop_key()

    def drop_key(self):
        """Dropa uma chave na posição onde o baú mímico morreu."""
        try:
            self.key_image = load_gif("assets/keys/mimic_key.gif")
            self.key = self.canvas.create_image(self.x, self.y, image=self.key_image[0])
            self.canvas.tag_raise(self.key)
            self.root.keys_on_canvas.append((self.key, self.x, self.y, "mimic"))  # Adiciona a chave à lista de chaves no canvas
            self.animate_key()
        except Exception as e:
            print(f"Erro ao dropar chave: {e}")

    def animate_key(self):
        """Inicia a animação da chave."""
        try:
            self.key_anim_id = self.root.after(100, self.update_key_animation)
        except Exception as e:
            print(f"Erro ao iniciar animação da chave: {e}")

    def update_key_animation(self):
        """Atualiza a animação da chave."""
        try:
            if self.key_anim_id:
                self.canvas.after_cancel(self.key_anim_id)
            self.key_image.append(self.key_image.pop(0))
            self.canvas.itemconfig(self.key, image=self.key_image[0])
            self.key_anim_id = self.root.after(100, self.update_key_animation)
        except Exception as e:
            print(f"Erro ao atualizar animação da chave: {e}")


class Boss:
    def __init__(self, root, canvas, x, y, player):
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.player = player
        self.keys_on_canvas = []
        self.boss_images = self.load_animations()
        self.image = self.canvas.create_image(x, y, image=self.boss_images["move"]["down"][0], state=tk.HIDDEN)
        self.is_visible = False
        self.is_moving = False
        self.boss_alive = True
        self.hp = 1000
        self.max_hp = 1000
        self.direction = "down"
        self.animation_speed = 150
        self.animation_index = 0
        self.movement_speed = self.animation_speed
        self.step_size = 2
        self.attack_cooldown = 1000
        self.can_attack = True
        self.animation_id = None
        self.movement_id = None
        self.key = None
        self.key_image = None
        self.key_anim_id = None
        self.health_bar = self.canvas.create_rectangle(self.x, self.y - 30, self.x + self.hp / self.max_hp * 50, self.y - 25, fill='red')
        self.canvas.itemconfig(self.health_bar, state='hidden')

    def load_animations(self):
        return {
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

    def load_gif(self, gif_path):
        return [tk.PhotoImage(file=gif_path, format=f'gif -index {i}') for i in range(4)]

    def reveal(self):
        self.is_visible = True
        self.canvas.itemconfig(self.image, state=tk.NORMAL)
        self.canvas.itemconfig(self.health_bar, state='normal')

    def start_movement(self):
        if self.is_visible and not self.is_moving:
            self.is_moving = True
            if self.animation_id is None:
                self.animate()
            if self.movement_id is None:
                self.move_towards_player()

    def move_towards_player(self):
        if not self.is_visible or not self.is_moving or not self.boss_alive:
            return
        player_coords = self.canvas.coords(self.player.image)
        if self.is_near_player(player_coords) and self.can_attack:
            self.attack()
        else:
            direction_vector = self.get_direction_vector(player_coords)
            self.update_position(direction_vector)
            self.movement_id = self.canvas.after(self.movement_speed, self.move_towards_player)

    def is_near_player(self, player_coords):
        player_x, player_y = player_coords
        return abs(self.x - player_x) < 20 and abs(self.y - player_y) < 20

    def update_position(self, direction_vector):
        target_x = self.x + direction_vector[0] * self.step_size
        target_y = self.y + direction_vector[1] * self.step_size
        self.x, self.y = target_x, target_y
        self.canvas.coords(self.image, self.x, self.y)
        self.direction = self.get_closest_direction(direction_vector)
        self.update_health_bar()

    def get_direction_vector(self, player_coords):
        player_x, player_y = player_coords
        direction_vector = np.array([player_x - self.x, player_y - self.y])
        norm = np.linalg.norm(direction_vector)
        if norm == 0:
            return np.array([0, 0])
        return direction_vector / norm

    def get_closest_direction(self, direction_vector):
        directions = {
            "left": np.array([-1, 0]),
            "right": np.array([1, 0]),
            "up": np.array([0, -1]),
            "down": np.array([0, 1]),
        }
        closest_direction = min(directions.keys(), key=lambda k: np.linalg.norm(direction_vector - directions[k]))
        return closest_direction

    def animate(self):
        if not self.boss_alive:
            return
        if self.animation_id is not None:
            self.canvas.after_cancel(self.animation_id)
        frames = self.boss_images["move"][self.direction]
        self.canvas.itemconfig(self.image, image=frames[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(frames)
        self.animation_id = self.canvas.after(self.animation_speed, self.animate)

    def attack(self):
        if not self.is_visible or not self.can_attack or not self.boss_alive:
            return
        self.can_attack = False
        if self.movement_id:
            self.canvas.after_cancel(self.movement_id)
            self.movement_id = None
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        frames = self.boss_images["attack"][self.direction]
        self.canvas.itemconfig(self.image, image=frames[0])
        self.canvas.after(self.animation_speed, self.update_attack_animation, frames, 1)
        self.player.receive_damage(20)

    def update_attack_animation(self, frames, frame_index):
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.canvas.after(self.animation_speed, self.update_attack_animation, frames, frame_index + 1)
        else:
            self.animate()
            self.move_towards_player()
            self.canvas.after(self.attack_cooldown, self.reset_attack)

    def reset_attack(self):
        if self.boss_alive:
            self.can_attack = True

    def take_damage(self, direction):
        if self.boss_alive:
            self.hp -= 10
            print(f"Boss recebeu dano. HP restante: {self.hp}")
            if self.hp <= self.max_hp:
                self.canvas.itemconfig(self.health_bar, state='normal')
            self.update_health_bar()
            if self.hp <= 0:
                self.die()
            else:
                if self.animation_id is not None:
                    self.canvas.after_cancel(self.animation_id)
                frames = self.boss_images["damage"][direction]
                self.update_damage_animation(frames, 0)

    def update_health_bar(self):
        health_width = self.hp / self.max_hp * 100  
        health_bar_x = self.x - health_width / 2  

        # Atualiza a health_bar no canvas
        self.canvas.coords(self.health_bar, health_bar_x, self.y - 25, health_bar_x + health_width, self.y - 30)

    def update_damage_animation(self, frames, frame_index):
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.animation_id = self.canvas.after(self.animation_speed, self.update_damage_animation, frames, frame_index + 1)
        else:
            self.animate()
            self.move_towards_player()

    def die(self):
        self.boss_alive = False
        if self.animation_id is not None:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        if self.movement_id is not None:
            self.canvas.after_cancel(self.movement_id)
            self.movement_id = None
        if self.key_anim_id is not None:
            self.canvas.after_cancel(self.key_anim_id)
            self.key_anim_id = None
        frames = self.boss_images["death"]
        self.update_death_animation(frames, 0)
        self.drop_key()

    def update_death_animation(self, frames, frame_index):
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.animation_id = self.canvas.after(self.animation_speed, self.update_death_animation, frames, frame_index + 1)
        else:
            self.remove_boss_from_canvas()
        print("Boss foi derrotado")

    def remove_boss_from_canvas(self):
        self.canvas.delete(self.image)
        self.image = None  

    def drop_key(self):
        """Dropa uma chave na posição onde o boss morreu."""
        try:
            self.key_image = self.load_gif("assets/keys/boss_key.gif")
            self.key = self.canvas.create_image(self.x, self.y, image=self.key_image[0])
            self.canvas.tag_raise(self.key)
            self.root.keys_on_canvas.append((self.key, self.x, self.y, "boss"))  # Adiciona a chave à lista de chaves no canvas
            self.animate_key()
        except Exception as e:
            print(f"Erro ao dropar chave: {e}")

    def animate_key(self):
        """Inicia a animação da chave."""
        try:
            self.key_anim_id = self.root.after(100, self.update_key_animation)
        except Exception as e:
            print(f"Erro ao iniciar animação da chave: {e}")

    def update_key_animation(self):
        """Atualiza a animação da chave."""
        try:
            if self.key_anim_id:
                self.canvas.after_cancel(self.key_anim_id)
            self.key_image.append(self.key_image.pop(0))
            self.canvas.itemconfig(self.key, image=self.key_image[0])
            self.key_anim_id = self.root.after(100, self.update_key_animation)
        except Exception as e:
            print(f"Erro ao atualizar animação da chave: {e}")
