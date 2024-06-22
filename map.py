import tkinter as tk
import PIL
from PIL import Image, ImageTk

TILE_SIZE = 32
X_OFFSET = 0  # Ajuste do eixo X
Y_OFFSET = 0  # Ajuste do eixo Y


MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


individual_images = {
    "wall_1": {"file": "assets/tileset/wall_1.png", "position": (5, 10, 0, 20)},
    "floor_1": {"file": "assets/tileset/floor_1.png", "position": (5, 12, 0, 10)},
    "gold_9": {"file": "assets/tileset/gold_9.png", "position": (5, 15, 0, -10)},
    "gold_1": {"file": "assets/tileset/gold_1.png", "position": (5, 12, 0, 0)},
    "gold_2": {"file": "assets/tileset/gold_2.png", "position": (9, 13, 0, 0)},
    "gold_3": {"file": "assets/tileset/gold_3.png", "position": (6, 14, 0, 0)},
    "gold_4": {"file": "assets/tileset/gold_4.png", "position": (7, 14, 0, 0)},
    "gold_5": {"file": "assets/tileset/gold_5.png", "position": (7, 13, 0, 0)},
    "gold_8": {"file": "assets/tileset/gold_8.png", "position": (5, 13, 10, 0)},    
    "floor_2": {"file": "assets/tileset/floor_2.png", "position": (5, 17, 0, 0)},
    "floor_4": {"file": "assets/tileset/floor_4.png", "position": (19, 15, -7, 7)},
    "floor_3": {"file": "assets/tileset/floor_3.png", "position": (11, 14, 9, 20)},
    "wall_3": {"file": "assets/tileset/wall_3.png", "position": (11, 13, 10, 14)},
    "wall_2": {"file": "assets/tileset/wall_2.png", "position": (5, 15, 0, 10)},
    "patch": {"file": "assets/tileset/patch.png", "position": (10, 18, -8, -20)},
    "wall_4": {"file": "assets/tileset/wall_4.png", "position": (14, 12, 14, 30)},
    "floor_5": {"file": "assets/tileset/floor_5.png", "position": (21, 8, 0, 0)},
    "stairs": {"file": "assets/tileset/stairs.png", "position": (21, 13, 0, 0)},
    "wall_5": {"file": "assets/tileset/wall_5.png", "position": (19, 13, -7, 14)},
    "sink": {"file": "assets/tileset/sink.png", "position": (20, 15, 0, -11)},
    "wall_6": {"file": "assets/tileset/wall_6.png", "position": (21, 6, 0, 10)},
    "table": {"file": "assets/tileset/table.png", "position": (22, 8, 0, -5)},
    "chair_2": {"file": "assets/tileset/chair_2.png", "position": (24, 8, -20, -5)},
    "chair_3": {"file": "assets/tileset/chair_3.png", "position": (22, 8, -15, -5)},
    "crate_2": {"file": "assets/tileset/crate_2.png", "position": (27, 11, 0, 0)},
    "chair_": {"file": "assets/tileset/chair_1.png", "position": (27, 11, -13, 0)},
    "sword": {"file": "assets/tileset/sword.png", "position": (28, 12, -18, -35)},
    "iron": {"file": "assets/tileset/iron.png", "position": (28, 12, -30, -20)},
    "weapons": {"file": "assets/tileset/weapons.png", "position": (25, 6, 0, 20)},
    "shield": {"file": "assets/tileset/shield.png", "position": (27, 12, 0, 0)},
    "crate_1": {"file": "assets/tileset/crate_1.png", "position": (18, 17, -10, 10)},
    

}

interaction_element = {
    "door_closed": {"file": "assets/tileset/door_closed.png", "position": (7, 16, 0, -5), "type": "door"},
    "door_open": {"file": "assets/tileset/door_open.png", "position": (7, 16, 0, -5), "type": "door"},
    "lock": {"file": "assets/tileset/lock.png", "position": (8, 16, 5, 5), "type": "lock_key"},
    "lock_key": {"file": "assets/tileset/lock_key.png", "position": (8, 16, 5, 5), "type": "lock_key"},

    "lever_up": {"file": "assets/tileset/lever_up.png", "position": (17, 13, 10, 20), "type": "lever"},
    "lever_down": {"file": "assets/tileset/lever_down.png", "position": (17, 13, 10, 20), "type": "lever"},
    "gate_closed": {"file": "assets/tileset/gate_closed.png", "position": (16, 13, 0, 15), "type": "gate"},
    "gate_open": {"file": "assets/tileset/gate_open.png", "position": (16, 13, 0, 15), "type": "gate"},
}

def create_map(canvas):
    for item, info in individual_images.items():
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

def create_interactive_elements(canvas, lever_state, gate_state, lock_state, door_state):
    lever_info = interaction_element[lever_state]
    gate_info = interaction_element[gate_state]
    lock_info = interaction_element[lock_state]
    door_info = interaction_element[door_state]

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

    if not hasattr(canvas, 'images'):
        canvas.images = []
    canvas.images.extend([lever_img, gate_img, lock_img, door_img])




def create_special_room(canvas, visibility="hidden"):
    special_room_x_offset = 0
    special_room_y_offset = 0

    special_room_elements = {
        "floor_7": {"file": "assets/tileset/floor_7.png", "position": (11, 6, 10, 0)},
        "wall_7": {"file": "assets/tileset/wall_7.png", "position": (11, 4, 10, 10)},
        "pillar_1": {"file": "assets/tileset/pillar_1.png", "position": (13, 5, -10, -10)},
        "pillar_2": {"file": "assets/tileset/pillar_2.png", "position": (18, 5, 0, -10)},
        "coffin": {"file": "assets/tileset/coffin.png", "position": (15, 5, 0, 0)},
    }

    special_room_items = []
    for item, info in special_room_elements.items():
        img = Image.open(info["file"])
        img = ImageTk.PhotoImage(img)
        item_id = canvas.create_image(
            info["position"][0] * TILE_SIZE + info["position"][2] + special_room_x_offset,
            info["position"][1] * TILE_SIZE + info["position"][3] + special_room_y_offset,
            image=img, anchor="nw", state=visibility
        )
        special_room_items.append((item_id, img))

    if not hasattr(canvas, 'special_room_items'):
        canvas.special_room_items = special_room_items
    else:
        canvas.special_room_items.extend(special_room_items)

def toggle_special_room_visibility(canvas, visibility="hidden"):
    for item_id, _ in canvas.special_room_items:
        canvas.itemconfigure(item_id, state=visibility)


def update_lever_state(canvas, lever_state):
    lever_info = interaction_element[lever_state]
    lever_img = Image.open(lever_info["file"])
    lever_img = ImageTk.PhotoImage(lever_img)

    canvas.itemconfig("lever", image=lever_img)

    if not hasattr(canvas, 'images'):
        canvas.images = []
    canvas.images.append(lever_img)


def update_gate_state(canvas, gate_state):
    gate_info = interaction_element[gate_state]
    gate_img = Image.open(gate_info["file"])
    gate_img = ImageTk.PhotoImage(gate_img)

    canvas.itemconfig("gate", image=gate_img)

    if not hasattr(canvas, 'images'):
        canvas.images = []
    canvas.images.append(gate_img)


def update_lock_state(canvas, lock_state):
    lock_info = interaction_element[lock_state]
    lock_img = Image.open(lock_info["file"])
    lock_img = ImageTk.PhotoImage(lock_img)

    canvas.itemconfig("lock", image=lock_img)

    if not hasattr(canvas, 'images'):
        canvas.images = []
    canvas.images.append(lock_img)


def update_door_state(canvas, door_state):
    door_info = interaction_element[door_state]
    door_img = Image.open(door_info["file"])
    door_img = ImageTk.PhotoImage(door_img)

    canvas.itemconfig("door", image=door_img)

    if not hasattr(canvas, 'images'):
        canvas.images = []
    canvas.images.append(door_img)