import pgzrun
import math

from pygame import Rect

TILE_SIZE = 18
ROWS = 30
COLS = 20

WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "COLISÃO CORRIGIDA"

plataformas = []
coins = []
obstacles = []
trees = []

hero = Actor("hero", (100, 100)) 
vel_y = 0
gravity = 0.5
dead = False

def load_map(caminho): # carrega as plataformas
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

def load_coins(caminho): #carrega as moedas
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


def load_obstacles(caminho): #carrega os obstaculos
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


def load_tree(caminho):
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

load_map('C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv')
load_coins('C:/Users/PC/Documents/GitHub/roguelike/game/coins.csv')
load_obstacles('C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv')
load_tree('C:/Users/PC/Documents/GitHub/roguelike/game/tree.csv')


def update():
    global vel_y, dead
    if dead:
        return

    # movimento lateral
    if keyboard.left:
        hero.x -= 3
    if keyboard.right:
        hero.x += 3

    # gravidade
    vel_y += gravity
    hero.y += vel_y

    heroi_rect = Rect(hero.x - 8, hero.y - 16, 16, 32)
    no_chao = False

    # --- colisão com plataformas ---
    for bloco in plataformas:
        bloco_rect = Rect(bloco.x - 9, bloco.y - 9, 18, 18)

        # Verifica colisão vertical realista
        if heroi_rect.colliderect(bloco_rect):
            # só para o herói se ele estiver DESCENDO e VINDO DE CIMA
            if vel_y > 0 and hero.y < bloco.y:
                hero.y = bloco.y - 18
                vel_y = 0
                no_chao = True

    # pular somente se realmente estiver no chão
    if no_chao and keyboard.up:
        vel_y = -10

    # --- colisão com moedas ---
    for coin in coins[:]:
        coin_rect = Rect(coin.x - 8, coin.y - 8, 16, 16)
        if heroi_rect.colliderect(coin_rect):
            coins.remove(coin)

    # --- colisão com obstáculos ---
    for obstacle in obstacles:
        obstacle_rect = Rect(obstacle.x - 8, obstacle.y - 8, 16, 16)
        if heroi_rect.colliderect(obstacle_rect):
            dead = True
            break


def draw():
    screen.clear()
    for bloco in plataformas:
        bloco.draw()
    for coin in coins:
        coin.draw()
    for t in trees:
        t.draw()
    for obstacle in obstacles:
        obstacle.draw()
    hero.draw()

    if dead:
        screen.draw.text("VOCÊ MORREU!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=40, color="red", shadow=(1, 1))


pgzrun.go()
