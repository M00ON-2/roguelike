import math # ? serve pra calculos de posição, colisão e movimento

import pgzrun

TILE_SIZE = 18
ROWS = 30
COLS = 20

WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS 
TITLE = "BOSTAAAAAAAAAAA"

plataforms = build("plataformer_plataform.csv", TILE_SIZE) 

def update():
    pass

def draw():
    screen.clear()
    screen.fill("skyblue")

pgzrun.go()