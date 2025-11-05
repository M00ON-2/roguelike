import pgzrun
import math
import random   
from pygame import Rect

import pgzrun

TILE_SIZE = 18
ROWS = 30
COLS = 20

WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS 
TITLE = "BOSTAAAAAAAAAAA"

# Armazena os blocos do mapa
plataformas = []
heroi = Actor("heroi", (100, 100))

# ! Função para carregar o "CSV" manualmente 
def carregar_mapa(caminho):
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")

    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor == "21" "22" "23":
               bloco = Actor("bloco")
               bloco.x = x * TILE_SIZE + TILE_SIZE // 2
               bloco.y = y * TILE_SIZE + TILE_SIZE // 2
               plataformas.append(bloco)

def carregar_coins(caminho):
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")

    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor != "-1":
               coin = Actor("coin")
               coin.x = x * TILE_SIZE + TILE_SIZE // 2
               coin.y = y * TILE_SIZE + TILE_SIZE // 2
               plataformas.append(coin)


carregar_mapa('C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv')
carregar_coins('C:/Users/PC/Documents/GitHub/roguelike/game/coins.csv')
# --- Movimento simples ---
vel_y = 0
gravidade = 0.5

def update():
    global vel_y

    # Movimento lateral
    if keyboard.left:
        heroi.x -= 3
    if keyboard.right:
        heroi.x += 3

    # Gravidade
    vel_y += gravidade
    heroi.y += vel_y

    # Colisão com plataformas
    heroi_rect = Rect(heroi.x - 16, heroi.y - 16, 32, 32)
    for bloco in plataformas:
        bloco_rect = Rect(bloco.x - 32, bloco.y - 32, 64, 64)
        if heroi_rect.colliderect(bloco_rect) and vel_y >= 0:
            heroi.y = bloco.y - 32  # pousa em cima do bloco
            vel_y = 0
            if keyboard.up:
                vel_y = -10  # pulo

def draw():
    screen.clear()
    for bloco in plataformas:
        bloco.draw()
    heroi.draw()

pgzrun.go()



# * update() atualizar o jogo toda hora
# draw() desenha o jogo 
# actor() objeto/coisa com imagem que pode aparecer na tela 
# * WIDTH e HEIGHT é pra definição do tamanho da tela
# screen.draw() é pra apresentar na tela
# Actor.pos ou Actor.x / Actor.y → define posição na tela
# Actor.draw() → desenha o sprite na tela atual

# ! • EXEMPLO DE DETECÇÃO DE MOVIMENTO

# if keyboard.left:
#   hero.x -= 5  # move 5 pixels para esquerda
# if keyboard.right:
#    hero.x += 5  # move 5 pixels para direita

# ! • EXEMPLO DE DETECÇÃO DE GRAVIDADE . \path\to\venv\Scripts\Activate.

# hero.vy += 0.5  # aceleração da gravidade
# hero.y += hero.vy

# if hero.y >= GROUND_Y:  # chão
  #  hero.y = GROUND_Y
  #  hero.vy = 0

# ! • EXEMPLO DE DETECÇÃO DE RELAÇÃO IMAGEM/ACTOR

# hero = Actor('hero_idle')
# hero.image = 'hero_run1'

# ! • EXEMPLO DE DETECÇÃO DE ANIMAÇÃO SPRITE

# frames = ['hero_run1', 'hero_run2', 'hero_run3']
# hero.frame = (hero.frame + 0.1) % len(frames)
# hero.image = frames[int(hero.frame)]



# Actor.pos ou Actor.x / Actor.y → define posição na tela
# Actor.draw() → desenha o sprite na tela atual