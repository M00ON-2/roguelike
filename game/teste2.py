import pgzrun
import random
import math
from pygame import Rect

# === CONFIG ===
TILE_SIZE = 18
ROWS = 30
COLS = 20
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Platformer Adventure"

# === GAME STATE ===
game_state = "menu"  # "menu", "playing", "dead"
music_on = True
sound_on = True

# === ENTITIES ===
platforms = []
coins = []
obstacles = []
trees = []
enemies = []

# === HERO ===
class Hero:
    def __init__(self, x, y):
        self.actor = Actor("hero_idle1", (x, y))
        self.vel_y = 0
        self.gravity = 0.5
        self.dead = False
        self.on_ground = False
        self.frame = 0
        self.anim_timer = 0
        self.state = "idle"  # "idle" or "walk"

    def rect(self):
        return Rect(self.actor.x - 8, self.actor.y - 16, 16, 32)

    def update(self):
        if self.dead:
            return

        # Movement
        move = 0
        if keyboard.left:
            self.actor.x -= 3
            move = -1
        elif keyboard.right:
            self.actor.x += 3
            move = 1

        # Gravity
        self.vel_y += self.gravity
        self.actor.y += self.vel_y

        self.on_ground = False
        self.check_platform_collisions()

        # Jump
        if self.on_ground and keyboard.up:
            self.vel_y = -10

        # Animation
        if move != 0:
            self.actor.angle = 0
            self.actor.flip_x = move < 0
            self.state = "walk"
        else:
            self.state = "idle"

        self.animate()

    def check_platform_collisions(self):
        hero_rect = self.rect()
        for block in platforms + trees:
            block_rect = Rect(block.x - 9, block.y - 9, 18, 18)
            if hero_rect.colliderect(block_rect):
                if self.vel_y > 0 and self.actor.y < block.y:
                    self.actor.y = block.y - 18
                    self.vel_y = 0
                    self.on_ground = True

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer > 6:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % 4
            if self.state == "walk":
                self.actor.image = f"hero_walk{self.frame + 1}"
            else:
                self.actor.image = f"hero_idle{self.frame + 1}"

hero = Hero(100, 100)


# === ENEMY ===
class Enemy:
    def __init__(self, x, y, left_limit, right_limit):
        self.actor = Actor("enemy_idle1", (x, y))
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.direction = 1
        self.frame = 0
        self.anim_timer = 0
        self.state = "walk"

    def rect(self):
        return Rect(self.actor.x - 8, self.actor.y - 8, 16, 16)

    def update(self):
        # Move left-right between limits
        self.actor.x += self.direction * 2
        if self.actor.x <= self.left_limit or self.actor.x >= self.right_limit:
            self.direction *= -1
            self.actor.flip_x = not self.actor.flip_x
        self.animate()

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % 4
            self.actor.image = f"enemy_walk{self.frame + 1}"

# Criação de inimigos
enemies.append(Enemy(300, 200, 260, 340))
enemies.append(Enemy(500, 150, 460, 560))


# === LOAD MAP ===
def load_map(caminho):
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")
    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor in ["21", "22", "23"]:
                image = "block1"
            elif valor in ["153", "154", "155", "156"]:
                image = "cloud"
            else:
                continue
            block = Actor(image)
            block.x = x * TILE_SIZE + TILE_SIZE // 2
            block.y = y * TILE_SIZE + TILE_SIZE // 2
            platforms.append(block)

load_map("C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv")

# === MUSIC & SOUND ===
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("bg_music")
    else:
        music.stop()

def toggle_sound():
    global sound_on
    sound_on = not sound_on


# === MENU ===
def draw_menu():
    screen.clear()
    screen.draw.text("MAIN MENU", center=(WIDTH // 2, 80), fontsize=50, color="white")
    screen.draw.text("1 - Start Game", center=(WIDTH // 2, 180), fontsize=40)
    screen.draw.text(f"2 - Music: {'ON' if music_on else 'OFF'}", center=(WIDTH // 2, 250), fontsize=40)
    screen.draw.text(f"3 - Sounds: {'ON' if sound_on else 'OFF'}", center=(WIDTH // 2, 320), fontsize=40)
    screen.draw.text("4 - Exit", center=(WIDTH // 2, 390), fontsize=40)
1
def update_menu():
    global game_state
    if keyboard.K_1:
        game_state = "playing"
        if music_on:
            music.play("bg_music")
    elif keyboard.K_2:
        toggle_music()
    elif keyboard.K_3:
        toggle_sound()
    elif keyboard.K_4:
        exit()


# === MAIN UPDATE ===
def update():
    global game_state

    if game_state == "menu":
        update_menu()
        return

    if game_state == "playing":
        hero.update()
        for enemy in enemies:
            enemy.update()

        # Check collisions with enemies
        hero_rect = hero.rect()
        for enemy in enemies:
            if hero_rect.colliderect(enemy.rect()):
                hero.dead = True
                game_state = "dead"
                if sound_on:
                    sounds.hit.play()
                break


# === DRAW ===
def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
        return

    for block in platforms:
        block.draw()
    for enemy in enemies:
        enemy.actor.draw()
    hero.actor.draw()

    if game_state == "dead":
        screen.draw.text("YOU DIED!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=60, color="red", shadow=(2, 2))


pgzrun.go()
