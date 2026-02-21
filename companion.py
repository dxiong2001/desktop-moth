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
import ctypes
from ctypes import wintypes
from moth.sprite import PixelSprite
from moth.moth import Moth
from behaviors.idle import IdleBehavior
from behaviors.blink import BlinkBehavior
from behaviors.sleep import SleepBehavior
from behaviors.sleepy import SleepyBehavior
from behaviors.sleep_transition import SleepTransitionBehavior
from behaviors.honk import HonkBehavior
from affects.sleep_z import SleepZBehavior
from affects.honk_glow import HonkGlowBehavior


running = True
SCALE = 0.15  
clear_surface = pygame.Surface((400, 400), pygame.SRCALPHA)

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

            # SCALE IMAGE
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
    pygame.display.set_icon(pygame.image.load("icon.png"))
    pygame.init()
    
    # Create a temporary window
    screen = pygame.display.set_mode((1, 1), pygame.NOFRAME)

    # Load images
    idle_primary_default = load_frames("assets/idle/moth-idle-default-clear")
    idle_primary_blink = load_frames("assets/idle/moth-idle-blink-clear")
    idle_primary_sleepy = load_frames("assets/idle/moth-idle-sleepy-clear")
    idle_primary_sleep_in = load_frames("assets/idle/moth-idle-sleep-in-clear")
    idle_primary_sleep = load_frames("assets/idle/moth-idle-sleep-clear")

    interaction_honk = load_frames("assets/interactions/moth-interaction-honk-clear")

    idle_secondary_sleep_z = load_frames("assets/secondary/moth-idle-sleep-z-clear")
    interaction_honk_glow = load_frames("assets/secondary/moth-interaction-honk-glow-clear")
    # Resize window to sprite size
    sprite_width = idle_primary_default[0].get_width()
    sprite_height = idle_primary_default[0].get_height()

    screen = pygame.display.set_mode(
        (sprite_width, sprite_height+400), pygame.NOFRAME
    )

    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    # Transparent + always on top
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        | win32con.WS_EX_LAYERED
        | win32con.WS_EX_TOPMOST
    )
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        | win32con.WS_EX_TOOLWINDOW  # hides from taskbar
    )
    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY
    )
    # Show window once ready
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

    current_anim = "idle_primary_default"
    secondary_frames = ""
    secondary_particles = []
    frame_index = 0
    frame_speed = 0.12
    
    SPI_GETWORKAREA = 0x0030

    rect = wintypes.RECT()
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETWORKAREA, 0, ctypes.byref(rect), 0
    )

    # Create moth
    print(sprite_height)
    moth = Moth(sprite_width, sprite_height)

    # Add behaviors
    moth.controller.add("idle", IdleBehavior(moth, idle_primary_default))
    moth.controller.add("blink", BlinkBehavior(moth, idle_primary_blink))
    moth.controller.add("sleep", SleepBehavior(moth, idle_primary_sleep))
    moth.controller.add("sleep_transition", SleepTransitionBehavior(moth, idle_primary_sleep_in))
    moth.controller.add("sleepy", SleepyBehavior(moth, idle_primary_sleepy))
    
    moth.controller.add("honk", HonkBehavior(moth, interaction_honk))

    moth.controller.add_affect("sleep_z", SleepZBehavior(moth, idle_secondary_sleep_z))
    moth.controller.add_affect("honk_glow", HonkGlowBehavior(moth, interaction_honk_glow))
    moth.controller.set("idle")


   
    right = rect.right
    bottom = rect.bottom
    x, y = right-sprite_width, bottom-sprite_height + 45

    clock = pygame.time.Clock()
    while running:

        dt = clock.tick(36) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        secondary_particles = [s for s in secondary_particles if s["alpha"] > 0]

        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOPMOST, x, y-200, 0, 0, win32con.SWP_NOSIZE
        )
        screen.fill((0, 0, 0, 0))  # RGBA with alpha=0
        moth.update(dt, screen)


        pygame.display.update()


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
