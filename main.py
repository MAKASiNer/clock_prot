import sys
import pygame
import pygame.draw
from pygame.draw import *
import datetime as dt
from math import sin, cos, pi

ZERO = [1/4, 1/4]
Array = list[list[list[float, float]]]


def str2arr(time_str: str, zero: list[float, float] = ZERO) -> Array:

    def load_tile(chr: str):
        chr = chr.replace('.', '. ').replace(':', '.. ')
        tile_str = open('media/%s.txt' % chr).read()
        return eval(tile_str.replace('zero', str(zero)))

    tiles = Array()
    y_offset = 0

    for liter in time_str:

        if liter == '\n':
            y_offset += 6
            continue

        tile = load_tile(liter)
        for y in range(len(tile)):

            if len(tiles) >= y + y_offset:
                tiles.append(list())
            tiles[y + y_offset] += tile[y]

    return tiles


def step(old: Array, new: Array, step: float):
    step = min(1, step)
    res = old.copy()
    for y in range(min(len(old), len(new))):
        for x in range(min(len(old[y]), len(new[y]))):
            delta = new[y][x][0] - old[y][x][0], new[y][x][1] - old[y][x][1]
            res[y][x] = [old[y][x][0] + delta[0] * step,
                         old[y][x][1] + delta[1] * step]
    return res


pygame.init()

size = width, height = 900, 600
black = 255, 255, 255

screen = pygame.display.set_mode(size)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(black)

    def dt_time2str(time) -> str:
        h = str(time.hour).rjust(2, '0')
        m = str(time.minute).rjust(2, '0')
        return f'{h}:{m}'

    now = dt.datetime.today()
    data_prev = str2arr(dt_time2str(now - dt.timedelta(minutes=1)))
    data_next = str2arr(dt_time2str(now))

    data = step(data_prev, data_next, now.second / 59)
    print(now)

    for y in range(len(data)):
        for x in range(len(data[y])):
            a, b = data[y][x]

            r, d = 20, 40
            h, m = 0.99, 0.99

            pygame.draw.circle(screen,
                               center=[x * d + r, y * d + r],
                               radius=r,
                               color="#9f9f9f",
                               width=1)

            pygame.draw.line(screen,
                             start_pos=[(x + 0.5) * d, (y + 0.5) * d],
                             end_pos=[(x + 0.5) * d + r * cos(a * pi) * h,
                                      (y + 0.5) * d + r * sin(-a * pi) * h],
                             color="#7f0000",
                             )

            pygame.draw.line(screen,
                             start_pos=[(x + 0.5) * d, (y + 0.5) * d],
                             end_pos=[(x + 0.5) * d + r * cos(b * pi) * h,
                                      (y + 0.5) * d + r * sin(-b * pi) * h],
                             color="#00007f",
                             )

    pygame.display.flip()
