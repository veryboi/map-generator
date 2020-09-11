import pygame
import random
from pygame.locals import *
import math
from opensimplex import OpenSimplex
from enum import Enum
from PIL import Image
import numpy as np

class Terrain(Enum):
    WATER = 0
    BEACH = 1
    FOREST = 2
    JUNGLE = 3
    SAVANNAH = 4
    DESERT = 5
    SNOW = 6

dimensions = (600,400)
screen = pygame.display.set_mode(dimensions)
pygame.init()
pygame.display.set_caption("Map Generator")
clock = pygame.time.Clock()

pix_size = 10
height = math.floor(dimensions[1]/pix_size)
width = math.floor(dimensions[0]/pix_size)

gen = OpenSimplex(random.randint(0, 10000))
gen2 = OpenSimplex(random.randint(0,10000))
def noise(nx, ny):
    return gen.noise2d(nx, ny) / 2.0 + 0.5
def noise2(nx, ny):
    return gen2.noise2d(nx, ny) / 2.0 + 0.5


grad = Image.open('gradient2.png')
pix = grad.convert('RGB')


def biome(e, m):
    x = pix.getpixel((math.floor(m * 198), 197-math.floor(e * 198)))
    return x


freq = 5
elevation = np.zeros((height, width, 2))
pos = [0,0]





def generate():
    for y in range(height):
        for x in range(width):
            nx = (x + pos[0]) / width - 0.5
            ny = (y + pos[1]) / height - 0.5
            a, b, c = 1, 0.7, 0.1
            e = min(0.99,max(0.01, (a * noise(freq * nx, freq * ny) + b * noise(2 * freq * nx, 2 * freq * ny) + c * noise(
                4 * freq * nx, 4 * freq * ny))/(a+b+c)))
            # print(e)
            m = min(0.99,max(0.01, noise2(freq * nx, freq * ny) + 0.5 * noise2(2 * freq * nx, 2 * freq * ny) + 0.25 * noise2(
                4 * freq * nx, 4 * freq * ny)))
            elevation[y][x] = [math.pow(e, 2), math.pow(m, 2)]
generate()
running = True
while running:
    keys_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                freq /= 2
            if event.button == 5:
                freq *= 2
            generate()
    if keys_pressed[K_LEFT]:
        pos[0]-=5
        generate()
    if keys_pressed[K_RIGHT]:
        pos[0]+=5
        generate()
    if keys_pressed[K_UP]:
        pos[1]-=5
        generate()
    if keys_pressed[K_DOWN]:
        pos[1]+=5
        generate()

    for h in range(height):
        for w in range(width):
            # print(elevation[h][w])
            e, m = elevation[h][w]

            pygame.draw.rect(screen,
                             biome(e,m),
                             pygame.Rect(w * pix_size, h * pix_size, pix_size, pix_size),
                             )
    pygame.display.flip()
    # clock.tick(60)
