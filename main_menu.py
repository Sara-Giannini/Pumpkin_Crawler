import tkinter as tk
from PIL import Image, ImageSequence, ImageTk
import quest1  # Importando o módulo do jogo "Quest 1"


def load_gif(gif_path):
    imgs = []
    with Image.open(gif_path) as img:
        for frame in ImageSequence.Iterator(img):
            img_pil = frame.convert('RGB')
            img_tk = ImageTk.PhotoImage(img_pil)
            imgs.append(img_tk)
    return imgs

def start():
    window.destroy()
    quest1.start_game()

def quit():
    print("Saindo...")
    window.destroy()

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
    global index_gif, imgs
    if index_gif == len(imgs):
        index_gif = 0
    label_gif.configure(image=imgs[index_gif])
    index_gif += 1
    window.after(100, update_gif)

update_gif()

img_start = ImageTk.PhotoImage(file="assets/menu/btn_start.png")
img_quit = ImageTk.PhotoImage(file="assets/menu/btn_quit.png")

btn_start = tk.Button(window, image=img_start, command=start, borderwidth=0, highlightthickness=0)
btn_start.place(relx=0.5, rely=0.8, anchor="center", width=150, height=67)

btn_quit = tk.Button(window, image=img_quit, command=quit, borderwidth=0, highlightthickness=0)
btn_quit.place(relx=0.5, rely=0.9, anchor="center", width=150, height=67)


window.mainloop()
