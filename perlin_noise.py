import sys
import random
from copy import deepcopy


class PerlinNoise:
    def __init__(self, depth=255,
                 size=(100, 100),
                 fromc=3,
                 toc=10
                 ):

        self.depth = depth
        self.fromc = fromc
        self.toc = toc
        self.size = size

    def generate(self):
        arr = []

        i = 0

        for step in range(self.fromc, self.toc + 1):
            arr.append([[] for _ in range(self.size[1])])
            for y in range(0, self.size[1], step):
                for x in range(0, self.size[0], step):
                    color = random.randint(0, self.depth)
                    for a in range(step):
                        for b in range(step):
                            if y + a < self.size[1] and x + b < self.size[0]:
                                arr[i][y + a].append(color)

            arr[i] = self.interpolation(arr[i])
            i += 1

        self.arr = []

        for y in range(self.size[1]):
            self.arr.append([])
            for x in range(self.size[0]):
                self.arr[y].append(0)
                for i in range(self.toc + 1 - self.fromc):
                    self.arr[y][x] += arr[i][y][x]
                self.arr[y][x] //= self.toc + 1 - self.fromc

        self.arr = self.interpolation(self.arr)

    def interpolation(self, arr0=None):
        arr = deepcopy(arr0)
        r = 2
        for y in range(len(arr0)):
            for x in range(len(arr0[0])):
                s = 0
                k = 0
                for a in range(-r, r + 1):
                    for b in range(-r, r + 1):
                        if 0 <= x + b < len(arr0[0]):
                            if 0 <= y + a < len(arr0):
                                s += arr0[y + a][x + b]
                                k += 1
                s //= k
                arr[y][x] = s

        return arr


if __name__ == '__main__':
    import pygame

    pygame.init()

    fps = 60
    window_size = (500, 500)
    px = 5

    window = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    noise = PerlinNoise(size=(window_size[0] // px, window_size[1] // px))
    noise.generate()

    while True:

        for y in range(window_size[1] // px):
            for x in range(window_size[0] // px):
                pygame.draw.rect(window, 3 * [noise.arr[y][x]], (x * px, y * px, px, px))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(fps)
        pygame.display.update()
