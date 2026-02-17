import pygame
import win32gui, win32con, win32api
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os
import random
import sys

running = True
SCALE = 0.15  
animations = {
    "idle_default": 7,
    "idle_blink": 7,
    "idle_sleepy": 14,
}

# ===============================
# LOAD FRAMES
# ===============================
def load_frames(folder):
    frames = []

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        sys.exit()

    for file in os.listdir(folder):
        if file.endswith(".png"):
            path = os.path.join(folder, file)

            img = pygame.image.load(path).convert_alpha()

            # ⭐ SCALE IMAGE
            w = int(img.get_width() * SCALE)
            h = int(img.get_height() * SCALE)
            img = pygame.transform.smoothscale(img, (w, h))

            frames.append(img)

    return frames


# ===============================
# COMPANION WINDOW
# ===============================
def companion():
    global running

    pygame.init()

    # 🟢 STEP 1 — Create a temporary window FIRST
    screen = pygame.display.set_mode((300, 300), pygame.NOFRAME)

    # 🟢 STEP 2 — Now loading images is safe
    idle_default = load_frames("assets/moth-idle-default-clear")
    idle_blink = load_frames("assets/moth-idle-blink-clear")
    idle_sleepy = load_frames("assets/moth-idle-sleepy-clear")
    # Resize window to sprite size
    sprite_width = idle_default[0].get_width()
    sprite_height = idle_default[0].get_height()

    screen = pygame.display.set_mode(
        (sprite_width, sprite_height), pygame.NOFRAME
    )

    hwnd = pygame.display.get_wm_info()["window"]

    # Transparent + always on top
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        | win32con.WS_EX_LAYERED
        | win32con.WS_EX_TOPMOST
    )

    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY
    )

    current_anim = "idle_default"
    frame_index = 0

    x, y = 400, 400
    clock = pygame.time.Clock()
    double_blink = False
    last_click_time = pygame.time.get_ticks()
    left_pressed = win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0
    sleepy_count = 0

    while running:
        mouse_x, mouse_y = win32api.GetCursorPos()

        over_sprite = (
            x <= mouse_x <= x + sprite_width and
            y <= mouse_y <= y + sprite_height
        )

        left_pressed = win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0

        if over_sprite and left_pressed:
            last_click_time = pygame.time.get_ticks()

        time_since_click = pygame.time.get_ticks() - last_click_time
        
        # ⭐ PROCESS EVENTS (prevents freezing)
        for event in pygame.event.get():
            pass
        if current_anim == "idle_default":
            frames = idle_default 
        elif current_anim == "idle_blink":
            frames = idle_blink
        elif current_anim == "idle_sleepy":
            frames = idle_sleepy

        frame_index += 0.15

        if frame_index >= len(frames):
            frame_index = 0

            if current_anim == "idle_default":
                if time_since_click > 35000 - (sleepy_count * 2000): 
                    current_anim = "idle_sleepy"
                    sleepy_count += 1
                    last_click_time = pygame.time.get_ticks()
                else:
                    rand = random.random()
                    if rand < 0.18:
                        current_anim = "idle_blink"
                    elif rand < 0.2:
                        current_anim = "idle_sleepy"
                        sleepy_count += 1
                        last_click_time = pygame.time.get_ticks()
                
            elif current_anim == "idle_blink":
                if random.random() < 0.6 and not double_blink:  # 30% chance of double blink
                    current_anim = "idle_blink"
                    double_blink = True
                else:
                    current_anim = "idle_default"
                    double_blink = False
            elif current_anim == "idle_sleepy":
                if sleepy_count > 5:
                    sleepy_count = 0
                else:
                    current_anim = "idle_default"

            else:
                current_anim = "idle_default"

        current_frame = frames[int(frame_index)]

        

        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOPMOST, x, y, 0, 0, win32con.SWP_NOSIZE
        )

        screen.fill((0, 0, 0))
        screen.blit(current_frame, (0, 0))
        pygame.display.update()

        clock.tick(60)

    pygame.quit()

# ===============================
# TRAY
# ===============================
def quit_app(icon, item):
    global running
    running = False
    icon.stop()

def tray():
    image = Image.open("icon.png")
    icon = pystray.Icon(
        "SkyMoth",
        image,
        menu=pystray.Menu(item("Quit", quit_app))
    )
    icon.run()

# ===============================
# RUN
# ===============================
threading.Thread(target=companion).start()
tray()
