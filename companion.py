import pygame
import win32gui, win32con, win32api
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os
import random
import sys
import math


running = True
SCALE = 0.15  
animations = {
    "idle_primary_default": 7,
    "idle_primary_blink": 7,
    "idle_primary_sleepy": 14,
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
    idle_primary_default = load_frames("assets/moth-idle-default-clear")
    idle_primary_blink = load_frames("assets/moth-idle-blink-clear")
    idle_primary_sleepy = load_frames("assets/moth-idle-sleepy-clear")
    idle_primary_sleep_in = load_frames("assets/moth-idle-sleep-in-clear")
    idle_primary_sleep = load_frames("assets/moth-idle-sleep-clear")

    idle_secondary_sleep_z = load_frames("assets/secondary/moth-idle-sleep-z-clear")
    # Resize window to sprite size
    sprite_width = idle_primary_default[0].get_width()
    sprite_height = idle_primary_default[0].get_height()

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

    current_anim = "idle_primary_default"
    current_secondary_anim = ""
    secondary_frames = ""
    secondary_particles = []
    frame_index = 0
    frame_speed = 0.12

    x, y = 400, 400
    clock = pygame.time.Clock()
    double_blink = False
    last_click_time = pygame.time.get_ticks()
    left_pressed = win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0
    sleepy_count = 0
    asleep = False
    while running:
        mouse_x, mouse_y = win32api.GetCursorPos()

        over_sprite = (
            x <= mouse_x <= x + sprite_width and
            y <= mouse_y <= y + sprite_height
        )
        left_pressed = win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0
        if over_sprite and left_pressed:
            if current_anim == "idle_primary_sleep" and asleep:
                print("clicked")
                current_anim = "idle_primary_default"
                frame_index = 0    
                asleep = False
            last_click_time = pygame.time.get_ticks()

        time_since_click = pygame.time.get_ticks() - last_click_time
        
                
        
        # ⭐ PROCESS EVENTS (prevents freezing)
        for event in pygame.event.get():
            pass
        if current_anim == "idle_primary_default":
            frames = idle_primary_default 
        elif current_anim == "idle_primary_blink":
            frames = idle_primary_blink
        elif current_anim == "idle_primary_sleepy":
            frames = idle_primary_sleepy
        elif current_anim == "idle_primary_sleep_in":
            frame_speed = 0.08
            frames = idle_primary_sleep_in
        elif current_anim == "idle_primary_sleep":
            asleep = True
            frames = idle_primary_sleep
            if random.random() < 0.008 and len(secondary_particles) < 3:  # spawn chance per frame
                secondary_particles.append({
                    "base_x":  -35 + sprite_width // 2,
                    "y": 5,
                    "vy": -0.4,

                    "alpha": 255,

                    "frame": 0,
                    "frame_speed": random.uniform(0.1, 0.25),

                    "wave_offset": random.uniform(0, 6.28),  # start phase
                    "wave_speed": random.uniform(0.03, 0.06),
                    "amplitude": random.uniform(6, 14)
                })
                secondary_frames = idle_secondary_sleep_z
        for s in secondary_particles:
            s["y"] += s["vy"]
            s["alpha"] -= 3

            # Animate frame
            s["frame"] += s["frame_speed"]
            if s["frame"] >= len(secondary_frames):
                s["frame"] = 0

            # ⭐ Update sine phase
            s["wave_offset"] += s["wave_speed"]
        frame_index += frame_speed
        if frame_index >= len(frames):
            frame_index = 0

            if current_anim == "idle_primary_default":
                if time_since_click > 5000 - (sleepy_count * 2000): 
                    current_anim = "idle_primary_sleepy"
                    sleepy_count += 1
                    last_click_time = pygame.time.get_ticks()
                    if sleepy_count > 1:
                        current_anim = "idle_primary_sleep_in"
                        sleepy_count = 0
                else:
                    rand = random.random()
                    if rand < 0.18:
                        current_anim = "idle_primary_blink"
                    elif rand < 0.2:
                        current_anim = "idle_primary_sleepy"
                        sleepy_count += 1
                        last_click_time = pygame.time.get_ticks()
                
            elif current_anim == "idle_primary_blink":
                if random.random() < 0.6 and not double_blink:  # 30% chance of double blink
                    current_anim = "idle_primary_blink"
                    double_blink = True
                else:
                    current_anim = "idle_primary_default"
                    double_blink = False
            elif current_anim == "idle_primary_sleepy":
                current_anim = "idle_primary_default"
            elif current_anim == "idle_primary_sleep_in":
                current_anim = "idle_primary_sleep"
                frames = idle_primary_sleep
                frame_speed = 0.15
            elif current_anim == "idle_primary_sleep":
                current_anim == "idle_primary_sleep"
            else:
                current_anim = "idle_primary_default"

        current_frame = frames[int(frame_index)]

        secondary_particles = [s for s in secondary_particles if s["alpha"] > 0]

        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOPMOST, x, y, 0, 0, win32con.SWP_NOSIZE
        )

        screen.fill((0, 0, 0))
        for s in secondary_particles:
            drift_x = s["base_x"] + math.sin(s["wave_offset"]) * s["amplitude"]

            frame_img = secondary_frames[int(s["frame"])].copy()
            frame_img.set_alpha(s["alpha"])

            screen.blit(frame_img, (drift_x, s["y"]))
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
