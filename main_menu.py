import tkinter as tk
from PIL import Image, ImageSequence, ImageTk

# Carregando o GIF
def carregar_gif(gif_path):
    """
    Carrega um GIF e o retorna como uma sequência de imagens PhotoImage.

    Args:
        gif_path (str): Caminho para o arquivo GIF.

    Returns:
        List[PhotoImage]: Lista de imagens PhotoImage do GIF.
    """
    imgs = []
    with Image.open(gif_path) as img:
        for frame in ImageSequence.Iterator(img):
            img_pil = frame.convert('RGB')
            img_tk = ImageTk.PhotoImage(img_pil)
            imgs.append(img_tk)
    return imgs

# Função para Start
def start():
    # Implementar a lógica para iniciar o jogo
    print("Start!")

# Função para sair
def sair():
    # Implementar a lógica para sair do jogo
    print("Saindo...")
    window.destroy()

# Criando a janela de menu principal
window = tk.Tk()
window.title("Menu Principal")
window.geometry("1920x1080")

# Carregando o GIF
imgs = carregar_gif("assets/giff.gif")

# Criando o canvas para o GIF
canvas_gif = tk.Canvas(window, width=1920, height=1080)
canvas_gif.pack()

# Criando a label para o GIF
label_gif = tk.Label(canvas_gif, image=imgs[0])
label_gif.pack()

# Atualizando o GIF a cada 100ms
indice_gif = 0
def atualizar_gif():
    global indice_gif, imgs
    if indice_gif == len(imgs):
        indice_gif = 0
    label_gif.configure(image=imgs[indice_gif])
    indice_gif += 1
    window.after(100, atualizar_gif)

atualizar_gif()

# Carregando as imagens dos botões
img_start = ImageTk.PhotoImage(file="assets/bnt_start.png")
img_sair = ImageTk.PhotoImage(file="assets/bnt_sair.png")

# Criando os botões
btn_start = tk.Button(window, image=img_start, command=start, borderwidth=0, highlightthickness=0)
btn_start.place(relx=0.5, rely=0.8, anchor="center", width=150, height=67)

btn_sair = tk.Button(window, image=img_sair, command=sair, borderwidth=0, highlightthickness=0)
btn_sair.place(relx=0.5, rely=0.9, anchor="center", width=150, height=67)

# Executando a interface
window.mainloop()
