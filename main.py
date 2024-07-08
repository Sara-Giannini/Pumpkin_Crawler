import tkinter as tk
from PIL import Image, ImageTk
import map
from player import Player, load_gif
from enemies import Boss, MimicChest
import numpy as np


def start_menu():
    """
    Configuração da janela de Menu Principal.

    Cria a janela principal do menu com um GIF animado de fundo e botões para 
    iniciar ou sair do jogo.
    """
    global window
    try:
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
            """Atualiza a imagem do GIF em loop."""
            nonlocal index_gif
            index_gif = (index_gif + 1) % len(imgs)
            label_gif.config(image=imgs[index_gif])
            window.after(100, update_gif)

        update_gif()

        # Imagens para estilizar os botões
        img_start = tk.PhotoImage(file="assets/menu/btn_start.png") 
        img_quit = tk.PhotoImage(file="assets/menu/btn_quit.png")

        btn_start = tk.Button(window, image=img_start, command=start_game, borderwidth=0, highlightthickness=0)
        btn_start.place(relx=0.5, rely=0.8, anchor="center", width=150, height=67)

        btn_quit = tk.Button(window, image=img_quit, command=quit_game, borderwidth=0, highlightthickness=0)
        btn_quit.place(relx=0.5, rely=0.9, anchor="center", width=150, height=67)

        window.mainloop()

    except Exception as e:
        print(f"Erro ao configurar a janela de Menu Principal: {e}")

def start_game():
    """
    Inicia o jogo.

    Fecha a janela do Menu Principal e abre a janela do jogo "Pumpkin Crawler.
    """
    global window
    try:
        window.destroy()
        game_root = tk.Tk()
        game = Game(game_root)
        game_root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")

def quit_game():
    """
    Sai do jogo.

    Fecha a janela do Menu Principal.
    """
    global window
    try:
        print("Saindo...")
        window.destroy()
    except Exception as e:
        print(f"Erro ao sair do jogo: {e}")

class Game:
    def __init__(self, root):
        """
        Inicializa o jogo.

        Configura a janela do jogo, cria o mapa, os inimigos e o jogador.
        """
        self.root = root
        self.root.title("Pumpkin Crawler")
        self.canvas = tk.Canvas(self.root, width=1280, height=720, bg='black')
        self.canvas.pack()

        # Posição inicial da Personagem Principal
        self.player_x = 25
        self.player_y = 8

        # Estado inicial dos objetos interativos no mapa
        self.lever_state = "lever_up"
        self.gate_state = "gate_closed"
        self.lock_state = "keyless_lock"
        self.door_state = "door_closed"
        self.boss_room_visible = False
        self.player_has_boss_key = False
        self.player_has_mimic_key = False
        self.boss_movement_active = False

        # Configuração do baú final 
        self.final_chest_x = 250
        self.final_chest_y = 370
        self.final_chest_img = tk.PhotoImage(file="assets/final_chest/final_chest.gif", format="gif -index 0")
        self.final_chest = self.canvas.create_image(self.final_chest_x, self.final_chest_y, image=self.final_chest_img, anchor='nw')
        self.final_chest_animation_frames = load_gif("assets/final_chest/final_chest.gif")
        self.final_chest_animated = False
        self.canvas.tag_raise(self.final_chest)

        # Inicializa variáveis de estado do jogo
        self.crate_hits = 0
        self.healing_potion = None
        self.healing_potion_bg = None
        self.canvas.bind("Motion", self.update_healing_potion_position)

        self.root.keys_on_canvas = []  # Inicializa a lista para armazenar as chaves 
        self.keys_collected = []  # Armazena as chaves coletadas pelo jogador

        # Criação do mapa, da sala secreta do boss e dos objetos interativos
        map.create_boss_room(self.canvas, visibility="hidden")
        map.create_map(self.canvas)
        map.create_interactions(self.canvas, self.lever_state, self.gate_state, self.lock_state, self.door_state)

        # Posição inicial do baú mímico
        self.mimic_x = 6
        self.mimic_y = 17
        self.mimic = MimicChest(self.root, self.canvas, self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET)

        # Posição inicial do boss
        self.boss_x = 17
        self.boss_y = 8
        self.boss = Boss(self.root, self.canvas, self.boss_x * map.TILE_SIZE + map.X_OFFSET, self.boss_y * map.TILE_SIZE + map.Y_OFFSET, None)  # Referência ao Player vai ser definida depois

        # Criação da personagem principal
        self.player = Player(self.canvas, self.player_x * map.TILE_SIZE + map.X_OFFSET, self.player_y * map.TILE_SIZE + map.Y_OFFSET, self.boss, self)

        # Define a referência do jogador no Boss
        self.boss.player = self.player

        # Bindings de eventos
        self.root.bind("<KeyPress>", self.handle_keypress)  # Vincula o pressionamento de teclas (especificamente a tecla "e" para interagir e "1" para utilizar a poção de cura)
        self.canvas.bind("<Button-1>", self.on_click)  # Vincula o clique esquerdo do mousepara mover a personagem (point and click)
        self.canvas.bind("<Button-3>", self.on_right_click)  # Vincula o clique direito do mouse para atacar

        self.update_map_for_states()
        self.after_id_mimic = None

        # Inicia animações e movimentos
        self.mimic.start_mimic_movement()
        self.boss.start_movement()

    def on_click(self, event):
        """
        Processa os eventos de clique com botão esquerdo do mouse.

        Move o jogador para a posição clicada, se o movimento for válido.
        """
        try:
            x, y = event.x, event.y
            tile_x = (x - map.X_OFFSET) // map.TILE_SIZE
            tile_y = (y - map.Y_OFFSET) // map.TILE_SIZE
            if self.player.is_valid_move(tile_x * map.TILE_SIZE + map.X_OFFSET, tile_y * map.TILE_SIZE + map.Y_OFFSET):
                self.player.move_towards(tile_x * map.TILE_SIZE + map.X_OFFSET, tile_y * map.TILE_SIZE + map.Y_OFFSET)
                self.update_healing_potion_position()
        except Exception as e:
            print(f"Erro ao processar clique esquerdo: {e}")

    def on_right_click(self, event):
        """
        Processa os eventos de clique com botão direito do mouse.

        Realiza ataquesnos inimigos e objetos interativos próximos.
        """
        mouse_x, mouse_y = event.x, event.y
        try:
            direction = self.get_direction_from_mouse(mouse_x, mouse_y)
            self.player.direction = direction
            self.player.attack(mouse_x, mouse_y)

            crate_info = map.interactions["crate_1"]
            crate_x = crate_info["position"][0] * map.TILE_SIZE + crate_info["position"][2] + map.X_OFFSET
            crate_y = crate_info["position"][1] * map.TILE_SIZE + crate_info["position"][3] + map.Y_OFFSET
            if self.is_near_player(crate_x, crate_y):
                self.hit_crate()
                self.handle_enemy_interactions()

            if self.is_near_player(self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET):
                direction = self.get_direction(self.mimic_x, self.mimic_y, self.player.x, self.player.y)
                self.mimic.take_damage(direction)
                if self.mimic.mimic_alive:
                    self.mimic.mimic_moving = True
                    self.mimic.smooth_move(self.player.x, self.player.y, direction)
                else:
                    self.mimic.mimic_alive = False
                    self.canvas.delete(self.mimic.image)
                    self.mimic.drop_key()  # Usa o método drop_key do MimicChest para soltar a chave

            if self.is_near_player(self.boss.x, self.boss.y):
                self.boss.attack()
                if not self.boss.boss_alive:
                    self.boss.drop_key()  # Usa o método drop_key do Boss para soltar a chave
                    self.canvas.delete(self.boss.image)  # Remove Boss do canvas

            if self.is_near_player(self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET):
                self.mimic.mimic_moving = True
                self.mimic.choose_random_direction()

            for key, key_x, key_y, key_type in self.keys_collected:
                if self.is_near_player(key_x * map.TILE_SIZE + map.X_OFFSET, key_y * map.TILE_SIZE + map.Y_OFFSET):
                    self.canvas.delete(key)
                    self.keys_collected.remove((key, key_x, key_y, key_type))
                    self.player_has_mimic_key = True
                    if key_type == "boss":
                        self.player_has_boss_key = True  # Pra rastrear as chaves separadamente

        except Exception as e:
            print(f"Erro ao processar clique direito: {e}")

    def handle_keypress(self, event):
        """
        Processa os eventos de pressionamento da tecla.

        Verifica se a tecla "e" foi pressionada para interações ou "1" para usar a poção de cura.
        """
        try:
            if event.keysym == 'e':
                self.collect_keys()
                self.handle_map_interactions()
            elif event.keysym == '1':
                self.use_healing_potion()
            else:
                self.player.handle_keypress(event)
            self.update_healing_potion_position()
        except Exception as e:
            print(f"Erro ao processar pressionamento de tecla: {e}")

    def is_near_player(self, element_x, element_y, max_distance=64):
        """
        Verifica se um objeto (elemento) interativo está próximo do jogador.

        Argumentos:
            element_x (int): Coordenada x do elemento.
            element_y (int): Coordenada y do elemento.
            max_distance (int): Distância máxima para considerar o elemento próximo. Padrão de 64.

        Retorna:
            bool: True se o elemento estiver próximo, False se o elemento estiver longe.
        """
        try:
            player_px = self.player.x
            player_py = self.player.y
            distance = ((player_px - element_x) ** 2 + (player_py - element_y) ** 2) ** 0.5
            return distance <= max_distance
        except Exception as e:
            print(f"Erro ao verificar proximidade do jogador: {e}")
            return False

    def handle_map_interactions(self):
        """
        Trabalha com as interações do jogador com os objetos interativos do mapa.

        Verifica se o jogador está próximo de uma alavanca, fechadura, baú mímico ou baú final,
        e executa a ação correspondente.
        """
        try:
            lever_info = map.interactions[self.lever_state]
            lever_x = lever_info["position"][0] * map.TILE_SIZE + lever_info["position"][2] + map.X_OFFSET
            lever_y = lever_info["position"][1] * map.TILE_SIZE + lever_info["position"][3] + map.Y_OFFSET
            
            lock_info = map.interactions[self.lock_state]
            lock_x = lock_info["position"][0] * map.TILE_SIZE + lock_info["position"][2] + map.X_OFFSET
            lock_y = lock_info["position"][1] * map.TILE_SIZE + lock_info["position"][3] + map.Y_OFFSET
            
            print(f"Verificando alavanca em ({lever_x}, {lever_y}) e fechadura em ({lock_x}, {lock_y})")
            
            if self.is_near_player(lever_x, lever_y):
                print("Interagindo com a alavanca")
                self.toggle_lever()
            elif self.is_near_player(lock_x, lock_y):
                print("Interagindo com a fechadura")
                if self.player_has_mimic_key:
                    self.toggle_lock()
            elif self.is_near_player(self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET):
                print("Interagindo com o Mimic")
                self.mimic.mimic_moving = True
                self.start_mimic_animation()
            
            for key, key_x, key_y, key_type in self.keys_collected:
                if self.is_near_player(key_x * map.TILE_SIZE + map.X_OFFSET, key_y * map.TILE_SIZE + map.Y_OFFSET):
                    print(f"Interagindo com a chave em ({key_x}, {key_y})")
                    self.canvas.delete(key)
                    self.keys_collected.remove((key, key_x, key_y, key_type))
                    self.player_has_mimic_key = True
                    if key_type == "boss":
                        self.player_has_boss_key = True  # Pra rastrer as chaves separadamente
            
            if self.is_near_player(self.final_chest_x, self.final_chest_y):
                if self.player_has_boss_key and not self.final_chest_animated:
                    print("Interagindo com o final_chest")
                    self.animate_final_chest()
            
            if self.healing_potion and self.is_near_player(self.canvas.coords(self.healing_potion)[0], self.canvas.coords(self.healing_potion)[1]):
                self.collect_healing_potion()

        except Exception as e:
            print(f"Erro ao processar interação: {e}")

    def handle_enemy_interactions(self):
        """
        Trabalha com as interações envolvendo os inimigos.

        Verifica se o jogador está próximo de baú mímico, Boss ou chaves e executa as ações correspondentes.
        """
        try:
            if self.is_near_player(self.mimic_x * map.TILE_SIZE + map.X_OFFSET, self.mimic_y * map.TILE_SIZE + map.Y_OFFSET):
                direction = self.get_direction(self.mimic_x, self.mimic_y, self.player.x, self.player.y)
                self.mimic.take_damage(direction)
                if self.mimic.mimic_alive:
                    self.mimic.mimic_moving = True
                    self.mimic.smooth_move(self.player.x, self.player.y, direction)
                else:
                    self.mimic.mimic_alive = False
                    self.canvas.delete(self.mimic.image)
                    self.mimic.drop_key()  # Usa o método drop_key do MimicChest para soltar a chave
            
            if self.is_near_player(self.boss.x, self.boss.y):
                self.boss.attack()
                if not self.boss.boss_alive:
                    self.boss.drop_key()  # Usa o método drop_key do Boss para soltar a chave
                    self.canvas.delete(self.boss.image)  # Remove Boss do canvas
            
            for key, key_x, key_y, key_type in self.keys_collected:
                if self.is_near_player(key_x * map.TILE_SIZE + map.X_OFFSET, key_y * map.TILE_SIZE + map.Y_OFFSET):
                    self.canvas.delete(key)
                    self.keys_collected.remove((key, key_x, key_y, key_type))
                    self.player_has_mimic_key = True
                    if key_type == "boss":
                        self.player_has_boss_key = True  # Rastrear chaves separadamente
            
        except Exception as e:
            print(f"Erro ao processar outras interações: {e}")

    def hit_crate(self):
        """
        Processa o evento de atacar a crate (caixote).

        Atualiza o estado da crate e solta uma poção de cura após a crate ser quebrada.
        """
        try:
            self.crate_hits += 1
            if self.crate_hits == 1:
                map.update_crate_state(self.canvas, "crate_cracked")
            elif self.crate_hits == 2:
                map.update_crate_state(self.canvas, "crate_broken")
                self.drop_healing_potion()
        except Exception as e:
            print(f"Erro ao quebar a crate: {e}")

    def drop_healing_potion(self):
        """
        Solta uma poção de cura na posição da crate quebrada.
        """
        try:
            crate_info = map.interactions["crate_broken"]
            potion_img = tk.PhotoImage(file="assets/player/itens/healing_potion.png")
            self.healing_potion = self.canvas.create_image(
                crate_info["position"][0] * map.TILE_SIZE + crate_info["position"][2] + map.X_OFFSET,
                crate_info["position"][1] * map.TILE_SIZE + crate_info["position"][3] + map.Y_OFFSET,
                image=potion_img, anchor='nw'
            )
            if not hasattr(self.canvas, 'images'):
                self.canvas.images = []
            self.canvas.images.append(potion_img)
        except Exception as e:
            print(f"Erro ao soltar a poção de cura: {e}")

    def collect_healing_potion(self):
        """
        Coleta a poção de cura e a remove do canvas.

        Adiciona um ícone de poção ao inventário do jogador, localizado acima de sua health bar.
        """
        try:
            self.canvas.delete(self.healing_potion)
            self.healing_potion = None

            potion_bg_img = Image.open("assets/player/itens/healing_potion_bg.png") 
            potion_bg_img = potion_bg_img.resize((20, 20), Image.LANCZOS)
            potion_bg_img = ImageTk.PhotoImage(potion_bg_img)
            self.healing_potion_bg = self.canvas.create_image(
                self.player.x, self.player.y - 20, image=potion_bg_img, anchor='nw'
            )
            self.healing_potion_collected = True
            self.canvas.images.append(potion_bg_img)
            self.update_healing_potion_position()
        except Exception as e:
            print(f"Erro ao coletar a poção de cura: {e}")

    def update_healing_potion_position(self):
        """
        Atualiza a posição do ícone da poção de cura no inventário do jogador conforme ele se movimenta.

        Posiciona o ícone da poção acima do jogador.
        """
        try:
            if self.healing_potion_bg:
                player_coords = self.canvas.coords(self.player.image)
                new_x = player_coords[0] + 5
                new_y = player_coords[1] - 40
                self.canvas.coords(self.healing_potion_bg, new_x, new_y)
        except Exception as e:
            print(f"Erro ao atualizar posição da poção de cura: {e}")

    def use_healing_potion(self):
        """
        Usa a poção de cura.

        Remove o ícone da poção do inventário e restaura a saúde do jogador ao máximo.
        """
        try:
            if self.healing_potion_bg:
                self.canvas.delete(self.healing_potion_bg)
                self.healing_potion_bg = None
                self.player.hp = self.player.max_hp
                self.player.update_health_bar()
        except Exception as e:
            print(f"Erro ao usar a poção de cura: {e}")

    def toggle_lever(self):
        """
        Alterna o estado da alavanca e atualiza o estado do portão.

        Abre ou fecha o portão dependendo do estado atual da alavanca.
        """
        try:
            self.lever_state = "lever_down" if self.lever_state == "lever_up" else "lever_up"
            self.gate_state = "gate_open" if self.gate_state == "gate_closed" else "gate_closed"

            map.update_lever_state(self.canvas, self.lever_state)
            map.update_gate_state(self.canvas, self.gate_state)

            self.update_map_for_states()

            if self.lever_state == "lever_down":
                self.boss_movement_active = True  # Ativa o movimento do boss quando a alavanca é ativada
                self.boss.start_movement()
                self.show_boss_room()
            else:
                self.boss_movement_active = False

        except Exception as e:
            print(f"Erro ao alternar alavanca: {e}")

    def show_boss_room(self):
        """
        Revela a sala do boss e inicia o movimento do boss.
        """
        try:
            if not self.boss_room_visible:
                self.boss_room_visible = True
                map.toggle_boss_room_visibility(self.canvas, visibility="normal")
            self.boss.reveal()
            self.boss.start_movement()
        except Exception as e:
            print(f"Erro ao mostrar sala do Boss: {e}")

    def toggle_lock(self):
        """
        Alterna o estado da fechadura e atualiza o estado da porta.

        Abre ou fecha a porta dependendo do estado atual da fechadura.
        """
        try:
            self.lock_state = "key_lock" if self.lock_state == "keyless_lock" else "keyless_lock"
            self.door_state = "door_open" if self.door_state == "door_closed" else "door_closed"

            map.update_lock_state(self.canvas, self.lock_state)
            map.update_door_state(self.canvas, self.door_state)

            self.update_map_for_states()
        except Exception as e:
            print(f"Erro ao alternar fechadura: {e}")

    def update_map_for_states(self):
        """
        Atualiza o mapa baseado no estado atual dos elementos.

        Abre ou fecha os caminhos no mapa de acordo com o estado dos portões e portas.
        """
        try:
            gate_pos = map.interactions["gate_closed"]["position"]
            door_pos = map.interactions["door_closed"]["position"]

            gate_x, gate_y = gate_pos[0], gate_pos[1]
            door_x, door_y = door_pos[0], door_pos[1]

            map.MAP[gate_y][gate_x] = 0 if self.gate_state == "gate_closed" else 1
            map.MAP[door_y][door_x] = 0 if self.door_state == "door_closed" else 1
            self.canvas.tag_raise(self.final_chest)
        except Exception as e:
            print(f"Erro ao atualizar mapa para os estados: {e}")

    def get_direction(self, from_x, from_y, to_x, to_y):
        """
        Obtém a direção de movimento com base nas coordenadas de origem e destino.

        Argumentos:
            from_x (int): Coordenada x de origem.
            from_y (int): Coordenada y de origem.
            to_x (int): Coordenada x de destino.
            to_y (int): Coordenada y de destino.

        Retorna:
            str: Direção de movimento ("left", "right", "up" ou "down").
        """
        try:
            if abs(from_x - to_x) > abs(from_y - to_y):
                return "left" if from_x > to_x else "right"
            else:
                return "up" if from_y > to_y else "down"
        except Exception as e:
            print(f"Erro ao obter direção: {e}")
            return "up"

    def get_direction_from_mouse(self, mouse_x, mouse_y):
        """
        Obtém a direção de movimento com base na posição do mouse.
        Será utilizado para que o ataque da personagem seja guiado na direção da seta do mouse.

        Argumentos:
            mouse_x (int): Coordenada x do mouse.
            mouse_y (int): Coordenada y do mouse.

        Retorna:
            str: Direção de movimento ("left", "right", "up" ou "down").
        """
        try:
            dx = mouse_x - self.player.x
            dy = mouse_y - self.player.y
            angle = np.arctan2(dy, dx)
            directions = {
                (-np.pi / 4, np.pi / 4): 'right',
                (np.pi / 4, 3 * np.pi / 4): 'down',
                (3 * np.pi / 4, -3 * np.pi / 4): 'left',
                (-3 * np.pi / 4, -np.pi / 4): 'up'
            }
            for (low, high), direction in directions.items():
                if low <= angle < high:
                    return direction
            return 'down'
        except Exception as e:
            print(f"Erro ao obter direção do mouse: {e}")
            return 'down'

    def collect_keys(self):
        """
        Verifica se o jogador está na mesma posição que uma chave e a coleta.

        Remove a chave do canvas e atualiza o estado do jogador para indicar a posse da chave.
        """
        try:
            for key_info in self.root.keys_on_canvas[:]:  # [:] pra copiar a lista e iterar sobre ela
                key, key_x, key_y, key_type = key_info
                print(f"Verificando chave em ({key_x}, {key_y}) com tipo {key_type}")
                if self.is_near_player(key_x, key_y):
                    print(f"Coletando chave em ({key_x}, {key_y})")
                    self.canvas.delete(key)  # Remove a chave do canvas
                    self.root.keys_on_canvas.remove(key_info)  # Remove a chave da lista de chaves no canvas
                    if key_type == "boss":
                        self.player_has_boss_key = True 
                    elif key_type == "mimic":
                        self.player_has_mimic_key = True
        except Exception as e:
            print(f"Erro ao coletar chave: {e}")

    def animate_final_chest(self):
        """
        Inicia a animação do baú final.
        """
        try:
            self.final_chest_animated = True
            self.current_final_chest_frame = 0
            self.update_final_chest_animation()
        except Exception as e:
            print(f"Erro ao iniciar animação do final_chest: {e}")

    def update_final_chest_animation(self):
        """
        Atualiza a animação do baú final.

        Exibe os frames da animação do baú final em intervalos regulares.
        """
        try:
            if self.current_final_chest_frame < len(self.final_chest_animation_frames):
                self.canvas.itemconfig(self.final_chest, image=self.final_chest_animation_frames[self.current_final_chest_frame])
                self.current_final_chest_frame += 1
                self.root.after(100, self.update_final_chest_animation)

            else:
                self.end_game()
        except Exception as e:
            print(f"Erro ao atualizar animação do final_chest: {e}")

    def end_game(self):
        """
        Termina o jogo.
        """
        print("Jogo terminado. Retornando ao menu principal.")
        self.root.destroy()
        start_menu()


# Define window como variável global
window = None

# Iniciar o menu principal ao executar 
if __name__ == "__main__":
    start_menu()
