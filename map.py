import tkinter as tk
import PIL
from PIL import Image, ImageTk

TILE_SIZE = 64
X_OFFSET = 0  # Ajuste do eixo X
Y_OFFSET = 0  # Ajuste do eixo Y

MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

individual_images = {
    "wall_1": {"file": "assets/tileset/wall_1.png", "position": (5, 5, -5, 0)},
    "floor_1": {"file": "assets/tileset/floor_1.png", "position": (5, 6, -5, -10)},
    "gold_9": {"file": "assets/tileset/gold_9.png", "position": (5, 7, 0, -15)},
    "gold_1": {"file": "assets/tileset/gold_1.png", "position": (5, 6, 5, -30)},
    "gold_2": {"file": "assets/tileset/gold_2.png", "position": (7, 6, -5, -15)},
    "gold_3": {"file": "assets/tileset/gold_3.png", "position": (5, 6, 0, 0)},
    "gold_4": {"file": "assets/tileset/gold_4.png", "position": (6, 6, -20, 0)},
    "gold_5": {"file": "assets/tileset/gold_5.png", "position": (6, 6, -10, 10)},
    "gold_8": {"file": "assets/tileset/gold_8.png", "position": (5, 6, 10, 10)},    
    "floor_2": {"file": "assets/tileset/floor_2.png", "position": (5, 8, -5, -10)},
    "floor_3": {"file": "assets/tileset/floor_3.png", "position": (8, 7, -10, 20)},
    "wall_3": {"file": "assets/tileset/wall_3.png", "position": (7, 7, 27, -15)},
    "wall_2": {"file": "assets/tileset/wall_2.png", "position": (5, 7, -5, 0)},
    "floor_4": {"file": "assets/tileset/floor_4.png", "position": (11, 8, -22, -20)},
    "patch": {"file": "assets/tileset/patch.png", "position": (7, 8, 20, 10)},
    "wall_4": {"file": "assets/tileset/wall_4.png", "position": (8, 7, 31, -30)},
    "floor_5": {"file": "assets/tileset/floor_5.png", "position": (12, 5, -15, -35)},
    "stairs": {"file": "assets/tileset/stairs.png", "position": (12, 7, -15, -28)},
    "wall_5": {"file": "assets/tileset/wall_5.png", "position": (11, 7, -22, -15)},
    "sink": {"file": "assets/tileset/sink.png", "position": (11, 8, 10, -37)},
    "wall_6": {"file": "assets/tileset/wall_6.png", "position": (12, 4, -15, -28)},
    "table": {"file": "assets/tileset/table.png", "position": (13, 4, -30, 20)},
    "chair_2": {"file": "assets/tileset/chair_2.png", "position": (13, 4, 15, 20)},
    "chair_3": {"file": "assets/tileset/chair_3.png", "position": (12, 4, 15, 20)},
    "crate_2": {"file": "assets/tileset/crate_2.png", "position": (15, 6, -35, -20)},
    "sword": {"file": "assets/tileset/sword.png", "position": (15, 6, -25, -25)},
    "iron": {"file": "assets/tileset/iron.png", "position": (15, 6, -32, 0)},
    "weapons": {"file": "assets/tileset/weapons.png", "position": (14, 4, -10, -15)},
    "shield": {"file": "assets/tileset/shield.png", "position": (15, 7, -35, -50)},
    "crate_1": {"file": "assets/tileset/crate_1.png", "position": (10, 8, 15, 0)},
    

}

interaction_element = {
    "door_closed": {"file": "assets/tileset/door_closed.png", "position": (6, 7, 0, 18), "type": "door"},
    "door_open": {"file": "assets/tileset/door_open.png", "position": (6, 7, 0, 18), "type": "door"},
    "lock": {"file": "assets/tileset/lock.png", "position": (7, 7, -25, 30), "type": "lock_key"},
    "lock_key": {"file": "assets/tileset/lock_key.png", "position": (7, 7, -25, 30), "type": "lock_key"},

    "lever_up": {"file": "assets/tileset/lever_up.png", "position": (10, 7, -5, 0), "type": "lever"},
    "lever_down": {"file": "assets/tileset/lever_down.png", "position": (10, 7, -5, 0), "type": "lever"},
    "gate_closed": {"file": "assets/tileset/gate_closed.png", "position": (9, 7, 15, -12), "type": "gate"},
    "gate_open": {"file": "assets/tileset/gate_open.png", "position": (9, 7, 15, -12), "type": "gate"},

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
    special_room_x_offset = 100 
    special_room_y_offset = 100  

    special_room_elements = {
        "floor_7": {"file": "assets/tileset/floor_7.png", "position": (6, 2, -10, -8)},
        "wall_7": {"file": "assets/tileset/wall_7.png", "position": (6, 1, -10, 0)},
        "pillar_1": {"file": "assets/tileset/pillar_1.png", "position": (7, 1, -20, 0)},
        "pillar_2": {"file": "assets/tileset/pillar_2.png", "position": (9, 1, 0, 0)},
        "coffin": {"file": "assets/tileset/coffin.png", "position": (8, 2, -20, -25)},
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

