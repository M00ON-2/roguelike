import math

import pgzrun
from pygame import Rect

# === CONFIGURAÇÕES BÁSICAS ===
TILE_SIZE = 18
ROWS = 30
COLS = 20

WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "COLISÃO CORRIGIDA"

# === LISTAS DE OBJETOS ===
plataformas = []
coins = []
obstacles = []
trees = []

# === HEROI ===
hero = Actor("hero", (100, 100))
vel_y = 0
gravity = 0.5
dead = False


# === FUNÇÕES DE CARREGAMENTO ===
def load_map(caminho):  # plataformas (terra e nuvens)
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
            plataformas.append(block)


def load_coins(caminho):  # moedas
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")
    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor != "-1":
                coin = Actor("coin")
                coin.x = x * TILE_SIZE + TILE_SIZE // 2
                coin.y = y * TILE_SIZE + TILE_SIZE // 2
                coins.append(coin)


def load_obstacles(caminho):  # obstáculos que matam
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")
    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor != "-1":
                obstacle = Actor("obstacle")
                obstacle.x = x * TILE_SIZE + TILE_SIZE // 2
                obstacle.y = y * TILE_SIZE + TILE_SIZE // 2
                obstacles.append(obstacle)


def load_tree(caminho):  # árvores (apenas decorativas)
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")
    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor != "-1":
                t = Actor("tree")
                t.x = x * TILE_SIZE + TILE_SIZE // 2
                t.y = y * TILE_SIZE + TILE_SIZE // 2
                trees.append(t)


# === CARREGAR OS MAPAS ===
load_map('C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv')
load_coins('C:/Users/PC/Documents/GitHub/roguelike/game/coins.csv')
load_obstacles('C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv')
load_tree('C:/Users/PC/Documents/GitHub/roguelike/game/tree.csv')


# === LÓGICA DO JOGO ===
def update():
    global vel_y, dead
    if dead:
        return

    # Movimento lateral
    if keyboard.left:
        hero.x -= 3
    if keyboard.right:
        hero.x += 3

    # Gravidade
    vel_y += gravity
    hero.y += vel_y

    heroi_rect = Rect(hero.x - 8, hero.y - 16, 16, 32)
    no_chao = False

    # --- Colisão com plataformas (terra e nuvem) ---
    for bloco in plataformas:
        largura, altura = bloco.width, bloco.height  # usa o tamanho real da sprite
        bloco_rect = Rect(bloco.x - largura / 2, bloco.y - altura / 2, largura, altura)

        if heroi_rect.colliderect(bloco_rect):
            # só colide se o herói estiver descendo e vindo de cima
            if vel_y > 0 and hero.y < bloco.y:
                hero.y = bloco_rect.top - 16  # 16 = metade da altura do herói
                vel_y = 0
                no_chao = True

    # Pular apenas se estiver no chão
    if no_chao and keyboard.up:
        vel_y = -10

    # --- Colisão com moedas ---
    for coin in coins[:]:
        coin_rect = Rect(coin.x - 8, coin.y - 8, 16, 16)
        if heroi_rect.colliderect(coin_rect):
            coins.remove(coin)

    # --- Colisão com obstáculos (morte) ---
    for obstacle in obstacles:
        obstacle_rect = Rect(obstacle.x - 8, obstacle.y - 8, 16, 16)
        if heroi_rect.colliderect(obstacle_rect):
            dead = True
            break


# === DESENHAR NA TELA ===
def draw():
    screen.clear()
    for bloco in plataformas:
        bloco.draw()
    for coin in coins:
        coin.draw()
    for obstacle in obstacles:
        obstacle.draw()
    for t in trees:
        t.draw()
    hero.draw()

    if dead:
        screen.draw.text("VOCÊ MORREU!",
                         center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=40,
                         color="red",
                         shadow=(1, 1))


pgzrun.go()
