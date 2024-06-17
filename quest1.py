import tkinter as tk
from PIL import Image, ImageTk

# Configurações do mapa (0 = espaço vazio, 1 = parede)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
    wall_image = ImageTk.PhotoImage(Image.open("assets/wall.png"))

    # Criando o canvas para o mapa do jogo
    game_canvas = tk.Canvas(game_window, width=1920, height=1080, bg="black")
    game_canvas.pack()

    # Desenhando o mapa do jogo
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == 1:
                game_canvas.create_image(x*TILE_SIZE, y*TILE_SIZE, image=wall_image, anchor="nw")

    # Criando o player
    player = game_canvas.create_image(1*TILE_SIZE, 1*TILE_SIZE, image=player_image, anchor="nw")

    # Função para mover o jogador
    def move_player(event):
        nonlocal player
        x, y = game_canvas.coords(player)
        if event.keysym == 'Up' and MAP[int(y//TILE_SIZE)-1][int(x//TILE_SIZE)] == 0:
            game_canvas.move(player, 0, -TILE_SIZE)
        elif event.keysym == 'Down' and MAP[int(y//TILE_SIZE)+1][int(x//TILE_SIZE)] == 0:
            game_canvas.move(player, 0, TILE_SIZE)
        elif event.keysym == 'Left' and MAP[int(y//TILE_SIZE)][int(x//TILE_SIZE)-1] == 0:
            game_canvas.move(player, -TILE_SIZE, 0)
        elif event.keysym == 'Right' and MAP[int(y//TILE_SIZE)][int(x//TILE_SIZE)+1] == 0:
            game_canvas.move(player, TILE_SIZE, 0)

    # Bind das teclas de seta para movimentar o player
    game_window.bind("<KeyPress-Up>", move_player)
    game_window.bind("<KeyPress-Down>", move_player)
    game_window.bind("<KeyPress-Left>", move_player)
    game_window.bind("<KeyPress-Right>", move_player)

    # Iniciando o loop do jogo
    game_window.mainloop()
