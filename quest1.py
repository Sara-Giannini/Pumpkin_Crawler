import tkinter as tk
from PIL import Image, ImageTk

# Configurações do mapa (0 = espaço vazio, 1 = parede superior, 2 = parede inferior, 3 = parede esquerda, 4 = parede direita, 5 = chão)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 2],
    [1, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 2],
    [1, 5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 5, 2],
    [1, 5, 1, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 1, 5, 2],
    [1, 5, 1, 5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 5, 1, 5, 1, 1, 5, 2],
    [1, 5, 1, 5, 1, 5, 1, 5, 5, 5, 5, 5, 1, 5, 1, 5, 5, 1, 5, 2],
    [1, 5, 1, 5, 1, 5, 1, 5, 1, 1, 1, 5, 1, 5, 1, 1, 1, 1, 5, 2],
    [1, 5, 1, 5, 1, 5, 1, 5, 5, 5, 1, 5, 1, 5, 1, 5, 5, 5, 5, 2],
    [1, 5, 1, 5, 1, 5, 1, 1, 1, 1, 1, 5, 1, 5, 1, 1, 1, 1, 5, 2],
    [1, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 1, 5, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4],
]

# Tamanho dos blocos
TILE_SIZE = 50

def start_game():
    # Criando a janela do jogo
    game_window = tk.Tk()
    game_window.title("Quest 1")
    game_window.geometry("1920x1080")

    # Carregando as imagens dos sprites
    player_image = ImageTk.PhotoImage(Image.open("assets/player.png"))
    tiles = {
        1: ImageTk.PhotoImage(Image.open("assets/tileset/wall_top.png")),
        2: ImageTk.PhotoImage(Image.open("assets/tileset/wall_bottom.png")),
        3: ImageTk.PhotoImage(Image.open("assets/tileset/wall_left.png")),
        4: ImageTk.PhotoImage(Image.open("assets/tileset/wall_right.png")),
        5: ImageTk.PhotoImage(Image.open("assets/tileset/floor.png")),
    }

    # Criando o canvas para o mapa do jogo
    game_canvas = tk.Canvas(game_window, width=1920, height=1980, bg="black")
    game_canvas.pack()

    # Desenhando o mapa do jogo
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile in tiles:
                game_canvas.create_image(x*TILE_SIZE, y*TILE_SIZE, image=tiles[tile], anchor="nw")

    # Criando o player
    player = game_canvas.create_image(1*TILE_SIZE, 1*TILE_SIZE, image=player_image, anchor="nw")

    # Função para mover o jogador
    def move_player(event):
        nonlocal player
        x, y = game_canvas.coords(player)
        x_tile, y_tile = int(x // TILE_SIZE), int(y // TILE_SIZE)

        if event.keysym == 'Up' and MAP[y_tile-1][x_tile] == 5:
            game_canvas.move(player, 0, -TILE_SIZE)
        elif event.keysym == 'Down' and MAP[y_tile+1][x_tile] == 5:
            game_canvas.move(player, 0, TILE_SIZE)
        elif event.keysym == 'Left' and MAP[y_tile][x_tile-1] == 5:
            game_canvas.move(player, -TILE_SIZE, 0)
        elif event.keysym == 'Right' and MAP[y_tile][x_tile+1] == 5:
            game_canvas.move(player, TILE_SIZE, 0)

    # Bind das teclas de seta para movimentar o player
    game_window.bind("<KeyPress-Up>", move_player)
    game_window.bind("<KeyPress-Down>", move_player)
    game_window.bind("<KeyPress-Left>", move_player)
    game_window.bind("<KeyPress-Right>", move_player)

    # Iniciando o loop do jogo
    game_window.mainloop()
