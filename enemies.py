import tkinter as tk
from PIL import Image, ImageTk
import random
import numpy as np
import map


class MimicChest:
    def __init__(self, root, canvas, x, y):
        """
        Inicializa o MimicChest.


        Argumentos:
            root (tk.Tk): Referência à raiz da interface.
            canvas (tk.Canvas): O canvas onde o Mimic vai ser desenhado.
            x (int): Posição inicial x do Mimic.
            y (int): Posição inicial y do Mimic.
        """
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.hp = self.max_hp = 150
        self.mimic_alive = True
        self.mimic_moving = False
        self.mimic_active = False
        self.animations = self.load_animations()
        self.current_animation = self.animations["move_down"] # Posição inicial padrão
        self.current_frame = 0
        self.image = self.canvas.create_image(self.x, self.y, image=self.current_animation[0], anchor='nw')
        self.after_id_mimic = None
        self.after_id_animation = None
        self.health_bar = self.canvas.create_rectangle(self.x, self.y - 10, self.x + 50, self.y - 5, fill='orange') #Configuração da barra de vida
        self.canvas.itemconfig(self.health_bar, state='hidden') # A barra inicia invisivel antes do primeiro dano
        self.update_animation()

    def load_animations(self):
        """
        Carrega todas as animações do baú mímico.


        Retorna:
            dict: Dicionário contendo as animações.
        """
        return {
            "move_down": self.load_gif("assets/mob_mimic_chest/move/move_down.gif"),
            "move_left": self.load_gif("assets/mob_mimic_chest/move/move_left.gif"),
            "move_right": self.load_gif("assets/mob_mimic_chest/move/move_right.gif"),
            "move_up": self.load_gif("assets/mob_mimic_chest/move/move_up.gif"),
            "damage_down": self.load_gif("assets/mob_mimic_chest/damage/damage_down.gif"),
            "damage_left": self.load_gif("assets/mob_mimic_chest/damage/damage_left.gif"),
            "damage_right": self.load_gif("assets/mob_mimic_chest/damage/damage_right.gif"),
            "damage_up": self.load_gif("assets/mob_mimic_chest/damage/damage_up.gif"),
        }

    def load_gif(self, path):
        """
        Carrega um GIF e converte cada frame para ImageTk.PhotoImage.


        Argumentos:
            path (str): Caminho do arquivo GIF.


        Retorna:
            list: Lista de frames do GIF como objetos ImageTk.PhotoImage.
        """
        frames = []
        try:
            gif = Image.open(path)
            while True:
                frame = gif.copy()
                frame = frame.convert("RGBA")
                mask = frame.getchannel("A")
                frame = frame.convert("RGB").convert("RGBA", dither=None, colors=256)
                frame.putalpha(mask)
                frames.append(ImageTk.PhotoImage(frame))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        except Exception as e:
            print(f"Erro ao carregar GIF {path}: {e}")
        return frames

    def choose_random_direction(self):
        """
        Escolhe uma direção aleatória para o movimento utilizando o módulo 'random'.


        Retorna:
            str: Uma das direções "up", "down", "left" ou "right".
        """
        directions = ["up", "down", "left", "right"]
        return random.choice(directions)

    def start_mimic_movement(self):
        """
        Inicia o movimento do baú mímico.
        """
        self.mimic_moving = True
        self.move()

    def move(self):
        """
        Move o baú mímico para a direção aleatória.
        """
        if self.mimic_alive and self.mimic_active:
            direction = self.choose_random_direction()
            move_offset = {
                "up": (0, -map.TILE_SIZE),
                "down": (0, map.TILE_SIZE),
                "left": (-map.TILE_SIZE, 0),
                "right": (map.TILE_SIZE, 0)
            }
            dx, dy = move_offset[direction]
            new_x, new_y = self.x + dx, self.y + dy
            if self.is_valid_move(new_x, new_y):
                self.smooth_move(new_x, new_y, direction)
            self.after_id_mimic = self.root.after(1000, self.move)

    def update_animation(self):
        """
        Atualiza a animação do baú mímico.
        """
        if self.mimic_alive and self.mimic_moving:
            if self.current_frame >= len(self.current_animation):
                self.current_frame = 0
            self.canvas.itemconfig(self.image, image=self.current_animation[self.current_frame])
            self.current_frame += 1
            self.after_id_animation = self.canvas.after(100, self.update_animation)

    def smooth_move(self, target_x, target_y, direction):
        """
        Move o baú mímico de maneira suave e constante (evitando saltos) para a posição alvo.


        Argumentos:
            target_x (int): Coordenada x de destino.
            target_y (int): Coordenada y de destino.
            direction (str): Direção do movimento.
        """
        if not self.is_valid_move(target_x, target_y):
            return
        current_x, current_y = self.canvas.coords(self.image)
        step_x = (target_x - current_x) / 50
        step_y = (target_y - current_y) / 50
        for i in range(50):
            self.canvas.after(i * 10, lambda i=i: self.canvas.move(self.image, step_x, step_y))
            self.canvas.after(i * 10, self.update_health_bar)
        if f"move_{direction}" in self.animations:
            self.current_animation = self.animations[f"move_{direction}"]
            self.current_frame = 0
            if self.after_id_animation:
                self.canvas.after_cancel(self.after_id_animation)
            self.update_animation()
        self.x, self.y = target_x, target_y

    def is_valid_move(self, x, y):
        """
        Verifica se o movimento para a posição (x, y) é válido.


        Argumentos:
            x (int): Coordenada x.
            y (int): Coordenada y.


        Retorna:
            bool: True se o movimento for válido, False caso seja inválido.
        """
        try:
            tile_x = (x - map.X_OFFSET) // map.TILE_SIZE
            tile_y = (y - map.Y_OFFSET) // map.TILE_SIZE
            if 0 <= tile_x < len(map.MAP[0]) and 0 <= tile_y < len(map.MAP):
                return map.MAP[tile_y][tile_x] == 1
            return False
        except Exception as e:
            print(f"Erro ao validar movimento: {e}")
            return False

    def take_damage(self, direction):
        """
        Reduz os pontos de vida do baú mímico ao receber dano.


        Argumentos:
            direction (str): Direção do ataque recebido para exibir a animação de acordo.
        """
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
                    if self.after_id_animation:
                        self.canvas.after_cancel(self.after_id_animation)
                    self.update_damage_animation()
                if not self.mimic_active:
                    self.mimic_active = True
                    self.start_mimic_movement()

    def update_health_bar(self):
        """
        Atualiza a barra de vida do baú mímico.
        """
        health_ratio = max(self.hp / self.max_hp, 0)
        self.canvas.coords(self.health_bar, self.x, self.y - 10, self.x + health_ratio * 50, self.y - 5)

    def update_damage_animation(self):
        """
        Atualiza a animação de dano do baú mímico.
        """
        if self.mimic_alive and self.current_frame < len(self.current_animation):
            self.canvas.itemconfig(self.image, image=self.current_animation[self.current_frame])
            self.current_frame += 1
            self.after_id_animation = self.canvas.after(100, self.update_damage_animation)
        else:
            self.current_frame = 0
            if "move_down" in self.animations:
                self.current_animation = self.animations["move_down"]
                if self.after_id_animation:
                    self.canvas.after_cancel(self.after_id_animation)
                self.update_animation()

    def die(self):
        """
        Define o estado de morte do baú mímico.
        """
        self.mimic_alive = False
        if self.after_id_mimic:
            self.root.after_cancel(self.after_id_mimic)
        if self.after_id_animation:
            self.canvas.after_cancel(self.after_id_animation)
        self.canvas.delete(self.image)
        self.canvas.delete(self.health_bar)
        print("Mimic Chest foi derrotado")
        self.drop_key()

    def drop_key(self):
        """
        Dropa uma chave na posição onde o baú mímico morreu.
        """
        try:
            self.key_image = self.load_gif("assets/keys/mimic_key.gif")
            self.key = self.canvas.create_image(self.x, self.y, image=self.key_image[0])
            self.canvas.tag_raise(self.key)
            self.root.keys_on_canvas.append((self.key, self.x, self.y, "mimic"))
            self.animate_key()
        except Exception as e:
            print(f"Erro ao dropar chave: {e}")

    def animate_key(self):
        """
        Inicia a animação da chave.
        """
        try:
            self.key_anim_id = self.root.after(100, self.update_key_animation)
        except Exception as e:
            print(f"Erro ao iniciar animação da chave: {e}")

    def update_key_animation(self):
        """
        Atualiza a animação da chave.
        """
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
        """
        Inicializa o Boss.


        Argumentos:
            root (tk.Tk): Referência à raiz da interface.
            canvas (tk.Canvas): O canvas onde o Boss vai ser desenhado.
            x (int): Posição inicial x do Boss.
            y (int): Posição inicial y do Boss.
            player (Player): Referência ao Player.
        """
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.player = player
        self.keys_on_canvas = []
        self.boss_images = self.load_animations()
        self.image = self.canvas.create_image(x, y, image=self.boss_images["move"]["down"][0], state=tk.HIDDEN) # Inicia o boss como não visível
        self.is_visible = False
        self.is_moving = False
        self.boss_alive = True
        self.hp = 300
        self.max_hp = 300
        self.direction = "down" # Posição inicial padrão
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
        self.health_bar = self.canvas.create_rectangle(self.x, self.y - 30, self.x + self.hp / self.max_hp * 50, self.y - 25, fill='red') # Configurações da barra de vida
        self.canvas.itemconfig(self.health_bar, state='hidden') # Inicia a barra de vida como não visível

    def load_animations(self):
        """
        Carrega todas as animações do Boss.


        Retorna:
            dict: Dicionário contendo as animações.
        """
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
        """
        Carrega um GIF e retorna uma lista de frames.


        Argumentos:
            gif_path (str): Caminho do arquivo GIF.


        Retorna:
            list: Lista de frames do GIF.
        """
        return [tk.PhotoImage(file=gif_path, format=f'gif -index {i}') for i in range(4)]

    def reveal(self):
        """
        Revela o Boss no canvas após a ativação da alavanca.
        """
        self.is_visible = True
        self.canvas.itemconfig(self.image, state=tk.NORMAL)
        self.canvas.itemconfig(self.health_bar, state='normal')

    def start_movement(self):
        """
        Inicia o movimento do Boss.
        """
        if self.is_visible and not self.is_moving:
            self.is_moving = True
            if self.animation_id is None:
                self.animate()
            if self.movement_id is None:
                self.move_towards_player()

    def move_towards_player(self):
        """
        Move o Boss em direção ao jogador, o perseguindo.
        """
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
        """
        Verifica se o Boss está próximo do jogador.


        Argumentos:
            player_coords (tuple): Coordenadas do jogador.


        Retorna:
            bool: True se o Boss estiver próximo, False caso esteja longe.
        """
        player_x, player_y = player_coords
        return abs(self.x - player_x) < 20 and abs(self.y - player_y) < 20

    def update_position(self, direction_vector):
        """
        Atualiza a posição do Boss com base no vetor de direção.
        Permitindo a movimentação diagonal.


        Argumentos:
            direction_vector (np.array): Vetor de direção para o movimento.
        """
        target_x = self.x + direction_vector[0] * self.step_size
        target_y = self.y + direction_vector[1] * self.step_size
        self.x, self.y = target_x, target_y
        self.canvas.coords(self.image, self.x, self.y)
        self.direction = self.get_closest_direction(direction_vector)
        self.update_health_bar()

    def get_direction_vector(self, player_coords):
        """
        Obtém o vetor de direção para o movimento em direção ao jogador.


        Argumentos:
            player_coords (tuple): Coordenadas do jogador.


        Retorna:
            np.array: Vetor de direção normalizado.
        """
        player_x, player_y = player_coords
        direction_vector = np.array([player_x - self.x, player_y - self.y])
        norm = np.linalg.norm(direction_vector)
        if norm == 0:
            return np.array([0, 0])
        return direction_vector / norm

    def get_closest_direction(self, direction_vector):
        """
        Obtém a direção mais próxima com base no vetor de direção.


        Argumentos:
            direction_vector (np.array): Vetor de direção.


        Retorna:
            str: Direção mais próxima ("left", "right", "up" ou "down").
        """
        directions = {
            "left": np.array([-1, 0]),
            "right": np.array([1, 0]),
            "up": np.array([0, -1]),
            "down": np.array([0, 1]),
        }
        closest_direction = min(directions.keys(), key=lambda k: np.linalg.norm(direction_vector - directions[k]))
        return closest_direction

    def animate(self):
        """
        Controla a animação do Boss.
        """
        if not self.boss_alive:
            return
        if self.animation_id is not None:
            self.canvas.after_cancel(self.animation_id)
        frames = self.boss_images["move"][self.direction]
        self.canvas.itemconfig(self.image, image=frames[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(frames)
        self.animation_id = self.canvas.after(self.animation_speed, self.animate)

    def attack(self):
        """
        Realiza o ataque do Boss no jogador.
        """
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
        """
        Atualiza a animação de ataque do Boss.


        Argumentos:
            frames (list): Lista de frames da animação.
            frame_index (int): Índice do frame atual.
        """
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.canvas.after(self.animation_speed, self.update_attack_animation, frames, frame_index + 1)
        else:
            self.animate()
            self.move_towards_player()
            self.canvas.after(self.attack_cooldown, self.reset_attack)

    def reset_attack(self):
        """
        Reseta o cooldown do ataque do Boss.
        """
        if self.boss_alive:
            self.can_attack = True

    def take_damage(self, direction):
        """
        Reduz os pontos de vida do Boss ao receber dano.


        Argumentos:
            direction (str): Direção do ataque recebido.
        """
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
        """
        Atualiza a barra de vida do Boss.
        """
        health_width = self.hp / self.max_hp * 100  
        health_bar_x = self.x - health_width / 2  
        self.canvas.coords(self.health_bar, health_bar_x, self.y - 25, health_bar_x + health_width, self.y - 30)

    def update_damage_animation(self, frames, frame_index):
        """
        Atualiza a animação de dano do Boss.


        Argumentos:
            frames (list): Lista de frames da animação.
            frame_index (int): Índice do frame atual.
        """
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.animation_id = self.canvas.after(self.animation_speed, self.update_damage_animation, frames, frame_index + 1)
        else:
            self.animate()
            self.move_towards_player()

    def die(self):
        """
        Define o estado de morte do Boss.
        """
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
        """
        Atualiza a animação de morte do Boss.


        Argumentos:
            frames (list): Lista de frames da animação.
            frame_index (int): Índice do frame atual.
        """
        if frame_index < len(frames):
            self.canvas.itemconfig(self.image, image=frames[frame_index])
            self.animation_id = self.canvas.after(self.animation_speed, self.update_death_animation, frames, frame_index + 1)
        else:
            self.remove_boss_from_canvas()
        print("Boss foi derrotado")

    def remove_boss_from_canvas(self):
        """
        Remove o Boss do canvas.
        """
        self.canvas.delete(self.image)
        self.image = None  

    def drop_key(self):
        """
        Dropa uma chave na posição onde o Boss morreu.
        """
        try:
            self.key_image = self.load_gif("assets/keys/boss_key.gif")
            self.key = self.canvas.create_image(self.x, self.y, image=self.key_image[0])
            self.canvas.tag_raise(self.key)
            self.root.keys_on_canvas.append((self.key, self.x, self.y, "boss"))
            self.animate_key()
        except Exception as e:
            print(f"Erro ao dropar chave: {e}")

    def animate_key(self):
        """
        Inicia a animação da chave.
        """
        try:
            self.key_anim_id = self.root.after(100, self.update_key_animation)
        except Exception as e:
            print(f"Erro ao iniciar animação da chave: {e}")

    def update_key_animation(self):
        """
        Atualiza a animação da chave.
        """
        try:
            if self.key_anim_id:
                self.canvas.after_cancel(self.key_anim_id)
            self.key_image.append(self.key_image.pop(0))
            self.canvas.itemconfig(self.key, image=self.key_image[0])
            self.key_anim_id = self.root.after(100, self.update_key_animation)
        except Exception as e:
            print(f"Erro ao atualizar animação da chave: {e}")




