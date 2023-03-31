import random
import pygame
import sys
from copy import deepcopy


class PerlinNoise:
    def __init__(self,
                 count=7,
                 size=(100, 100)
                 ):

        self.count = count
        self.size = size

    def generate(self):
        arr = []

        step = 10
        for i in range(self.count):
            arr += [[]]
            for y in range(0, self.size[1], step):
                arr[i] += [[] for _ in range(step)]
                for x in range(0, self.size[0], step):
                    color = random.randint(0, 255)
                    color = random.randint(0, 1) * 255
                    for a in range(step):
                        for b in range(step):
                            arr[i][y + a] += [color]
            step -= 1
            arr[i] = self.bilinear_interpolation(arr[i])

        self.a = arr

        self.arr = []
        for y in range(self.size[1]):
            self.arr += [[]]
            for x in range(self.size[0]):
                color = 0
                for i in range(self.count):
                    color += arr[i][y][x]
                color //= self.count

                self.arr[y] += [color]

    def interpolation(self, arr0=None):
        if arr0 is None:
            arr0 = self.arr
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

    def bilinear_interpolation(self, arr0=None):
        if arr0 is None:
            arr0 = self.arr
        arr = deepcopy(arr0)
        for y in range(len(arr0)):
            for x in range(len(arr0[0])):
                x1 = max(x - 1, 0)
                y1 = max(y - 1, 0)
                x2 = min(x + 1, len(arr0[0]) - 1)
                y2 = min(y + 1, len(arr0) - 1)

                fxy1 = (x2 - x) / (x2 - x1) * arr[y1][x1] + (x - x1) / (x2 - x1) * arr[y1][x2]
                fxy2 = (x2 - x) / (x2 - x1) * arr[y2][x1] + (x - x1) / (x2 - x1) * arr[y2][x2]

                fxy = (y2 - y) / (y2 - y1) * fxy1 + (y - y1) / (y2 - y1) * fxy2

                arr[y][x] = fxy

        return arr


if __name__ == '__main__':

    pygame.init()

    fps = 60
    window_size = (500, 500)
    px = 5

    window = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    noise = PerlinNoise(size=(window_size[0] // px, window_size[1] // px))
    noise.generate()
    noise.a += [noise.bilinear_interpolation()]

    i = 0

    while True:

        for y in range(window_size[1] // px):
            for x in range(window_size[0] // px):
                pygame.draw.rect(window, 3 * [noise.a[i][y][x]], (x * px, y * px, px, px))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                i += 1
                i %= len(noise.a)

        clock.tick(fps)
        pygame.display.update()
