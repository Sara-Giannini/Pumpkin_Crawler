import tkinter as tk
from PIL import Image, ImageTk


# Constantes de configuração do mapa
TILE_SIZE = 32 # Tamanho padrão dos tiles
# Offset horizontal e  Offset vertical para ajustar a posição dos tileset de forma mais detalhada
X_OFFSET = 0 
Y_OFFSET = 0  

# Definição da estrutura do mapa, [1] para onde a movimentação é permitida, [0] para paredes
MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


# Tileset com a definição de cada tile e suas respectivas posições e arquivos
tileset = {
    "wall_1": {"file": "assets/tileset/wall_1.png", "position": (5, 10, 0, 0)},
    "floor_1": {"file": "assets/tileset/floor_1.png", "position": (5, 12, 0, 0)},
    "gold_9": {"file": "assets/tileset/gold_9.png", "position": (5, 14, 0, 10)},
    "gold_1": {"file": "assets/tileset/gold_1.png", "position": (5, 12, 0, -10)},
    "gold_2": {"file": "assets/tileset/gold_2.png", "position": (9, 13, 0, 0)},
    "gold_3": {"file": "assets/tileset/gold_3.png", "position": (7, 14, 0, 0)},
    "gold_4": {"file": "assets/tileset/gold_4.png", "position": (7, 13, 0, 0)},
    "gold_5": {"file": "assets/tileset/gold_5.png", "position": (8, 13, 0, 0)},
    "gold_8": {"file": "assets/tileset/gold_8.png", "position": (5, 13, 10, 0)},    
    "floor_2": {"file": "assets/tileset/floor_2.png", "position": (5, 17, 0, -5)},
    "floor_4": {"file": "assets/tileset/floor_4.png", "position": (20, 15, 0, 0)},
    "floor_3": {"file": "assets/tileset/floor_3.png", "position": (12, 14, 0, 0)},
    "wall_3": {"file": "assets/tileset/wall_3.png", "position": (12, 13, 0, 0)},
    "wall_2": {"file": "assets/tileset/wall_2.png", "position": (5, 15, 0, -5)},
    "patch": {"file": "assets/tileset/patch.png", "position": (10, 18, -15, 10)},
    "wall_4": {"file": "assets/tileset/wall_4.png", "position": (15, 12, 0, 0)},
    "floor_5": {"file": "assets/tileset/floor_5.png", "position": (22, 7, 0, 5)},
    "stairs": {"file": "assets/tileset/stairs.png", "position": (22, 13, 0, -15)},
    "wall_5": {"file": "assets/tileset/wall_5.png", "position": (20, 13, 0, 0)},
    "sink": {"file": "assets/tileset/sink.png", "position": (21, 14, 0, 15)},
    "wall_6": {"file": "assets/tileset/wall_6.png", "position": (22, 6, 0, -25)},
    "table": {"file": "assets/tileset/table.png", "position": (24, 7, 0, -7)},
    "chair_2": {"file": "assets/tileset/chair_2.png", "position": (26, 7, -20, -5)},
    "chair_3": {"file": "assets/tileset/chair_3.png", "position": (24, 7, -20, -5)},
    "crate_2": {"file": "assets/tileset/crate_2.png", "position": (29, 10, -30, 28)},
    "chair_": {"file": "assets/tileset/chair_1.png", "position": (28, 11, -13, 0)},
    "sword": {"file": "assets/tileset/sword.png", "position": (28, 10, 15, 28)},
    "iron": {"file": "assets/tileset/iron.png", "position": (28, 10, 6, 35)},
    "weapons": {"file": "assets/tileset/weapons.png", "position": (27, 6, 0, -10)},
    "shield": {"file": "assets/tileset/shield.png", "position": (27, 7, 0, -8)},
}

# Elementos interativos do mapa, com suas respectivas posições e tipos
interactions = {
    "key_lock": {"file": "assets/interactive/key_lock.png", "position": (8, 16, 5, 5), "type": "lock"},
    "keyless_lock": {"file": "assets/interactive/keyless_lock.png", "position": (8, 16, 5, 5), "type": "lock"},
    "door_closed": {"file": "assets/interactive/door_closed.png", "position": (7, 16, 0, -10), "type": "door"},
    "door_open": {"file": "assets/interactive/door_open.png", "position": (7, 16, 0, -10), "type": "door"},
    
    "lever_up": {"file": "assets/interactive/lever_up.png", "position": (18, 13, 10, 0), "type": "lever"},
    "lever_down": {"file": "assets/interactive/lever_down.png", "position": (18, 13, 10, 0), "type": "lever"},
    "gate_closed": {"file": "assets/interactive/gate_closed.png", "position": (17, 13, 0, -5), "type": "gate"},
    "gate_open": {"file": "assets/interactive/gate_open.png", "position": (17, 13, 0, -5), "type": "gate"},

    "crate_1": {"file": "assets/interactive/crate_1.png", "position": (19, 17, 0, 10), "type": "crate"},
    "crate_cracked": {"file": "assets/interactive/crate_1_cracked.png", "position": (19, 17, 0, 10), "type": "crate"},
    "crate_broken": {"file": "assets/interactive/crate_1_broken.png", "position": (19, 17, 0, 10), "type": "crate"},
}


def create_map(canvas):
    """
    Cria o mapa no canvas baseado no tileset definido.

    Argumentos:
        canvas (tk.Canvas): O canvas onde o mapa é desenhado.
    """
    for item, info in tileset.items():
        try:
            img = Image.open(info["file"])
            img = ImageTk.PhotoImage(img)
            canvas.create_image(
                info["position"][0] * TILE_SIZE + info["position"][2] + X_OFFSET,
                info["position"][1] * TILE_SIZE + info["position"][3] + Y_OFFSET,
                image=img, anchor="nw"
            )
            if not hasattr(canvas, 'images'):
                canvas.images = []
            canvas.images.append(img)
        except Exception as e:
            print(f"Erro ao carregar a imagem {info['file']}: {e}")

def create_interactions(canvas, lever_state, gate_state, lock_state, door_state):
    """
    Cria as interações no canvas baseado no estado dos elementos.

    Argumentos:
        canvas (tk.Canvas): O canvas onde as interações serão desenhadas.
        lever_state (str): Estado da alavanca.
        gate_state (str): Estado do portão.
        lock_state (str): Estado da fechadura.
        door_state (str): Estado da porta.
    """
    try:
        lever_info = interactions[lever_state]
        gate_info = interactions[gate_state]
        lock_info = interactions[lock_state]
        door_info = interactions[door_state]

        lever_img = Image.open(lever_info["file"])
        lever_img = ImageTk.PhotoImage(lever_img)

        gate_img = Image.open(gate_info["file"])
        gate_img = ImageTk.PhotoImage(gate_img)

        lock_img = Image.open(lock_info["file"])
        lock_img = ImageTk.PhotoImage(lock_img)

        door_img = Image.open(door_info["file"])
        door_img = ImageTk.PhotoImage(door_img)

        lever_id = canvas.create_image(
            lever_info["position"][0] * TILE_SIZE + lever_info["position"][2] + X_OFFSET,
            lever_info["position"][1] * TILE_SIZE + lever_info["position"][3] + Y_OFFSET,
            image=lever_img, anchor="nw", tags=("lever",)
        )

        gate_id = canvas.create_image(
            gate_info["position"][0] * TILE_SIZE + gate_info["position"][2] + X_OFFSET,
            gate_info["position"][1] * TILE_SIZE + gate_info["position"][3] + Y_OFFSET,
            image=gate_img, anchor="nw", tags=("gate",)
        )

        lock_id = canvas.create_image(
            lock_info["position"][0] * TILE_SIZE + lock_info["position"][2] + X_OFFSET,
            lock_info["position"][1] * TILE_SIZE + lock_info["position"][3] + Y_OFFSET,
            image=lock_img, anchor="nw", tags=("lock",)
        )

        door_id = canvas.create_image(
            door_info["position"][0] * TILE_SIZE + door_info["position"][2] + X_OFFSET,
            door_info["position"][1] * TILE_SIZE + door_info["position"][3] + Y_OFFSET,
            image=door_img, anchor="nw", tags=("door",)
        )

        crate_info = interactions["crate_1"]
        crate_img = Image.open(crate_info["file"])
        crate_img = ImageTk.PhotoImage(crate_img)
        crate_id = canvas.create_image(
            crate_info["position"][0] * TILE_SIZE + crate_info["position"][2] + X_OFFSET,
            crate_info["position"][1] * TILE_SIZE + crate_info["position"][3] + Y_OFFSET,
            image=crate_img, anchor='nw', tags=("crate",)
        )

        if not hasattr(canvas, 'images'):
            canvas.images = []
        canvas.images.extend([lever_img, gate_img, lock_img, door_img, crate_img])
    except Exception as e:
        print(f"Erro ao criar interações: {e}")

def create_boss_room(canvas, visibility="hidden"):
    """
    Cria a sala do Boss no canvas, que irá iniciar "bloqueada" para o jogador nnão visível no canvas.

    Argumentos:
        canvas (tk.Canvas): O canvas onde a sala do Boss é desenhada.
        visibility (str): Define a visibilidade dos itens na sala do Boss.
    """
    boss_room_x_offset = 0
    boss_room_y_offset = 0

    # Todos os tilesets contidos na sala do Boss
    boss_room_tileset = {
        "floor_6": {"file": "assets/tileset/floor_6.png", "position": (12, 5, 0, 0)},
        "wall_7": {"file": "assets/tileset/wall_7.png", "position": (12, 3, 0, 10)},
        "pillar_1": {"file": "assets/tileset/pillar_1.png", "position": (14, 4, -10, 0)},
        "pillar_2": {"file": "assets/tileset/pillar_2.png", "position": (19, 4, -10, 0)},
        "coffin": {"file": "assets/tileset/coffin.png", "position": (16, 4, 0, 0)},
    }

    boss_room_items = []
    try:
        for item, info in boss_room_tileset.items():
            img = Image.open(info["file"])
            img = ImageTk.PhotoImage(img)
            item_id = canvas.create_image(
                info["position"][0] * TILE_SIZE + info["position"][2] + boss_room_x_offset,
                info["position"][1] * TILE_SIZE + info["position"][3] + boss_room_y_offset,
                image=img, anchor="nw", state=visibility
            )
            boss_room_items.append((item_id, img))
    except Exception as e:
        print(f"Erro ao criar sala do Boss: {e}")

    if not hasattr(canvas, 'boss_room_items'):
        canvas.boss_room_items = boss_room_items
    else:
        canvas.boss_room_items.extend(boss_room_items)

def toggle_boss_room_visibility(canvas, visibility="hidden"):
    """
    Alterna a visibilidade dos itens na sala do Boss.

    Argumentos:
        canvas (tk.Canvas): O canvas onde a sala do Boss foi desenhada.
        visibility (str): Define a visibilidade dos itens.
    """
    for item_id, _ in canvas.boss_room_items:
        canvas.itemconfigure(item_id, state=visibility)

def update_lever_state(canvas, lever_state):
    """
    Atualiza o estado da alavanca no canvas.

    Argumentos:
        canvas (tk.Canvas): O canvas onde a alavanca foi desenhada.
        lever_state (str): O novo estado da alavanca.
    """
    try:
        lever_info = interactions[lever_state]
        lever_img = Image.open(lever_info["file"])
        lever_img = ImageTk.PhotoImage(lever_img)

        canvas.itemconfig("lever", image=lever_img)

        if not hasattr(canvas, 'images'):
            canvas.images = []
        canvas.images.append(lever_img)
    except Exception as e:
        print(f"Erro ao atualizar estado da alavanca: {e}")

def update_gate_state(canvas, gate_state):
    """
    Atualiza o estado do portão no canvas.

    Argumentos:
        canvas (tk.Canvas): O canvas onde o portão foi desenhado.
        gate_state (str): O novo estado do portão.
    """
    try:
        gate_info = interactions[gate_state]
        gate_img = Image.open(gate_info["file"])
        gate_img = ImageTk.PhotoImage(gate_img)

        canvas.itemconfig("gate", image=gate_img)

        if not hasattr(canvas, 'images'):
            canvas.images = []
        canvas.images.append(gate_img)
    except Exception as e:
        print(f"Erro ao atualizar estado do portão: {e}")

def update_lock_state(canvas, lock_state):
    """
    Atualiza o estado da fechadura no canvas.

    Argumentos:
        canvas (tk.Canvas): O canvas onde a fechadura foi desenhada.
        lock_state (str): O novo estado da fechadura.
    """
    try:
        lock_info = interactions[lock_state]
        lock_img = Image.open(lock_info["file"])
        lock_img = ImageTk.PhotoImage(lock_img)

        canvas.itemconfig("lock", image=lock_img)

        if not hasattr(canvas, 'images'):
            canvas.images = []
        canvas.images.append(lock_img)
    except Exception as e:
        print(f"Erro ao atualizar estado da fechadura: {e}")

def update_door_state(canvas, door_state):
    """
    Atualiza o estado da porta no canvas.

    Argumentos:
        canvas (tk.Canvas): O canvas onde a porta foi desenhada.
        door_state (str): O novo estado da porta.
    """
    try:
        door_info = interactions[door_state]
        door_img = Image.open(door_info["file"])
        door_img = ImageTk.PhotoImage(door_img)

        canvas.itemconfig("door", image=door_img)

        if not hasattr(canvas, 'images'):
            canvas.images = []
        canvas.images.append(door_img)
    except Exception as e:
        print(f"Erro ao atualizar estado da porta: {e}")

def update_crate_state(canvas, crate_state):
    """
    Atualiza o estado do caixote (crate) no canvas.

    Argumentos:
        canvas (tk.Canvas): O canvas onde o caixote foi desenhado.
        crate_state (str): O novo estado do caixote.
    """
    try:
        crate_info = interactions[crate_state]
        crate_img = Image.open(crate_info['file'])
        crate_img = ImageTk.PhotoImage(crate_img)
        canvas.itemconfig("crate", image=crate_img)
        if not hasattr(canvas, 'images'):
            canvas.images = []
        canvas.images.append(crate_img)
    except Exception as e:
        print(f"Erro ao atualizar de crate: {e}")
