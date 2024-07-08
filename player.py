import tkinter as tk
from PIL import Image, ImageSequence, ImageTk
import numpy as np
import map


ANIMATIONS = {
    'idle_down': 'assets/player/idle/idle_down.gif',
    'idle_left': 'assets/player/idle/idle_left.gif',
    'idle_right': 'assets/player/idle/idle_right.gif',
    'idle_up': 'assets/player/idle/idle_up.gif',
    'run_down': 'assets/player/run/run_down.gif',
    'run_left': 'assets/player/run/run_left.gif',
    'run_right': 'assets/player/run/run_right.gif',
    'run_up': 'assets/player/run/run_up.gif',
    'attack_down': 'assets/player/attack/attack_down.gif',
    'attack_left': 'assets/player/attack/attack_left.gif',
    'attack_right': 'assets/player/attack/attack_right.gif',
    'attack_up': 'assets/player/attack/attack_up.gif',
    'death': 'assets/player/death/death.png',
}


def load_gif(gif_path):
    imgs = []
    try:
        with Image.open(gif_path) as img:
            for frame in ImageSequence.Iterator(img):
                img_pil = frame.convert('RGBA')
                img_tk = ImageTk.PhotoImage(img_pil)
                imgs.append(img_tk)
        if not imgs:
            raise ValueError(f"Erro: nenhum frame carregado para {gif_path}")
    except Exception as e:
        print(f"Erro ao carregar GIF {gif_path}: {e}")
    return imgs

class Player:
    def __init__(self, canvas, start_x, start_y, boss, game):
        self.canvas = canvas
        self.x = start_x
        self.y = start_y
        self.target_x = start_x
        self.target_y = start_y
        self.direction = 'down'
        self.is_moving = False
        self.is_attacking = False
        self.hp = 200  # Pontos de vida do player
        self.max_hp = 200
        self.boss = boss  # Referência ao boss
        self.game = game  # Referência ao objeto Game
        self.is_dead = False  # Verifica se o player está morto

        self.animations = {key: load_gif(path) for key, path in ANIMATIONS.items() if path.endswith('.gif')}
        self.death_image = ImageTk.PhotoImage(file=ANIMATIONS['death'])

        for key, anim in self.animations.items():
            if not anim:
                print(f"Erro: animação {key} não carregada")
        self.current_animation = self.animations['idle_down']
        self.current_frame = 0

        self.image = self.canvas.create_image(
            self.x, self.y,
            image=self.current_animation[self.current_frame],
            anchor='nw'
        )
        self.health_bar = self.canvas.create_rectangle(self.x - 10, self.y - 10, self.x + self.hp / self.max_hp * 50, self.y - 5, fill='lightgreen')
        self.animate()

    def is_alive(self):
        return self.hp > 0

    def animate(self):
        if self.is_dead:
            return  # Não faz nada se o player estiver morto

        self.current_frame += 1
        if self.current_frame >= len(self.current_animation):
            self.current_frame = 0
            if self.is_attacking:
                self.is_attacking = False
                self.current_animation = self.animations[f'idle_{self.direction}']

        self.canvas.itemconfig(self.image, image=self.current_animation[self.current_frame])
        self.update_health_bar()
        self.canvas.after(150, self.animate)

    def move_to(self):
        if self.is_moving and not self.is_dead:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = np.sqrt(dx**2 + dy**2)
            speed = 3
            if distance < speed:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
                self.current_animation = self.animations[f'idle_{self.direction}']
            else:
                angle = np.arctan2(dy, dx)
                new_x = self.x + speed * np.cos(angle)
                new_y = self.y + speed * np.sin(angle)
                if self.is_valid_move(new_x, new_y):
                    self.x = new_x
                    self.y = new_y
                    if abs(dx) > abs(dy):
                        if dx > 0:
                            self.direction = 'right'
                        else:
                            self.direction = 'left'
                    else:
                        if dy > 0:
                            self.direction = 'down'
                        else:
                            self.direction = 'up'
                    self.current_animation = self.animations[f'run_{self.direction}']
                    self.canvas.coords(self.image, self.x, self.y)
                    self.game.update_healing_potion_position()  # Atualiza a posição da poção 
                    self.canvas.after(50, self.move_to)

    def move_towards(self, target_x, target_y):
        if self.is_dead:
            return  # Não faz nada se o player estiver morto

        self.target_x = target_x
        self.target_y = target_y

        if not self.is_moving:
            self.is_moving = True
            self.move_to()

    def is_valid_move(self, x, y):
        tile_x = int((x - map.X_OFFSET) / map.TILE_SIZE)
        tile_y = int((y - map.Y_OFFSET) / map.TILE_SIZE)
        if 0 <= tile_x < len(map.MAP[0]) and 0 <= tile_y < len(map.MAP):
            return map.MAP[tile_y][tile_x] == 1
        return False

    def attack(self, mouse_x=None, mouse_y=None):
        if self.is_dead:
            return  # Não faz nada se o player estiver morto

        # Implementação do ataque do player usando mouse_x e mouse_y
        if mouse_x is not None and mouse_y is not None:
            print(f"Ataque na direção: x={mouse_x}, y={mouse_y}")

        if not self.is_attacking:
            self.is_attacking = True
            self.is_moving = False  # Cancelar movimentação
            self.target_x = self.x  # Parar o movimento atual
            self.target_y = self.y
            self.current_animation = self.animations[f'attack_{self.direction}']
            self.current_frame = 0
            print(f'Atacando na direção {self.direction} com {len(self.current_animation)} frames')

        else:
            print("Ataque padrão")

            # Verifica se o Player atingiu o Boss
            if self.boss.boss_alive:
                boss_coords = self.canvas.coords(self.boss.image)  # Acessa diretamente a imagem do Boss
                if self.is_near_boss(boss_coords):
                    self.attack_boss()

    def is_near_boss(self, boss_coords):
        boss_x, boss_y = boss_coords
        return abs(self.x - boss_x) < 20 and abs(self.y - boss_y) < 20

    def attack_boss(self):
        # Simula o ataque no Boss
        self.boss.take_damage(self.direction)

    def receive_damage(self, damage):
        if self.is_dead:
            return  # Não faz nada se o player estiver morto

        self.hp -= damage
        print(f"Você recebeu {damage} de dano. HP restante: {self.hp}")
        if self.hp <= 0:
            self.die()
        self.update_health_bar

    def update_health_bar(self):
        health_ratio = max(self.hp / self.max_hp, 0)
        self.canvas.coords(self.health_bar, self.x - 10, self.y - 10, self.x - 10 + health_ratio * 50, self.y - 5)

    def die(self):
        self.hp = 0
        self.is_dead = True  # Define a verificação como True
        self.canvas.itemconfig(self.image, image=self.death_image)
        self.update_health_bar()
        print("Você morreu.")
