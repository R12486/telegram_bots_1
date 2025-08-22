import pgzrun
import json
import math
from random import randint

WIDTH = 960
HEIGHT = 720

# === ЗАГРУЗКА СОСТОЯНИЯ ===
try:
    with open("save.txt", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {
        "счёт": 0,
        "след. счёт": 5,
        "победы": 0,
        "сигнал": 0,
        "скорость": 1.0,
        "скин": "red",
        "открытые_скины": ["red"]
    }

score = data["счёт"]
next_score = data["след. счёт"]
victories = data["победы"]
signal = data["сигнал"]
speed = data["скорость"]
skin = data["скин"]
unlocked_skins = set(data["открытые_скины"])

# === АКТЁРЫ ===
bird = Actor(skin)
bird.pos = (100, HEIGHT // 2)
target = (WIDTH // 2, HEIGHT // 2)

pigs = []
NUM_PIGS = 5

skins_shop = ["red", "blue", "green", "yellow"]
skin_properties = {
    "red": 1.0,
    "blue": 1.3,
    "green": 0.8,
    "yellow": 1.6
}

shop_index = 0
in_shop = False

# === СОЗДАНИЕ СВИНЕЙ ===
def create_pigs():
    pigs.clear()
    for _ in range(NUM_PIGS):
        pig = Actor("pig")
        pig.x = WIDTH // 2 + randint(-150, 150)
        pig.y = HEIGHT // 2 + randint(-150, 150)
        pigs.append(pig)

create_pigs()

# === ОТРИСОВКА ===
def draw():
    screen.clear()
    screen.blit("background", (0, 0))

    if in_shop:
        draw_shop()
    else:
        for pig in pigs:
            pig.draw()
        bird.draw()
        screen.draw.text(f"Счёт: {score}", (20, 20), fontsize=40, color="white")
        screen.draw.text(f"Победы: {victories}", (20, 70), fontsize=30, color="white")
        screen.draw.text("Нажми S для магазина", (WIDTH - 280, 20), fontsize=30, color="yellow")

# === ОТРИСОВКА МАГАЗИНА ===
def draw_shop():
    screen.draw.text("МАГАЗИН СКИНОВ", center=(WIDTH//2, 60), fontsize=60, color="white")
    for i, name in enumerate(skins_shop):
        y = 150 + i * 100
        color = "green" if name in unlocked_skins else "gray"
        screen.draw.text(f"{name}  {'[Открыт]' if name in unlocked_skins else '[Закрыт]' }", center=(WIDTH//2, y), fontsize=40, color=color)
    screen.draw.text("Кликни по скину для выбора / покупки", center=(WIDTH//2, HEIGHT - 80), fontsize=30, color="white")
    screen.draw.text("Нажми S, чтобы вернуться", center=(WIDTH//2, HEIGHT - 40), fontsize=25, color="yellow")

# === ОБНОВЛЕНИЕ ===
def update():
    global score, next_score, victories, signal, speed, NUM_PIGS

    if in_shop:
        return

    if signal == 1:
        dx = target[0] - bird.x
        dy = target[1] - bird.y
        dist = math.hypot(dx, dy)

        if dist > 5:
            bird.x += dx / dist * speed
            bird.y += dy / dist * speed
        else:
            for pig in pigs:
                if bird.colliderect(pig):
                    score += 1
                    sounds.recording1.play()
                    pigs.remove(pig)
                    break
            bird.pos = (100, HEIGHT // 2)
            signal = 0
            speed = skin_properties.get(skin, 1.0)

    if not pigs:
        victories += 1
        NUM_PIGS += 1
        next_score += 5
        create_pigs()

    if score < 0:
        sounds.recording2.play()
        quit()

# === УПРАВЛЕНИЕ ===
def on_mouse_down(pos):
    global signal, skin

    if in_shop:
        for i, name in enumerate(skins_shop):
            y = 150 + i * 100
            if y - 30 <= pos[1] <= y + 30:
                if name in unlocked_skins:
                    skin = name
                    bird.image = skin
                else:
                    if score >= 5:
                        score -= 5
                        unlocked_skins.add(name)
                        skin = name
                        bird.image = skin
                        sounds.recording1.play()
        return

    if bird.collidepoint(pos) and signal == 0:
        signal = 1
        dx = target[0] - bird.x
        dy = target[1] - bird.y
        dist = math.hypot(dx, dy)
        speed = dist / 100 * skin_properties.get(skin, 1.0)

# === КЛАВИШИ ===
def on_key_down(key):
    global in_shop
    if key == keys.S:
        in_shop = not in_shop

# === СОХРАНЕНИЕ ===
def save_state():
    data["счёт"] = score
    data["след. счёт"] = next_score
    data["победы"] = victories
    data["сигнал"] = signal
    data["скорость"] = speed
    data["скин"] = skin
    data["открытые_скины"] = list(unlocked_skins)
    with open("save.txt", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

import atexit
atexit.register(save_state)

pgzrun.go()