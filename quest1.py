import tkinter as tk

def start_game():
    # Criando a janela do jogo
    game_window = tk.Tk()
    game_window.title("Quest 1")
    game_window.geometry("1920x1080")

    # Criando o canvas para o mapa do jogo
    game_canvas = tk.Canvas(game_window, width=1920, height=1080, bg="black")
    game_canvas.pack()

    # Desenhando o mapa do jogo (exemplo simples, depois adiciona mais complexidade)
    # Aqui, pode carregar imagens, criar sprites, etc.
    # Desenhando uma grade representando um mapa:
    for i in range(0, 1920, 50):
        for j in range(0, 1080, 50):
            game_canvas.create_rectangle(i, j, i+50, j+50, outline="white")

    # Função para mover o jogador
    def move_player(event):
        if event.keysym == 'Up':
            game_canvas.move(player, 0, -10)
        elif event.keysym == 'Down':
            game_canvas.move(player, 0, 10)
        elif event.keysym == 'Left':
            game_canvas.move(player, -10, 0)
        elif event.keysym == 'Right':
            game_canvas.move(player, 10, 0)

    # Criando o player (um quadrado vermelho)
    player = game_canvas.create_rectangle(950, 500, 970, 520, fill="red")

    # Bind das teclas de seta para movimentar o player
    game_window.bind("<KeyPress-Up>", move_player)
    game_window.bind("<KeyPress-Down>", move_player)
    game_window.bind("<KeyPress-Left>", move_player)
    game_window.bind("<KeyPress-Right>", move_player)

    # Iniciando o loop do jogo
    game_window.mainloop()
